# t1_gbdt — Strong tabular baseline (GBDT) + bounded-target losses

Owner: Aurèle

## Papers / ideas
- Knesset VAD paper: binomial GLM with logit link for scores in [0,1] (arXiv 2512.05231, code: github.com/HaifaCLG/Polarization)
- SemEval-2026 Task 3 DimABSA/DimStance: VA as two regressions, logistic-loss regression (arXiv 2604.07066, github.com/DimABSA/DimABSA2026)

## Code
- `train_lgbm.py [l2|xent|logit] [drop_family] [n_rows]`: one LightGBM per target, shared 5 folds, early stopping, logs with `log_result`, writes the submission.
  - `l2`: plain regression. `xent`: LightGBM `cross_entropy` (labels in [0,1]). `logit`: regression on logit(y), sigmoid back.
  - `drop_family`: ablation, drop A (surface), B (nrc_), D (glove_), F (native_), G (en_), H (ctx_).
  - `n_rows`: subsample for quick tests (e.g. `20000`).
- `run_all.sh`: the 3 losses on all features, then the 6 ablations with the best loss.
- Saves feature importance (gain) to `importance_<obj>_<drop>.csv`.

Pipeline tested end to end on fake targets (20k rows, ~1.5 min on 2 cores). Full train = 870k rows: run on a strong machine.

## Plan
1. [ready] LightGBM, all features + source + year. Team reference score.
2. [todo] CatBoost, compare.
3. [ready] Losses: l2 vs xent vs logit (check target range first).
4. [ready] Ablation by family.
5. [todo] Tuning on the best setup.
6. [auto] Best OOF + test preds exported by `log_result` for the ensemble.

## Results
_Blocked: no targets released yet (see CLAUDE.md §3). Run `bash tracks/t1_gbdt/run_all.sh` as soon as `y_train` is in `data/raw/`._

## Conclusions and limits
_To fill._
