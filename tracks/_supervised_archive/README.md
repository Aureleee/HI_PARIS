# Supervised archive

These tracks were written when we thought the train had labels. It does not (the challenge is unsupervised).
Kept because parts are reused with pseudo-labels (see t2 and t4): `t6_papers/m1_induced_lexicon.py` (induced lexicon),
`t6_papers/m3_small_transformer.py` (transformer from scratch), `t1_gbdt/train_lgbm.py` (GBDT on pseudo-labels).
They read `data/processed/y_train.parquet`: point them to pseudo-labels instead.
