# Defence sheet: notebook 1 (business understanding, data understanding, data preparation)

## The story in five lines
1. Three tasks, all predicted the day before the season: team ranking (a), in-season coach changes (b), penalty minutes per player (c). NHL only, 1967-2009, 2009 is the final test.
2. Team strength persists but regresses to the mean (slope 0.62); last season's **luck** only matters once you control for points (partial r = -0.17).
3. Coach changes follow bad results and especially bad defence, but the signal is weak (logistic AUC 0.62 in-sample).
4. Penalty minutes are a stable player trait (PIM per game slope 0.82), but games played are not, and they are unknown in advance.
5. Data preparation: six quality dimensions, within-season z-scores, outliers kept and capped, iterative imputation validated on held-out seasons, redundancy removed (27 features), two exported tables.

## Section by section

| Section | What the cell does |
|---|---|
| 1 | Stakeholders, business goals G1-G4 with numeric success criteria, data mining goals with metric, baseline and threshold. |
| 2.1 | Loads the 22 CSVs into DuckDB and lists rows, columns, years, leagues and missing share per table. |
| 2.2 | Builds a team-season table with SQL and pairs each season with the previous season of the same **franchise** (franchID survives relocations). |
| 2.3 | Describes points per game; Shapiro-Wilk and D'Agostino reject normality (p about 0.006), so we use rank-based tests. |
| 2.4 | Kruskal-Wallis and Brown-Forsythe by decade: goals per game drift strongly (epsilon^2 = 0.42), the within-season z-score removes it. |
| 2.5 | Spearman heatmap of last-season features against next-season points and coach change, with Benjamini-Hochberg correction. |
| 2.6 | OLS of this season's points z on last season's: slope 0.622, R^2 0.40. |
| 2.7 | Mann-Whitney (with rank-biserial effect size), chi-square on thirds of last season's standing, Wilson intervals by quintile. |
| 2.8 | Multivariable logistic regression of coach change with odds ratios, forest plot and VIFs. |
| 2.9 | Does luck matter? OLS with and without luck, F-test, partial correlation, added-variable plot. |
| 2.10 | PCA on eight last-season style variables (from 1983, when shots against exist); PC1 = strength axis. |
| 2.11 | k-means with silhouette for k = 2..8; k = 4 used only for description (styles form a continuum). |
| 2.12 | Mutual information with both targets, compared with Spearman. |
| 2.13 | Task (c): player-season table (stints summed), PIM distribution by position, league penalty level by season. |
| 2.14 | Task (c): pairs consecutive seasons of the same player; persistence of PIM, PIM per game and games played. |
| 2.15 | Table of the knowledge extracted. |
| 3.1 | Format conversions (text to number, birth date to age, wide monthly columns to long), the team profile from seven sources, match rates. |
| 3.2 | 28 SQL checks over six quality dimensions; the Phoenix 2009 coach fix in a derived copy. |
| 3.3 | Final team-season table: lag features, business concepts, opening-day coach facts (tenure, career record). |
| 3.4 | Within-season z-scores (before/after boxplots), log of coach career games, quartile tiers. 3.4.1: coach-change rate by tenure x standing. |
| 3.5 | Outliers with z-score, IQR and Isolation Forest; domain explanations; cap at +/-3. |
| 3.6 | Imputation experiment: mean, median, KNN and iterative imputer, fitted on seasons up to 1999, tested on hidden values of 2000-2008. 3.6.1: what imputation does to variance and correlations. |
| 3.7 | Redundancy: clusters of features with |Spearman| > 0.9, then iterative VIF removal. |
| 3.8 | Why NHL from 1967 (structure and completeness of the eras). |
| 3.9 | Learning curve from 10 rows upward, and training windows (last 5/10/20/30 seasons vs all). |
| 3.10 | Coach-change rate over time; 3.10.1: no handling, class weights, over-sampling and SMOTE compared inside the folds. |
| 3.11 | Export of `modeling_table.csv` with leakage assertions. |
| 3.12-3.13 | Task (c): player table export and rolling-origin baselines. |

