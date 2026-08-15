## 1. Registry airfields and places

- [x] 1.1 Expand `data/theatres/Normandy/airfields.yaml` to the eight verified keys (`NeedsOarPoint=28`, `Chailey=27`, `Funtington=29`, `Tangmere=30`, `FordAF=31`, `Maupertus=4`, `SaintPierreduMont=1`, `Carpiquet=19`). Comment PyDCS names (`Ford_AF`, `Saint Pierre du Mont`). Do not invent ids or dump all 38 fields.
- [x] 1.2 Add `channel_place` rows `needs_oar_point_home` and `cherbourg_channel_cap` to `data/shared/planning_options.yaml` with `meta.theatre: Normandy`. CAP meta: bearing 180, distance 63 km, altitude 4000 m, domain sea, example `examples/needs_oar_point_cap.yaml`. Keep family `channel_place`. Do not edit leftover `data/channel/` if present.
- [x] 1.3 Update `test_normandy_airfields_exactly_needs_oar_point` to the exact eight-key map; assert `Maupertus` on Normandy is 4 and does not resolve on TheChannel.

## 2. CAP example and compile contracts

- [x] 2.1 Add `examples/needs_oar_point_cap.yaml`: theatre Normandy, 1944-06-06 09:00 `sunny_clear`, player `SpitfireLFMkIX` / `NeedsOarPoint` / UK blue / cold_parking, CAP 180/63/4000 circle weapons_free, two Average `Bf-109K-4` ThirdReich red, `objectives: [{type: patrol}]`.
- [x] 2.2 Add N1-style validate + compile contracts (extend `test_normandy_freeflight.py` or new test + `fixtures_support` helper): zip members, theatre `Normandy`, `airdromeId=28`, `SpitfireLFMkIX`, `Bf-109K-4`, start_time 32400, TakeOffParking, Player, frequencies 124.0 and 40.0, CAP Orbit Circle. No full golden dump. Channel CAP goldens unchanged.

## 3. Invent, schema, options filter

- [x] 3.1 Lift `host_normandy_combat_nudge` for CAP only (drop CAP from `_NORMANDY_COMBAT_TYPES`). Intercept / GA / escort / recon stay every-turn refuse; never capture or write refused drafts. Update prompt/nudge copy.
- [x] 3.2 Schema: `build_spec_schema("cap", theatre="Normandy")` loads the new example; intercept/GA/escort/recon still raise with no Manston skeleton. Update `SPEC_SHAPE_REMINDER` / notes / `tool_bridge` schema text. Stub LLM stays Manston.
- [x] 3.3 `list_mission_options(*, theatre=)` filters `channel_place` by `meta.theatre`. Other families pass through. Omitted theatre returns all. Wire the optional arg on the agent tool.
- [x] 3.4 Flip 0b tests that used Normandy CAP JSON as the refused type over to intercept. Add positives: CAP nudge is None; chat/planner may capture/write CAP; `list_mission_options(theatre=)` place filter; Channel `channel_place` rows stay TheChannel.

## 4. Docs

- [x] 4.1 BACKLOG F1 `idea` → `building`; README Status (Normandy CAP invent); ARCHITECTURE if the options-filter API is worth a line.
- [x] 4.2 Lessons + skills: CAP invent allowed; still no Channel geometry copy; Spec key `FordAF` for PyDCS `Ford_AF`; intercept/domain still fail-closed.

## 5. Merge gate

- [x] 5.1 `uv run ruff check src tests` and `uv run ruff format --check src tests`
- [x] 5.2 `uv run pytest -q`
- [x] 5.3 Compile `examples/needs_oar_point_cap.yaml` (and keep Needs Oar Point free-flight compiling)
- [ ] 5.4 ME Instant Action on Normandy Needs Oar Point CAP (human do-soon after merge — not a merge blocker)
