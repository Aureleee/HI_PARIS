# CLAUDE.md — Hi!ckathon #7 (Hi! PARIS)

> Context file for Claude Code. Read it fully before touching the code.
> Source of truth: the organizers' Drive folder "Hi!ckathon-Challenge" + `Reglement_Hickathon2026.pdf`.
> Last update: Fri 27 Nov 2026, ~21:15.
>
> **Every Claude agent of the team: start with "▶ START HERE" just below.**

---

## ▶ START HERE (every Claude agent, every new session)

### 1. Find out who you work for
1. Run `git config user.name`, `git config user.email` and `git branch --show-current`.
2. Match with the team table in §1 (name or GitHub login). If it's unclear, **ask the user: "Who are you: Aurèle, Nel, Rubens, Sachit or Kishan?"** Never guess.
3. Their role = their track in §0bis:

| Person | Branch | Track | Track plan |
|---|---|---|---|
| Aurèle | `aurele` | `t1_gbdt` | `tracks/t1_gbdt/README.md` |
| Nel | `nel` | `t2_chunks` | `tracks/t2_chunks/README.md` |
| Rubens | `rubens` | `t3_ushape` | `tracks/t3_ushape/README.md` |
| Sachit | `sachit` | `t4_text` | `tracks/t4_text/README.md` |
| Kishan | `kishan` | `t5_domain` | `tracks/t5_domain/README.md` |

(Owners may swap tracks. If the user says so, follow the user and update this table.)

### 2. First-time setup on a new computer (do it yourself, then confirm)
1. If git has no identity: ask the user for their name + GitHub email, then `git config user.name "..."` and `git config user.email "..."` (repo only).
2. Go to their branch: `git checkout <branch>` if it exists on origin (`git fetch origin` first), else `git checkout -b <branch> && git push -u origin <branch>`.
3. If `data/processed/` is empty: `bash scripts/download_data.sh` (installs requirements, downloads the Drive, converts to parquet). If gdown fails, tell the user to download the Drive folder by hand into `data/raw/` and then run `python src/prepare_data.py`.
4. Check `.claude/settings.json` exists (sync hooks). Remind the user to accept the hooks once.

### 3. Brief the user, then start
Tell the user in a few lines: who they are in the team, their track, the papers behind it, the plan steps from their track README, and the timeline (§0bis). Then start step 1 of their plan right away.

### 4. End of EVERY piece of work: give the push command
Even though the hooks auto-push, **always end your reply with a copy-paste block** so the user can push cleanly by hand (hooks may be off, or the user may work without Claude Code). **Check the OS first** (`uname` works on Mac/Linux; on Windows the prompt is PowerShell or `$env:OS` is `Windows_NT`) and give the matching block. Fill in the real path, branch and message. Never put Claude in the message or as co-author.

**Mac / Linux** (Terminal):
```bash
# push my branch
cd <repo path> && git add -A && git commit -m "<short message>" ; git push -u origin <branch>
# ready to share with the team: push my branch + merge into main + push main
cd <repo path> && git add -A && git commit -m "<short message>" ; bash scripts/ship.sh
```

**Windows** (PowerShell, in the repo folder):
```powershell
# push my branch
cd <repo path>; git add -A; git commit -m "<short message>"; git push -u origin <branch>
# ready to share with the team
cd <repo path>; git add -A; git commit -m "<short message>"; python scripts\gitsync.py ship
```

`ship` = push own branch + merge it into `main` + push `main`. No Pull Request needed.
`scripts/gitsync.py` (`sync` | `push` | `ship`) is the cross-platform Python version of the `.sh` scripts: use it on Windows, or anywhere bash is missing.

### 5. Windows notes
- Claude Code on Windows needs **Git for Windows** (it brings Git Bash). With it, the `bash` hooks in `.claude/settings.json` work as on Mac. If a hook fails with "bash not found", install Git for Windows, or run `python scripts\gitsync.py sync` at the start and `python scripts\gitsync.py push` at the end by hand.
- Data download on Windows (PowerShell, in the repo):
  ```powershell
  pip install -r requirements.txt
  gdown --folder "https://drive.google.com/drive/folders/1i2Ith9mfzTHyb1DX2WHSuXxeB2PCWjNM" -O data/raw
  python src/prepare_data.py
  ```
