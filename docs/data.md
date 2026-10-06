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
To be populated from the executed EDA audit. Raw files will remain unchanged. Current findings: no exact duplicate rows; one shared Coaches team-season-stint key (Detroit 1998), which must be retained as co-coaching.
