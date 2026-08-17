## 1. Recipe, example, place

- [x] 1.1 Add Caucasus intercept spawn literals (Batumi + −40 km easting);
      keep Channel Hawkinge/Dover and Normandy Cherbourg literals bit-identical
- [x] 1.2 Add `examples/batumi_dawn_intercept.yaml` (Batumi, Su-25T, Russia
      Su-25T, 06:00)
- [x] 1.3 Extend `batumi_black_sea_cap` and `batumi_home` mission_types with
      `intercept`

## 2. Invent and schema

- [x] 2.1 Allow Caucasus `intercept` in invent refuse table; escort/recon still
      refuse every turn
- [x] 2.2 Schema: Caucasus+intercept loads the new example; dedicated notes (no
      Hawkinge concatenation)
- [x] 2.3 Update prompts, repair nudges, validation hint, `SPEC_SHAPE_REMINDER`

## 3. Tests and docs

- [x] 3.1 Validate+compile example; Channel intercept recipe/goldens unchanged
- [x] 3.2 Schema/invent tests: Caucasus intercept allowed; escort still refused;
      Syria intercept still fail-closed
- [x] 3.3 Update BACKLOG F2f, README, LESSONS (`channel-ids` / `agent-tooling`),
      matching skills + orchestrator baseline
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
