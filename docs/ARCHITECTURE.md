# Architecture baseline — Football Career: Become a Legend

## Confirmed decisions
- Universe: real-world football.
- Scope: full football universe; player career is the primary user journey.
- Interface: hybrid narrative + dashboard.
- Runtime: Python in Pydroid 3; standard library first.

## Layer boundaries
- `domain/`: entities and invariants, independent of UI and persistence.
- `engine/`: world time, orchestration and domain events.
- `systems/`: career, training, match, transfers, competitions and world simulation.
- `data/`: sourced football records and source metadata.
- `persistence/`: versioned save/load and recovery.
- `interfaces/`: terminal input, dashboards and narrative presentation.
- `tests/`: automated verification.

## Real-world data policy
Every imported record must carry provenance: provider/source, source URL or dataset identifier, retrieval timestamp, and license/terms review. Do not fabricate real players, clubs, competitions, fixtures, results, ratings or contracts. Separate imported people from user-created career characters.

`TODO(design): select approved data providers, licensing strategy, update cadence and offline snapshot policy.`

## Design authority
The Production Bible is authoritative. Do not invent gameplay rules, ratings, progression curves, calendar rules, match formulas, transfer logic or monetization values. Mark unresolved values `TODO(design)`.

## Stage 1 deliverables
- Modular package structure.
- Event bus and calendar clock primitives.
- Domain entity shells with provenance fields.
- Versioned JSON save manager with atomic writes and backup recovery.
- Minimal hybrid terminal/dashboard shell.
- Unit tests for clock, event bus and save round-trip.

## Deliberate omissions
No fabricated football database, ratings, match outcomes, training formulas, league schedules, transfer valuations or undefined guild mechanics. These require Bible reconciliation and/or sourced data.
