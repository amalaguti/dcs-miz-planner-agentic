## 1. Recipe, example, place

- [x] 1.1 Add Normandy intercept spawn literals (NeedsOarPoint + −63 km northing); keep Channel Hawkinge/Dover literals bit-identical
- [x] 1.2 Add `examples/needs_oar_point_dawn_intercept.yaml` (NeedsOarPoint, Spitfire, Bf-109K-4, 06:00)
- [x] 1.3 Extend `cherbourg_channel_cap` mission_types with `intercept`

## 2. Invent and schema

- [x] 2.1 Allow Normandy `intercept` in invent refuse table; escort/recon still refuse every turn
- [x] 2.2 Schema: Normandy+intercept loads the new example; dedicated notes (no Hawkinge concatenation)
- [x] 2.3 Update prompts, repair nudges, validation hint, `SPEC_SHAPE_REMINDER`

## 3. Tests and docs

- [x] 3.1 Validate+compile example; Channel intercept recipe/goldens unchanged
- [x] 3.2 Schema/invent tests: Normandy intercept allowed; escort still refused
- [x] 3.3 Update BACKLOG, README, LESSONS (`channel-ids` / `agent-tooling`), matching skills
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