- Use `python` (not `python3`) and backslashes in paths in PowerShell. `&&` does not exist in old PowerShell: chain with `;`.
- SSH key: `git clone git@github.com:Aureleee/HI_PARIS.git` needs an SSH key added to GitHub (`ssh-keygen -t ed25519`, then paste `~\.ssh\id_ed25519.pub` in GitHub → Settings → SSH keys).

---

## 0. Team workflow (MANDATORY for every Claude agent)

5 people, 5 Claude agents, 1 repo: `git@github.com:Aureleee/HI_PARIS.git` (SSH only, never HTTPS).

### Branches
- **One branch per person**, named after the first name: `aurele`, `nel`, `rubens`, `sachit`, `kishan`.
- **Never commit or push directly to `main`.** If the current branch is `main`, stop and ask the user to run `git checkout -b <firstname>` (or `git checkout <firstname>` if it exists).
- `main` = what works. When your code runs end to end, merge it from the terminal with `bash scripts/ship.sh` (merges your branch into `main` and pushes). No Pull Request needed. Tell the team when you ship.

### Automatic sync (already wired, see `.claude/settings.json`)
- **Before each prompt** (`UserPromptSubmit` hook → `scripts/sync.sh`): auto-commits local changes, pulls your own branch, then merges `origin/main` into it. Its output appears in your context as `[sync] ...`.
- **After each answer** (`Stop` hook → `scripts/autopush.sh`): commits everything and pushes your branch.
- If you see `[sync] CONFLICT`: stop, tell the user, resolve the conflict with them, commit, then continue. Never discard a teammate's work to make a conflict disappear.
- If the hooks are not active (e.g. first run, hook approval pending), do it by hand: `bash scripts/sync.sh` at the start, `bash scripts/autopush.sh` at the end.

### Avoiding conflicts
- Your code lives in `tracks/<your_track>/`. Don't edit someone else's track; copy what you need.
- Shared code lives in `src/`. Small focused changes, announced to the team.
- Results: only through `log_result()` (each track has its own CSV, so no conflicts).

### Commits
- Commit messages short, English, imperative: `add lgbm baseline on nrc features`.
- **No Claude attribution anywhere on GitHub**: no `Co-Authored-By: Claude`, no "Generated with Claude" in commits, PRs or files. Commits are authored by the human's own git identity.
- Never commit data (`data/`, `*.csv`, `*.parquet`, models). `.gitignore` covers it and `autopush.sh` refuses files > 50 MB.

### First setup for a teammate
```bash
git clone git@github.com:Aureleee/HI_PARIS.git && cd HI_PARIS
git checkout -b <firstname> && git push -u origin <firstname>
bash scripts/download_data.sh      # Drive -> data/raw -> data/processed (parquet)
```
Then open Claude Code in the repo and accept the project hooks.

---

## 0bis. Research tracks (one per person, compared on the same ground)

Each person owns **one track**: one research idea from a recent paper, reimplemented from scratch, pushed as far as possible (implementation, tests, training, ablations). At the end we compare all tracks on the same folds and ensemble the best ones.

| Track | Default owner | Idea | Main refs |
|---|---|---|---|
| `t1_gbdt` | Aurèle | Strong GBDT baseline on the 342 features + losses for bounded targets (logit link, cross-entropy) | arXiv 2512.05231, 2604.07066 |
| `t2_chunks` | Nel | Score sentences/chunks, then length-weighted aggregation (mimics how the target is built) | arXiv 2512.05231 |
| `t3_ushape` | Rubens | Joint valence–arousal: U-shape, chained and multi-output models | arXiv 2601.21483, 2608.30828 |
| `t4_text` | Sachit | Text models trained from scratch: sparse TF-IDF + linear, small NN, stacking | arXiv 2604.07066 |
| `t5_domain` | Kishan | Train/test shift, validation design, per-country models, error and bias analysis | arXiv 2609.26346, 2512.10882 |

Owners can swap. **The detailed plan of each track is in `tracks/<track>/README.md`. Read yours before coding.**

### Rules for every track (mandatory, so results are comparable)
1. **Work only in `tracks/<your_track>/`** (notebooks + scripts). Do not edit another track's folder.
2. **Use `src/common.py`** for everything shared:
   - `load()` to read data, `feature_cols()` for the 342 features,
   - `folds(ids)` for CV: **the same 5 folds for everyone**, deterministic from the id. Never use your own split for reported scores.
   - `score()` = the shared metric. Primary: `rmse_mean` (lower is better) until the official HFactory metric is known, then we switch.
