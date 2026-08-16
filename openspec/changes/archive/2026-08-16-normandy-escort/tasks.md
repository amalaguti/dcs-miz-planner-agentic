## 1. Example and place

- [x] 1.1 Add `examples/needs_oar_point_escort.yaml` (NeedsOarPoint, Spitfire, MosquitoFBMkVI, Bf-109K-4, 180/63)
- [x] 1.2 Extend `cherbourg_channel_cap` and `needs_oar_point_home` mission_types with `escort`

## 2. Invent and schema

- [x] 2.1 Allow Normandy `escort` in invent refuse table; recon still refuses every turn
- [x] 2.2 Schema: Normandy+escort loads the new example; dedicated notes (no Manston 120/55 concatenation)
- [x] 2.3 Update prompts, repair nudges, `SPEC_SHAPE_REMINDER`

## 3. Tests and docs

- [x] 3.1 Validate+compile example; Channel escort goldens unchanged
- [x] 3.2 Schema/invent tests: Normandy escort allowed; recon still refused
- [x] 3.3 Update BACKLOG, README, LESSONS (`agent-tooling`), matching skills
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
