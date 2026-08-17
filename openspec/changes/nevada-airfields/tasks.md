## 1. Registry and example

- [x] 1.1 Extend `data/theatres/Nevada/airfields.yaml` to the eight curated keys
- [x] 1.2 Add `examples/groom_lake_cold_freeflight.yaml` (GroomLake, USA blue,
      Su-25T)

## 2. Infer and tools

- [x] 2.1 Extend `infer_theatre` to the new Nevada Spec keys
- [x] 2.2 Confirm `find_airfield` is theatre-scoped (GroomLake 2 ≠
      MountPleasant ≠ MervilleCalonne)

## 3. Tests and docs

- [x] 3.1 Registry tests: eight AFs; GroomLake 2 vs MountPleasant/Merville;
      Nellis 4 vs Maupertus/Dunkirk; `Groom_Lake` unknown
- [x] 3.2 Validate+compile Groom Lake contracts; invent still FF-only at Nellis
- [x] 3.3 Update BACKLOG F4b, README, LESSONS (`channel-ids`), matching skills
- [x] 3.4 `uv run ruff check` + `ruff format --check` + `uv run pytest -q`
