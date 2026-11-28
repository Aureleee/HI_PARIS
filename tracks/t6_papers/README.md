# t6_papers — Nel's papers, rule-compliant versions

Owner: Nel (track run by Aurèle's agent on Sat 28 Nov). **UNSUPERVISED, no pretrained models (rules art. 7).**

## Papers
1. Buechel et al. 2019, *A Time Series Analysis of Emotional Loading in Central Bank Statements*. https://aclanthology.org/D19-5103/
2. Mendes & Martins 2023, *Quantifying Valence and Arousal in Text with Multilingual Pre-trained Transformers*. https://arxiv.org/abs/2302.14021
3. Kim et al. 2024, *Is Small Really Beautiful for Central Bank Communication?* https://alexandria.unisg.ch/entities/publication/ac12c353-85e3-4b48-9f6b-13081bcdf209
4. Shah et al. 2023, *Trillion Dollar Words*. https://aclanthology.org/2023.acl-long.368/
5. Werlen et al. 2021, *Emotions in the Parliament*. https://ceur-ws.org/Vol-2957/paper2.pdf

## What each paper became here
| Paper | Rule-compliant version | Where | Status |
|---|---|---|---|
| Werlen 2021 | Lexicon mean per speech | `tracks/t1_lexicon/baselines.py` | done, LB ≈ 0.27 / 0.13 |
| Mendes & Martins 2023 | Text model reading the raw multilingual text, 2 outputs (V, A). Pretrained transformers are forbidden, so it is **trained from scratch by distillation**: TF-IDF + ridge learns to reproduce our best rule scores (t1 `rules_neg_excl_cues`, LB 0.30 / 0.24) on the 870k unlabeled train speeches. It reads the original FR/EN text, so it can score words the English lexicon misses. | `distill.py`, `pseudo.py` | done, 2 sizes |
| Kim 2024 | Small vs bigger model: `small` = unigrams, 2^18 hashed features, all train; `big` = uni+bigrams, 2^20, 500k train speeches (2^21 ran out of memory on 7 GB). | `distill.py small|big` | done |
| Buechel 2019 | Emotion as a time series per institution → yearly/monthly curves per parliament, for the mockup and the pitch | results explorer + t1 `figs/per_year.png` | partly done (yearly curves) |
| Shah 2023 | Link tone to outside events (they link Fed tone to markets) | pitch / valorisation | idea |

## Results (held-out fold of the train, agreement with the rule scores)
| Model | corr valence | corr arousal | test corr with rules (V / A) |
|---|---|---|---|
| small | 0.802 | 0.828 | 0.802 / 0.779 |
| big | **0.867** | **0.884** | 0.846 / 0.828 |

Kim's question, answered on our data: the bigger model reproduces the rule scores clearly better.

## Submissions
| Name on HFactory | File | Valence | Arousal |
|---|---|---|---|
| `t6-blend-rules-distill-big` | `t6_papers__blend_rules_distill_big.csv` (50/50 rules + big text model, same scale as rules) | **0.33** | **0.32** |
| (not uploaded) | `t6_papers__distill_big.csv`, `distill_small`, `blend_rules_distill_small` | | |

If the blend beats 0.30 / 0.24: the text model adds what the lexicon misses → push it (char n-grams, small NN). If it loses: distillation mostly smooths, like the failed shrinkage → stop this branch.
