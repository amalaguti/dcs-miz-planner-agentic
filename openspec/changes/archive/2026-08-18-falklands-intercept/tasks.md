## 1. Recipe, example, place

- [x] 1.1 Add Falklands intercept spawn literals (Mount Pleasant + 150° / 40 km offset)
- [x] 1.2 Add `examples/mount_pleasant_dawn_intercept.yaml`
- [x] 1.3 Extend `mount_pleasant_south_atlantic_cap` and `mount_pleasant_home` with intercept

## 2. Invent and schema

- [x] 2.1 Allow Falklands intercept; GA/escort/recon still refuse
- [x] 2.2 Schema Falklands+intercept loads the new example; dedicated notes

## 3. Hint hygiene

- [x] 3.1 Derive `intercept_unsupported_theatre` hint from `INTERCEPT_SPAWN_RECIPES` keys; derive `domain_unsupported_theatre` hints from `DOMAIN_THEATRES`

## 4. Tests and docs

- [x] 4.1 Validate+compile; Channel goldens unchanged (`30989.935547`)
- [x] 4.2 Invent/schema tests: intercept allowed; GA/escort/recon still refuse
- [x] 4.3 BACKLOG F5d, README, LESSONS, matching skills
- [x] 4.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
