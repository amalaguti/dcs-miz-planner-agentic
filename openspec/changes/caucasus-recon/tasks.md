## 1. Example and place

- [x] 1.1 Add `examples/batumi_kutaisi_recon.yaml` (Batumi, Su-25T, Ural-375 observe, 43/110)
- [x] 1.2 Extend `kutaisi_inland_strike` and `batumi_home` mission_types with `recon`

## 2. Invent and schema

- [x] 2.1 Allow Caucasus `recon` in invent table (all six types)
- [x] 2.2 Schema: Caucasus+recon loads the new example; dedicated notes (no french_coast concatenation)
- [x] 2.3 Update prompts, repair nudges, `SPEC_SHAPE_REMINDER`

## 3. Tests and docs

- [x] 3.1 Validate+compile example; Channel recon goldens unchanged
- [x] 3.2 Schema/invent tests: Caucasus recon allowed
- [x] 3.3 Update BACKLOG, README, LESSONS (`agent-tooling`, `channel-ids`), matching skills
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
