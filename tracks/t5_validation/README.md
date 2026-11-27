# t5_validation — Validation without labels, leaderboard strategy, bias analysis (feeds the report)

Owner: Kishan (default, swap freely). **UNSUPERVISED: there are no training labels.**

## Papers / ideas
- Arousal is hard to read from text alone (arXiv 2512.10882).
- Cross-national tone differences are country-specific (arXiv 2609.26346).
- Werlen 2021: the lexicon choice changes results a lot; arousal agrees poorly between lexicons.

## Plan
1. FIRST: find the metric and the upload limit on HFactory. Write them in CLAUDE.md §2. Plan the uploads for the team (we cannot test everything on the LB).
2. Agreement table between all methods (`agreement()` in src/common.py): where do they disagree (source, length, era)?
3. Sanity checks that should hold: exclamation ↑ → arousal ↑; positive words → valence ↑; per-source and per-year curves look plausible.
4. Facts already checked: test = random split, same sources/years as train (see CLAUDE.md §3).
5. `x_Italia.csv`: unlabeled Italian speeches (text + date + 214 features, no id/source). Use it as an out-of-domain check, and for the product.
6. Draft the 'limits and biases' section: translation to English, English lexicon on FR speeches, short speeches, arousal from text only, era drift. Do NOT try to reconstruct test targets (rules art. 7 bis v).

## How to log
Every method that produces test scores: `log_submission(track, experiment, test_ids, pred, notes)` from `src/common.py`
→ `submissions/<track>__<experiment>.csv` to upload on HFactory, then write the LB score in `results/runs/<track>.csv`.

## Results
_To fill (numbers, plots, what worked)._

## Conclusions and limits
_To fill. Goes almost as is into the final report._
