# Defence sheet: notebook 3 (classification: task b)

## The story in five lines
1. About one team in five changes coach during a season, so accuracy is useless; the main metric is PR-AUC (random level about 0.20).
2. A one-feature model on last season's points already gets PR-AUC 0.310; the best model, gradient boosting, gets 0.331. It clearly beats chance but is **not proven** better than that baseline.
3. Resampling (including SMOTE) does not improve the ranking; it only shifts the probabilities. SMOTE on the whole data leaks badly (random forest 0.646 instead of 0.269).
4. G2 is met narrowly: 41.7% of the real changes are in the riskiest quarter of teams (needed: 40%).
5. Risk factors: many goals against, weak penalty kill, many players used, a coach without a winning record; deep playoff runs and a recent change lower the risk.

## Section by section

| Section | What the cell does |
|---|---|
| 1 | Loads the table, class balance per group of seasons, change rate over time; metric table and G2 criterion. |
| 2 | Five baselines (majority, constant prevalence, stratified random, rule on last-season points, one-feature logistic) and the metric functions. |
| 3 | Seven algorithms with defaults, and the helpers `pipeline`, `fit_predict`, `evaluate_many`. |
| 4.1 | SMOTE on the whole data vs inside the folds (shuffled 5-fold CV): the leakage demonstration. |
| 4.2 | Five strategies x seven algorithms on the tuning seasons; effect on flags at 0.5; class counts before and after. |
| 5 | Grid search with the chosen strategy, timing, and the selection rule. 5.1: validation curves. |
| 6 | Threshold with the best F1, with and without a 40% limit; PR curves; precision/recall/F1 by threshold. |
| 7 | All models and baselines on 2002-2008, the G2 check; 7.1 PR/ROC curves, confusion matrix, calibration; 7.2 Friedman, Wilcoxon, paired bootstrap. |
| 8 | Training vs evaluation PR-AUC; 8.1 learning curve with 20-100% of the training rows. |
| 9 | Improvement path: default -> strategy -> tuned -> threshold, on tuning and evaluation seasons. |
| 10 | Permutation importance of boosting and odds ratios of a logistic regression with bootstrap intervals. |
| 11 | Depth-3 tree with balanced class weights, change rate per leaf. |
| 12 | Final test on 2009, team list, CSV. |
| 13 | Conclusion and rubric table. |

## Code you must be able to explain
- **`pipeline(model, strategy, params)` (3):** builds imputer -> scaler -> (resampler) -> classifier as an **imblearn** Pipeline. The resampler only runs during `fit`, so it changes the training seasons only; predictions are made on the real data.
- **`fit_predict` / `predict_seasons` (3):** rolling origin; also stores `k` (expected number of changes = training prevalence x teams) and the PR-AUC on the training rows.
- **`evaluate_many` (3):** runs many independent configurations at the same time on all CPU cores with `joblib`; the only parallel code.
- **`hits_at(pred, k)` (2):** counts the real changes among the k highest scores of a season. If several teams are tied at the cut-off, they share the remaining places (expected value), so a constant prediction gets exactly the random-flagging result.
- **`scores` (2):** computes all metrics for a set of predictions: pooled and per-season PR-AUC, ROC-AUC, Brier (only for real probabilities), precision@k, recall@k, top-quarter share, and with a threshold also precision, recall, F1 and the share flagged.
- **`pick_threshold` (6):** tries every distinct predicted probability as threshold, skips those that flag more than 40% of the teams, and keeps the one with the best F1.
- **Leak demo (4.1):** `SMOTE.fit_resample` returns the real rows first and the synthetic ones after, so `p_wrong[:len(y_pool)]` scores only the real rows.
- **Paired bootstrap (7.2):** the same 2,000 resamples of the 180 team-seasons are used for every method, so the differences are paired.
- **Selection rule (5):** best pooled tuning PR-AUC; if several are within 0.005, the best mean per season decides (same idea as the tie-break of notebook 2).

