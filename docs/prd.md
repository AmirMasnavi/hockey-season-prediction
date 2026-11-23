# Hockey prediction project

## Objective
Use the supplied historical hockey database to predict, for a designated new season, (a) final regular-season team ranking and (b) the set of teams that change coaches and (c) how many penalty minutes (PIM) each player will accumulate during the regular season.

All predictions are made the day before the first game of that season. The dataset's year denotes the starting year (2005 means 2005–06).

## Business understanding
**Stakeholders:** team management and front offices, league analysts, sports media and betting/fantasy markets.

**Business goals**
1. Anticipate each team's competitive standing before the season, to set expectations, budgets and marketing.
2. Anticipate which teams will replace their coach during the season, so staff, agents and media can plan.
3. Anticipate how many penalty minutes each player will accumulate in the regular season (coaching staff, fantasy markets).

**Success criteria**
1. Predicted standings are clearly closer to the real final standings than repeating last season's order.
2. Coach changes are flagged with useful precision and recall, better than predicting "no change" or picking teams at random.
3. Player PIM predictions have a mean absolute error at least 5% below "same PIM as last season" (scaled to the schedule), in the mean and in more than half of the validation seasons.

**Constraint:** only information available the day before the season's first game may be used.

## Data mining goals
| Business goal | Data mining goal | Primary measure |
|---|---|---|
| 1. Standing | Regression of each team's points per game, then sort within the season into a ranking | Spearman correlation and mean absolute rank error per season, vs last-season-order baseline |
| 2. Coach change | Binary classification: will the team have more than one coach stint this season | PR-AUC, precision, recall and F1, vs majority/prevalence baselines |
| 3. Player PIM | Count regression per player-season: total regular-season PIM | MAE (primary), RMSE, Spearman, vs persistence (last season's PIM) |

## Adopted decisions (2026-11-02)
No instructor is available to clarify the assignment; these team decisions replace the former open questions.
- **League:** NHL only. It is the only league that continues to 2009.
- **Test season:** 2009 is the final test. Earlier seasons are used for chronological (expanding-window) validation. 2009 was inspected descriptively during EDA, but no model will be fitted or tuned on it. Code should accept a new season file if one is supplied later.
- **Ranking:** predict points per game and sort teams within the season. League-wide rank is the primary output; division rank (matching stored Teams.rank in 2009) is secondary. Ties use minimum rank; official tie-breakers are not implemented.
- **Coach change:** more than one distinct coach stint in the target season (in-season replacement). An offseason hire is already known the day before the season, so it is not a prediction target. Co-coaches sharing a stint do not count as a change.
- **Joins:** prior-season features join on (league, franchise) with exact year t−1; teams without that season keep missing lags rather than borrowing older seasons.
- **Task (c) (adopted 2026-11-21):** one row per player and NHL season, stints on several teams summed; every player with at least one regular-season game in season t, goalies included; target = total regular-season PIM. Features: previous NHL season of the player, career before t, biography, opening team (first stint in t) and its prior-season PIM level. Games played in t is never a feature. The player list of season t stands in for opening-day rosters. Same splits/folds as the team tasks. Table: data/processed/player_pim_table.csv.
- **Tools:** Python, plus SQLite or DuckDB for data preparation queries.

## Current scope
Business understanding, data understanding and data preparation are complete in one notebook, notebooks/1_eda.ipynb (tasks a, b and c). Target seasons from 1967. Validation: rolling origin, one season ahead, 13 folds 1995–2008, each trained on all earlier seasons (expanding window); choices are made on folds 1995–2001, folds 2002–2008 only compare and test; split column: train_pool ≤ 1994, validation 1995–2008, test 2009. Notebook 2_regression (tasks a and c) is complete: task (a) final model Lasso on the ppg z-score (evaluation Spearman 0.545 vs persistence 0.518, not significant; G1 partly met); task (c) final model gradient boosting with Poisson loss (evaluation MAE 17.39 vs 19.43, 10.5% better in all six seasons; G4 met). Notebook 3_classification (task b) is complete: final model gradient boosting (evaluation pooled PR-AUC 0.331 vs 0.310 for the one-feature baseline and 0.20 for chance; gain not significant; G2 met narrowly: 41.7% of changes in the riskiest quarter). Next: 4_feature_selection. Next: modeling with expanding-window validation, baselines, several algorithms, fold-internal imputation/resampling/feature selection, tuning, significance tests and feature importance.

## Deliverables / acceptance
- docs/prd.md, docs/agent.md, docs/memory.md, docs/data.md and a root AGENTS.md entry point.
- Executed notebooks/1_eda.ipynb: business understanding, data understanding (statistical tests, regression to the mean, logistic regression, PCA, k-means, mutual information, player PIM analysis) and data preparation (integration, six quality dimensions, feature engineering, transformation, outliers, imputation experiment, redundancy removal, sampling, imbalance comparison with SMOTE inside folds).
- data/processed/modeling_table.csv (938 team-seasons, 27 features: 24 plus 3 missing indicators; targets, split and fold columns).
- data/processed/player_pim_table.csv (29,689 player-seasons, 15 features, target_pim; same split and folds).
- Executed notebooks/2_regression.ipynb: tasks (a) and (c) with baselines, several algorithms, grid search on folds 1995–2001, comparison and significance tests on 2002–2008, overfitting analysis, model improvement (task a), feature importance, white-box models and one final test on 2009; predictions in data/processed/predictions_2009_ranking.csv and predictions_2009_pim.csv.
- Executed notebooks/3_classification.ipynb: task (b) with baselines, seven algorithms, imbalance strategies inside the folds (and a SMOTE leakage demonstration), grid search, threshold selection, evaluation with significance tests, overfitting analysis, model improvement, feature importance, a white-box tree and the 2009 test; predictions in data/processed/predictions_2009_coach.csv.
- Reproducible environment requirements; reports/eda/source_sha256.json for raw-data verification.
- Raw data unchanged; no notebook execution errors; every code cell has markdown before and after; findings grounded in output.

## Evaluation plan for later
Ranking: MAE for points per game, within-season Spearman correlation and mean absolute rank error, league-wide (primary) and by division (secondary). Coach changes: precision, recall, F1, PR-AUC and calibrated probabilities, compared with prevalence/majority baselines. Threshold choice must use validation data only. Player PIM: MAE (primary), RMSE and Spearman per season, vs persistence (MAE 20.81 on validation) and position mean.

## Course reference
The user supplied a Titanic supervised-learning Colab lab. Apply its data inspection, class imbalance, cutoff-based feature selection and training-only preprocessing principles. For hockey, adapt validation to future seasons with chronological splits. 2009 was inspected descriptively during EDA; it remains the final test because no model is fitted or tuned on it.

## Open questions
New entrants are kept with missing lags and a has_prev indicator; no new franchise appears in validation or test.
