# Hockey data reference

## Source and cutoff
User-supplied assignment and two ER diagram images, plus 22 local CSVs in hockey_development_data/. Local files are authoritative for actual columns and values; diagram SQL types are schematic, not pandas dtypes. Seasons use their starting year. Predictions for year t must use information available before its first game.

## Relationships
Teams is the team-season anchor: (year, lgID, tmID). franchID tracks franchise identity across name/team-code changes; use it with league for historical lags. Player tables join Teams on team-season keys and Master on non-null playerID. Coaches joins Master on non-null coachID, and Teams on team-season keys. Validate Master ID uniqueness and join cardinality before use. Never join missing IDs to other missing IDs. Awards and supplementary tables have different grains; aggregate before joining. Tables without lgID need explicit league resolution; do not blindly assume team/year uniquely identifies a league.

## Initial interpretation
- Teams.rank repeats between divisions in 2009: it is not a global NHL ranking. Historical scope may vary with competition structure.
- G means games in Teams and related team tables; G means goals in Scoring. Coaches uses lowercase g/w/l/t.
- Coaches.stint orders appointments; shared stints can be co-coaches. Multiple coach rows do not necessarily mean a temporal replacement.
- Master includes retrospective retirement/death/career-end fields. Exclude these as predictive features. Historical roster rows do not establish who was contracted before the next season.
- Blank values are not universally zero. Missing T after ties disappear, OTL before introduction, and shootout fields before 2005 can be structurally absent; inspect by era before deriving totals.
- Post* columns and postseason tables describe completed outcomes: only prior-season versions may enter preseason features.

## Inventory, quality and cleaning
Raw files remain unchanged. All 22 tables have zero exact duplicates. Main checked keys have no nulls or duplicates; nine tested team/Master relationships have zero orphan rows. No text cells required trimming. Detroit 1998 has two co-coaches sharing stint 1; retain both.


## Full file inventory

Grains below describe intended observation units; only the main keys tested in the notebook are verified.

| Table | Rows × columns | Year range | Grain / purpose |
|---|---:|---|---|
| AwardsCoaches | 75 × 5 | 1930–2009 | Coach-award-year record. Coach recognition; multiple awards possible |
| AwardsMisc | 120 × 6 | 1965–2009 | Award recipient-year record. Mixed recipient identifiers and award categories |
| AwardsPlayers | 2,021 × 6 | 1917–2009 | Player-award-year record. Awards and all-star recognition; potential multiple rows per person/year |
| Coaches | 1,741 × 14 | 1909–2009 | Coach-team-season-stint. Ordered coaching appointments; co-coaches possible |
| CombinedShutouts | 50 × 8 | 1929–2009 | Event with goalie pair. Dated combined shutouts, regular/postseason flag; no lgID |
| Goalies | 4,096 × 23 | 1909–2009 | Player-team-season-stint. Goalie outcomes plus Post* outcomes |
| GoaliesSC | 31 × 11 | 1912–1925 | Player-team-season finals record. Early Stanley Cup goalie records |
| GoaliesShootout | 346 × 8 | 2005–2009 | Player-team-season-stint. Shootout goalie results; no lgID |
| HOF | 356 × 4 | 1945–2009 | Induction record. Induction year/category; future recognition is leakage |
| Master | 7,469 × 31 | Not seasonal | Person record. Player/coach/HOF identifiers and biography |
| Scoring | 43,848 × 31 | 1909–2009 | Player-team-season-stint. Regular-season scoring plus Post* outcomes |
| ScoringSC | 284 × 10 | 1912–1925 | Player-team-season finals record. Early Stanley Cup player scoring |
| ScoringShootout | 1,487 × 7 | 2005–2009 | Player-team-season-stint. Shootout attempts, goals, game-deciding goals; no lgID |
| ScoringSup | 137 × 4 | 1987–1990 | Player-season supplemental record. Supplemental assists; inspect aggregation before joining |
| SeriesPost | 802 × 13 | 1912–2009 | Season-round-series. Series winners/losers; inspect composite key before use |
| TeamSplits | 1,459 × 43 | 1909–2009 | Team-season. Home/road and monthly records |
| TeamVsTeam | 23,862 × 8 | 1909–2009 | Team-season-opponent. Directed head-to-head record |
| Teams | 1,459 × 27 | 1909–2009 | Team-season. Main team outcomes, standings and franchise anchor |
| TeamsHalf | 41 × 11 | 1916–1920 | Team-season-half. Historical split-season standings |
| TeamsPost | 895 × 17 | 1913–2009 | Team-season postseason record. Postseason team metrics |
| TeamsSC | 30 × 10 | 1912–1925 | Team-season finals record. Early Stanley Cup team records |
| abbrev | 58 × 3 | Not seasonal | Type/code dictionary record. Decode competition abbreviations using Type and Code |


