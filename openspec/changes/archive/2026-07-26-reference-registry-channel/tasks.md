## 1. Registry data & API

- [x] 1.1 Add packaged YAML under `src/dcs_miz_planner/data/channel/` (airfields, aircraft+radio, weather presets; optional empty/minimal payloads)
- [x] 1.2 Implement Channel registry loader (`importlib.resources`) and lookup API (airdrome id, aircraft/radio, theatre, weather preset, list helpers)
- [x] 1.3 Keep or thin `reference.py` as a compatibility façade over the registry
- [x] 1.4 Unit tests: Manston=5, Spitfire 124 MHz, unknown airfield error, `TheChannel` supported

## 2. Compiler wiring

- [x] 2.1 Switch `PyDCSCompiler` to resolve theatre/aircraft/airfield/radio via the registry API
- [x] 2.2 Confirm PyDCS payload-scan disable remains in place (no install payload harvest)
- [x] 2.3 Existing Manston compile tests still pass; compile example to `out/`

## 3. Docs & acceptance

- [x] 3.1 Update `docs/BACKLOG.md`: item `building` while applying; settle “YAML not SQLite” in pending decisions
- [x] 3.2 Brief README note if registry path becomes user-visible (keep README short)
- [x] 3.3 Human acceptance: open compiled Manston `.miz` in DCS Mission Editor / Instant Action (accepted in-game 2026-07-26)
