# t1_lexicon — Lexicon estimators (Werlen 2021 + NRC VAD v2), no training

Owner: Aurèle. **UNSUPERVISED: there are no training labels.**

## Papers / ideas
- Werlen et al. 2021, *Emotions in the Parliament* (https://ceur-ws.org/Vol-2957/paper2.pdf): speech valence/arousal = unweighted mean of the words found in a lexicon. They warn that short texts and the lexicon choice change results a lot, and arousal is the least reliable dimension.
- NRC VAD Lexicon v2 (Mohammad 2025, arXiv 2503.23547): human V/A/D norms for 55k English terms. The organizers' `nrc_*` features are this lexicon applied to the English version of each speech.
- Empirical Bayes shrinkage (classic): a mean over few words is noisy, pull it toward the population mean in proportion to its noise.

## Code
- `baselines.py`: 7 estimators → 7 submission files (`log_submission`). Writes `eb_constants.json`.
- `checks.py`: label-free checks + figures in `figs/` (not in git: run the script to get them) + `checks_report.md`.

## The 7 estimators (test set, NRC [0,1] scale)

| Run | What | mean V | std V | mean A | std A |
|---|---|---|---|---|---|
| `raw_mean` | Werlen as is: `nrc_*_mean` | 0.564 | 0.074 | 0.459 | 0.057 |
| `median` | `nrc_*_median` | 0.532 | 0.077 | 0.472 | 0.059 |
| `mean_median` | (mean + median) / 2 | 0.548 | 0.074 | 0.466 | 0.057 |
| `mid_q` | (q10 + q90) / 2 | 0.586 | 0.082 | 0.454 | 0.064 |
| `polarity` | share of words > 0.6 minus share < 0.4, moment-matched to raw | 0.564 | 0.074 | 0.459 | 0.057 |
| `eb_global` | empirical Bayes shrinkage to the corpus mean | 0.563 | 0.019 | 0.463 | 0.011 |
| `eb_source` | same, shrunk to the parliament's mean | 0.562 | 0.021 | 0.462 | 0.013 |

### Empirical Bayes, how K was estimated (no labels)
Model: var(speech mean | n matched words) = τ² + σ²/n. Posterior mean = (n·mean + K·μ)/(n + K), K = σ²/τ².
- τ² read on long speeches (n ≥ 100, noise negligible): **V 0.00072, A 0.00033**.
- σ² = median over n ∈ [5, 50] of n·(var − τ²): **V 0.0144, A 0.0137**.
- **K ≈ 20 (valence), 41 (arousal)**: a speech needs 20–40 lexicon words before we trust its own mean more than the population mean.
- First attempt used the per-speech `nrc_*_std`: wrong, it is 0 for one-word speeches, so noise was underestimated (K ≈ 6). Fixed.

## Label-free checks (`checks_report.md`, `figs/`)
1. **Short speeches are noise** (`figs/noise_vs_length.png`): std of the speech score is 0.19 (V) with 1 matched word, 0.06 with 5–10, 0.027 above 100. Median speech has 24 matched words; 13 % have ≤ 3; 0.7 % have none (scored 0.5 by the organizers).
2. **Agreement between variants** (Pearson, test): mean/median/mid_q/polarity agree at r = 0.76–0.98. The EB versions agree only r ≈ 0.63 (V) and 0.57 (A) with raw: they change short speeches a lot. So `raw_mean` vs `eb_global` on the LB is the most informative pair of uploads.
3. **Sanity (Spearman, speeches with ≥ 5 words)**:
   - negations → lower valence (ρ = −0.15) ✅
   - high-arousal context words → arousal (ρ = +0.62) ✅ (same lexicon, expected)
   - **exclamation marks → arousal: ρ ≈ −0.01** ❌. The lexicon ignores punctuation, so it misses part of arousal. → input for t3 (combine with punctuation cues).
4. **Arousal vs valence** (`figs/arousal_vs_valence.png`): no clear U-shape with the lexicon scores, only a slight rise at the negative end. Different from the DimStance finding (human labels): another sign that lexicon arousal is weak.
5. **Per parliament and year** (`figs/per_year.png`): English-speaking parliaments score higher valence (≈ 0.57) than French ones (≈ 0.55). Likely partly a translation effect (FR → EN before the English lexicon), to discuss in the report. Arousal slowly rises over time in UK and US. The Sénat shows a jump in valence around 2001: probably a change in the transcripts, not in the debates (to check before using it in the product).
6. Italian set: not checked yet (file not converted in this run).

## Upload plan (uploads are limited, coordinate with t5)
1. `t1_lexicon__raw_mean.csv`: the reference (pure Werlen).
2. `t1_lexicon__eb_global.csv`: if it beats raw clearly, the hidden scores behave like a smoother, more "true" emotion than a noisy word average → shrinkage and blends will pay. If it is clearly worse, the hidden scores are close to a word-level lexicon average → stay close to raw, focus on chunking (t2).
3. Then, depending on 1–2: `mid_q` or `median` (robust centres) or `eb_source`.
Files are in `Desktop/HACKATHON/submissions/` on Aurèle's Mac (outside the repo).

## Results
| Run | LB valence | LB arousal |
|---|---|---|
| raw_mean | ≈ 0.27 (crowd of teams at that score) | 0.13 (our Group 34, Sat 10:18) |
| eb_global | 0.03 (Sat 12:45) ❌ | — |

## What the leaderboard taught us (Sat 12:45)
- `eb_global` scored **0.03** vs ≈ 0.27 for the raw lexicon. Shrinking short speeches toward the mean destroys the signal: the hidden scores keep strong values on short speeches. So they are **not** a noisy word average that a statistician would smooth: they come from a model that gives confident scores even to a 2-word interjection.
- Together with the target name (`*_chunks_weighted_mean`), the most likely recipe is a **transformer V/A regressor run on chunks of each speech, then a length-weighted mean** (chunks because transformers read ~512 tokens max). The best candidate is Mendes & Martins 2023 (multilingual V/A transformers, code and models public), which is also on the organizers'/Nel's paper list. Not confirmed.
- The jump from 0.27 to 0.83 at the top of the leaderboard fits teams running such pretrained models. **Rules art. 7 forbid pretrained models, and art. 7 bis (v) forbids rebuilding the targets from public sources**: ask the organizers in writing before going that way.

## Conclusions and limits (draft for the report)
- The organizers' NRC features already give a Werlen-style estimator for free. Its main weakness is noise on short speeches, which we quantify (K ≈ 20–40 words) and correct with empirical Bayes.
- Lexicon arousal misses punctuation and intensity cues; valence looks more reliable, as in Werlen 2021.
- The lexicon is English and FR speeches were translated: part of the FR/EN gap may be translation, not politics.
