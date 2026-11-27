# t3_ushape — Joint valence–arousal modelling (U-shape)

Owner: Rubens (default assignment, swap freely)

## Papers / ideas
- DimStance: broadly U-shaped valence–arousal relation in all datasets, arousal lowest near neutral valence (arXiv 2601.21483)
- Four Slavic parliaments: valence dominates, arousal-like curvature on the extremes (arXiv 2608.30828)
- SemEval-2026 Task 3 best systems: two regressions, compare with joint heads (arXiv 2604.07066)

## Plan
1. Plot arousal vs valence on train, by source. Is there a U? Where is the minimum?
2. Chained model: OOF valence prediction v̂, then add |v̂ − c| and (v̂ − c)² as features for arousal (c fitted). Do it with proper nested OOF (no leakage).
3. Multi-output models: CatBoost `MultiRMSE`, small MLP from scratch with 2 heads (PyTorch) on the 342 features.
4. Reverse chain (arousal first) and both orders averaged.
5. Compare against independent models from t1 on the shared folds.

## Results
_Best runs are in results/RESULTS.md. Summarize here: what worked, what did not, numbers, plots._

## Conclusions and limits
_To fill. This section goes almost as is into the final report._
