# Independent EDA review — 2026-10-06

## Assessment
An independent agent inspected project instructions/docs, the executed notebook, source data, exported reports, requirements and README before publication. The reviewer found the current EDA sound for its scope: counts and lag joins matched exports, execution had no errors, all code cells had intent/findings markdown, and target/cutoff caveats were explicit. No modeling has been performed.

## Accepted improvements

| Finding / suggestion | Resolution |
|---|---|
| Coaching stints can include postseason-only appointments | Added an audit/export identifying Ottawa 2001 stint 3 (regular g missing, postg=12). Added sensitivity check: restricting to g > 0 changes zero observed binary labels, but may change endpoint sets. Retained provisional all-appointment proxies and documented endpoint ambiguity. |
| Recent-era restriction has a very small sample | Added an era sample-size report. Target years from 2005 onward have 120 matched rows across 2006–2009, including 19 coaching-change positives. Documented need for uncertainty and era comparison. |
| Include observed coach/performance association in conclusion | Conclusion records prior points/game 0.952 vs 1.033, from 214 change / 984 no-change matched rows, without causal or validation claims. |
| Clarify future requirements and redundant features | Conclusion identifies official test membership, entrant/gap policy, preseason roster knowledge, chronological evaluation and training-only preprocessing. Records 0.946 correlation between prior points/game and goal difference/game. |

Also added a reproducible Python notebook runner/checker and source checksum verification to make the existing execution workflow repeatable.

## Deferred until modeling

1. Confirm test season/league, ranking scope and ties, coaching definition, submission format, evaluation metrics and task (c).
2. Establish target-season team membership independently of outcomes; retain new/unknown teams with a documented fallback.
3. Compare relevant historical eras before choosing training data. Use expanding chronological folds and report season-level metrics; coach positives per season may be very few.
4. Compare persistence ranking and majority/prevalence baselines first. Fit preprocessing only within training folds and choose thresholds on validation folds.
5. Add player/goalie/coach features only after resolving roster availability, stints, denominators, postseason-only records and co-coaching aggregation.
6. Broaden numerical plausibility and specialist-table relationship checks when those tables enter predictive features. Current join audit is explicitly limited to the nine checked relationships.
7. Colab execution remains unverified; pinned dependencies describe the tested local Python 3.14 environment.
