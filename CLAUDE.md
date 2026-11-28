# CLAUDE.md — Hi!ckathon #7 (Hi! PARIS)

> Context file for Claude Code. Read it fully before touching the code.
> Source of truth: the organizers' Drive folder "Hi!ckathon-Challenge" + `Reglement_Hickathon2026.pdf`.
> Last update: Fri 27 Nov 2026, ~23:20.
>
> ## ⚠️ THE CHALLENGE IS UNSUPERVISED (changed Fri 23:15)
> **There are NO training labels and there will be none.** `x_train_final` has no valence/arousal, and that is by design.
> We do not train models on targets. We **estimate valence and arousal directly** with state-of-the-art unsupervised methods
> (lexicons, chunk scoring, combination of signals, weak supervision on pseudo-labels), and we compare methods
> with the HFactory leaderboard + agreement between methods. Every supervised idea is archived in `tracks/_supervised_archive/`.
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
| Aurèle | `aurele` | `t1_lexicon` | `tracks/t1_lexicon/README.md` |
| Nel | `nel` | `t2_chunks` (+ `t6_papers` if time) | `tracks/t2_chunks/README.md` |
| Rubens | `rubens` | `t3_combine` | `tracks/t3_combine/README.md` |
| Sachit | `sachit` | `t4_weak` | `tracks/t4_weak/README.md` |
| Kishan | `kishan` | `t5_validation` | `tracks/t5_validation/README.md` |

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
- Results: only through `log_submission()` (each track has its own CSV in `results/runs/`, so no conflicts).

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

## 0bis. Research tracks — UNSUPERVISED (one per person, compared on the same ground)

No labels: each person owns **one family of state-of-the-art unsupervised methods**, implements it, and produces test scores.
We compare all runs on the HFactory leaderboard (limited uploads, planned by t5) and by agreement between methods, then blend the best.

| Track | Default owner | Idea | Main refs |
|---|---|---|---|
| `t1_lexicon` | Aurèle | Lexicon baselines from the organizers' NRC features (mean, median, shrinkage for short speeches). First LB anchors. **3 submissions ready.** | Werlen 2021; NRC VAD v2 (arXiv 2503.23547) |
| `t2_chunks` | Nel | Score chunks/sentences, then **length-weighted mean** (= the target name). Lexicons induced per language from the doc-level NRC scores, since there is no `text_en`. | Werlen 2021; arXiv 2512.05231 |
| `t3_combine` | Rubens | Combine signals without labels: arousal from several cues (lexicon, `ctx_*`, punctuation, distance of V to 0.5), negation correction for valence, factor analysis | arXiv 2601.21483, 2608.30828 |
| `t4_weak` | Sachit | Weak supervision: text models trained from scratch on lexicon pseudo-labels (TF-IDF ridge, small transformer), lexicon expansion by label propagation | arXiv 1703.09825, 1708.03910, 2302.14021 |
| `t5_validation` | Kishan | Metric + upload plan, agreement between methods, sanity checks, Italian set, biases for the report | arXiv 2512.10882, 2609.26346 |
| `t6_papers` | Nel / whoever has time | Nel's papers: emotion time series per parliament (Buechel 2019) for the mockup/pitch, valorisation (Shah 2023) | `tracks/t6_papers/README.md` |

Owners can swap. **The detailed plan of each track is in `tracks/<track>/README.md`. Read yours before coding.**

### Rules for every track (mandatory, so results are comparable)
1. **Work only in `tracks/<your_track>/`**. Do not edit another track's folder.
2. **Use `src/common.py`**: `load()`, `feature_cols()` (the 214 features), `log_submission()`, `agreement()`, `write_submission()`.
3. **Every method that produces test scores**: `log_submission(track, experiment, test_ids, pred, notes)`:
   - writes `submissions/<track>__<experiment>.csv` (exact `y_test_zero` format) to upload on HFactory,
   - saves `results/test/<track>__<experiment>.parquet` (for blending and agreement),
   - adds a line in `results/runs/<track>.csv` with mean/std of the scores. **After uploading, write the LB score in its `lb` column.**
4. `python scripts/leaderboard.py` rebuilds `results/RESULTS.md` (all runs sorted by LB). On merge conflict: rerun, never hand-edit.
5. **Uploads are limited**: coordinate with t5 before uploading. Never upload two near-identical files.
6. Keep scores on the NRC [0,1] scale unless the LB shows otherwise.
7. The unlabeled train (870k speeches with features) can be used freely: fitting lexicons, pseudo-labels, normalisation stats.
8. No pretrained models (unless organizers say otherwise in writing), no AutoML, no external data without written OK (see §4). **Never try to reconstruct the hidden test targets** (rules art. 7 bis v), e.g. by probing the leaderboard on purpose.
9. Keep `tracks/<track>/README.md` up to date: numbers, plots, what worked, limits. It goes almost as is into the final report.

### How your Claude agent should work on a track
- Start with the simplest working version, log it, then iterate.
- Always compare with the current best run in `results/RESULTS.md` and with `agreement()`.
- Add simple plots (distributions, per-source/year curves, scatter V vs A), not only prints.
- Keep code short.

