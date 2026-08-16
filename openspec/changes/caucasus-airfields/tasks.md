## 1. Registry and example

- [x] 1.1 Extend `data/theatres/Caucasus/airfields.yaml` to the eight curated keys
- [x] 1.2 Add `Russia` to `data/era/modern/countries.yaml`
- [x] 1.3 Add `examples/mozdok_cold_freeflight.yaml` (Mozdok, Russia red, Su-25T)

## 2. Infer and tools

- [x] 2.1 Extend `infer_theatre` to the new Caucasus Spec keys
- [x] 2.2 Confirm `find_airfield` is theatre-scoped (Mozdok 28 ≠ NeedsOarPoint)

## 3. Tests and docs

- [x] 3.1 Registry tests: eight AFs; Mozdok 28 vs NeedsOarPoint; Russia modern; Channel+Russia unknown
- [x] 3.2 Validate+compile Mozdok contracts; invent still FF-only at Batumi
- [x] 3.3 Update BACKLOG, README, LESSONS (`channel-ids`), matching skills
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
