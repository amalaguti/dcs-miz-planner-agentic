## 1. Registry, era, terrain

- [x] 1.1 Add `data/theatres/Nevada/theatre.yaml` (`id: Nevada`, `era: modern`) and `airfields.yaml` (`Nellis: 4` only). Comment PyDCS name Nellis. Do not dump all 17 fields.
- [x] 1.2 Add `USA` to `data/era/modern/countries.yaml` alongside Georgia and Turkey. Do not put USA in `era/wwii`. `usaaf` is not a country. Reuse existing `Su-25T` @ 251.0. Germany must not be a known id in any era.
- [x] 1.3 Bind `Nevada` → PyDCS `Nevada()` in `theatre_terrain.py`.
- [x] 1.4 Era-filter stays in force: Channel+USA or Channel+Su-25T fail; Nevada+UK or Nevada+Spitfire fail; Caucasus+Georgia and Syria+Turkey still ok.

## 2. Example, invent, schema

- [x] 2.1 Add `examples/nellis_cold_freeflight.yaml`: theatre Nevada, 2024-06-06 09:00 `sunny_clear`, player `Su-25T` / `Nellis` / USA blue / Player / cold_parking.
- [x] 2.2 Schema: `theatre=Nevada` + free_flight → Nellis example; intercept/cap/GA/escort/recon raise with no Manston/NeedsOarPoint/Batumi/Incirlik. Infer theatre from `Nevada` or airfield `Nellis`. `_SCHEMA_THEATRES` includes Nevada. Dedicated `_NEVADA_FF_NOTES` — do not concatenate `_COMMON_NOTES` / `_TYPE_NOTES`. Soft immersion floor stays TheChannel-only.
- [x] 2.3 Invent refuse every turn: TheChannel all six; Normandy FF+CAP; Caucasus/Syria/Nevada FF only (CAP refused). Repair of domain/intercept errors MUST use inferred theatre — do not hardcode Syria/Caucasus/Normandy onto Nevada. Stub LLM stays Manston.
- [x] 2.4 Hermetic inventory: Nevada AVAILABLE + planner_supported=True. Retarget `test_unsupported_installed_map` onto Falklands. N1 compile tests (`Su-25T`, airdromeId 4, start_time 32400, TakeOffParking, Player, frequency 251.0). Channel goldens unchanged. Strike `list_strike_targets(theatre="Nevada")` empty.

## 3. Docs

- [x] 3.1 BACKLOG F4 `idea` → `building`; README Status (Nevada Nellis FF; invent FF-only); fleet table planner smoke.
- [x] 3.2 Lessons + skills: Nellis=4; USA not usaaf; Nevada invent FF only; schema notes must not concatenate Channel bundles.

## 4. Merge gate

- [x] 4.1 `uv run ruff check src tests` and `uv run ruff format --check src tests`
- [x] 4.2 `uv run pytest -q`
- [x] 4.3 Compile `examples/nellis_cold_freeflight.yaml`
- [ ] 4.4 ME Instant Action on Nevada Nellis (human do-soon after merge — not a merge blocker)
