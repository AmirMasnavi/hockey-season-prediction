# Hockey prediction project

Start with [notebook 1](notebooks/1_eda.ipynb): business understanding, data understanding and data preparation for all three tasks: (a) team ranking, (b) in-season coach changes, (c) penalty minutes per player. It exports the two modeling tables. [Notebook 2](notebooks/2_regression.ipynb) models the two regression tasks: Part A ranks the teams (task a), Part B predicts each player's penalty minutes (task c). [Notebook 3](notebooks/3_classification.ipynb) models task (b), the in-season coach changes. Notebook 4_feature_selection comes next.

## Project map

- `docs/prd.md`: objective, scope, acceptance criteria and open questions.
- `docs/agent.md`: project rules; root `AGENTS.md` routes agents here.
- `docs/memory.md`: current status, decisions and next steps.
- `docs/data.md`: table inventory, relationships, field meanings, quality findings and cutoff rules.
- `hockey_development_data/`: original 22 CSVs; preserve unchanged.
- `notebooks/1_eda.ipynb`: intent → code → findings for every analysis step; DuckDB SQL for integration and quality checks.
- `notebooks/2_regression.ipynb`: baselines, algorithm comparison, tuning, significance tests, feature importance, white-box models and the 2009 test for tasks (a) and (c).
- `notebooks/3_classification.ipynb`: the same for task (b), plus imbalance handling inside the folds (with a SMOTE leakage demonstration), threshold selection and calibration.
- `data/processed/modeling_table.csv`: modeling table with train/validation/test split.
- `data/processed/player_pim_table.csv`: player-season table for task (c), penalty minutes per player.
- `data/processed/predictions_2009_ranking.csv`, `data/processed/predictions_2009_pim.csv`, `data/processed/predictions_2009_coach.csv`: final 2009 predictions of notebooks 2 and 3.
- `reports/eda/source_sha256.json`: checksums used to confirm the raw CSVs are unchanged.

## Run locally

Verified with Python 3.12 on Windows. Install `requirements.txt` (in a virtual environment if you like) and select that Python as the notebook kernel.

```bash
python -m pip install -r requirements.txt
```

Run all cells from the project root or `notebooks/`. To execute and verify the notebook with the current Python:

```bash
python scripts/run_eda.py                                   # executes notebooks/1_eda.ipynb and checks it
python scripts/run_eda.py notebooks/2_regression.ipynb      # same for notebook 2
python scripts/run_eda.py notebooks/3_classification.ipynb  # same for notebook 3
python scripts/run_eda.py notebooks/2_regression.ipynb --check   # checks the saved outputs without rerunning
```

Notebook 1 runs in under a minute. Notebook 2 computes for about 6 minutes on a fast 8-core desktop (grid searches run in parallel on all cores); expect two to three times longer on a laptop. Notebook 3 computes for about 2-3 minutes. Run notebook 1 first, since notebooks 2 and 3 read its exported tables.

The checker verifies that every code cell ran without errors and sits between markdown cells, that the notebook ends with the conclusion, and that the raw CSVs match their checksums (line endings are normalised, so Windows checkouts pass). Local notebook execution requires permission to open localhost kernel ports. `requirements.txt` lists top-level packages with minimum versions.

## Run on Colab

Open the `.ipynb` in Colab and place `hockey_development_data/` directly in `/content/` (or change ROOT to the folder containing it). Install the two packages Colab lacks first (`!pip install duckdb imbalanced-learn`). Colab execution has not been verified in this project.

## Current decisions

The team adopted these decisions (details in `docs/prd.md`): NHL only; 2009 is the final test season, with earlier seasons used for chronological validation; ranking is predicted points per game sorted league-wide (division rank secondary); a coach change means more than one coach during the season; task (c) predicts each player's total regular-season PIM (one row per player-season, all teams summed). All predictions must use information available the day before the target season begins.


## Independent review

A second agent reviewed the earlier EDA notebooks (since replaced by `1_eda.ipynb`); the review and accepted improvements are in `docs/review.md`. The current notebook was audited on 2026-11-21: every findings cell was checked against its executed output.

Private project repository: [AmirMasnavi/hockey-season-prediction](https://github.com/AmirMasnavi/hockey-season-prediction).
