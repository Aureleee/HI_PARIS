# Lab notebook — what was tried, what worked, what failed, why

**Every agent: read this before running any experiment, and add a line after each one.**
Do not repeat an experiment already listed here unless you change something and say what.
Newest entries at the top of each table. Scores = HFactory interim leaderboard (higher is better).

## Key facts learned (read first)
1. **No labels exist.** `x_train_final` has no targets, `y_test_sample.csv` / `y_test_zero.csv` are all zeros. Unsupervised task.
2. **Two competitions (Valence, Arousal), metric unknown, higher is better.** Uploads are counted per competition.
3. **The raw lexicon (`nrc_V_mean`, `nrc_A_mean`) scores ≈ 0.27 valence / 0.13 arousal.** About 15 teams sit exactly there.
4. **Shrinking short speeches toward the mean destroys the score** (empirical Bayes: 0.09 / 0.03). The hidden scores keep strong values on very short speeches.
5. **The hidden scores most likely come from a transformer V/A model run on chunks of each speech, then a length-weighted mean** (target name `*_chunks_weighted_mean`, behaviour on short speeches, top teams at 0.83/0.72). Probably Mendes & Martins 2023. Not confirmed.
6. **Pretrained models are forbidden (rules art. 7)** and rebuilding the targets from public sources is forbidden (art. 7 bis v). Confirmed by Aurèle: the rules will not change. So we imitate what a transformer captures with rules and models trained from scratch.
7. What a transformer captures and the lexicon mean misses, and that **helped**: negation (VADER flip), exclamation, arousal cues (punctuation, uppercase, emotional extremity).
8. **A text model trained from scratch on rule pseudo-labels, blended with the rules, helps a lot** (0.33 / 0.32): it reads the original FR/EN text. Push this direction (self-training, char n-grams, bigger models).

## Experiments (LB = interim leaderboard)

| When | Who | Track | Submission name | File | Valence | Arousal | Verdict | Why / lesson |
|---|---|---|---|---|---|---|---|---|
| Sat 13:15 | Aurèle | t6 | `t6-blend-rules-distill-big` | `t6_papers__blend_rules_distill_big.csv` | **0.33** | **0.32** | ✅ best so far | 50/50 rules + text model trained from scratch (TF-IDF uni+bigrams, ridge) distilled on the rule scores, reading the raw FR/EN text. Arousal +0.08: the text model sees intensity cues and non-English words the lexicon misses. Unlike shrinkage, distillation keeps short speeches' strong values (it reads their words). Code: `tracks/t6_papers/distill.py`. |
| Sat 12:58 | Aurèle | t1 | `t1-rules-neg-excl-cues` | `t1_lexicon__rules_neg_excl_cues.csv` | 0.30 | 0.24 | ✅ | VADER negation flip + exclamation boost (valence); lexicon arousal + emotional extremity + punctuation/uppercase cues (arousal). Arousal almost doubles: the lexicon misses intensity cues a transformer sees. Code: `tracks/t1_lexicon/rules.py`. |
| Sat 12:40 | Aurèle | t1 | `Test Submission 1` (= `t1-eb-global`) | `t1_lexicon__eb_global.csv` | 0.09 | 0.03 | ❌ do not retry | Empirical Bayes shrinkage of short speeches. Kills the signal: the hidden scores are not a noisy word average. Any method that pulls short speeches to the mean will fail. |
| Sat 10:18 | team | t1 | `Test Submission` | `1127_2302_lexicon_baseline.csv` | (≈0.27, crowd) | 0.13 | baseline | Raw `nrc_*_mean`. Reference for everything else. |

## Computed but NOT uploaded
| File | What | Expected |
|---|---|---|
| `t6_papers__distill_big.csv` → name **`t6-distill-big`** | The text model alone (no rules) | **Next upload**: tells whether to give the text model more weight than 50/50. |
| `t6_papers__blend_rules_selftrain_word.csv` | Self-training round 2 (OOF text preds blended with rules as new pseudo-labels, retrain) | ❌ Don't upload: r = 0.997 with `t6-blend-rules-distill-big`. Self-training converges to the same model. |
 (ready in `Desktop/HACKATHON/submissions/` on Aurèle's Mac)
| File | What | Expected |
|---|---|---|
| `t1_lexicon__median.csv`, `mean_median`, `mid_q`, `polarity` | Robust centres of the lexicon | ≈ raw (r 0.76–0.98 with raw). Low priority. |
| `t1_lexicon__eb_source.csv` | Shrinkage to parliament mean | ❌ same failure as eb_global. Don't upload. |
| `t1_lexicon__rules_neg.csv` | Negation only, arousal = raw | Superseded by rules_neg_excl_cues. |
| `t6_papers__distill_small/big.csv`, `blend_rules_distill_small.csv` | Same, small model or text model alone | Kim's small vs big: big reproduces the rules better (0.87/0.88 vs 0.80/0.83). Upload only if the blend wins. |

## Ideas not tried yet (pick one, then log it)
- Intensifiers (VADER boosters: "very", "extremely") with `ctx_intensifier_scope_*`.
- Per-chunk scoring: score sentences, then length-weighted mean (t2), mimics the target recipe.
- Tune the arousal cue weights a little (they were fixed by hand, never fitted).
- "But" rule (VADER): words after "but" weigh more.
- Text models from scratch on the pseudo-labels: done in t6 (TF-IDF ridge, 2 sizes, self-training). Not tried: char n-grams (OOM at 250k docs on 8 GB: ~580 non-zeros per speech, try ≤ 100k docs or batches), small NN, all 870k with bigrams (needs > 7 GB RAM). Weight of text model vs rules in the blend (50/50 so far).

## Don't
- Don't upload near-duplicates (raw vs median vs mean_median): wasted uploads.
- Don't shrink toward a mean (global, per parliament, per period).
- Don't use pretrained models or external data (rules). Don't try to reconstruct test targets.
