# Defence sheets

Preparation for the presentation and the questions afterwards. One sheet per notebook:

- [1_eda_defence.md](1_eda_defence.md): business understanding, data understanding, data preparation (all three tasks)
- [2_regression_defence.md](2_regression_defence.md): task (a) team ranking and task (c) penalty minutes
- [3_classification_defence.md](3_classification_defence.md): task (b) in-season coach changes

Each sheet has:
1. **The story in five lines**: what to say if you only get one minute.
2. **Section by section**: what each non-trivial cell does, in one sentence.
3. **Code you must be able to explain**: the functions a teacher is most likely to point at.
4. **Likely questions and answers.**
5. **Key numbers** to know by heart.

How to use them: split the sections between you, and make sure the person presenting a section can explain every code cell in it without reading. If an answer here does not convince you, change the notebook, not just the answer.

## Ideas that come back in every notebook

| Idea | One-sentence answer |
|---|---|
| Prediction time | Everything is predicted the day before the season starts, so features only come from season t-1 and from the opening-day coach (stint 1). |
| Rolling origin | To predict season s we train on all seasons before s and predict the whole season s; never shuffled rows, because the future must not train the past. |
| Tuning vs evaluation seasons | Every choice is made on 1995-2001; 2002-2008 are only used to compare and test; 2009 is used once at the end. |
| Within-season z-scores | Scoring levels change by era (1980s vs 2000s), so each statistic is compared with the other teams of the same season. |
| Pipelines | Imputer, scaler (and resampler) are inside the pipeline, so they are fitted on the training seasons of each fold only: no leakage. |
| Six evaluation seasons | Small sample: the smallest possible two-sided Wilcoxon p-value is 2 / 2^6 = 0.031, so we read effect sizes and intervals, not only p-values. |
| Seeds | Notebook 1 mostly uses 42 (0 in some imputers), notebooks 2 and 3 use 0; fixed seeds make every run identical. |