3. **Log every run** (good or bad) with `log_result(track, experiment, train_ids, y, oof, test_ids, test_pred, notes=...)`:
   - one line in `results/scores/<track>.csv`,
   - OOF preds in `results/oof/`, test preds in `results/test/` (needed for the final ensemble).
   Name experiments clearly: `lgbm_all_feats_l2`, `lgbm_xent`, `chunks_sent_wmean`...
4. Run `python scripts/leaderboard.py` to rebuild `results/RESULTS.md` (best run per track + all runs). If `RESULTS.md` conflicts on merge: rerun the script, never hand-edit.
5. Keep `tracks/<track>/README.md` up to date: what was implemented, numbers, plots, what worked, limits. It goes almost as is into the final report.
6. Changes to `src/common.py` (folds, metric) only after telling the team. `t5_domain` may change the folds if the test turns out to be a time split: then everyone reruns their best run.
7. No pretrained models, no AutoML, no external data without written OK (see §4). Fit any vectorizer/encoder on train only, inside the folds when it uses the target.
8. To submit on HFactory: `write_submission(test_ids, pred, name)` → `submissions/<name>.csv`. Put the LB score in the `lb` field of the run.

### How your Claude agent should work on a track
- Start with the simplest working version, log it, then iterate. One experiment = one logged run.
- After each meaningful result: update the track README, run the leaderboard script. The hooks push automatically.
- Always compare against the current best `t1_gbdt` run in `results/RESULTS.md`.
- Add simple plots (bars, curves, scatter) in the notebook, not only prints.
- Keep code short. No big generic frameworks.

### Timeline
| When | What |
|---|---|
| Fri night | Setup, data download, first run of each track (even a bad one). `t5` checks the train/test shift. |
| Sat 12:00 | Every track has a full working result logged. |
| Sat 22:00 | Tracks frozen. Best OOF/test preds of each track in `results/`. |
| Sun morning | Ensemble on `main` (weighted average / ridge stacking on OOFs), final submission. |
| Sun 16:00 | All deliverables uploaded. |

---

## 1. The event

- **Hi!ckathon #7**, organized by Hi! PARIS (HEC Paris + IP Paris). Partners: TotalEnergies, Capgemini, L'Oréal, Vinci, Schneider Electric.
- **Theme: "AI & Democracy".**
- Location: ENSTA Paris, 828 bd des Maréchaux, Palaiseau. In person only.
- **Team (re-formed after the official list), room 13.18**:
  | Name | GitHub |
  |---|---|
  | Aurèle Habbard (repo owner) | `Aureleee` |
  | Nel Choisnet Dupuij | `neldupuij` |
  | Rubens Do Fetal | `rdzinhoo941` |
  | Sachit Kumar | `sachitkumardps` |
  | Kishan Modi | `kmodi2412` |
- Data hosting + leaderboard submissions: **HFactory (Data Factory HEC)**, https://hfactory.io/
- Comms: Discord (optional). Emergency contact: Pierre-Antoine Amiand-Leroy, 06 36 93 00 85.

### Timeline (Paris time)

| When | What |
|---|---|
| Fri 27 Nov, 20:00 | Kick-off, dataset reveal |
| Sun 29 Nov, **16:00** | End of challenge / restitution (welcome doc) |
| Sun 29 Nov, **18:00** | Hard deadline for the 4 deliverables (rules, art. 8). **Aim for 16:00.** |
| Sun 29 Nov, ~20:00 | Pre-selection of finalist teams |
| Mon 30 Nov, 18:00–18:30 | Closing ceremony: finalists pitch (mockup + valorisation), awards ~20:00 |

Missing any of the 4 deliverables = not eligible for selection.

---

## 2. The task

**Regression on parliamentary speeches.** For each speech, predict two continuous targets:

- `valence_chunks_weighted_mean`
- `arousal_chunks_weighted_mean`

Name suggests the targets are emotion scores (valence = positive/negative, arousal = calm/excited) computed on text chunks of the speech, then averaged with weights (probably chunk length). They are **not** the NRC lexicon features we get as input, but those are the obvious first proxies.

