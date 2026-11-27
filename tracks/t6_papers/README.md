# t6_papers — Nel's papers: lexicon method (Werlen), emotion time series (Buechel), small vs large (Kim), valorisation (Shah)

Owner: Nel / whoever has time (default, swap freely). **UNSUPERVISED: there are no training labels.**

## Papers / ideas
1. Buechel et al. 2019, Emotional Loading in Central Bank Statements. https://aclanthology.org/D19-5103/
2. Mendes & Martins 2023, V/A with multilingual transformers. https://arxiv.org/abs/2302.14021
3. Kim et al. 2024, Is Small Really Beautiful for Central Bank Communication? https://alexandria.unisg.ch/entities/publication/ac12c353-85e3-4b48-9f6b-13081bcdf209
4. Shah et al. 2023, Trillion Dollar Words. https://aclanthology.org/2023.acl-long.368/
5. Werlen et al. 2021, Emotions in the Parliament. https://ceur-ws.org/Vol-2957/paper2.pdf

## Plan
Unsupervised version of the 3 models (the supervised scripts are kept in `tracks/_supervised_archive/t6_papers/`):
- Werlen → lexicon mean: done in t1 (raw/median/shrink) and t2 (chunks, induced lexicons).
- Mendes + Kim → distillation into a model trained from scratch, small vs bigger: done in t4.
- **Buechel → emotion time series (this track)**: build monthly V/A series per parliament from the best scores (train + test), detect peaks and trends, link them to known events (elections, crises, COVID). This is the core of the mockup and of the pitch.
- **Shah → valorisation**: like they link Fed tone to markets, we link parliament tone to outside events. Product idea for the pitch.

## How to log
Every method that produces test scores: `log_submission(track, experiment, test_ids, pred, notes)` from `src/common.py`
→ `submissions/<track>__<experiment>.csv` to upload on HFactory, then write the LB score in `results/runs/<track>.csv`.

## Results
_To fill (numbers, plots, what worked)._

## Conclusions and limits
_To fill. Goes almost as is into the final report._
