"""t1_lexicon: lexicon estimators of valence/arousal, no training (Werlen et al. 2021 + NRC VAD v2).
Werlen: speech score = unweighted mean of the V/A of the words found in the lexicon.
The organizers give it as nrc_V_mean / nrc_A_mean (NRC VAD on the English text, 0.5 if no word matched).

Variants (all on the NRC [0,1] scale):
  raw_mean      Werlen as is.
  median        robust to a few extreme words.
  mean_median   average of both.
  mid_q         (q10 + q90) / 2, robust centre.
  polarity      0.5 + (share of words > 0.60 - share < 0.40) / 2, then moment-matched to raw_mean.
  eb_global     empirical Bayes shrinkage: a speech with n matched words has a noisy mean
                (noise variance sigma2/n). Posterior mean = (n*mean + K*mu) / (n + K), K = sigma2/tau2,
                estimated on train+test features (no labels), see below.
  eb_source     same, shrunk to the mean of its own parliament.
Usage: python tracks/t1_lexicon/baselines.py"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import numpy as np
import pandas as pd

from src.common import load, log_submission

TR = "t1_lexicon"
cols = ["id", "source", "nrc_hit_count_log"] + [f"nrc_{d}_{s}" for d in "VA" for s in
        ["mean", "std", "median", "q10", "q90", "fraction_below_040", "fraction_above_060"]]
tr, te = load("x_train_final", cols), load("x_test_final", cols)
alld = pd.concat([tr, te])


def n_words(d):
    return np.expm1(d["nrc_hit_count_log"].to_numpy()).round()


def V(d, s):  # (n, 2) array of a statistic for V and A
    return d[[f"nrc_V_{s}", f"nrc_A_{s}"]].to_numpy(float)


# empirical Bayes constants, from all unlabeled speeches (train + test features, no labels).
# Model: var(mean | n matched words) = tau2 + sigma2 / n.
#   tau2  = between-speech "true" variance: read on long speeches (n >= 100) where noise is negligible.
#   sigma2 = word-level noise: median over n in [5, 50] of n * (var - tau2).
# (The per-speech nrc_*_std is 0 for 1-word speeches, so it cannot be used directly.)
alld = alld.assign(n=n_words(alld))
ok = alld["n"] > 0
mu = V(alld[ok], "mean").mean(0)
K, tau2, sigma2 = [], [], []
for c in ["nrc_V_mean", "nrc_A_mean"]:
    g = alld[ok & (alld["n"] <= 300)].groupby("n")[c].var()
    t2 = alld.loc[alld["n"] >= 100, c].var()
    mid = g.loc[5:50]
    s2 = float(np.median(mid.index.values * (mid.values - t2)))
    tau2.append(t2); sigma2.append(s2); K.append(s2 / t2)
K = np.array(K)
mu_src = alld[ok].groupby("source")[["nrc_V_mean", "nrc_A_mean"]].mean()
json.dump({"K": K.round(2).tolist(), "tau2": np.round(tau2, 6).tolist(), "sigma2": np.round(sigma2, 5).tolist(),
           "mu": mu.round(4).tolist(), "mu_source": mu_src.round(4).to_dict("index")},
          open(Path(__file__).parent / "eb_constants.json", "w"), indent=1)
print("K =", K.round(1), "tau2 =", np.round(tau2, 5), "sigma2 =", np.round(sigma2, 4), "mu =", mu.round(4))

ids, n = te["id"].to_numpy(), n_words(te)[:, None]
raw = V(te, "mean")


def eb(prior):
    out = (n * raw + K * prior) / (n + K)
    return np.where(n > 0, out, prior)


def moment_match(x, ref):
    return (x - x.mean(0)) / x.std(0) * ref.std(0) + ref.mean(0)


preds = {
    "raw_mean": (raw, "Werlen: nrc_*_mean"),
    "median": (V(te, "median"), "nrc_*_median"),
    "mean_median": ((raw + V(te, "median")) / 2, "average of mean and median"),
    "mid_q": ((V(te, "q10") + V(te, "q90")) / 2, "(q10+q90)/2"),
    "polarity": (moment_match(0.5 + (V(te, "fraction_above_060") - V(te, "fraction_below_040")) / 2, raw),
                 "share >0.6 minus share <0.4, moment-matched"),
    "eb_global": (eb(mu), f"empirical Bayes, K={K.round(1).tolist()}"),
    "eb_source": (eb(mu_src.loc[te["source"]].to_numpy()), "empirical Bayes to the parliament mean"),
}
for name, (p, note) in preds.items():
    log_submission(TR, name, ids, np.clip(p, 0, 1), note)