## Verified EDA findings

- NHL: 1,265 team-seasons, 1917–2009; year 2004 is absent. No external explanation was verified. In 2009, 30 teams are divided into six groups, each ranked 1–5; 15 teams share a points total with at least one other team.
- Complete NHL coach coverage. Multiple distinct stints flag 225/1,265 seasons (17.79%); the latest season has 3/30. These are appointment-change proxies, not verified dismissals.
- Exact t−1 franchise joins provide features for 1,198 rows; 67 lack a prior-calendar-year match. Historical 2009 illustration: 1,168 earlier eligible rows and 30 holdout rows. This is not the final assigned split.
- Pooled prior-season points/game correlation with next-season points/game is 0.636. Prior goal difference/game correlation is 0.637. These descriptive correlations combine eras and do not establish out-of-sample performance.
- Across 150 NHL rows from 2005–2009, T is always blank, OTL is complete, G = W + L + OTL and Pts = 2W + OTL always hold. Before 1999, NHL OTL is wholly absent; before 2005, SoW/SoL are wholly absent. Missing special-teams data is concentrated in early history.
- Coach totals differ from team totals in games/wins for Detroit 1998 (shared co-coaching). Loss totals differ in 147 team-seasons: Detroit 1998 plus 146 rows in 1999–2003. This is compatible with era-dependent loss accounting but is not verified as a universal rule. Retain the source values and avoid cross-table equality assumptions.
- Teams.playoff contains stage codes (SC, CQF, etc.), ND, and 454 blanks in NHL. Do not infer a binary participation label without resolving these semantics.

## Cleaning decision log

| Decision | Status / reason |
|---|---|
| Trim text and normalize empty strings in derived copies | Applied; zero cells changed |
| Preserve raw CSVs | Applied; notebook only reads DATA and writes reports |
| Deduplicate rows | No action; zero exact duplicates |
| Drop duplicate coach stint | Rejected; co-coaches are legitimate separate rows |
| Fill every blank with zero | Rejected; structural absence differs from unknown data |
| Fill era-inapplicable T/OTL in accounting expressions | Candidate only; modern identities verified; no raw imputation |
| Divide team totals by G | Applied to derived exploratory features; scoring rules still vary |
| Join all tables on team ID alone | Rejected; requires year, league, grain-aware aggregation |
| Use exact year t−1 + franchise + league | Applied; gaps remain missing, not shifted to latest appearance |
| Aggregate player/goalie features | Deferred; stints, minutes, roster availability and denominator rules need work |
| Imputation/scaling learned from full history | Rejected for modeling; fit on training seasons only |

## Target and feature contract

For regression, exploratory targets are target_points, target_points_per_game and target_points_rank_tied. target_stored_rank is included for inspection only until ranking scope is confirmed. Rank 1 means best. Points ties use minimum rank (e.g. 1, 2, 2, 4); no official tie-breaks are claimed.

For classification, inseason_change_proxy = 1 when the team has more than one distinct coach stint in year t. Shared coaches within one stint do not create an additional change. Missing coverage/stints must remain unknown. offseason_change_proxy compares first coach set in t against final coach set in t−1 and is unknown without exact prior-year coverage. Assignment semantics are still unclarified, as confirmed by the user.

The learning preview is descriptive, not ready-made X: whitelist prev_* feature columns only. Current-season team name/ID/franchise identify the row; year is a temporal index; current outcomes and all labels must be excluded from predictive inputs. Season-t rosters, games, splits, scoring, awards and postseason tables are unavailable at the cutoff. Prior-season outcomes may be used when finalized before that cutoff. Career end, death, future awards/HOF and final roster usage cannot be used retrospectively as if known preseason.

## Field reminders

Identifiers: playerID / coachID / hofID identify people in different roles; tmID is a seasonal team code; franchID links franchise history; lgID/confID/divID describe competition membership. stint orders appearances within a season. GP and team G count games; player G counts goals; A assists; Pts points; GF/GA goals for/against; SA shots against; SOG shots on goal; PIM penalty minutes; SHO shutouts; Min minutes; PPG/PPA power-play goals/assists; SHG/SHA short-handed goals/assists in scoring. In Teams, SHA refers to short-handed goals against under the assignment glossary. PPC/PKC and PKG require explicit confirmation before deriving special-teams rates. Coaches.t should not automatically be interpreted identically to Teams.T across eras. Goalies T/OL combines categories. Master height/weight units are not supplied explicitly: values suggest inches/pounds, but this remains an inference.

## Reproducible reports

reports/eda/table_inventory.csv, column_profile.csv, text_cleaning_audit.csv, join_audit.csv, coach_target_candidates.csv and team_season_learning_preview.csv are generated by the notebook. The ER images provide relationship context; observed CSV values determine actual types and verified keys.
