# t4_weak — Weak supervision / distillation: text models trained from scratch on pseudo-labels

Owner: Sachit (default, swap freely). **UNSUPERVISED: there are no training labels.**

## Papers / ideas
- Lexicon expansion by label propagation over word vectors (Alhothali & Hoey 2017, arXiv 1703.09825; Giulianelli 2017, arXiv 1708.03910).
- Mendes & Martins 2023 (arXiv 2302.14021): continuous V/A regressor with 2 heads; here trained from scratch, no pretrained weights.

## Plan
1. Pseudo-labels = best t1 estimator (`nrc_*_mean`) on the 870k train speeches (unlabeled, but features exist).
2. Train text models from scratch to predict them from `clean_text`: TF-IDF word + char n-grams → Ridge; then the small transformer (`tracks/_supervised_archive/t6_papers/m3_small_transformer.py`, set y = pseudo-labels). Use shared folds to check fit (`log_result` works with pseudo-labels).
3. Why it can beat the lexicon: the text model sees words the lexicon misses (non-English, rare words), and smooths noisy short speeches.
4. Predict test → `log_submission`. Then blend 50/50 with the lexicon score.
5. Optional: word2vec trained from scratch on our corpus + label propagation to expand the lexicon.

## How to log
Every method that produces test scores: `log_submission(track, experiment, test_ids, pred, notes)` from `src/common.py`
→ `submissions/<track>__<experiment>.csv` to upload on HFactory, then write the LB score in `results/runs/<track>.csv`.

## Results
_To fill (numbers, plots, what worked)._

## Conclusions and limits
_To fill. Goes almost as is into the final report._
