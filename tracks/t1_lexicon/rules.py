"""t1_lexicon: rule-based corrections that a transformer captures and a plain lexicon mean misses.
No training, no pretrained model, only the organizers' features.

Valence, negation (VADER, Hutto & Gilbert 2014): a word in the scope of a negation is not counted
as is but multiplied by -0.74 around neutral. With the organizers' features:
  h = share of NRC hits in a negation scope (ctx_negation_scope_hit_fraction)
  v = mean valence of those negated words (ctx_negation_scope_valence_mean)
  corrected mean = nrc_V_mean - 1.74 * h * (v - 0.5)
Exclamation marks amplify the distance to neutral (VADER: +0.292 per '!' up to 4, on its own scale),
here a mild version on the density.

Arousal: a transformer's arousal rises with emotional extremity (U-shape, DimStance) and with
exclamations / uppercase / repeated punctuation, which the lexicon ignores. We add these cues to
the lexicon arousal, each z-scored, with fixed theory-driven weights (no labels to fit them).

All outputs are moment-matched to raw_mean so the scale stays the NRC one.
Usage: python tracks/t1_lexicon/rules.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import numpy as np

from src.common import load, log_submission

TR = "t1_lexicon"
te = load("x_test_final").drop(columns="clean_text")
ids = te["id"].to_numpy()
raw = te[["nrc_V_mean", "nrc_A_mean"]].to_numpy(float)
z = lambda x: (x - x.mean()) / (x.std() + 1e-12)
mm = lambda x, ref: z(x) * ref.std() + ref.mean()

# valence: negation flip (VADER), then mild exclamation boost of the distance to neutral
h, v = te["ctx_negation_scope_hit_fraction"], te["ctx_negation_scope_valence_mean"]
val_neg = te["nrc_V_mean"] - 1.74 * h * (v - 0.5)
boost = 1 + 0.3 * np.clip(te["exclamation_density"] / (te["exclamation_density"].quantile(0.99) + 1e-12), 0, 1)
val_neg_excl = 0.5 + (val_neg - 0.5) * boost

# arousal: lexicon + extremity (U-shape) + punctuation/uppercase cues
cues = {
    "nrc_A_mean": 1.0,
    "nrc_V_mean_abs_neutral": 0.5,          # U-shape: emotional extremity
    "exclamation_density": 0.3,
    "repeated_punctuation_density": 0.15,
    "uppercase_word_fraction": 0.15,
    "ctx_high_arousal_fraction": 0.3,
}
aro = sum(w * z(te[c].astype(float)) for c, w in cues.items())

out = {
    "rules_neg": (np.c_[mm(val_neg, raw[:, 0]), raw[:, 1]], "valence: VADER negation flip; arousal = raw"),
    "rules_neg_excl_cues": (np.c_[mm(val_neg_excl, raw[:, 0]), mm(aro, raw[:, 1])],
                            "valence: negation + exclamation boost; arousal: lexicon + extremity + punctuation cues"),
}
for name, (p, note) in out.items():
    log_submission(TR, name, ids, np.clip(p, 0, 1), note)
    for j, d in enumerate(["valence", "arousal"]):
        print(f"   {name} {d}: corr with raw = {np.corrcoef(p[:, j], raw[:, j])[0, 1]:.3f}")
