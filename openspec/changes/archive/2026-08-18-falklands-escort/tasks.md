## 1. Example and place

- [x] 1.1 Add `examples/mount_pleasant_south_atlantic_escort.yaml` (MountPleasant, Su-25T, UK package, Argentina bounce, 150/40, 09:00)
- [x] 1.2 Extend `mount_pleasant_south_atlantic_cap` and `mount_pleasant_home` mission_types with escort

## 2. Invent and schema

- [x] 2.1 Allow Falklands `escort` in invent refuse table; GA and recon still refuse every turn
- [x] 2.2 Schema: Falklands+escort loads the new example; dedicated notes (no Manston 120/55 concatenation)
- [x] 2.3 Update prompts, repair nudges, `SPEC_SHAPE_REMINDER`

## 3. Tests and docs

- [x] 3.1 Validate+compile example; Channel escort goldens unchanged
- [x] 3.2 Schema/invent tests: Falklands escort allowed; GA still refused
- [x] 3.3 Update BACKLOG F5e, README, LESSONS (`agent-tooling` / `channel-ids`), matching skills + orchestrator baseline
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
