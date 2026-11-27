# t3_combine — Combine unsupervised signals (no labels): theory-driven scores, U-shape, factor analysis

Owner: Rubens (default, swap freely). **UNSUPERVISED: there are no training labels.**

## Papers / ideas
- DimStance (arXiv 2601.21483): U-shaped valence–arousal relation, arousal lowest near neutral valence.
- Four Slavic parliaments (arXiv 2608.30828): valence dominates, arousal shows on the extremes.
- Organizers' features: punctuation (`exclamation_density`, `question_density`), contextual emotion (`ctx_*`), negation/intensifier scopes.

## Plan
1. Correlation map of all 214 features with `nrc_V_mean` and `nrc_A_mean` on train (unlabeled train is fine here).
2. Arousal is the hard one: build an arousal score from several cues (nrc_A, `ctx_high_arousal_fraction`, exclamation/question density, uppercase, repeated punctuation, |V − 0.5|). Combine with first principal component / factor analysis, or z-score average.
3. Valence: correct the lexicon mean with negation scopes (`ctx_negation_scope_*`) and intensifiers.
4. Keep everything on the [0,1] NRC scale at the end (match mean/std of t1 raw) so LB scores are comparable.
5. Upload the 2 best combos; log with `log_submission`.

## How to log
Every method that produces test scores: `log_submission(track, experiment, test_ids, pred, notes)` from `src/common.py`
→ `submissions/<track>__<experiment>.csv` to upload on HFactory, then write the LB score in `results/runs/<track>.csv`.

## Results
_To fill (numbers, plots, what worked)._

## Conclusions and limits
_To fill. Goes almost as is into the final report._
