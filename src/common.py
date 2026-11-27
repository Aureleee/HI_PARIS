"""Shared helpers for every track.
UNSUPERVISED setting: there are NO training labels. Every method produces scores directly,
we compare methods by (1) their leaderboard score on HFactory and (2) their agreement with each other.
`folds`, `score`, `log_result` are kept for pseudo-label experiments (e.g. distillation in t4)."""
import csv
import subprocess
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
RES = ROOT / "results"
TARGETS = ["valence_chunks_weighted_mean", "arousal_chunks_weighted_mean"]
META = ["id", "clean_text", "text_en", "date", "source"]
N_FOLDS = 5


def load(name="x_train_final", columns=None):
    """name: x_train_final, x_test_final, x_Italia, y_test_zero (parquet from src/prepare_data.py)."""
    return pd.read_parquet(DATA / f"{name}.parquet", columns=columns)


def feature_cols(df):
    """The precomputed numeric features (everything except metadata and targets)."""
    return [c for c in df.columns if c not in META + TARGETS]


def folds(ids):
    """Deterministic fold (0..4) from the id: identical for everyone, whatever the row order."""
    ids = np.asarray(ids, dtype=np.uint64)
    return ((ids * np.uint64(2654435761)) % np.uint64(2**32) % np.uint64(N_FOLDS)).astype(int)


def score(y_true, y_pred):
    """y_*: arrays of shape (n, 2), columns = [valence, arousal].
    Primary metric = rmse_mean until the official HFactory metric is known."""
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    out = {}
    for i, t in enumerate(["valence", "arousal"]):
        e = y_pred[:, i] - y_true[:, i]
        out[f"rmse_{t}"] = float(np.sqrt(np.mean(e**2)))
        out[f"mae_{t}"] = float(np.mean(np.abs(e)))
        out[f"r_{t}"] = float(np.corrcoef(y_true[:, i], y_pred[:, i])[0, 1])
    out["rmse_mean"] = (out["rmse_valence"] + out["rmse_arousal"]) / 2
    return out


def log_result(track, experiment, train_ids, y, oof, test_ids=None, test_pred=None, notes="", lb=""):
    """Call this after EVERY run, good or bad.
    - appends one line to results/scores/<track>.csv
    - saves OOF preds to results/oof/<track>__<experiment>.parquet (for the final ensemble)
    - saves test preds to results/test/<track>__<experiment>.parquet if given"""
    s = score(y, oof)
    who = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True).stdout.strip()
    row = {"time": time.strftime("%Y-%m-%d %H:%M"), "track": track, "experiment": experiment, "who": who,
           **{k: round(v, 5) for k, v in s.items()}, "lb": lb, "notes": notes}
    f = RES / "scores" / f"{track}.csv"
    f.parent.mkdir(parents=True, exist_ok=True)
    new = not f.exists()
    with open(f, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(row))
        if new:
            w.writeheader()
        w.writerow(row)

    def _save(folder, ids, pred):
        p = RES / folder / f"{track}__{experiment}.parquet"
        p.parent.mkdir(parents=True, exist_ok=True)
        pred = np.asarray(pred, dtype="float32")
        pd.DataFrame({"id": ids, "valence": pred[:, 0], "arousal": pred[:, 1]}).to_parquet(p, index=False)

    _save("oof", train_ids, oof)
    if test_pred is not None:
        _save("test", test_ids, test_pred)
    print(f"[{track}/{experiment}]", {k: round(v, 4) for k, v in s.items()})
    return s


def write_submission(test_ids, pred, name):
    """Writes submissions/<name>.csv in the exact y_test_zero format (same ids, same order)."""
    tpl = load("y_test_zero")
    sub = pd.DataFrame({"id": test_ids, TARGETS[0]: np.asarray(pred)[:, 0], TARGETS[1]: np.asarray(pred)[:, 1]})
    sub = tpl[["id"]].merge(sub, on="id", how="left")
    assert len(sub) == len(tpl) and sub[TARGETS].notna().all().all(), "missing or extra ids"
    out = ROOT / "submissions" / f"{name}.csv"
    out.parent.mkdir(exist_ok=True)
    sub.to_csv(out, index=False)
    print("written", out, sub.shape)


def log_submission(track, experiment, test_ids, pred, notes=""):
    """Unsupervised mode. Writes submissions/<track>__<experiment>.csv (y_test_zero format),
    saves results/test/<track>__<experiment>.parquet and appends a line to results/runs/<track>.csv.
    After uploading on HFactory, write the LB score in the `lb` column of that line."""
    pred = np.asarray(pred, dtype="float32")
    write_submission(test_ids, pred, f"{track}__{experiment}")
    p = RES / "test" / f"{track}__{experiment}.parquet"
    p.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"id": test_ids, "valence": pred[:, 0], "arousal": pred[:, 1]}).to_parquet(p, index=False)
    who = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True).stdout.strip()
    row = {"time": time.strftime("%Y-%m-%d %H:%M"), "track": track, "experiment": experiment, "who": who,
           "mean_v": round(float(pred[:, 0].mean()), 4), "std_v": round(float(pred[:, 0].std()), 4),
           "mean_a": round(float(pred[:, 1].mean()), 4), "std_a": round(float(pred[:, 1].std()), 4),
           "lb": "", "notes": notes}
    f = RES / "runs" / f"{track}.csv"
    f.parent.mkdir(parents=True, exist_ok=True)
    new = not f.exists()
    with open(f, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(row))
        if new:
            w.writeheader()
        w.writerow(row)
    print(f"[{track}/{experiment}]", {k: row[k] for k in ("mean_v", "std_v", "mean_a", "std_a")})


def agreement(names):
    """Pearson correlation between the test predictions of several runs (results/test/<name>.parquet).
    High agreement between independent methods = more trust, when no labels exist."""
    d = {n: pd.read_parquet(RES / "test" / f"{n}.parquet").set_index("id") for n in names}
    out = {}
    for dim in ["valence", "arousal"]:
        out[dim] = pd.DataFrame({n: x[dim] for n, x in d.items()}).corr().round(3)
    return out
