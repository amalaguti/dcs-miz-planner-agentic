## 1. Registry, era, terrain

- [x] 1.1 Add `data/theatres/Falklands/theatre.yaml` (`id: Falklands`, `era: modern`) and `airfields.yaml` (`MountPleasant: 2` only). Comment PyDCS name `Mount Pleasant`. Do not dump all 27 fields. Spec key is `MountPleasant`, not `Mount_Pleasant`.
- [x] 1.2 Add `UK` to `data/era/modern/countries.yaml` alongside Georgia, Turkey, and USA. Keep UK in `era/wwii`. Reuse existing `Su-25T` @ 251.0. Do not add Spitfire to modern. Germany must not be a known id in any era.
- [x] 1.3 Bind `Falklands` → PyDCS `Falklands()` in `theatre_terrain.py`.
- [x] 1.4 Era-filter: Channel+UK still OK (wwii); Falklands+Spitfire or Falklands+USA fail; Channel+Su-25T still fail.

## 2. Example, invent, schema

- [x] 2.1 Add `examples/mount_pleasant_cold_freeflight.yaml`: theatre Falklands, 2024-06-06 09:00 `sunny_clear`, player `Su-25T` / `MountPleasant` / UK blue / Player / cold_parking.
- [x] 2.2 Schema: `theatre=Falklands` + free_flight → Mount Pleasant example; intercept/cap/GA/escort/recon raise with no Manston/NeedsOarPoint/Batumi/Incirlik/Nellis. Infer theatre from `Falklands` or airfield `MountPleasant`. Dedicated `_FALKLANDS_FF_NOTES` — do not concatenate `_COMMON_NOTES` / `_TYPE_NOTES`. Soft immersion floor stays TheChannel-only.
- [x] 2.3 Invent refuse every turn: TheChannel all six; Normandy FF+CAP; Caucasus/Syria/Nevada/Falklands FF only (CAP refused). Repair MUST use inferred theatre — do not hardcode Nevada/Syria/Caucasus/Normandy. Stub LLM stays Manston.
- [x] 2.4 Hermetic inventory: Falklands AVAILABLE + planner_supported=True. Retarget `test_unsupported_installed_map` onto Kola. N1 compile tests (`Su-25T`, airdromeId 2, start_time 32400, TakeOffParking, Player, frequency 251.0). Channel goldens unchanged. Strike `list_strike_targets(theatre="Falklands")` empty.

## 3. Docs

- [x] 3.1 BACKLOG F5 `idea` → `building`; README Status (Falklands Mount Pleasant FF; invent FF-only); fleet table planner smoke.
- [x] 3.2 Lessons + skills: MountPleasant=2 (not Mount_Pleasant); UK dual-era; Falklands invent FF only; schema notes must not concatenate Channel bundles.

## 4. Merge gate

- [x] 4.1 `uv run ruff check src tests` and `uv run ruff format --check src tests`
- [x] 4.2 `uv run pytest -q`
- [x] 4.3 Compile `examples/mount_pleasant_cold_freeflight.yaml`
- [ ] 4.4 ME Instant Action on Falklands Mount Pleasant (human do-soon after merge — not a merge blocker)
