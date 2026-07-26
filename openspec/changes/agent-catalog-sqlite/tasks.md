## 1. Known catalog schema and sync

- [x] 1.1 Define `catalog_*` SQLite schema for known theatres, airfields, aircraft, weather, payloads, Spec enums + sync metadata
- [x] 1.2 Implement idempotent sync from packaged Channel YAML + Spec enums
- [x] 1.3 Keep install inventory tables separate; implement known / discovered / offerable theatre join helpers

## 2. Query surface and discovery visibility

- [x] 2.1 Python query API: list by type; theatre views with known vs install flags
- [x] 2.2 CLI `dcs-miz catalog sync` and `dcs-miz catalog list [--type …] [--json]` (include discovery-inclusive theatre listing)
- [x] 2.3 Note/stub only: aircraft module discovery deferred (no install harvest into known); optional backlog pointer
- [x] 2.4 Tests with temp DB: known sync; offerable join; list CLI; Ruff clean

## 3. Docs and ad-hoc maintenance

- [x] 3.1 Document promote-to-known workflow (edit YAML → accept in DCS when compile-supported → catalog sync); update ARCHITECTURE / README / BACKLOG
- [x] 3.2 Acceptance: catalog sync + list known resources; list discovered theatres from local inventory without claiming them as known