Corpus: speeches from several parliaments.
- `source` values seen in the sample: `assemblee`, `senat` (FR), `uk_commons` (UK), `us_congress` (US).
- Plus a separate Italian file (`x_Italia.csv`), see §3.
- Dates seen: 1989 → 2026.

**Metric: not written in any Drive file yet.** It is "communicated at kick-off" (rules art. 7). Check HFactory / Discord and fill it here:
- Metric: `TODO`
- Submission limit per day: `TODO`
- Public/private leaderboard split: `TODO`

### Submission format

Template = `y_test_zero.csv`:

```
id,valence_chunks_weighted_mean,arousal_chunks_weighted_mean
869896,0,0
869897,0,0
...
```

One row per test `id`, same order and same ids as the template. Test ids start at 869896 and look contiguous.

---

## 3. Data (Drive folder "Hi!ckathon-Challenge")

Drive folder: https://drive.google.com/drive/folders/1i2Ith9mfzTHyb1DX2WHSuXxeB2PCWjNM

| File | Size | Content |
|---|---|---|
| `x_train_final.csv` | 1.85 GB | Train set. Should contain the targets (there is no separate `y_train`). **Check the header first.** |
| `x_test_final.csv` | 818 MB | Test features |
| `y_test_zero.csv` | 4.1 MB | Submission template (all zeros) |
| `x_Italia.csv` | 909 MB | Italian parliament speeches. Role unclear: extra test domain? unlabeled transfer set? **Ask organizers.** |
| `sample_x_test.csv` / `.xlsx` | 22 MB / 16 MB | 460-row sample to look at the schema |
| `Features_dictionary_EN_FR.xlsx` | 74 KB | Definition of every feature (EN + FR) |
| `dictionnaire_thematiques_parlement.xlsx` | 44 KB | 10 political themes × 50 terms each, in FR / EN / IT, with a "polysemous" flag |
| `Reglement_Hickathon2026.pdf` | 319 KB | Rules |
| `liste_participants_groupes (1).pdf` | 22 KB | Teams and rooms |

**Data is NOT in git** (GitHub refuses files > 100 MB, and rules art. 7 bis forbid spreading the dataset). Everyone gets it with one command:

```bash
bash scripts/download_data.sh   # gdown of the whole Drive folder into data/raw/, then parquet in data/processed/
```

If gdown fails (Drive quota / permissions), download the files by hand from the Drive folder into `data/raw/`, then run `python src/prepare_data.py`. Always load the parquet files, not the CSVs.

### What we know from the real files (checked Fri 27 Nov, 22:45)
- `x_train_final`: **869,896 rows**, ids 0 → 869,895. `x_test_final`: **372,812 rows**, ids 869,896 → 1,242,707.
- **⚠️ The train file has NO target columns** (no valence/arousal) and there is no `y_train` in the Drive. Asked the organizers / check HFactory. When it arrives: put it in `data/raw/`, run `python src/prepare_data.py`, it becomes `data/processed/y_train.parquet` (columns `id` + the 2 targets). All training scripts read it from there.
- 218 columns: `id`, `clean_text`, `date`, `source` + **214 features**. Families A, B, D, F, G, H only. **No `tfidf_svd_*`, no `char_tfidf_svd_*`, no `text_en`.**
- `source` = 25 % each: `assemblee` (2007–2024), `senat` (1996–2026), `uk_commons` (1988–2019), `us_congress` (1994–2024).
- **Test = random split**: same sources, same years, same length distribution as train. The shared random folds in `src/common.py` are the right validation.
- **Drive download quota**: on Friday night gdown fails with "Too many users have viewed or downloaded this file". Workaround: open the file in the browser and use "Download", or make a copy in your own Drive and download the copy.

### Columns (from `sample_x_test.csv`, 218 columns)

Metadata: `id`, `clean_text` (raw speech, original language), `date` (YYYY-MM-DD), `source`.

Precomputed features, 342 defined in the dictionary, grouped in families:

