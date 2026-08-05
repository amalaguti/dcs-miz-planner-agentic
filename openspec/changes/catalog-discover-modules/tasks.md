## 1. Implementation

- [x] 1.1 Models: `AircraftModuleRecord` + field on `TheatreInventory`
- [x] 1.2 Probe folder harvest + WWII skip list + reverse Spec-id map
- [x] 1.3 SQLite `aircraft_modules` table; schema v2; replace/load with theatres
- [x] 1.4 Catalog `AircraftAvailabilityView` + `join_aircraft_views` + `list_aircraft`
- [x] 1.5 CLI: `catalog list --type aircraft` uses join; remove deferred note
- [x] 1.6 Tests: probe/cache/refresh + catalog join with fake trees
- [x] 1.7 BACKLOG `#8a.1` done; README/LESSONS

## 2. Verification

- [x] 2.1 `uv run pytest -q`
