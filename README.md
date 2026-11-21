# Hockey prediction project

Start with [notebook 1](notebooks/1_eda.ipynb): business understanding, data understanding and data preparation for all three tasks: (a) team ranking, (b) in-season coach changes, (c) penalty minutes per player. It exports the two modeling tables. Modeling notebooks (2_regression, 3_classification, 4_feature_selection) come next.

## Project map

- `docs/prd.md`: objective, scope, acceptance criteria and open questions.
- `docs/agent.md`: project rules; root `AGENTS.md` routes agents here.
- `docs/memory.md`: current status, decisions and next steps.
- `docs/data.md`: table inventory, relationships, field meanings, quality findings and cutoff rules.
- `hockey_development_data/`: original 22 CSVs; preserve unchanged.
- `notebooks/1_eda.ipynb`: intent → code → findings for every analysis step; DuckDB SQL for integration and quality checks.
- `data/processed/modeling_table.csv`: modeling table with train/validation/test split.
- `data/processed/player_pim_table.csv`: player-season table for task (c), penalty minutes per player.
- `reports/eda/source_sha256.json`: checksums used to confirm the raw CSVs are unchanged.

## Run locally

Verified with Python 3.12 on Windows. Install `requirements.txt` (in a virtual environment if you like) and select that Python as the notebook kernel.

```bash
python -m pip install -r requirements.txt
```

Run all cells from the project root or `notebooks/`. To execute and verify the notebook with the current Python:

```bash
python scripts/run_eda.py            # executes notebooks/1_eda.ipynb and checks it
python scripts/run_eda.py --check    # checks the saved outputs without rerunning
```

The checker verifies that every code cell ran without errors and sits between markdown cells, that the notebook ends with the conclusion, and that the raw CSVs match their checksums (line endings are normalised, so Windows checkouts pass). Local notebook execution requires permission to open localhost kernel ports. `requirements.txt` lists top-level packages with minimum versions.

## Run on Colab

Open the `.ipynb` in Colab and place `hockey_development_data/` directly in `/content/` (or change ROOT to the folder containing it). Install the two packages Colab lacks first (`!pip install duckdb imbalanced-learn`). Colab execution has not been verified in this project.

## Current decisions

The team adopted these decisions (details in `docs/prd.md`): NHL only; 2009 is the final test season, with earlier seasons used for chronological validation; ranking is predicted points per game sorted league-wide (division rank secondary); a coach change means more than one coach during the season; task (c) predicts each player's total regular-season PIM (one row per player-season, all teams summed). All predictions must use information available the day before the target season begins.


## Independent review

A second agent reviewed the earlier EDA notebooks (since replaced by `1_eda.ipynb`); the review and accepted improvements are in `docs/review.md`. The current notebook was audited on 2026-11-21: every findings cell was checked against its executed output.

Private project repository: [AmirMasnavi/hockey-season-prediction](https://github.com/AmirMasnavi/hockey-season-prediction).
