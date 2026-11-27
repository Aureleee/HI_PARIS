# t2_chunks — Chunk scoring + length-weighted mean (mimic how the target is named and built)

Owner: Nel (default, swap freely). **UNSUPERVISED: there are no training labels.**

## Papers / ideas
- Target names: `*_chunks_weighted_mean` → the organizers scored chunks of each speech, then took a weighted mean (weights = chunk length, most likely).
- Werlen 2021: mean of lexicon words per unit of text.
- Knesset VAD paper (arXiv 2512.05231): sentence scores aggregated per document (mean, share of extreme sentences, variance).

## Plan
1. Problem: `clean_text` is in the original language (FR for assemblee/senat) and we have NO `text_en`. The NRC lexicon is English.
2. Way out without external data: **induce a word lexicon in each language from the organizers' doc-level scores** (pseudo-labels): word value = smoothed mean of `nrc_V_mean`/`nrc_A_mean` over the train speeches containing it (same code as `tracks/_supervised_archive/t6_papers/m1_induced_lexicon.py`, with y = nrc scores). Train speeches are unlabeled but have the features: use them all.
3. Split each speech into chunks (sentences; and fixed 50/100-word windows). Score each chunk with the induced lexicon. Aggregate: weighted mean by chunk length (= the target name), plain mean, median.
4. Compare chunk-weighted vs whole-speech scores, and their agreement with t1.
5. If organizers allow the raw NRC VAD lexicon file (ask!): redo step 3 with it on the English sources.

## How to log
Every method that produces test scores: `log_submission(track, experiment, test_ids, pred, notes)` from `src/common.py`
→ `submissions/<track>__<experiment>.csv` to upload on HFactory, then write the LB score in `results/runs/<track>.csv`.

## Results
_To fill (numbers, plots, what worked)._

## Conclusions and limits
_To fill. Goes almost as is into the final report._
