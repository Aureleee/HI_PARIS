"""t6 / M2 — Emotional loading as a time series (Buechel et al. 2019).
Buechel: the emotion of central bank statements moves with the period (economy, who is in office).
Here: the tone of a speech also depends on its context = same parliament, same month.
We add context features: mean of key emotion features per (source, month) and per (source, year),
computed on train+test FEATURES only (never on targets), then LightGBM on everything.
Usage: python tracks/t6_papers/m2_period_context.py [n_rows]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import lightgbm as lgb
import numpy as np
import pandas as pd

from src.common import TARGETS, feature_cols, folds, load, log_result, write_submission

n_rows = int(sys.argv[1]) if len(sys.argv) > 1 else None
KEY = ["nrc_V_mean", "nrc_A_mean", "nrc_D_mean", "ctx_high_arousal_fraction", "exclamation_density",
       "question_density", "negation_word_fraction", "log_n_words"]

tr = load("x_train_final").drop(columns="clean_text").merge(load("y_train"), on="id")
te = load("x_test_final").drop(columns="clean_text")
allf = pd.concat([tr.drop(columns=TARGETS), te])
d = pd.to_datetime(allf["date"], errors="coerce")
allf["month"], allf["year"] = d.dt.to_period("M").astype(str), d.dt.year
for g in ["month", "year"]:
    m = allf.groupby(["source", g])[KEY].transform("mean")
    allf[[f"{c}_{g}_mean" for c in KEY]] = m.to_numpy()
    allf[[f"{c}_{g}_dev" for c in KEY]] = (allf[KEY] - m).to_numpy()  # speech vs its period
    allf[f"n_{g}"] = allf.groupby(["source", g])["id"].transform("size")
allf["source"] = allf["source"].astype("category")
cols = [c for c in feature_cols(allf) if c != "month"] + ["source"]

tr = allf.iloc[:len(tr)].assign(**{t: tr[t].to_numpy() for t in TARGETS})
te = allf.iloc[len(tr):]
if n_rows:
    tr = tr.sample(n_rows, random_state=0)
y = tr[TARGETS].to_numpy(float)
fold = folds(tr["id"])
p = dict(objective="regression", learning_rate=0.05, num_leaves=127, min_child_samples=50, feature_fraction=0.7,
         bagging_fraction=0.8, bagging_freq=1, verbose=-1, seed=2026)
oof, test = np.zeros_like(y), np.zeros((len(te), 2))
for j in range(2):
    for k in range(5):
        t, v = fold != k, fold == k
        m = lgb.train(p, lgb.Dataset(tr.loc[t, cols], y[t, j]), 5000,
                      valid_sets=[lgb.Dataset(tr.loc[v, cols], y[v, j])],
                      callbacks=[lgb.early_stopping(100, verbose=False)])
        oof[v, j] = m.predict(tr.loc[v, cols])
        test[:, j] += m.predict(te[cols]) / 5
name = "m2_period_context" + (f"_n{n_rows}" if n_rows else "")
log_result("t6_papers", name, tr["id"].to_numpy(), y, oof, te["id"].to_numpy(), test,
           notes=f"{len(cols)} feats incl. source x month/year context")
if not n_rows:
    write_submission(te["id"].to_numpy(), test, "t6_m2_context")
