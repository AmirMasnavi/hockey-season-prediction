# Hockey prediction project

## Objective
Use the supplied historical hockey database to predict, for a designated new season, (a) final regular-season team ranking and (b) the set of teams that change coaches. Task (c) is TBA.

All predictions are made the day before the first game of that season. The dataset's year denotes the starting year (2005 means 2005–06).

## Current scope
First understand the files, schemas, sample rows, coverage, missingness, relationships, season/league differences, and target definitions. Produce an executed introductory notebook with intent → code → findings throughout. Propose conservative cleaning decisions and a small historical team-season learning table. Do not train or tune models yet.

## Provisional modeling decisions
- Start EDA with NHL, while inventorying all supplied leagues. Final competition scope remains unconfirmed.
- Ranking: examine stored rank before using it. Explore points/points-per-game regression followed by within-season ordering. Derived tied points ranks are exploratory and do not implement official standings tie-breaks.
- Coach changes: inspect ordered coach stints within season; distinguish in-season changes from offseason turnover. Co-coaches and missing coverage need explicit treatment.
- Join prior season features to target-year labels using (league, franchise) and exact year t−1. New entrants and missing years need a later fallback policy.
- Use chronological backtests; latest observed season can illustrate a holdout but is not the assigned test season.

## Deliverables / acceptance
- docs/prd.md, docs/agent.md, docs/memory.md, docs/data.md and a root AGENTS.md entry point.
- Executed notebooks/01_data_understanding.ipynb with real data previews, coverage, quality audit, target exploration, plots, and a leakage-safe lag example.
- Reproducible environment requirements and small EDA audit exports under reports/eda/.
- Raw data unchanged; no notebook execution errors; every code cell has markdown before and after; findings grounded in output.

## Evaluation plan for later
Ranking: MAE for numeric target, within-season Spearman correlation and ranking error; clarify expected league/conference/division ordering and tie policy first. Coach changes: precision, recall, F1, PR-AUC and calibrated probabilities, compared with prevalence/majority baselines. Threshold choice must use validation data only.

## Open questions
Official test season and league scope; ranking scope and official tie policy; whether coach changes mean during-season replacement or include offseason turnover; handling new teams and gaps; task (c). Only development CSVs have been supplied so far.
