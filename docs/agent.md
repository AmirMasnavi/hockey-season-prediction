# Project rules for agents

- Read this file and memory.md at the start of each session. Read prd.md for scope and data.md for data semantics.
- Keep communication concise. Ask about consequential ambiguities; continue independent work while waiting.
- Preserve original CSVs. Perform cleaning in derived copies; document every substantive rule and its evidence.
- Prediction time is the day before the new season starts. Features for season t must be available before that cutoff. Never use season-t outcomes, final roster usage, postseason results, or future biography/career information as features.
- Use franchise identity and league when connecting seasons. Require exact year adjacency for one-year lags; do not silently bridge missing seasons or inactive franchises.
- Respect table grain and validate join cardinality. Coach stints can contain co-coaches; player stints must not be mistaken for unique players.
- Every notebook code cell must sit between an intent markdown cell and a findings markdown cell. Findings must match executed output and distinguish observations from assumptions.
- Use chronological validation, not shuffled team rows. Keep all teams from a season together. Fit cleaning/imputation only on training data once modeling starts.
- Update memory.md after meaningful milestones, with decisions, unresolved questions, verification, and the next step. Update data.md when new data facts are established.
- Make small commits at completed milestones, as requested by the user. Stage intended project files only; do not commit environments, caches, or secrets. Do not push unless requested.
- Task (c) is TBA: do not invent it. Do not claim an official target definition or test season until confirmed.
