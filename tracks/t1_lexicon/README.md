# t1_lexicon — Lexicon baselines from the given NRC features + first LB anchors

Owner: Aurèle (default, swap freely). **UNSUPERVISED: there are no training labels.**

## Papers / ideas
- Werlen et al. 2021 (Emotions in the Parliament): speech V/A = unweighted mean of the lexicon words it contains. https://ceur-ws.org/Vol-2957/paper2.pdf
- NRC VAD Lexicon v2 (Mohammad 2025, arXiv 2503.23547): the lexicon behind the organizers' `nrc_*` features (55k English terms).

## Plan
1. [done] `baselines.py`: raw mean, median, shrinkage to the corpus mean for speeches with few matched words. Upload `raw_mean` first: it tells us the scale and gives the reference LB score.
2. Use 2–3 uploads to learn the metric behaviour (does shrinkage help? → RMSE-like; no change → correlation-like).
3. Use the other NRC stats: (q10+q90)/2, trimmed means, `nrc_V_fraction_above_060 - nrc_V_fraction_below_040`.
4. Per-source recentering if it helps on LB (careful: only a few uploads, see t5).
5. Hand the best simple estimator to t3 (combination) and t4 (pseudo-labels).

## How to log
Every method that produces test scores: `log_submission(track, experiment, test_ids, pred, notes)` from `src/common.py`
→ `submissions/<track>__<experiment>.csv` to upload on HFactory, then write the LB score in `results/runs/<track>.csv`.

## Results
_To fill (numbers, plots, what worked)._

## Conclusions and limits
_To fill. Goes almost as is into the final report._
