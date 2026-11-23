# Defence sheet: notebook 2 (regression: tasks a and c)

## The story in five lines
1. **Task (a):** nine algorithms predict each team's points per game; sorting gives the ranking. The final model (Lasso on the within-season z-score) beats "same order as last season" by +0.027 Spearman (0.545 vs 0.518), in 4 of 6 seasons, **not significantly**. Its level (MAE) is clearly better.
2. Last season's goal difference is the backbone; PDO (shooting % + save %) corrects for luck.
3. **Task (c):** five algorithms predict each player's total penalty minutes. Gradient boosting with Poisson loss is 10.5% better than persistence (MAE 17.39 vs 19.43) and better in all six seasons; in 2009, 10.3% better with a bootstrap interval that excludes zero.
4. Penalty minutes come from the player's habit (career rate) and playing time; the team hardly matters.
5. All choices on 1995-2001, comparison on 2002-2008, one test on 2009.

## Section by section

| Section | What the cell does |
|---|---|
| 1 | Loads `modeling_table.csv`, defines the seasons and the four metrics (Spearman, pair accuracy, rank error, MAE), all inside a season. |
| 2 | Three baselines: persistence, regression to the mean (slope fitted on training seasons), league average. |
| 3 | Defines the nine algorithms with their grids and `build()`, which makes a fresh pipeline. |
| 4 | Grid search on the tuning seasons (parallel), defaults vs tuned, training vs validation score, tuning time. 4.1: validation curves. |
| 5 | Every tuned model on 2002-2008; 5.1 season by season; 5.2 Friedman, Wilcoxon with Holm and rank-biserial; 5.3 bootstrap interval of the gain. |
| 6 | Training vs evaluation gap; 6.1 learning curve over years of history. |
| 7 | Improvement steps (defaults, tuned, z target, ensembles) with a rule fixed before running; 7.1 the chosen model vs persistence. |
| 8 | Permutation importance (single features and groups) and Ridge coefficients; 8.1 the figure. |
| 9 | Depth-3 tree and its rules; 9.1 Ridge coefficients on 1967-2008. |
| 10 | Final test on 2009, team list, bootstrap, CSV; 10.1 predicted vs actual rank. |
| 11-12 | Task (c): player table, metrics, three baselines (position mean, persistence scaled to the schedule, career rate x last GP). |
| 13 | Task (c): five algorithms (Poisson GLM, Ridge on log(1+PIM), k-NN, random forest, boosting with Poisson loss), grid search, rule = lowest tuning MAE. 13.1: boosting iterations. |
| 14 | Task (c) comparison with Wilcoxon and Holm; 14.1 by position and history. |
| 15 | Task (c) permutation importance; 15.1 depth-3 tree and Poisson factors. |
| 16 | Task (c) final test on 2009, by group, bootstrap, top-10, CSV. |
| 17 | Conclusion for both tasks and the rubric table. |

## Code you must be able to explain
- **`fit_predict` (4):** trains on all seasons before `season`, predicts that season, and computes the Spearman on the training seasons too (for the overfitting gap). With the z target, it converts back to ppg with the mean and standard deviation of the last training season.
- **`build(name, params)` (3):** `clone(model)` makes a fresh copy of the model, `set_params(**params)` sets the grid values, and the copy goes into the pipeline imputer -> scaler -> model.
- **`tune` (4) with `Parallel`:** the grid points do not depend on each other, so `joblib` evaluates them on all CPU cores at the same time; results are identical to a plain loop.
- **`rank_biserial` (5.2):** the effect size of the Wilcoxon test: (sum of the ranks of the positive differences - sum of the negative ones) / sum of all ranks. +1 = wins every season, 0 = no effect.
- **`bootstrap_diff` (5.3):** resamples the teams of each season with replacement 1,000 times and recomputes the Spearman of both predictions; the 2.5% and 97.5% percentiles of the mean difference are the interval.
- **`permutation_drops` (8):** shuffles one feature (or a group) among the teams of a season and measures how much the Spearman drops; shuffling a group together avoids correlated features hiding each other.
- **Rule of section 7:** among the steps within 0.005 of the best tuning Spearman, take the lowest tuning MAE.
- **`predict_pim` fallback (13):** players without a previous season get the training mean of such players, by position; last season's totals are scaled by schedule length.
- **`TransformedTargetRegressor` and `regressor__alpha` (13):** fits Ridge on log(1 + PIM) and transforms the predictions back with exp - 1; `regressor__alpha` is how scikit-learn names the alpha of the inner Ridge.

