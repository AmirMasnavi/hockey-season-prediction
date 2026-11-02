# Hockey prediction project

## Objective
Use the supplied historical hockey database to predict, for a designated new season, (a) final regular-season team ranking and (b) the set of teams that change coaches. Task (c) is TBA.

All predictions are made the day before the first game of that season. The dataset's year denotes the starting year (2005 means 2005–06).

## Business understanding
**Stakeholders:** team management and front offices, league analysts, sports media and betting/fantasy markets.

**Business goals**
1. Anticipate each team's competitive standing before the season, to set expectations, budgets and marketing.
2. Anticipate which teams will replace their coach during the season, so staff, agents and media can plan.

**Success criteria**
1. Predicted standings are clearly closer to the real final standings than repeating last season's order.
2. Coach changes are flagged with useful precision and recall, better than predicting "no change" or picking teams at random.

**Constraint:** only information available the day before the season's first game may be used.

## Data mining goals
| Business goal | Data mining goal | Primary measure |
|---|---|---|
| 1. Standing | Regression of each team's points per game, then sort within the season into a ranking | Spearman correlation and mean absolute rank error per season, vs last-season-order baseline |
| 2. Coach change | Binary classification: will the team have more than one coach stint this season | PR-AUC, precision, recall and F1, vs majority/prevalence baselines |

## Adopted decisions (2026-11-02)
No instructor is available to clarify the assignment; these team decisions replace the former open questions.
- **League:** NHL only. It is the only league that continues to 2009.
- **Test season:** 2009 is the final test. Earlier seasons are used for chronological (expanding-window) validation. 2009 was inspected descriptively during EDA, but no model will be fitted or tuned on it. Code should accept a new season file if one is supplied later.
- **Ranking:** predict points per game and sort teams within the season. League-wide rank is the primary output; division rank (matching stored Teams.rank in 2009) is secondary. Ties use minimum rank; official tie-breakers are not implemented.
- **Coach change:** more than one distinct coach stint in the target season (in-season replacement). An offseason hire is already known the day before the season, so it is not a prediction target. Co-coaches sharing a stint do not count as a change.
- **Joins:** prior-season features join on (league, franchise) with exact year t−1; teams without that season keep missing lags rather than borrowing older seasons.
- **Task (c):** ignored until announced.
- **Tools:** Python, plus SQLite or DuckDB for data preparation queries.

## Current scope
Phase 1 (EDA, notebooks/01_data_understanding.ipynb) is complete. Next: data preparation (quality, outliers, feature engineering, era selection), then modeling with chronological validation, baselines, several algorithms, tuning, significance tests and feature importance.

## Deliverables / acceptance
- docs/prd.md, docs/agent.md, docs/memory.md, docs/data.md and a root AGENTS.md entry point.
- Executed notebooks/01_data_understanding.ipynb with real data previews, coverage, quality audit, target exploration, plots, and a leakage-safe lag example.
- Reproducible environment requirements and small EDA audit exports under reports/eda/.
- Raw data unchanged; no notebook execution errors; every code cell has markdown before and after; findings grounded in output.

## Evaluation plan for later
Ranking: MAE for points per game, within-season Spearman correlation and mean absolute rank error, league-wide (primary) and by division (secondary). Coach changes: precision, recall, F1, PR-AUC and calibrated probabilities, compared with prevalence/majority baselines. Threshold choice must use validation data only.

## Course reference
The user supplied a Titanic supervised-learning Colab lab. Apply its data inspection, class imbalance, cutoff-based feature selection and training-only preprocessing principles. For hockey, adapt validation to future seasons with chronological splits. 2009 was inspected descriptively during EDA; it remains the final test because no model is fitted or tuned on it.

## Open questions
Task (c). Fallback policy for new teams and seasons without a prior year.
