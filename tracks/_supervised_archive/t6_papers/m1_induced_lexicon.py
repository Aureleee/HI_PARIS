"""t6 / M1 — Induced lexicon + mean over matched words (Werlen et al. 2021, Buechel et al. 2019).
Werlen: speech score = unweighted mean of valence/arousal of the words found in a lexicon.
We have no allowed external lexicon, so we INDUCE one from the train folds:
  word value = smoothed mean target of the speeches containing the word (shrunk to the global mean).
Speech score = mean value of its known words, then a small LightGBM calibrates it with source/year.
Usage: python tracks/t6_papers/m1_induced_lexicon.py [n_rows]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from src.common import TARGETS, folds, load, log_result, write_submission

n_rows = int(sys.argv[1]) if len(sys.argv) > 1 else None
K = 20  # smoothing: a word seen in few speeches stays close to the global mean

tr = load("x_train_final", ["id", "clean_text", "date", "source"]).merge(load("y_train"), on="id")
te = load("x_test_final", ["id", "clean_text", "date", "source"])
if n_rows:
    tr = tr.sample(n_rows, random_state=0)
y = tr[TARGETS].to_numpy(float)
fold = folds(tr["id"])

vec = CountVectorizer(lowercase=True, min_df=5, max_features=200_000, binary=True, token_pattern=r"(?u)\b\w\w+\b")
Xtr, Xte = vec.fit_transform(tr["clean_text"]), vec.transform(te["clean_text"])


def lexicon(X, yy):
    df = np.asarray(X.sum(0)).ravel()
    return (X.T @ yy + K * yy.mean(0)) / (df[:, None] + K)  # (n_words, 2)


def score(X, lex, mu):
    n = np.asarray(X.sum(1)).ravel()[:, None]
    return np.where(n > 0, (X @ lex) / np.maximum(n, 1), mu)  # mean over matched words


lex_oof = np.zeros_like(y)
for k in range(5):
    t, v = fold != k, fold == k
    lex_oof[v] = score(Xtr[v], lexicon(Xtr[t], y[t]), y[t].mean(0))
lex_full = lexicon(Xtr, y)
lex_te = score(Xte, lex_full, y.mean(0))
log_result("t6_papers", "m1_lexicon_raw" + (f"_n{n_rows}" if n_rows else ""), tr["id"].to_numpy(), y, lex_oof,
           te["id"].to_numpy(), lex_te, notes="Werlen-style mean of induced word values, no calibration")


# calibration with source/year (like per-language/session effects in Werlen)
def feats(d, s):
    return pd.DataFrame({"lv": s[:, 0], "la": s[:, 1], "year": pd.to_datetime(d["date"], errors="coerce").dt.year.values,
                         "source": d["source"].astype("category").values})


F, Ft = feats(tr, lex_oof), feats(te, lex_te)
oof, test = np.zeros_like(y), np.zeros((len(te), 2))
p = dict(objective="regression", learning_rate=0.05, num_leaves=31, verbose=-1, seed=2026)
for j in range(2):
    for k in range(5):
        t, v = fold != k, fold == k
        m = lgb.train(p, lgb.Dataset(F[t], y[t, j]), 300)
        oof[v, j] = m.predict(F[v])
        test[:, j] += m.predict(Ft) / 5
name = "m1_lexicon_calibrated" + (f"_n{n_rows}" if n_rows else "")
log_result("t6_papers", name, tr["id"].to_numpy(), y, oof, te["id"].to_numpy(), test, notes="+ source/year calibration")

# top words of the induced lexicon (useful for the report and the mockup)
words = np.array(vec.get_feature_names_out())
df = np.asarray(Xtr.sum(0)).ravel()
L = pd.DataFrame({"word": words, "df": df, "valence": lex_full[:, 0], "arousal": lex_full[:, 1]})
L[L.df >= 50].sort_values("valence").to_csv(Path(__file__).parent / "induced_lexicon.csv", index=False)
if not n_rows:
    write_submission(te["id"].to_numpy(), test, "t6_m1_lexicon")
