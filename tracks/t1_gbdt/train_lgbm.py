"""t1_gbdt: one LightGBM per target on the precomputed features + source + year.
Usage: python tracks/t1_gbdt/train_lgbm.py [l2|xent|logit] [drop_family] [n_rows]
  l2    : plain regression
  xent  : LightGBM cross_entropy (targets must be in [0,1])
  logit : regression on logit(y), predictions passed through a sigmoid
  drop_family: A B D F G H (ablation) or none
  n_rows: subsample train for quick tests"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import lightgbm as lgb
import numpy as np
import pandas as pd

from src.common import TARGETS, feature_cols, folds, load, log_result, write_submission

obj = sys.argv[1] if len(sys.argv) > 1 else "l2"
drop = sys.argv[2] if len(sys.argv) > 2 else "none"
n_rows = int(sys.argv[3]) if len(sys.argv) > 3 else None

FAMILY = {"B": "nrc_", "D": "glove_", "F": "native_", "G": "en_", "H": "ctx_"}

tr = load("x_train_final").drop(columns="clean_text")
te = load("x_test_final").drop(columns="clean_text")
y_df = load("y_train")
tr = tr.merge(y_df[["id"] + TARGETS], on="id")
if n_rows:
    tr = tr.sample(n_rows, random_state=0)
for d in (tr, te):
    d["year"] = pd.to_datetime(d["date"], errors="coerce").dt.year
    d["source"] = d["source"].astype("category")

cols = feature_cols(tr) + ["source"]
if drop == "A":
    cols = [c for c in cols if c.startswith(tuple(FAMILY.values())) or c in ("source", "year")]
elif drop in FAMILY:
    cols = [c for c in cols if not c.startswith(FAMILY[drop])]

y = tr[TARGETS].to_numpy(float)
eps = 1e-4
fold = folds(tr["id"])
params = dict(learning_rate=0.05, num_leaves=127, min_child_samples=50, feature_fraction=0.7,
              bagging_fraction=0.8, bagging_freq=1, lambda_l2=1.0, verbose=-1, n_jobs=-1, seed=2026)
params["objective"] = "cross_entropy" if obj == "xent" else "regression"

oof = np.zeros_like(y)
test = np.zeros((len(te), 2))
for j in range(2):
    yt = np.log((y[:, j].clip(eps, 1 - eps)) / (1 - y[:, j].clip(eps, 1 - eps))) if obj == "logit" else y[:, j]
    for k in range(5):
        trn, val = fold != k, fold == k
        m = lgb.train(params, lgb.Dataset(tr.loc[trn, cols], yt[trn]), 5000,
                      valid_sets=[lgb.Dataset(tr.loc[val, cols], yt[val])],
                      callbacks=[lgb.early_stopping(100, verbose=False)])
        p_val, p_te = m.predict(tr.loc[val, cols]), m.predict(te[cols]) / 5
        if obj == "logit":
            p_val, p_te = 1 / (1 + np.exp(-p_val)), 1 / (1 + np.exp(-m.predict(te[cols]))) / 5
        oof[val, j] = p_val
        test[:, j] += p_te
        print(TARGETS[j], "fold", k, "iters", m.best_iteration, flush=True)
    if j == 0:
        imp = pd.Series(m.feature_importance("gain"), index=cols).sort_values(ascending=False)
        imp.to_csv(Path(__file__).parent / f"importance_{obj}_{drop}.csv")

name = f"lgbm_{obj}_drop{drop}" + (f"_n{n_rows}" if n_rows else "")
log_result("t1_gbdt", name, tr["id"].to_numpy(), y, oof, te["id"].to_numpy(), test,
           notes=f"{len(cols)} feats")
if not n_rows:
    write_submission(te["id"].to_numpy(), test, f"t1_{name}")
