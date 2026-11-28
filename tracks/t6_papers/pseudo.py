"""Shared: the rule-based scores (t1 rules_neg_excl_cues) for any split, used as pseudo-labels."""
import numpy as np


def rule_scores(df, ref=None):
    """Same formulas as tracks/t1_lexicon/rules.py. ref: dataframe whose raw-lexicon moments set the scale."""
    ref = df if ref is None else ref
    z = lambda x, r: (x - r.mean()) / (r.std() + 1e-12)
    h, v = df["ctx_negation_scope_hit_fraction"], df["ctx_negation_scope_valence_mean"]
    val = df["nrc_V_mean"] - 1.74 * h * (v - 0.5)
    q = ref["exclamation_density"].quantile(0.99) + 1e-12
    val = 0.5 + (val - 0.5) * (1 + 0.3 * np.clip(df["exclamation_density"] / q, 0, 1))
    rh, rv = ref["ctx_negation_scope_hit_fraction"], ref["ctx_negation_scope_valence_mean"]
    rval = ref["nrc_V_mean"] - 1.74 * rh * (rv - 0.5)
    rval = 0.5 + (rval - 0.5) * (1 + 0.3 * np.clip(ref["exclamation_density"] / q, 0, 1))
    cues = {"nrc_A_mean": 1.0, "nrc_V_mean_abs_neutral": 0.5, "exclamation_density": 0.3,
            "repeated_punctuation_density": 0.15, "uppercase_word_fraction": 0.15, "ctx_high_arousal_fraction": 0.3}
    aro = sum(w * z(df[c].astype(float), ref[c].astype(float)) for c, w in cues.items())
    raro = sum(w * z(ref[c].astype(float), ref[c].astype(float)) for c, w in cues.items())
    V = (val - rval.mean()) / rval.std() * ref["nrc_V_mean"].std() + ref["nrc_V_mean"].mean()
    A = (aro - raro.mean()) / raro.std() * ref["nrc_A_mean"].std() + ref["nrc_A_mean"].mean()
    return np.c_[V, A].clip(0, 1)
