# t5_domain — Countries, time, validation design and bias analysis (feeds the report)

Owner: Kishan (default assignment, swap freely)

## Papers / ideas
- Cross-national: tone shifts mirror country-specific conditions, no universal pattern (arXiv 2609.26346)
- Arousal is hard to get from text alone, mostly carried by voice/face (arXiv 2512.10882)
- Knesset VAD paper limitations: lower reliability for arousal, editing practices changing over time (arXiv 2512.05231)

## Plan
1. FIRST (Friday night): train vs test shift on source, date, length. Adversarial validation (classifier train-vs-test). Tell the team if the shared random folds are wrong (e.g. test = later years) and propose new folds.
2. Role of `x_Italia.csv`: labeled? in the test? unseen-language generalization?
3. Global model vs per-source models vs source interactions. Leave-one-parliament-out CV to measure transfer.
4. Error analysis of the best model (t1): by source, year, length, language. Where are we bad?
5. Draft the 'limits and biases' section of the report: translation to English, English-centric lexicons, era drift, arousal from text only, country gaps.

## Results
_Best runs are in results/RESULTS.md. Summarize here: what worked, what did not, numbers, plots._

## Conclusions and limits
_To fill. This section goes almost as is into the final report._
