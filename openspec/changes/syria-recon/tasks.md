## 1. Example and place

- [x] 1.1 Add `examples/incirlik_aleppo_recon.yaml` (Incirlik, Su-25T, Ural-375
      observe country Syria, 121/200, no payload)
- [x] 1.2 Extend `aleppo_inland_strike` and `incirlik_home` mission_types with
      `recon` (do not add recon to `incirlik_iskenderun_cap`)

## 2. Invent and schema

- [x] 2.1 Allow Syria `recon` in invent table (all six types)
- [x] 2.2 Schema: Syria+recon loads the new example; dedicated notes (no
      french_coast concatenation)
- [x] 2.3 Update prompts, repair nudges (Aleppo 121/200 not Iskenderun 180/40),
      `SPEC_SHAPE_REMINDER`

## 3. Tests and docs

- [x] 3.1 Validate+compile example; Channel recon goldens unchanged
- [x] 3.2 Schema/invent tests: Syria recon allowed; Nevada still fail-closed
- [x] 3.3 Update BACKLOG F3g, README, LESSONS (`agent-tooling` / `channel-ids`),
      matching skills + orchestrator baseline
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
