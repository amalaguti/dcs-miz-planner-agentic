## 1. Recipe, example, place

- [x] 1.1 Add Nevada intercept spawn literals (Nellis + 350° / 40 km offset)
- [x] 1.2 Add `examples/nellis_dawn_intercept.yaml`
- [x] 1.3 Extend `nellis_north_range_cap` and `nellis_home` with intercept

## 2. Invent and schema

- [x] 2.1 Allow Nevada intercept; GA/escort/recon still refuse
- [x] 2.2 Schema Nevada+intercept loads the new example; dedicated notes

## 3. Tests and docs

- [x] 3.1 Validate+compile; Channel goldens unchanged (`30989.935547`)
- [x] 3.2 Invent/schema tests: intercept allowed; GA/escort/recon still refuse
- [x] 3.3 BACKLOG F4d, README, LESSONS, matching skills
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
