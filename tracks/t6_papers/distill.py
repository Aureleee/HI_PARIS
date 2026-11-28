"""t6 / Mendes & Martins 2023 + Kim et al. 2024, rule-compliant version.
Mendes: a text model predicts valence and arousal from the raw text, in any language.
Kim: does a bigger model help? -> compare a small and a bigger text model.
No labels and no pretrained weights here: we DISTIL our best rule-based scores (t1 rules_neg_excl_cues,
LB 0.30) into text models trained from scratch on the 870k unlabeled train speeches.
Why it can help: the text model reads the original text (FR/EN), so it scores words and interjections
the English lexicon misses, and smooths noise across similar speeches.
Usage: python tracks/t6_papers/distill.py [small|big] [n_train]"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer, TfidfTransformer
from sklearn.linear_model import Ridge

from pseudo import rule_scores
from src.common import folds, load, log_submission

size = sys.argv[1] if len(sys.argv) > 1 else "small"
n_train = int(sys.argv[2]) if len(sys.argv) > 2 else None
cfg = {"small": dict(n_features=2**18, ngram_range=(1, 1)), "big": dict(n_features=2**20, ngram_range=(1, 2))}[size]
t0 = time.time()

tr = load("x_train_final").drop(columns=["date"])
if n_train:
    tr = tr.sample(n_train, random_state=0)
te = load("x_test_final").drop(columns=["date"])
y_tr = rule_scores(tr)
y_te_rules = rule_scores(te, ref=tr)

vec = HashingVectorizer(lowercase=True, alternate_sign=False, norm=None, token_pattern=r"(?u)\b\w+\b|[!?]", **cfg)
Xtr = vec.transform(tr["clean_text"].fillna(""))
tfidf = TfidfTransformer(sublinear_tf=True).fit(Xtr)
Xtr, Xte = tfidf.transform(Xtr), tfidf.transform(vec.transform(te["clean_text"].fillna("")))
print(f"vectorized {Xtr.shape} in {time.time() - t0:.0f}s", flush=True)

# held-out check on fold 0: how well does the text model reproduce the rule scores?
f = folds(tr["id"])
pred_te = np.zeros((len(te), 2))
for j, dim in enumerate(["valence", "arousal"]):
    m = Ridge(alpha=1.0, solver="sparse_cg").fit(Xtr[f != 0], y_tr[f != 0, j])
    p = m.predict(Xtr[f == 0])
    r = np.corrcoef(p, y_tr[f == 0, j])[0, 1]
    print(f"{dim}: held-out corr text model vs rule scores = {r:.3f}  ({time.time() - t0:.0f}s)", flush=True)
    pred_te[:, j] = Ridge(alpha=1.0, solver="sparse_cg").fit(Xtr, y_tr[:, j]).predict(Xte)


def mm(x, ref):  # same mean/std as the rule scores
    return (x - x.mean(0)) / x.std(0) * ref.std(0) + ref.mean(0)


ids = te["id"].to_numpy()
text = mm(pred_te, y_te_rules)
log_submission("t6_papers", f"distill_{size}", ids, text.clip(0, 1), f"text model from scratch ({size}) distilled on rule scores")
log_submission("t6_papers", f"blend_rules_distill_{size}", ids, mm(0.5 * text + 0.5 * y_te_rules, y_te_rules).clip(0, 1),
               f"50/50 rules + distilled text model ({size})")
for j, dim in enumerate(["valence", "arousal"]):
    print(f"{dim}: corr(text model, rules) on test = {np.corrcoef(text[:, j], y_te_rules[:, j])[0, 1]:.3f}")
print(f"done in {time.time() - t0:.0f}s")