| Family | Prefix | # | What |
|---|---|---|---|
| A | `log_n_*`, `*_density`, `type_token_ratio`, ... | 29 | Surface stats on the cleaned source-language text: length, word length, punctuation densities, `question_present`, `interruption_cue_present`, negation fraction |
| B | `nrc_*` | 32 | NRC VAD lexicon on the English text: hit count, coverage, then for V / A / D: mean, std, min, max, median, q10, q90, share <0.40, share >0.60, mean distance to 0.5 |
| D | `glove_mean_00..49` | 50 | Mean 50D GloVe vector of the English text |
| E | `tfidf_svd_00..63` | 64 | Word TF-IDF (1–2 grams) + TruncatedSVD 64D, fit on TRAIN `text_en` |
| F | `native_*` | 37 | Rhetorical cues in the native language: pronouns, negations, obligation, questions/exclamations by position... |
| G | `en_*` | 38 | Same kind of cues on the English (translated) text: pronouns, comparison, polite address, emphasis, frames... |
| H | `ctx_*` | 28 | Contextual emotion features: high-arousal fractions, negation/intensifier scopes, emotional runs, first vs last third |
| I | `char_tfidf_svd_00..63` | 64 | Char 3–5 gram TF-IDF + SVD 64D on TRAIN `text_en` |

**Warning**: the sample has only 214 features. Families E and I (`tfidf_svd_*`, `char_tfidf_svd_*`) are missing from it. Check whether they are in the final train/test files.

Note: the features talk about a `text_en` column (English translation). It is not in the sample. Check if it is in the final files. If yes, it is gold for our own text models.

---

## 4. Rules that constrain the code (rules art. 7, 7 bis, 7 ter)

Breaking any of these = disqualification.

- **Python only.** Code as `.py` / `.ipynb`.
- **No pretrained models.** No CamemBERT, no sentence-transformers, no HF checkpoints, no pretrained embeddings we load ourselves. Everything we train is trained from scratch on the provided data. (The GloVe/NRC features are given by the organizers, using them as columns is fine.)
- **No AutoML**: AutoGluon, H2O AutoML, auto-sklearn, FLAML, TPOT banned (list may be extended at kick-off).
- **No scraping.** No enriching the data with external personal data.
- **Tools and APIs: authorized by the organizers for our team** (written confirmation, Fri 27 Nov). This covers Claude (paid plan), coding assistants and external APIs used **during development**.
- **Exception: AI inside the delivered product.** If the final deliverable (mockup / app) runs an AI model at runtime (e.g. a feature that analyses a speech), that model must run **locally**. No call to an external AI API in the product.
- **No personal GPU.** Only the compute provided by the organizers.
- The leaderboard model still follows "no pretrained models" (above) unless organizers say otherwise.
- **Do not try to rebuild the test set or the targets** from the public sources the data comes from.
- Data is for the contest only. No sharing, delete it after the event.
- Never attribute intentions/opinions to a named person based on model outputs (relevant for the mockup and the video).
- Code must be released under an open-source licence, preferably **LGPL v3**, with this header in the project:

  > The present code is developed during a contest called « HI!CKATHON » organized at the request of HEC Paris and Institut Polytechnique de Paris, in the context of the Hi ! PARIS Center

Allowed: LightGBM, XGBoost, CatBoost, scikit-learn, PyTorch (training from scratch), Optuna for manual tuning, etc.

---

## 5. The 4 deliverables

The data part must be at least half of the work.

1. **Data-science project** (this repo): notebooks + scripts, predictions submitted on HFactory → leaderboard.
2. **Short report** (`.pdf`, `.pptx` or `.docx`): approach, methodology, **limits and biases**, team organisation, valorisation plan.
3. **Clickable mockup** of the tool/service built from our results: Figma link or web app online until the jury is done, or a `.html` file.
4. **Video pitch**: between **2:30 and 3:00**, one take without editing, speakers visible on screen when they talk. Slides can be added.

### Prizes (one per team max)

- **Technical excellence**: best leaderboard score.
- **Scientific approach**: best justification, comparison to state of the art, analysis of limits and biases.
- **Innovation**: most innovative and complete mockup.
- **Best pitch**: best projection into a real use case (citizens, institutions, media).
- **Audience favourite**: public vote on Monday.

---

## 6. Plan

### Phase 0 — setup (Fri night)
- [ ] Get HFactory access, find the metric, fill §2.
- [ ] `bash scripts/download_data.sh` (each teammate).
- [ ] Check train header: targets, `text_en`, families E/I present?
- [ ] Check `x_Italia.csv`: labeled? in the test? Ask organizers.
- [ ] Submit `y_test_zero` + a train-mean baseline to validate the pipeline.

