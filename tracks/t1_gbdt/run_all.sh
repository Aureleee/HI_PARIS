#!/usr/bin/env bash
# Full t1 plan: 3 losses on all features, then family ablation with the best loss.
set -e
cd "$(git rev-parse --show-toplevel)"
for o in l2 xent logit; do python tracks/t1_gbdt/train_lgbm.py $o; done
python scripts/leaderboard.py
BEST=$(python -c "import pandas as p;d=p.read_csv('results/scores/t1_gbdt.csv');print(d.sort_values('rmse_mean').experiment.iloc[0].split('_')[1])")
for f in A B D F G H; do python tracks/t1_gbdt/train_lgbm.py $BEST $f; done
python scripts/leaderboard.py
