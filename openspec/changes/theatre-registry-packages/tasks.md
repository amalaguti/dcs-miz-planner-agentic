## 1. Package YAML split

- [x] 1.1 Create `data/era/wwii/` and move `aircraft.yaml`, `aircraft_failures.yaml`, `payloads.yaml`, `ground_units.yaml`, `ships.yaml`, `target_motion.yaml` from `data/channel/` (ids unchanged)
- [x] 1.2 Create `data/shared/` and move entire `weather_presets.yaml`, `weather_gallery.yaml`, and `planning_options.yaml` from `data/channel/`
- [x] 1.3 Add `data/theatres/TheChannel/theatre.yaml` (`id: TheChannel`, `era: wwii`) and `airfields.yaml` with the 12 Channel keys only (Abbeville 1, MervilleCalonne 2, SaintOmer 3, Dunkirk 4, Manston 5, Hawkinge 6, Lympne 7, Detling 8, Eastchurch 10, HighHalden 12, Headcorn 13, BigginHill 14 — no ids 9 or 11)
- [x] 1.4 Add `data/theatres/Normandy/theatre.yaml` (`id: Normandy`, `era: wwii`) and `airfields.yaml` with `NeedsOarPoint: 28` only
- [x] 1.5 Delete `data/channel/` (`theatres.yaml`, combined `airfields.yaml`, `__init__.py`, leftover files)

## 2. Registry walker and scoped lookup

- [x] 2.1 Load era + shared + walk `theatres/*/theatre.yaml` via `resources.files("dcs_miz_planner.data")`; fail closed on missing `theatre.yaml`, `id` ≠ folder name, unknown `era`, duplicate name inside one theatre, empty airfields, non-mapping YAML
- [x] 2.2 Store airfields per theatre; add `airdrome_id(name, theatre=None)` (scoped map when theatre set; unique-name fallback when omitted; ambiguous name fails)
- [x] 2.3 Keep `ChannelRegistry` / `get_channel_registry()`; add `from_packaged_packages()`; alias `from_packaged_yaml()`; keep test constructor `airfields=` + optional `airfield_theatres=`
- [x] 2.4 Soften error text from `Unknown Channel airfield` to `Unknown airfield`; update tests that match the old string

## 3. Call sites

- [x] 3.1 Pass `spec.theatre` into airfield lookup from `validation.py` (player airfield + any airport resolve)
- [x] 3.2 Pass `spec.theatre` from `compiler/pydcs_compiler.py` player airport resolve
- [x] 3.3 Fix `reference.airdrome_id(theatre, name)` to use scoped lookup; drop or restrict unused flat `CHANNEL_AIRDROME_IDS`
- [x] 3.4 Point `target_motion.py` at `data/era/wwii/target_motion.yaml` and `weather_gallery.py` at `data/shared/weather_gallery.yaml`
- [x] 3.5 Leave catalog `SOURCE_LABEL` and strike-unit `theatre_id="TheChannel"` unchanged (Slice 0b)

## 4. Tests

- [x] 4.1 Extend `test_channel_registry.py` (or add `test_theatre_registry_packages.py`): scoped Manston/NeedsOarPoint cases; Channel keys exactly the 12 verified names; Normandy keys exactly `{NeedsOarPoint: 28}`; `sunny_clear` resolves with no Normandy weather file; loader has no `data.channel` package
- [x] 4.2 Add validation test: `theatre: Normandy` + `airfield: Manston` fails; `theatre: TheChannel` + `airfield: NeedsOarPoint` fails
- [x] 4.3 Confirm Channel goldens, `test_normandy_freeflight.py`, `test_theatre_terrain.py`, `test_catalog.py` Normandy rows, weather/shelf tests, and `_tiny_registry` catalog tests stay green

## 5. Docs

- [x] 5.1 Update README / ARCHITECTURE / BACKLOG F0 (`idea` → `building`) so SoT is packaged packages, not `data/channel/`
- [x] 5.2 Update `docs/lessons/channel-ids.md` and `.cursor/skills/dcs-dev-channel-ids/SKILL.md` for theatre-scoped lookup (replaces `airfield_theatres`)
- [x] 5.3 Fix leftover `data/channel/` path strings in weather / pydcs-compile / agent-tooling lessons if they would be wrong after the move

## 6. Merge gate

- [x] 6.1 `uv run ruff check src tests` and `uv run ruff format --check src tests`
- [x] 6.2 `uv run pytest -q`
- [x] 6.3 Compile `examples/manston_cold_freeflight.yaml` and `examples/needs_oar_point_cold_freeflight.yaml`
- [ ] 6.4 ME Instant Action on Channel Manston and Normandy Needs Oar Point (human do-soon after merge — not a merge blocker)
