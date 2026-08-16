## 1. Registry, era, terrain

- [x] 1.1 Add `_KNOWN_ERAS` value `modern`. Walk `data/era/<era>/` for `countries.yaml` + `aircraft.yaml` (era-keyed). Leave wwii payloads/ground/ships/failures paths unchanged. Do not put Georgia or Su-25T in `era/wwii`.
- [x] 1.2 Add `data/era/modern/countries.yaml` (`Georgia` only) and `data/era/modern/aircraft.yaml` (`Su-25T` radio 251.0). Germany must not be a known id in any era.
- [x] 1.3 Add `data/theatres/Caucasus/theatre.yaml` (`id: Caucasus`, `era: modern`) and `airfields.yaml` (`Batumi: 22` only). Comment PyDCS name Batumi.
- [x] 1.4 Bind `Caucasus` → PyDCS `Caucasus()` in `theatre_terrain.py`.
- [x] 1.5 Era-filter `known_countries` / known aircraft in allowlists + validation via `era_for_theatre(spec.theatre)`. Channel+Georgia or Channel+Su-25T fail; Caucasus+UK or Caucasus+Spitfire fail.

## 2. Example, invent, schema

- [x] 2.1 Add `examples/batumi_cold_freeflight.yaml`: theatre Caucasus, 2024-06-06 09:00 `sunny_clear`, player `Su-25T` / `Batumi` / Georgia blue / Player / cold_parking.
- [x] 2.2 Schema: `theatre=Caucasus` + free_flight → Batumi example; intercept/cap/GA/escort/recon raise with no Manston/NeedsOarPoint. Infer theatre from `Caucasus` or airfield `Batumi`. `_SCHEMA_THEATRES` includes Caucasus.
- [x] 2.3 Generalize combat invent refuse (every turn): TheChannel all six; Normandy FF+CAP; Caucasus FF only (CAP refused). Repair of domain/intercept errors MUST use inferred theatre — do not hardcode Normandy onto Caucasus. Stub LLM stays Manston.
- [x] 2.4 Hermetic inventory + N1 compile tests (`Su-25T`, airdromeId 22, start_time 32400, TakeOffParking, Player, frequency 251.0). Channel goldens unchanged. Strike `list_strike_targets(theatre="Caucasus")` empty.

## 3. Docs

- [x] 3.1 BACKLOG F2 `idea` → `building`; README Status (Caucasus Batumi FF; invent FF-only); fleet table planner smoke.
- [x] 3.2 Lessons + skills: modern era; Batumi=22; Su-25T 251 UHF; Georgia not USAF; era-filter validate; Caucasus invent FF only.

## 4. Merge gate

- [x] 4.1 `uv run ruff check src tests` and `uv run ruff format --check src tests`
- [x] 4.2 `uv run pytest -q`
- [x] 4.3 Compile `examples/batumi_cold_freeflight.yaml`
- [ ] 4.4 ME Instant Action on Caucasus Batumi (human do-soon after merge — not a merge blocker)