## Likely questions and answers
- **Why predict points per game and not the rank directly?** A rank is relative; predicting ppg and sorting inside the season gives the ranking and a level (for budgets). Spearman then measures the order.
- **Why your own grid search loop instead of GridSearchCV?** GridSearchCV's cross-validation would shuffle seasons and score across teams of different seasons; we need rolling-origin folds and a within-season score.
- **Why split the validation seasons into tuning and evaluation?** So the comparison and the tests are done on seasons that played no part in any choice; otherwise the scores would be optimistic.
- **Why is the default Lasso NaN?** Its default alpha = 1 sets every coefficient to zero, so it predicts a constant and the Spearman is undefined.
- **Why is k-NN's training score 0.99?** With distance weights every training team is its own nearest neighbour, so it is predicted perfectly: pure memorisation.
- **The random forest has the biggest gap but the best evaluation score. How?** Averaging many deep trees cancels much of their variance; a gap only shows memorisation, the evaluation score shows generalisation.
- **Why the z-score target in step 3?** The league level of ppg moves with the era; the z-score removes it and the conversion back uses the latest level, so MAE falls from 0.127 to 0.120 (tuning) with the same Spearman.
- **Why not use the ensemble, which was best on evaluation (0.555)?** It was worse on the tuning seasons (0.592 vs 0.615); choosing it would reuse the evaluation seasons for a choice.
- **Why is nothing significant in task (a)?** Six seasons; Friedman p = 0.29, Wilcoxon p = 0.56 for the final model. A significant Wilcoxon needs a model that wins all six seasons.
- **What is PDO and why is its coefficient negative?** Shooting % + save %: a luck indicator. Teams with high PDO last year tend to fall back, regression to the mean.
- **Task (c): why MAE and not RMSE?** PIM has a long tail; MAE is robust to the few 300+ minute seasons and easy to read in minutes. RMSE is reported to show the tail.
- **Why Poisson loss?** PIM is a count, cannot be negative and its variance grows with the mean; a Poisson loss fits that better than least squares.
- **Why is the training MAE higher than the validation MAE in task (c)?** The training seasons include the 1980s with almost twice as many penalties, so absolute errors are larger there; it is not "negative overfitting". The validation curve is the better check.
- **Why does the boosting curve go flat after 400 iterations?** Histogram gradient boosting turns on early stopping above 10,000 rows: it keeps 10% of the training rows aside and stops when they stop improving.
- **Why median imputation in task (c) but iterative in task (a)?** All missing values in the player table belong to players without a previous season, already flagged by indicators; and iterative imputation on 20,000+ rows would make tuning very slow.
- **Why is the model worse for goalies?** Goalie PIM is tiny (mean 3.9) and last season's value is already the best rule; we propose combining the two in notebook 4.
- **Why is the 2009 test more convincing in task (c) than in task (a)?** About 960 players instead of 30 teams, so the bootstrap interval is narrow and excludes zero.

## Key numbers
| What | Task (a) | Task (c) |
|---|---|---|
| Persistence, evaluation | Spearman 0.518 | MAE 19.43 |
| Final model, evaluation | Lasso z target 0.545 | Boosting (Poisson) 17.39 |
| Seasons beating persistence | 4 of 6 | 6 of 6 |
| Test 2009 | 0.540 vs 0.474 | 15.36 vs 17.12 (gain interval 0.96 to 2.50) |
| Significance | Wilcoxon p = 0.56 | Wilcoxon p = 0.031 (Holm 0.156) |
| Most important features | goals against, goals for, PDO | career PIM per game, last season's PIM |
| Business goal | G1 partly met | G4 met |
