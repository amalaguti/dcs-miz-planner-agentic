## 1. Registry and example

- [x] 1.1 Extend `data/theatres/Syria/airfields.yaml` to the eight curated keys
- [x] 1.2 Add `Syria` to `data/era/modern/countries.yaml`
- [x] 1.3 Add `examples/palmyra_cold_freeflight.yaml` (Palmyra, Syria red, Su-25T)

## 2. Infer and tools

- [x] 2.1 Extend `infer_theatre` to the new Syria Spec keys
- [x] 2.2 Confirm `find_airfield` is theatre-scoped (Palmyra 28 ≠ Mozdok ≠ NeedsOarPoint)

## 3. Tests and docs

- [x] 3.1 Registry tests: eight AFs; Palmyra 28 vs Mozdok/NeedsOarPoint; Syria country modern; Channel+Syria unknown
- [x] 3.2 Validate+compile Palmyra contracts; invent still FF-only at Incirlik
- [x] 3.3 Update BACKLOG, README, LESSONS (`channel-ids`), matching skills
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
