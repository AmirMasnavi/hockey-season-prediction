# Hockey prediction project

Start with [the executed introductory notebook](notebooks/01_data_understanding.ipynb). It inspects the supplied tables, explores ranking and coach-change targets, documents cleaning decisions, and builds an exact prior-year feature example. It contains saved tables and plots; no models have been trained yet.

## Project map

- `docs/prd.md`: objective, scope, acceptance criteria and open questions.
- `docs/agent.md`: project rules; root `AGENTS.md` routes agents here.
- `docs/memory.md`: current status, decisions and next steps.
- `docs/data.md`: table inventory, relationships, field meanings, quality findings and cutoff rules.
- `hockey_development_data/`: original 22 CSVs; preserve unchanged.
- `notebooks/01_data_understanding.ipynb`: intent → code → findings for every analysis step.
- `notebooks/02_data_preparation.ipynb`: data quality, integration (DuckDB SQL), feature engineering, outliers, imputation, redundancy and training-era choice.
- `data/processed/modeling_table.csv`: modeling table with train/validation/test split.
- `reports/eda/`: reproducible profiles, join checks, provisional coach labels and learning preview.

## Run locally

Notebook 01 was verified with Python 3.14 (macOS); both notebooks were verified with Python 3.11 (Linux). Create a virtual environment, install `requirements.txt`, and select its Python interpreter as the notebook kernel in your notebook editor. The current workspace already has `.venv` prepared.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Run all cells from the project root or `notebooks/`. Outputs are saved in `reports/eda/`. To execute and verify the notebook using the current Python environment:

```bash
.venv/bin/python scripts/run_eda.py                                       # notebook 01
.venv/bin/python scripts/run_eda.py notebooks/02_data_preparation.ipynb   # notebook 02
.venv/bin/python scripts/run_eda.py notebooks/02_data_preparation.ipynb --check
```

The first command executes every cell and checks structure, errors and source checksums. The second checks saved notebook outputs without rerunning them. Local notebook execution requires permission to open localhost kernel ports. `requirements.txt` lists top-level packages with minimum versions.

## Run on Colab

Open the `.ipynb` in Colab and place `hockey_development_data/` directly in `/content/` (or change ROOT to the folder containing it). The notebook then runs with Colab's available pandas/numpy/matplotlib; local paths or a local `.venv` are not required there. Colab execution has not been verified in this project.

## Current decisions

The team adopted these decisions (details in `docs/prd.md`): NHL only; 2009 is the final test season, with earlier seasons used for chronological validation; ranking is predicted points per game sorted league-wide (division rank secondary); a coach change means more than one coach during the season. All predictions must use information available the day before the target season begins.


## Independent review

A second agent reviewed the EDA before publication. The review and accepted improvements are recorded in `docs/review.md`. The notebook finishes with a consolidated conclusion covering findings, target ambiguities, feature availability and ordered next steps. Modern-era-only modeling has only 120 matched rows over four seasons, so the next modeling decision must weigh historical comparability against sample size.

Private project repository: [AmirMasnavi/hockey-season-prediction](https://github.com/AmirMasnavi/hockey-season-prediction).
