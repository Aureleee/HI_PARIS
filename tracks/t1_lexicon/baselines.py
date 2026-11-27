"""t1_lexicon: direct lexicon baselines from the organizers' NRC VAD features (no training).
Werlen et al. 2021: speech V/A = mean of the V/A of its lexicon words. The organizers already give it:
nrc_V_mean / nrc_A_mean (NRC VAD v2 on the English text, fallback 0.5 when no word matched).
Variants:
  raw     : nrc_*_mean
  median  : nrc_*_median (robust to a few extreme words)
  shrink  : short speeches have few matched words, so their mean is noisy:
            (n * mean + K * corpus_mean) / (n + K), n = number of matched words
Usage: python tracks/t1_lexicon/baselines.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import numpy as np

from src.common import load, log_submission

K = 5
te = load("x_test_final", ["id", "nrc_hit_count_log", "nrc_V_mean", "nrc_A_mean", "nrc_V_median", "nrc_A_median"])
ids = te["id"].to_numpy()
n = np.expm1(te["nrc_hit_count_log"].to_numpy())[:, None]
mean = te[["nrc_V_mean", "nrc_A_mean"]].to_numpy()
mu = mean[n[:, 0] > 0].mean(0)

log_submission("t1_lexicon", "raw_mean", ids, mean, "nrc_V_mean, nrc_A_mean")
log_submission("t1_lexicon", "median", ids, te[["nrc_V_median", "nrc_A_median"]].to_numpy(), "nrc_*_median")
log_submission("t1_lexicon", f"shrink_k{K}", ids, (n * mean + K * mu) / (n + K), f"shrink to corpus mean, K={K}")
