# t1_gbdt — Strong tabular baseline (GBDT) + bounded-target losses

Owner: Aurèle (default assignment, swap freely)

## Papers / ideas
- Knesset VAD paper: binomial GLM with logit link for scores in [0,1] (arXiv 2512.05231, code: github.com/HaifaCLG/Polarization)
- SemEval-2026 Task 3 DimABSA/DimStance: VA as two regressions, logistic-loss regression (arXiv 2604.07066, github.com/DimABSA/DimABSA2026)

## Plan
1. LightGBM on all 342 features + `source` (categorical) + year. One model per target. This is the team reference score.
2. Same with CatBoost. Compare.
3. Losses for bounded targets: L2 vs LightGBM `objective="cross_entropy"` vs L2 on logit(y) then sigmoid. Check target range first.
4. Ablation by feature family (A, B, D, E, F, G, H, I): drop one family at a time, then each family alone.
5. Tuning (Optuna by hand, no AutoML) on the best setup.
6. Export the best OOF + test preds for the final ensemble.

## Results
_Best runs are in results/RESULTS.md. Summarize here: what worked, what did not, numbers, plots._

## Conclusions and limits
_To fill. This section goes almost as is into the final report._
