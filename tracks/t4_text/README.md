# t4_text — Text models trained from scratch (no pretrained weights)

Owner: Sachit (default assignment, swap freely)

## Papers / ideas
- SemEval-2026 Task 3: most systems use pretrained LMs (forbidden here), we keep the regression setup and replace the encoder by models trained from scratch (arXiv 2604.07066)
- Organizers' own features E and I are TF-IDF + SVD on text_en: we go further with the full sparse matrices

## Plan
1. Word 1–2 gram and char 3–5 gram TF-IDF on `clean_text` (raw multilingual) and on `text_en` if present. Fit vectorizers on train only.
2. Ridge / SGDRegressor / LinearSVR per target on the sparse matrices. Tune alpha.
3. Small neural model trained from scratch in PyTorch: bag-of-ngrams (fastText-like) or 1D CNN with embeddings learned from zero.
4. Stacking: OOF text predictions as extra features into the t1 LightGBM. Measure the gain.
5. Per-language check (FR vs EN sources): does raw text beat text_en?

## Results
_Best runs are in results/RESULTS.md. Summarize here: what worked, what did not, numbers, plots._

## Conclusions and limits
_To fill. This section goes almost as is into the final report._
