# Defence sheet: notebook 4 (feature selection & task c improvement)

## The story in five lines
1. Every feature selector (filter, wrapper and combined filter -> wrapper) runs **inside** the rolling-origin pipeline, fitted only on `year < season` to avoid leakage.
2. Selecting features on all seasons before splitting inflates Task (b) logistic PR-AUC on `EVAL` from `0.293` to `0.297`, proving why selection must stay inside the folds.
3. For **Task (a)**, `Combined MI(18)->RFE(10)` with Lasso beats `All 27` on tuning (`0.6200` vs `0.6152` Spearman) and matches closely on evaluation (`0.5404` vs `0.5455`, Wilcoxon `p = 0.562`), while `Combined f_reg(18)->RFE(10)` also boosts Random Forest (`0.5653 -> 0.5747` on tuning).
4. For **Task (b)**, keeping all `27` features with Gradient Boosting (`0.2992` tuning, `0.3315` evaluation PR-AUC) beats every reduced subset (`0.1764-0.2212` tuning), because coach-change signals are weak and distributed.
5. For **Task (c)**, keeping all `15` features is best, and **model improvement** (`HGB 500, lr=0.05 + Goalie rule`) lowers MAE across all splits: `20.739 -> 20.654` (`TUNE`), `17.389 -> 17.350` (`EVAL`), and `15.330 -> 15.219` (`2009`, with Goalie MAE dropping `2.773 -> 2.271`).

## Section by section

| Section | What the cell does |
|---|---|
| 1 | Loads both processed tables (`938` team-seasons, `29,689` player-seasons), sets `TUNE`/`EVAL`/`TEST` splits, and demonstrates leakage when `f_classif` runs before splitting. |
| 2 | Task (a): compares `SelectKBest` (`f_regression`, `mutual_info_regression`), `RFE`, `SequentialFeatureSelector` (forward), and combined `SelectKBest -> RFE` inside folds on `TUNE` (`1995-2001`). |
| 2.1 | Stability heatmap of `Combined f_reg(18)->RFE(10)` across all 13 folds, plus `EVAL` (`2002-2008`) Wilcoxon test and `2009` check. |
| 3 | Task (b): compares `f_classif`, `mutual_info_classif`, `RFE`, and combined `SelectKBest -> RFE` with Gradient Boosting and Logistic Regression on `TUNE`. |
| 3.1 | Stability heatmap of `Combined f_clf(15)->RFE(8)` across folds, plus `EVAL` and `2009` comparison against `All 27 (GB)`. |
| 4 | Task (c): tests filter, wrapper, combined selection, `HGB 500 (lr=0.05)`, and the **goalie persistence rule** on `TUNE`. |
| 4.1 | Evaluates the Task (c) improvement on `EVAL` and `2009` with MAE broken down by position (`Forward`, `Defence`, `Goalie`) and bar chart. |
| 5 | Conclusion table across all three tasks and rubric coverage summary. |

## Code you must be able to explain
- **`Pipeline` with selector inside (1, 2, 3, 4):** `Imputer -> Scaler -> SelectKBest -> RFE -> Model`. Because `SelectKBest` and `RFE` are pipeline steps, `fit` only sees `year < season` in each fold.
- **Leakage demo (1):** `f_classif` is run on `df_dev` (`1967-2008`) once before the loop, then `eval_clf_folds(leaked_cols, EVAL, inside_k=None)` is compared against `eval_clf_folds(TEAM_FEATURES, EVAL, inside_k=5)`.
- **`pim_eval(..., goalie_rule=True)` (4):** For returning goalies (`pos_goalie == 1 & has_prev_player == 1`), replaces the tree prediction with schedule-scaled `prev_pim` (`prev_pim * season_games / prev_year_games`), keeping the Poisson HGB prediction for skaters and rookie goalies.

## Likely questions and answers
- **Why combine filter and wrapper instead of using only one?** Filters (`f_test`, mutual information) are fast and score features independently; wrappers (`RFE`) evaluate feature subsets jointly with a model. Combining `SelectKBest -> RFE` removes clear noise first and lets `RFE` refine the remaining subset.
- **Why didn't feature selection improve Task (a) Lasso or Task (b) Gradient Boosting on `EVAL`?** Lasso already performs embedded L1 selection (`alpha=0.001`), so `Combined MI(18)->RFE(10)` matches its accuracy with 10 features instead of 27 (`p=0.562`). For Task (b), Gradient Boosting with `max_depth=2` already selects splits greedily, and removing features discards weak but complementary cues.
- **Why did the goalie rule help Task (c)?** Goalies take very few penalties (mostly 0 or 2-4 minutes) and 40% have 0 PIM; a global Poisson tree trained mostly on skaters slightly over-predicts goalies, whereas schedule-scaled persistence is sharper for returning goalies.
- **Were any choices made on `EVAL` or `2009`?** No. All `k` values, filter/wrapper combinations, and the `HGB 500 + Goalie rule` were selected strictly on `TUNE` (`1995-2001`).

## Key numbers
| What | Number |
|---|---|
| Leakage demo (`EVAL` PR-AUC, Task b LR k=5) | `0.297` leaked vs `0.293` inside-fold |
| Task (a) `TUNE` Spearman (`Combined MI->RFE` vs `All 27` Lasso) | `0.6200` vs `0.6152` |
| Task (a) `EVAL` Spearman (`Combined MI->RFE` vs `All 27`, Wilcoxon) | `0.5404` vs `0.5455` (`p = 0.562`); `Combined f_reg->RFE` `0.5576` |
| Task (b) `TUNE` / `EVAL` PR-AUC (`All 27 GB` vs best reduced) | `TUNE`: `0.2992` vs `0.2212`; `EVAL`: `0.3315` vs `0.2434` |
| Task (c) `EVAL` MAE (`HGB 500 + Goalie rule` vs NB2 `HGB 300`) | `17.350` vs `17.389` |
| Task (c) `2009` MAE (`HGB 500 + Goalie rule` vs NB2 `HGB 300`) | `15.219` vs `15.330` (Goalie: `2.271` vs `2.773`) |
