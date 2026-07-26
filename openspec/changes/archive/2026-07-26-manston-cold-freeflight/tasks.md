## 1. Python project skeleton

- [x] 1.1 Initialize uv Python project with `requires-python = ">=3.12,<3.14"` and package layout under `src/`
- [x] 1.2 Add runtime dependency on PyDCS; add `out/` to `.gitignore`
- [x] 1.3 Add minimal package modules: models, compiler interface, CLI entrypoint stubs

## 2. Mission Spec (free flight)

- [x] 2.1 Implement Pydantic Mission Spec models for free-flight fields (theatre, date, start_time, weather preset, player)
- [x] 2.2 Add checked-in example `examples/manston_cold_freeflight.yaml` (TheChannel, SpitfireLFMkIX, Manston, cold parking, 09:00, sunny_clear)
- [x] 2.3 Load/validate the example YAML into the Mission Spec model via a small helper or CLI path

## 3. Miz compiler (PyDCS)

- [x] 3.1 Implement `CompilerInterface` and a PyDCS-backed compiler that maps Manston → airdromeId 5
- [x] 3.2 Place player as cold parking (`TakeOffParking` / From Parking Area), skill Player, type SpitfireLFMkIX on TheChannel
- [x] 3.3 Apply start_time 32400 and `sunny_clear` weather mapping
- [x] 3.4 Write `.miz` to `out/` and assert zip contains `mission`, `options`, `theatre`, `warehouses`

## 4. CLI and docs

- [x] 4.1 Wire CLI command to compile a Mission Spec path to `out/*.miz`
- [x] 4.2 Update README with how to install deps, compile the Manston example, and open the `.miz` in DCS
- [x] 4.3 Mark `manston-cold-freeflight` as building/done in `docs/BACKLOG.md` when appropriate

## 5. Acceptance

- [x] 5.1 Manually open compiled `.miz` in DCS Mission Editor / Instant Action and confirm cold Spitfire at Manston ~09:00 clear weather
  - Accepted 2026-07-26: opens in the Mission Editor and flies after the radio fix below. Also reproduced manually in the ME (WWII coalitions + Channel) as a reference build.
- [x] 5.2 Record any PyDCS/parking/weather tweaks needed; keep Mission Spec public API stable
  - Radio: PyDCS's 251 MHz default is out of the Spitfire's VHF band and DCS rejects it on launch. Group frequency now comes from `AIRCRAFT_RADIO_MHZ` (Spitfire 124, per stock ED missions). See `docs/LESSONS_LEARNED.md`.
