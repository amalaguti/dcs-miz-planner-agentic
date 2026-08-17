## 1. Example and place

- [x] 1.1 Add `examples/incirlik_iskenderun_escort.yaml` (Incirlik, Su-25T,
      Turkey Su-25T package, Syria Su-25T bounce, 180/40, 09:00)
- [x] 1.2 Extend `incirlik_iskenderun_cap` and `incirlik_home` mission_types
      with `escort`

## 2. Invent and schema

- [x] 2.1 Allow Syria `escort` in invent refuse table; GA and recon still
      refuse every turn
- [x] 2.2 Schema: Syria+escort loads the new example; dedicated notes (no
      Manston 120/55 concatenation)
- [x] 2.3 Update prompts, repair nudges, `SPEC_SHAPE_REMINDER`

## 3. Tests and docs

- [x] 3.1 Validate+compile example; Channel escort goldens unchanged
- [x] 3.2 Schema/invent tests: Syria escort allowed; GA still refused
- [x] 3.3 Update BACKLOG F3e, README, LESSONS (`agent-tooling` / `channel-ids`),
      matching skills + orchestrator baseline
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