### Timeline
| When | What |
|---|---|
| Fri night | Setup, data. t1 baselines uploaded (gives the metric's behaviour). t5 finds metric + upload limit. |
| Sat 12:00 | Every track has at least one submission file logged. |
| Sat 22:00 | Tracks frozen. |
| Sun morning | Blend of the best methods on `main`, final submission. |
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

## 2. The task (UNSUPERVISED)

For each test speech, estimate two continuous scores, **without any training label**:

- `valence_chunks_weighted_mean` (negative ↔ positive)
- `arousal_chunks_weighted_mean` (calm ↔ excited)

The names say how the hidden truth was built: emotion scores computed on **chunks** of each speech, then a **weighted mean** (most likely by chunk length). Our job: reproduce the best possible estimate with unsupervised state-of-the-art methods. The organizers' `nrc_*` features (NRC VAD lexicon on the English text, scale [0,1]) are the natural starting point: test means are `nrc_V_mean` ≈ 0.564, `nrc_A_mean` ≈ 0.459.

Corpus: `assemblee`, `senat` (FR), `uk_commons` (UK), `us_congress` (US), 1988 → 2026. Plus `x_Italia.csv`: unlabeled Italian speeches (text, date, 214 features; no id, no source).

### HFactory (checked Sat 28 Nov, 12:40)
- Platform: https://app.hfactory.io/activities/832/topics/851/dcf9138f-9345-4395-8115-0ae1490f3a2c/submissions (log in with your HFactory account). Our official group there is **Group 34**.
- **Two separate competitions: Valence and Arousal**, each with its own submissions page and leaderboard. **10 submissions per competition in total**, until **Sun 29 Nov, 16:00**. Upload the full CSV (`id` + both columns, 372,812 rows, `y_test_zero` format) to each.
- Metric: not written ("No guideline information"). **Higher is better** (top scores 0.83 valence, 0.72 arousal on Sat 12:40). Interim leaderboard on a subset; the final ranking uses another subset.
- **A big group of teams sits at 0.27 (valence) and 0.13 (arousal): almost surely the raw lexicon (`nrc_*_mean`)**. Our Group 34 already has 0.13 on arousal (uploaded 10:18). So `t1_lexicon__raw_mean` is known: no need to upload it.
- `y_test_sample.csv` on the Guidelines page = the same all-zero template as `y_test_zero.csv`. **No labels anywhere.**
- Compute instance: a hosted data science environment, CPU free, 30 credits for GPU.

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
| `x_train_final.csv` | 1.85 GB | 870k UNLABELED speeches (text + features). No targets: the challenge is unsupervised. |
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
- **No target columns anywhere, by design: the challenge is unsupervised** (confirmed Fri 23:15). The train file is 870k unlabeled speeches we can use to fit lexicons, pseudo-labels and statistics.
- 218 columns: `id`, `clean_text`, `date`, `source` + **214 features**. Families A, B, D, F, G, H only. **No `tfidf_svd_*`, no `char_tfidf_svd_*`, no `text_en`.**
- `source` = 25 % each: `assemblee` (2007–2024), `senat` (1996–2026), `uk_commons` (1988–2019), `us_congress` (1994–2024).
- **Test = random split**: same sources, same years, same length distribution as train.
- Speeches are short: median ≈ 35 words; 0.5 % of test speeches have no NRC word at all (`nrc_*_mean` falls back to 0.5).
- **Drive download quota**: on Friday night gdown fails with "Too many users have viewed or downloaded this file". Workaround: open the file in the browser and use "Download", or make a copy in your own Drive and download the copy.

### Columns (from `sample_x_test.csv`, 218 columns)

Metadata: `id`, `clean_text` (raw speech, original language), `date` (YYYY-MM-DD), `source`.

Precomputed features: 342 defined in the dictionary, **214 actually present** (families E and I missing):

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

## 6. Plan (unsupervised)

### Phase 0 — Fri night
- [x] Data downloaded and converted. Test = random split. No labels (by design).
- [x] t1: 3 lexicon baselines ready (`raw_mean`, `median`, `shrink_k5`), in `Desktop/HACKATHON/submissions/` on Aurèle's Mac.
- [ ] Find the metric + upload limit on HFactory (t5). Upload `t1_lexicon__raw_mean` first.

### Phase 1 — Sat morning: one family of methods per person (see §0bis)
- t2 chunks + induced lexicons, t3 combination, t4 weak supervision, t5 validation, t6 time series.

### Phase 2 — Sat afternoon/evening
- Agreement table between all methods. Upload the most promising ones (t5 plans the uploads).
- Blend: average of the best 2–3 methods (weights from LB).

### Phase 3 — product + report (Sat evening → Sun)
- Mockup: emotion barometer of parliaments (FR / UK / US / IT) by theme (`dictionnaire_thematiques_parlement.xlsx`) and over time (t6). Any AI inside the mockup runs locally (our own scoring). No ranking of named MPs.
- Report: methods, why these unsupervised choices, agreement analysis, limits and biases (English lexicon on translated FR text, short speeches, arousal from text only, era drift).
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
│   ├── t1_lexicon/ t2_chunks/ t3_combine/ t4_weak/ t5_validation/ t6_papers/
│   └── _supervised_archive/   # old supervised code, reusable with pseudo-labels
├── results/
│   ├── runs/            # <track>.csv, one line per submission (log_submission), LB filled by hand
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
- Each method: log it with `log_submission()` (see §0bis), never by hand.
- Always write predictions with the exact columns and ids of `y_test_zero.csv`; assert row count and id order before saving.
- Do not suggest anything that breaks §4 (pretrained models, AutoML, paid APIs, scraping).
- Git: follow §0. SSH remote `git@github.com:Aureleee/HI_PARIS.git`.

---

## 9. Open questions (to ask organizers / check on HFactory)

1. Evaluation metric (RMSE? correlation?), averaged over the 2 targets? Upload limit per day?
2. How were the hidden scores computed (which lexicon/model, chunk size, weights)? Even a hint helps.
3. Can we use the **NRC VAD lexicon file** itself (word level)? The organizers used it for the `nrc_*` features.
4. In this unsupervised setting, are **pretrained models** still forbidden (rules art. 7)? Get a written answer before using any.
5. Role of `x_Italia.csv` (is it scored? only for the product?).
6. Compute provided by organizers and how to access it.
