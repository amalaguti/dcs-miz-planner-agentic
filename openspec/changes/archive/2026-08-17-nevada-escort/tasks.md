## 1. Example and place

- [x] 1.1 Add `examples/nellis_north_range_escort.yaml` (Nellis, Su-25T,
      USA Su-25T package, Russia Su-25T bounce, 350/40, 09:00)
- [x] 1.2 Extend `nellis_north_range_cap` and `nellis_home` mission_types
      with `escort`

## 2. Invent and schema

- [x] 2.1 Allow Nevada `escort` in invent refuse table; GA and recon still
      refuse every turn
- [x] 2.2 Schema: Nevada+escort loads the new example; dedicated notes (no
      Manston 120/55 concatenation)
- [x] 2.3 Update prompts, repair nudges, `SPEC_SHAPE_REMINDER`

## 3. Tests and docs

- [x] 3.1 Validate+compile example; Channel escort goldens unchanged
- [x] 3.2 Schema/invent tests: Nevada escort allowed; GA still refused
- [x] 3.3 Update BACKLOG F4e, README, LESSONS (`agent-tooling` / `channel-ids`),
      matching skills + orchestrator baseline
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
