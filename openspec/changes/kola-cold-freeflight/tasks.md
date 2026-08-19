## 1. Registry, era, terrain

- [x] 1.1 Add `data/theatres/Kola/theatre.yaml` (`id: Kola`, `era: modern`) and `airfields.yaml` (`Bodo: 7` only). Comment PyDCS name `Bodo`. Do not dump all 37 fields.
- [x] 1.2 Add `Norway` to `data/era/modern/countries.yaml`. Do not add Norway to `era/wwii`. Reuse existing `Su-25T` @ 251.0. Germany must not be a known id in any era.
- [x] 1.3 Bind `Kola` → PyDCS `Kola()` in `theatre_terrain.py`.
- [x] 1.4 Era-filter: Channel+Norway fails; Kola+Norway+Su-25T ok; Channel+UK still OK; Channel+Su-25T still fails. Spitfire dual-era stays.

## 2. Example, invent, schema

- [x] 2.1 Add `examples/bodo_cold_freeflight.yaml`: theatre Kola, 2024-06-06 09:00 `sunny_clear`, player `Su-25T` / `Bodo` / Norway blue / Player / cold_parking.
- [x] 2.2 Schema: `theatre=Kola` + free_flight → Bodo example; intercept/cap/GA/escort/recon raise with no prior-map skeleton. Infer theatre from `Kola` or airfield `Bodo`. Dedicated `_KOLA_FF_NOTES` — do not concatenate `_COMMON_NOTES` / `_TYPE_NOTES`. Soft immersion floor stays TheChannel-only.
- [x] 2.3 Invent refuse every turn: existing maps unchanged; Kola FF only (CAP refused). Repair MUST use inferred theatre — do not hardcode Falklands/Nevada/Syria onto Kola. Stub LLM stays Manston.
- [x] 2.4 Hermetic inventory: Kola AVAILABLE + planner_supported=True. Retarget `test_unsupported_installed_map` onto Iraq. Retarget compile-without-binding onto Iraq. Retarget “exists in pydcs but unbound” onto GermanyCW. Retarget domain/intercept `theatre=` copies onto Iraq. N1 compile tests (`Su-25T`, airdromeId 7, start_time 32400, TakeOffParking, Player, frequency 251.0). Channel goldens unchanged. Strike `list_strike_targets(theatre="Kola")` empty of dual-offered trucks.

## 3. Docs

- [x] 3.1 BACKLOG F6 `kola-cold-freeflight` `building` → (done at finish); README Status (Kola Bodo FF; invent FF-only); fleet table planner smoke.
- [x] 3.2 Lessons + skills: Bodo=7; Norway modern-only; Kola invent FF only; unbound stand-in is Iraq / GermanyCW; schema notes must not concatenate Channel bundles. Orchestrator: Kola Stage A bound.

## 4. Merge gate

- [x] 4.1 `uv run ruff check src tests` and `uv run ruff format --check src tests`
- [x] 4.2 `uv run pytest -q`
- [x] 4.3 Compile `examples/bodo_cold_freeflight.yaml`
- [ ] 4.4 ME Instant Action on Kola Bodo (human do-soon after merge — not a merge blocker)
