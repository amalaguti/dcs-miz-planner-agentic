## 1. Registry countries and era

- [x] 1.1 Add `data/era/wwii/countries.yaml` with only `UK` and `ThirdReich` (Germany hint only, not a known id)
- [x] 1.2 Persist theatre→era from `theatre.yaml`; expose `era_for_theatre` / `list_countries` on the registry
- [x] 1.3 Wire `allowlists.KNOWN_COUNTRIES` and `catalog/sync` countries from the registry (drop hardcoded frozensets)

## 2. Domain and intercept

- [x] 2.1 Theatre-key domain classification; pass `theatre=spec.theatre` into `airdrome_id` from `airfield_relative_map_point`
- [x] 2.2 Validate/randomize: non-Channel Specs with strike/recon/path geometry fail `domain_unsupported_theatre` (do not run UK–FR chord)
- [x] 2.3 Intercept recipe table with only TheChannel Hawkinge `26989.935547`/`-29402.577148` + Dover `+4000`/`-6000`; validate + compile fail `intercept_unsupported_theatre` otherwise
- [x] 2.4 Keep join-up 120° as generic airfield-relative default

## 3. Path clamp, places, invent

- [x] 3.1 Skip path clamp and Channel harbour immersion unless `spec.theatre == TheChannel`
- [x] 3.2 Tag `channel_place` rows `meta.theatre: TheChannel` (do not rename family; no Normandy place rows)
- [x] 3.3 Unlock invent/prompts/schema for offerable theatres; Normandy free_flight from NeedsOarPoint example; combat types refuse with repair nudge
- [x] 3.4 `get_mission_spec_schema` optional `theatre=`: Normandy+free_flight → NeedsOarPoint envelope; Normandy+combat → no Manston skeleton
- [x] 3.5 Stub default stays Manston; optional test-only NeedsOarPoint JSON

## 4. Catalog, METAR, reweather, realism

- [x] 4.1 Catalog schema v5→v6; strike units `era_id=wwii` and `theatre_id=TheChannel`; `list_strike_targets(theatre="Normandy")` empty
- [x] 4.2 METAR ICAO `EGMH` only for TheChannel; Normandy briefs omit fake ICAO
- [x] 4.3 Miz-patch reweather fail-closed unless theatre is TheChannel
- [x] 4.4 WWII date realism from era map (applies to Normandy), not `if theatre != TheChannel: skip`

## 5. Tests and docs

- [x] 5.1 Add `tests/test_theatre_agnostic_planning.py` (or extend existing): domain/intercept fail-closed, clamp skip, countries set, strike tags, schema theatre=, METAR, miz-patch, realism
- [x] 5.2 Confirm Channel goldens including intercept (`x=30989.935547`, `y=-35402.577148`), `test_normandy_freeflight.py`, and Slice 0 package tests stay green
- [x] 5.3 Update README / ARCHITECTURE / BACKLOG F0b (`idea` → `building`) and lessons/skills for theatre-keyed helpers (no invented Normandy ids)

## 6. Merge gate

- [x] 6.1 `uv run ruff check src tests` and `uv run ruff format --check src tests`
- [x] 6.2 `uv run pytest -q`
- [x] 6.3 Compile `examples/manston_cold_freeflight.yaml` and `examples/needs_oar_point_cold_freeflight.yaml`
- [ ] 6.4 ME Instant Action on Channel Manston and Normandy Needs Oar Point (human do-soon after merge — not a merge blocker)
