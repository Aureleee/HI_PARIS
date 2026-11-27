# t6_papers — Models inspired by Nel's paper list

Owner: Nel (proposed, he found the papers) or whoever has time. Can be split.

## Papers
1. **A Time Series Analysis of Emotional Loading in Central Bank Statements** — Buechel et al., 2019. VAD of ECB/Fed press statements 1998–2019; emotion moves with the state of the economy and the person in office. https://aclanthology.org/D19-5103/
2. **Quantifying Valence and Arousal in Text with Multilingual Pre-trained Transformers** — Mendes & Martins, 2023. Continuous V/A prediction in several languages; model size matters a lot. https://arxiv.org/abs/2302.14021
3. **Is Small Really Beautiful for Central Bank Communication?** — Kim et al., 2024. Small (FinBERT) vs large (GPT-4, Llama) models on FOMC text. https://alexandria.unisg.ch/entities/publication/ac12c353-85e3-4b48-9f6b-13081bcdf209
4. **Trillion Dollar Words: A New Financial Dataset, Task & Market Analysis** — Shah et al., 2023. Hawkish/dovish classification of Fed communication + link to market outcomes. https://aclanthology.org/2023.acl-long.368/
5. **Emotions in the Parliament: Lexical Emotion Analysis of Parliamentarian Speech Transcriptions** — Werlen et al., 2021. Valais parliament, French + German; speech V/A = unweighted mean of the words found in a lexicon (about 10 % coverage); lexicon choice changes results a lot, arousal agrees poorly between lexicons. https://ceur-ws.org/Vol-2957/paper2.pdf

Pretrained models (FinBERT, GPT-4, Llama, multilingual transformers) are forbidden here: we keep the **ideas** and train everything from scratch.

## The 3 models (code ready, tested on fake targets only)

| Model | Script | From which paper | Idea |
|---|---|---|---|
| M1 | `m1_induced_lexicon.py [n_rows]` | Werlen 2021 (+ Buechel 2019) | No external lexicon allowed, so we **induce** one from the train folds: word value = smoothed mean target of the speeches containing it. Speech = mean of its words (Werlen). Then a small LightGBM calibrates with source/year. Exports `induced_lexicon.csv` (most negative/positive words: great for the report and the mockup). |
| M2 | `m2_period_context.py [n_rows]` | Buechel 2019 | Emotion is a time series: a speech depends on its period. Adds per (parliament, month) and (parliament, year) means of key emotion features + the speech's deviation from its period. Features only, never targets. Then LightGBM. |
| M3 | `m3_small_transformer.py [tiny\|small] [n_rows] [epochs]` | Mendes 2023 + Kim 2024 | Mendes' setup (encoder → mean pooling → 2 sigmoid heads) but trained **from scratch** with a hashed word vocab. Kim's question: does a bigger model help? Compare `tiny` (d=64, 1 layer) vs `small` (d=192, 3 layers). CPU is slow: start with `n_rows=100000`, 1–2 epochs. |

Shah 2023 is not a model for us: use it for the **valorisation** part (link the tone of debates to outside events, like they link Fed tone to markets).

## How to run
```bash
python tracks/t6_papers/m1_induced_lexicon.py 50000   # quick test, then without the number for the full run
python tracks/t6_papers/m2_period_context.py 50000
python tracks/t6_papers/m3_small_transformer.py tiny 100000 1
python scripts/leaderboard.py
```
All runs are logged with `log_result` (shared folds/metric), comparable with every other track.

## Results
_Blocked: no `y_train` released yet (see CLAUDE.md §3)._

## Conclusions and limits
_To fill._
