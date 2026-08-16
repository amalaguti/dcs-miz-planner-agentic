## 1. Registry, era, terrain

- [x] 1.1 Add `data/theatres/Syria/theatre.yaml` (`id: Syria`, `era: modern`) and `airfields.yaml` (`Incirlik: 16` only). Comment PyDCS name Incirlik. Do not dump all 59 fields.
- [x] 1.2 Add `Turkey` to `data/era/modern/countries.yaml` alongside Georgia. Do not put Turkey in `era/wwii`. Reuse existing `Su-25T` @ 251.0. Germany must not be a known id in any era.
- [x] 1.3 Bind `Syria` → PyDCS `Syria()` in `theatre_terrain.py`.
- [x] 1.4 Era-filter stays in force: Channel+Turkey or Channel+Su-25T fail; Syria+UK or Syria+Spitfire fail; Caucasus+Georgia still ok.

## 2. Example, invent, schema

- [x] 2.1 Add `examples/incirlik_cold_freeflight.yaml`: theatre Syria, 2024-06-06 09:00 `sunny_clear`, player `Su-25T` / `Incirlik` / Turkey blue / Player / cold_parking.
- [x] 2.2 Schema: `theatre=Syria` + free_flight → Incirlik example; intercept/cap/GA/escort/recon raise with no Manston/NeedsOarPoint/Batumi. Infer theatre from `Syria` or airfield `Incirlik`. `_SCHEMA_THEATRES` includes Syria. Dedicated `_SYRIA_FF_NOTES` — do not concatenate `_COMMON_NOTES` / `_TYPE_NOTES`.
- [x] 2.3 Invent refuse every turn: TheChannel all six; Normandy FF+CAP; Caucasus FF only; Syria FF only (CAP refused). Repair of domain/intercept errors MUST use inferred theatre — do not hardcode Caucasus or Normandy onto Syria. Stub LLM stays Manston.
- [x] 2.4 Hermetic inventory: Syria AVAILABLE + planner_supported=True. Retarget `test_unsupported_installed_map` onto Nevada. N1 compile tests (`Su-25T`, airdromeId 16, start_time 32400, TakeOffParking, Player, frequency 251.0). Channel goldens unchanged. Strike `list_strike_targets(theatre="Syria")` empty.

## 3. Docs

- [x] 3.1 BACKLOG F3 `idea` → `building`; README Status (Syria Incirlik FF; invent FF-only); fleet table planner smoke.
- [x] 3.2 Lessons + skills: Incirlik=16; Turkey not USAF; Syria invent FF only; schema notes must not concatenate Channel bundles.

## 4. Merge gate

- [x] 4.1 `uv run ruff check src tests` and `uv run ruff format --check src tests`
- [x] 4.2 `uv run pytest -q`
- [x] 4.3 Compile `examples/incirlik_cold_freeflight.yaml`
- [ ] 4.4 ME Instant Action on Syria Incirlik (human do-soon after merge — not a merge blocker)