## Code you must be able to explain
- **`COACH_SQL` (2.2):** numbers the coaches of each franchise-season twice with `ROW_NUMBER()`: once by lowest stint (the opening-day coach) and once by highest stint (the coach at the end). More than one distinct stint = an in-season change. Co-coaches in the same stint are not a change.
- **Coach career window (3.3):** `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING` sums all earlier seasons of the coach but never the current one, so no season-t information enters.
- **Tenure loop (3.3):** goes season by season because tenure builds on last season's value: new coach -> 0, same coach all last season -> previous tenure + 1, took over during last season -> 1.
- **`to_long` (3.1):** pandas `melt` turns the 32 monthly columns (FebW, FebL, ...) into one row per team, month and result; `'FebW'[:3]` is the month, `[3:]` the result.
- **Quality checks (3.2):** each check is one SQL query returning (flagged rows, tested rows); `count(*) FILTER (WHERE ...)` counts only the rows that break the rule.
- **Imputation experiment (3.6):** we hide 15% of the known values in the held-out seasons, impute them with imputers fitted on the training seasons only, and compare with the truth (RMSE in standard deviations), five different masks.
- **VIF loop (3.7):** repeatedly removes the feature with the highest variance inflation factor until all are below 10.
- **Player career window (3.12):** the same "up to the season before" window as for coaches, per player.

## Likely questions and answers
- **Why z-score inside each season instead of over all data?** Goals per game differ by decade (Kruskal-Wallis H = 384, epsilon^2 = 0.42); after the within-season z-score the decades no longer differ (points z: H = 0.24, p = 0.99). A ranking is a within-season comparison anyway. It uses no information from other seasons, so it cannot leak.
- **Isn't using the 2009 teams' z-scores leakage?** The z-scores of the *features* use the previous season, complete before the cutoff. Only the target z-score uses season t, and it is never an input.
- **Why franchID and not tmID?** Team codes change when a team moves (13 NHL franchises used several codes); by franchise we find the previous season for 913 rows instead of 903.
- **Why are the 1979 WHA teams new entrants?** Their franchID continues from the WHA, but we only build NHL lags, so they have no previous NHL season.
- **What is luck?** Points share minus the Pythagorean expectation GF^2 / (GF^2 + GA^2): points that the goal difference did not justify.
- **Why does luck have no raw correlation but a significant partial one?** Lucky teams also had more points last season (r = 0.26), and points push next season up while luck pushes it down: the two effects cancel (suppression). Controlling for points reveals r = -0.17.
- **Why non-parametric tests?** Normality is rejected (Shapiro p = 0.006) and coach change is binary.
- **Why k = 4 when the silhouette prefers k = 2?** Silhouette is low for every k (at most 0.22), so styles are a continuum. k = 4 is only used to describe types; clusters are not features.
- **How do you know the iterative imputer is better?** On hidden values of later seasons: RMSE 0.715 SD vs 0.986 for the mean imputer, stable over five masks; it also keeps correlations better (error 0.028 vs 0.045).
- **Why keep outliers?** They are real (Edmonton dynasty, Quebec 1989); a ranking must get the extreme teams right. We only cap continuous z-scores at +/-3 (27 cells).
- **Why drop points per game, the best predictor?** It is almost exactly explained by goals for, goals against and luck (VIF 49.2). It is still exported as the persistence baseline column.
- **Why 1967?** Earlier eras have 6-7 teams and 0-16% special-teams data; from 1967 all needed fields are complete and the league structure resembles 2009.
- **Is old history outdated?** No: the expanding window (Spearman 0.581) beats the last 5 seasons (0.516, p < 0.001) and the last 30 (0.564, p = 0.010).
- **Why not SMOTE by default?** In 3.10.1 no treatment had the best pooled PR-AUC (0.272) and resampling doubled the predicted probabilities (about 0.40 vs a real rate of 0.20).
- **Task (c): why sum a traded player's stints?** The question asks for the player's PIM in the regular season, regardless of team.
- **Why not use games played as a feature for task (c)?** It is only known after the season. It explains much of total PIM (rho 0.70), which is why errors remain.
- **Why is persistence scaled in 3.13?** 1994 had 48 games, so last season's PIM underestimates 1995; scaling by schedule length (82/48) makes the baseline fair.
- **The 3.13 baseline (20.81) differs from notebook 2 (19.43). Why?** Notebook 1 averages all 13 validation seasons (1995-2008); notebook 2 reports only the evaluation seasons 2002-2008, which have fewer penalties.

## Key numbers
| What | Number |
|---|---|
| NHL team-seasons 1967-2009 / exported rows | 938 |
| Coach-change rate 1967-2008 | 21.0% (191 of 908) |
| Regression to the mean slope | 0.622 (R^2 0.40) |
| Partial correlation of luck | -0.172 |
| Logistic odds ratio of last season's points | 0.495 per SD; in-sample AUC 0.618 |
| PCA PC1 | 40% of variance, Spearman -0.56 with next points |
| Imputation RMSE (iterative vs mean) | 0.715 vs 0.986 |
| Features exported | 27 (24 + 3 indicators) |
| Expanding window vs persistence (Spearman) | 0.581 vs 0.561 |
| PIM per game persistence slope | 0.815 |
| Player-seasons in the PIM table | 29,689 |
