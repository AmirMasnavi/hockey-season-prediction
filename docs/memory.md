# Project memory

Last updated: 2026-10-06 (Europe/Lisbon)

## User preferences
Concise communication; all analysis in Python; start with casual EDA; code sandwiched between intent and findings markdown; maintain project docs/memory; make frequent milestone commits.

## Completed
- Created prd.md, agent.md, memory.md, data.md under docs/, with root AGENTS.md routing to the canonical rules.
- Built and executed notebooks/01_data_understanding.ipynb: 12 analysis steps, 39 cells, raw previews, profiles, join checks, era missingness, season structure, ranking/coach candidates, plots, exact t−1 feature table and explicit X/y previews. All code cells have intent/findings markdown.
- Added eight reproducible EDA report CSVs, README and pinned tested Python environment requirements. Raw CSVs preserved.
- Read the user's Colab in the existing in-app browser after web retrieval failed. It is 01_supervised_learning_tabular_CLASS.ipynb, a Titanic supervised-learning lab. Its inspection/class balance/leakage/pipeline principles inform the project; its shuffled splits are not appropriate for future-season hockey validation. Added info(), categorical summaries, majority-class ratio and plot. Did not modify or run the reference notebook.

## Established facts
22 CSV tables; seasonal tables end at 2009. Teams: 1,459 rows, including 1,265 NHL; Scoring: 43,848; Coaches: 1,741. Five league codes occur. NHL lacks 2004. Checked keys and NHL franchise-season identity are unique and non-null. No exact duplicates or text-trimming changes. Nine tested team/Master relationships have zero orphans. Detroit 1998 has two co-coaches sharing stint 1.

In 2009 rank is division-scoped (six groups, each 1–5), not global NHL rank; points ties affect 15 teams. Complete NHL coaching coverage; 225/1,265 (17.79%) have multiple stints. A no-change predictor has 82.21% descriptive accuracy, not a held-out score. Coach loss totals differ from team losses in 147 rows: 1998 co-coaching plus 1999–2003 accounting differences. Modern NHL games/points identities hold in all 150 rows from 2005–2009.

Exact t−1 franchise join: 1,198 matched rows, 67 unmatched; 2005 is intentionally unmatched because 2004 is absent. Historical 2009 illustration: 1,168 earlier eligible rows and 30 holdout rows. Prior points/game and goal-difference/game correlations with next-season points/game are 0.636 and 0.637, pooled across eras; no predictive validation claim.

## Decisions
NHL is provisional for detailed EDA. Keep raw data unchanged; no broad imputation. Use exact calendar-year lags. Stored rank needs scope confirmation; points/points-game regression with within-season sorting is a candidate. Co-coaches sharing a stint do not alone imply a change. Missing labels stay unknown. Only prev_* columns are whitelisted for X_preview; current outcomes and labels are excluded. This EDA inspected development seasons including 2009; reserve a genuinely untouched final test later. No model training yet.

## User clarification / pending questions
User confirmed the assignment has not clarified coach-change semantics. Keep in-season and offseason proxies provisional. User requested all work in Python and provided a course reference, but did not specify test season/league. Official target ranking scope/tie rules and task (c) remain unknown.

## Next step
Independent review complete; repository publication is the current milestone. Then review findings together; confirm target scope when assignment details arrive. Choose a relevant era and explicit feature policy, then chronological backtests with simple baselines before model comparison. Do not invent task (c).

## Verification / environment
Python 3.14 project .venv with pandas, numpy, matplotlib, nbformat, nbclient, ipykernel. Local Jupyter execution required permission for localhost kernel ports. Dependencies and milestone Git writes were approved automatically. requirements.txt pins the tested environment. Notebook is portable to Colab with the CSV folder supplied, but Colab execution is unverified.

## Milestone commits
40ae1ad — initial scope/rules/memory.
3f4589f — executed introductory EDA and reports.
Subsequent commit finalizes course-reference checks, source-data snapshot and documentation; consult git log for its hash.


## Active milestone: conclusion, independent review and private repository
User authorized creating a new private GitHub repository and pushing the project after an independent agent review. Before implementation, record this milestone and commit it. Add a comprehensive notebook conclusion; review data/target correctness, reproducibility, omissions and future requirements; apply justified improvements; verify and commit; create a private repository and push. Final test season and coach-change definition remain unconfirmed. Initial GitHub authentication check failed under restricted network; recheck with network access before concluding authentication is unavailable.

Starting milestone committed as 0b2e6a3. GitHub authentication works with network access (account AmirMasnavi); no remote exists yet. Independent review agent dispatched. Comprehensive conclusion added to notebook, covering every analysis section and outstanding modeling requirements.


## Review and publication status
- Starting state/memory committed: 0b2e6a3. Complete notebook conclusion committed: 422ca59.
- Independent review completed and final verification passed. Findings and resolutions are in docs/review.md. Added postseason-only Ottawa 2001 coaching audit, regular-g>0 sensitivity (zero binary label differences), and modeling era sample sizes. Modern target-era sample: 120 matched rows across 2006–2009, 19 positives. Proxies remain provisional; no model training.
- Added scripts/run_eda.py: execute with the active Python interpreter or use --check for saved-output verification. Verified 12 executed code cells, five figures, intent/findings sandwiches, complete final conclusion and 22 source checksums. Eight CSV reports plus source checksum JSON. Colab remains unverified.
- Created new private repository: https://github.com/AmirMasnavi/hockey-season-prediction. Reviewed implementation committed as 9ad882d and successfully pushed to origin/main. GitHub confirmed isPrivate=true and default branch main. This publication-status note is committed afterward; use git log for the latest documentation commit. Working tree was clean after the implementation push.
- Next substantive work: confirm targets/test membership; choose training era and gap/entrant policy; build chronological baseline evaluation before model comparison. Reviewer found no remaining blockers to publication.
