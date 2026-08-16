## 1. Example and place

- [x] 1.1 Add `examples/needs_oar_point_recon.yaml` (NeedsOarPoint, Spitfire, Blitz observe, 180/133)
- [x] 1.2 Extend `maupertus_inland_strike` and `needs_oar_point_home` mission_types with `recon`

## 2. Invent and schema

- [x] 2.1 Allow Normandy `recon` in invent table (all six types)
- [x] 2.2 Schema: Normandy+recon loads the new example; dedicated notes (no french_coast concatenation)
- [x] 2.3 Update prompts, repair nudges, `SPEC_SHAPE_REMINDER`

## 3. Tests and docs

- [x] 3.1 Validate+compile example; Channel recon goldens unchanged
- [x] 3.2 Schema/invent tests: Normandy recon allowed
- [x] 3.3 Update BACKLOG, README, LESSONS (`agent-tooling`), matching skills
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
