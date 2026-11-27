# t2_chunks — Chunk/sentence scoring then weighted aggregation (mimic how the target is built)

Owner: Nel (default assignment, swap freely)

## Papers / ideas
- Knesset VAD paper: sentence-level VAD then per-document aggregation: mean, share of sentences >0.7 / <0.3, variance of V (arXiv 2512.05231)
- The target names themselves: `*_chunks_weighted_mean` = scores computed on chunks, then weighted mean

## Plan
1. Split `clean_text` into sentences/chunks (and `text_en` if present). Look at the length distribution.
2. Per-chunk features computed by us: length, punctuation, negations, questions/exclamations, uppercase, numbers.
3. Per-chunk emotion score learned from train only (no external lexicon): e.g. TF-IDF + ridge trained at speech level, applied to each chunk (multiple-instance style). Fit inside folds to avoid leakage.
4. Aggregate per speech: length-weighted mean (like the target), min, max, std, q10/q90, share of extreme chunks, first vs last chunk.
5. Feed the aggregates (+ the 342 features) to LightGBM. Compare with and without.
6. Test chunk sizes (sentence, 50 words, 100 words) and weighting (by chars vs by words).

## Results
_Best runs are in results/RESULTS.md. Summarize here: what worked, what did not, numbers, plots._

## Conclusions and limits
_To fill. This section goes almost as is into the final report._