### Phase 1 — EDA (Fri night / Sat morning)
- [ ] Target distributions, correlation valence vs arousal, by `source` and by year.
- [ ] Train vs test shift: `source`, `date`, text length. Are test ids a later time period or a random split? Validation must mimic it.
- [ ] Quick feature importance; how much do `nrc_V_*` / `nrc_A_*` explain alone.

### Phase 2 — models (Sat)
- Validation: KFold with stratification on `source` (+ time-based split if the test is later in time).
- Baseline: ridge on the 342 features.
- Main: GBDT (LightGBM / CatBoost), one model per target, `source` as categorical, date → year.
- Own text features from scratch: TF-IDF on `clean_text` (and `text_en` if present) → ridge / linear SVR, stacked into the GBDT.
- Optional: small NN trained from scratch on TF-IDF.
- Theme features from `dictionnaire_thematiques_parlement.xlsx` (counts per theme, FR/EN/IT).
- Ensemble the best ones. Tune on CV, not on the leaderboard.

### Phase 3 — product + report (Sat evening → Sun)
- Mockup idea space: emotion/tone barometer of parliamentary debates by theme, country and time (FR / UK / US / IT). Use the theme dictionary to slice. No ranking of named MPs.
- Report: method, CV vs LB, error analysis by source/language/period, biases (translation to English, NRC lexicon bias, US/UK vs FR, era drift).
- Video: script, rehearse, record in one take before Sunday 15:00.

### Phase 4 — wrap up (Sun before 16:00)
- [ ] Final submission.
- [ ] Repo clean, LGPL v3 `LICENSE`, header in README.
- [ ] Upload all 4 deliverables.

---

## 7. Repo layout (target)

```
HI_PARIS/
├── CLAUDE.md
├── README.md            # contest header + how to run
├── LICENSE              # LGPL v3
├── .gitignore           # data/, *.csv, *.parquet, models
├── .claude/settings.json  # sync hooks
├── requirements.txt
├── tracks/              # one folder per research track (see §0bis)
│   ├── t1_gbdt/  t2_chunks/  t3_ushape/  t4_text/  t5_domain/
├── results/
│   ├── scores/          # <track>.csv, one line per run (log_result)
│   ├── oof/  test/      # predictions for the final ensemble
│   └── RESULTS.md       # generated by scripts/leaderboard.py
├── scripts/
│   ├── sync.sh          # pull own branch + merge origin/main (before each prompt)
│   ├── autopush.sh      # commit + push own branch (after each answer)
│   ├── download_data.sh # Drive -> data/raw -> parquet
│   ├── leaderboard.py   # results/scores -> results/RESULTS.md
│   ├── ship.sh          # merge your branch into main + push
│   └── gitsync.py       # same as sync/autopush/ship, cross-platform (Windows)
├── data/
│   ├── raw/             # Drive CSVs (never committed)
│   └── processed/       # parquet
├── notebooks/           # EDA, experiments (01_eda.ipynb, ...)
├── src/
│   ├── prepare_data.py  # csv -> parquet, dtypes
│   ├── features.py      # extra features (TF-IDF, themes, date)
│   ├── cv.py            # folds
│   ├── train.py         # models, OOF preds
│   └── predict.py       # writes submission in the y_test_zero format
├── submissions/
├── report/
└── mockup/
```

---

## 8. Working conventions for Claude

- Never commit data or anything from the Drive.
- Keep code short and readable, the team reads it in a rush.
- Fixed seeds everywhere (organizers use 2026).
- Each experiment: log it with `log_result()` (see §0bis), never by hand.
- Always write predictions with the exact columns and ids of `y_test_zero.csv`; assert row count and id order before saving.
- Do not suggest anything that breaks §4 (pretrained models, AutoML, paid APIs, scraping).
- Git: follow §0. SSH remote `git@github.com:Aureleee/HI_PARIS.git`.

---

## 9. Open questions (to ask organizers / check on HFactory)

1. Evaluation metric, and is it averaged over the 2 targets?
2. Role of `x_Italia.csv` (part of the test? labels?).
3. Are `text_en`, `tfidf_svd_*`, `char_tfidf_svd_*` in the final train/test files?
4. Submission limits and leaderboard split.
5. Compute provided by organizers (GPU? RAM?) and how to access it.
6. Licence of the source data (communicated at kick-off).