## Likely questions and answers
- **Why not accuracy?** "Never change" is 80% accurate and finds no change; accuracy rewards ignoring the minority class.
- **Why PR-AUC instead of ROC-AUC?** PR-AUC focuses on the rare class; ROC-AUC can look decent when positives are few. A random model scores about the prevalence in PR-AUC, which is easy to read.
- **Pooled vs per season?** Pooled is one number over all 180 team-seasons (more stable); per season shows how much it varies (sd about 0.15).
- **Why did resampling not help?** It changes what the learner sees, which pushes the probabilities up, but hardly changes the *order* of the teams, which is what PR-AUC measures. Notebook 1 (3.10.1) found the same.
- **Why show the wrong SMOTE on purpose?** To show the leakage: each synthetic row mixes a real positive with its neighbour, so validation information sits in the training set. Random forest 0.646 vs 0.269 when done correctly.
- **Why a 40% limit on the threshold?** Without it, the best F1 flags 82% of the teams for boosting (95% for the forest): a watch list of almost everyone is useless.
- **Why is the threshold chosen on the tuning seasons?** It is a model parameter; choosing it on the evaluation seasons would be optimistic.
- **Why gradient boosting?** Best pooled PR-AUC on the tuning seasons (0.299); also best per season, best calibrated and best on the evaluation seasons. It was chosen before looking at the evaluation seasons.
- **Was the selection rule changed?** In an earlier version the tree and boosting tied on the tuning seasons and the per-season tie-break was added then; it uses tuning-season numbers only, and in this version boosting is best on pooled PR-AUC alone. This is stated in the limitations.
- **Is the model better than the baseline?** Not shown: Friedman p = 0.90, bootstrap gain +0.021 with interval -0.129 to +0.158. It is clearly better than chance (bootstrap probability 99.5%).
- **Is G2 really met?** Yes, narrowly: PR-AUC 0.331 >= 0.250 and 15 of 36 changes (41.7%) in the riskiest quarter. One change fewer would miss it; the baseline gets 30.6%.
- **Boosting has a big training-evaluation gap (0.81 vs 0.41). Is it overfitting?** It memorises its training rows, but small trees and a modest learning rate keep the variance in check; its evaluation score is the best. The gap alone does not show a bad model.
- **Why are the under-sampled logistic regression's probabilities so high?** Under-sampling trains on 50/50 data, so it predicts as if half the teams change coach (predicted 0.18-0.69 vs observed 0.14-0.33).
- **Why does coach tenure matter for the trees but not for the logistic model?** Its effect is not monotone (risky in some years of a tenure, safe in others, notebook 1 3.4.1), which trees capture and a linear model cannot.
- **Why does power-play % raise the odds?** Probably a correlation with other features or chance; we do not interpret it as a hockey effect. The missing-goalie-data flag marks old seasons.
- **The 2009 test caught nothing. Is the model useless?** 2009 had only 3 changes (prevalence 0.10, half the usual rate); even 8 randomly flagged teams would miss all three about 38% of the time. One season of 3 positives says almost nothing.
- **Why do tree results differ from the colleague's first version?** The feature columns are in a different order; tree splits that tie are broken by feature order. Linear, k-NN, naive Bayes and SVM results are identical; the conclusions do not change.

## Key numbers
| What | Number |
|---|---|
| Changes in tuning / evaluation seasons | 37 of 193 / 36 of 180 |
| Baseline (one-feature logistic), evaluation PR-AUC | 0.310 |
| Gradient boosting, evaluation PR-AUC (pooled / per season) | 0.331 / 0.407 +- 0.158 |
| Boosting at threshold 0.237 | precision 0.333, recall 0.444, F1 0.381 (16 of 36 found, 32 false alarms) |
| Precision@k (boosting vs random) | 0.361 vs 0.200 |
| Top-quarter share (G2) | 41.7% (needed 40%; baseline 30.6%) |
| SMOTE leak, random forest | 0.646 wrong vs 0.269 right |
| Friedman / bootstrap gain | p = 0.90 / +0.021 (-0.129 to +0.158) |
| Grid search | 560 fits in 22 seconds (parallel) |
| 2009 | 3 changes, none flagged; PR-AUC 0.103 vs prevalence 0.100 |
