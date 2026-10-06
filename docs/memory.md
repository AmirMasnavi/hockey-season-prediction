# Project memory

Last updated: 2026-10-06 (Europe/Lisbon)

## User preferences
Concise communication; start with casual EDA; code sandwiched between intent and findings markdown; maintain project docs and memory; make frequent milestone commits.

## Current status
Project documentation initialized. Local CSV inventory inspected; introductory notebook is being built. No modeling yet.

## Established facts
22 CSV tables; seasonal tables end at 2009. Teams has 1,459 rows (1,265 NHL), Scoring 43,848 rows, Coaches 1,741 rows. Five league codes occur. NHL lacks year 2004. Teams keys (year, lgID, tmID) and NHL franchise-season keys are unique. No exact duplicate rows in the 22 tables. Detroit 1998 has two co-coaches sharing stint 1.

## Working decisions
Use NHL for initial target exploration, subject to confirmation. Preserve raw data. Interpret years as season start years. Require exact calendar-year lags. Stored rank needs scope inspection; explore points-based targets without claiming official ordering. Coach target semantics still pending.

## Pending user clarification
Official test season/league; in-season versus offseason-inclusive coach changes. Questions asked asynchronously; do not silently treat unanswered questions as confirmed.

## Next action
Execute the introductory notebook, document findings/cleaning decisions and save quality/target audit reports. Commit each completed milestone.
