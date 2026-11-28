"""t6 / Mendes & Martins 2023 (from scratch), round 2: self-training + character n-grams.
Round 1 (distill.py): text model learns the rule scores -> blend 50/50 gave LB 0.33 / 0.32 (rules alone 0.30 / 0.24).
Round 2 here:
  1. Out-of-fold (2 folds) text-model predictions on train, blended 50/50 with the rule scores
     -> new pseudo-labels, closer to what scored best on the leaderboard (classic self-training).
  2. Retrain on them with word uni+bigrams AND character 3-5 grams (punctuation, French elisions,
     typos, words the English lexicon never sees).
  3. Test prediction, moment-matched to the rule scale, and blended 50/50 with the rules again.
Usage: python tracks/t6_papers/selftrain.py [n_train] [char]   (char n-grams need a lot of RAM: use n_train <= 100000)"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction.text import HashingVectorizer, TfidfTransformer
from sklearn.linear_model import Ridge

from pseudo import rule_scores
from src.common import load, log_submission

n_train = int(sys.argv[1]) if len(sys.argv) > 1 else 400000
use_char = len(sys.argv) > 2 and sys.argv[2] == "char"
t0 = time.time()
COLS = ["id", "clean_text", "nrc_V_mean", "nrc_A_mean", "nrc_V_mean_abs_neutral", "ctx_negation_scope_hit_fraction",
        "ctx_negation_scope_valence_mean", "exclamation_density", "repeated_punctuation_density",
        "uppercase_word_fraction", "ctx_high_arousal_fraction"]
tr = load("x_train_final", COLS).sample(n_train, random_state=1).reset_index(drop=True)
te = load("x_test_final", COLS)
y_rules_tr, y_rules_te = rule_scores(tr), rule_scores(te, ref=tr)

word = HashingVectorizer(lowercase=True, alternate_sign=False, norm=None, n_features=2**20,
                         ngram_range=(1, 2), token_pattern=r"(?u)\b\w+\b|[!?]")
char = HashingVectorizer(lowercase=False, alternate_sign=False, norm=None, n_features=2**18,
                         analyzer="char_wb", ngram_range=(3, 5))


def feats(texts, fit=None):
    W = word.transform(texts).astype(np.float32)
    if not use_char:
        if fit is None:
            fit = (TfidfTransformer(sublinear_tf=True).fit(W),)
        return fit[0].transform(W), fit
    C = char.transform(texts).astype(np.float32)
    if fit is None:
        fit = (TfidfTransformer(sublinear_tf=True).fit(W), TfidfTransformer(sublinear_tf=True).fit(C))
    return sp.hstack([fit[0].transform(W), 0.7 * fit[1].transform(C)]).tocsr(), fit


Xtr, fit = feats(tr["clean_text"].fillna(""))
print(f"features {Xtr.shape} in {time.time() - t0:.0f}s", flush=True)


def predict_test(models):  # test in batches of 50k to fit in memory
    texts = te["clean_text"].fillna("").tolist()
    out = []
    for i in range(0, len(texts), 50000):
        X, _ = feats(texts[i:i + 50000], fit)
        out.append(np.c_[[m.predict(X) for m in models]].T)
    return np.vstack(out)


def mm(x, ref):
    return (x - x.mean(0)) / x.std(0) * ref.std(0) + ref.mean(0)


# 1. out-of-fold text predictions on train (2 folds) -> round-2 pseudo-labels
half = np.arange(len(tr)) % 2 == 0
oof = np.zeros_like(y_rules_tr)
for j in range(2):
    for a, b in [(half, ~half), (~half, half)]:
        oof[b, j] = Ridge(alpha=1.0, solver="sparse_cg").fit(Xtr[a], y_rules_tr[a, j]).predict(Xtr[b])
    print(f"dim {j}: OOF corr with rules = {np.corrcoef(oof[:, j], y_rules_tr[:, j])[0, 1]:.3f} ({time.time() - t0:.0f}s)", flush=True)
y2 = 0.5 * mm(oof, y_rules_tr) + 0.5 * y_rules_tr

# 2. retrain on round-2 pseudo-labels, predict test
models = [Ridge(alpha=1.0, solver="sparse_cg").fit(Xtr, y2[:, j]) for j in range(2)]
del Xtr
pred = predict_test(models)
text = mm(pred, y_rules_te)
ids = te["id"].to_numpy()
log_submission("t6_papers", "selftrain_" + ("wordchar" if use_char else "word"), ids, text.clip(0, 1), "round 2 self-training, word+char text model alone")
log_submission("t6_papers", "blend_rules_selftrain_" + ("wordchar" if use_char else "word"), ids, mm(0.5 * text + 0.5 * y_rules_te, y_rules_te).clip(0, 1),
               "50/50 rules + round-2 word+char text model")
for j, d in enumerate(["valence", "arousal"]):
    print(f"{d}: corr(text, rules) test = {np.corrcoef(text[:, j], y_rules_te[:, j])[0, 1]:.3f}")
print(f"done in {time.time() - t0:.0f}s")
