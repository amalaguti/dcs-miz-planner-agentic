# Full-catalog resource taxonomy and gaps

Process checklist remains [`docs/THEATRE_TARGET_PROMOTE.md`](../../../docs/THEATRE_TARGET_PROMOTE.md).
This file is the orchestrator’s capture list and Channel-hardcode watchlist.

## Resource taxonomy

Curate into packaged YAML; never scrape ME trees. CLI `dcs-miz catalog list --type`
today: theatres, airfields, aircraft, weather, payloads, planning_options,
strike_units, mission_types, start_types, coalitions, objective_types, countries.
Capture the kinds below even if they stay grouped under planning_options.

### Must capture per theatre (cannot plan without)

| Kind | Channel today |
|------|----------------|
| Theatre id + PyDCS terrain bind | `TheChannel`, `Normandy` |
| Airfields (name → airdromeId) | 12 Channel + NeedsOarPoint |
| Countries (PyDCS class names) | `UK`, `ThirdReich` from `era/wwii/countries.yaml` |
| Coalitions | blue/red |
| Aircraft + group radio MHz | 5 WWII types |
| Start types | cold parking |
| Weather presets + CloudPreset ids | Channel climatology |
| Time of day | planning family |
| Places / geometry recipes | `channel_place` |
| Land/sea domain clamp | Channel UK–FR chord |

### Stage C/D (Channel-complete, not first smoke)

Ground units, ships, payloads (CLSID+pylon), strike classes + motion + AI
presets, player-flight knobs (generic; parking is per-AF), ROE / opposition /
behaviour / inspiration / dynamics, aircraft failures, curated sounds, example
Specs + goldens, Assets-pack honesty.

### Only when the map has them

Helicopters; FARPs / oil rigs / carriers as spawn; tankers / AWACS / SEAD / SAM;
statics (`#17b`, usually later); artillery class; theatre-specific weather
(dust, etc.); parking geometry from stock `.miz` / PyDCS — not invented lat/lon.
ATC freqs are **not** flight radio.

### Discovery-only (never YAML-promote)

Installed aircraft module folders; campaigns / Doc PDFs (inspiration);
disabled terrains or terrains without PyDCS modules.

## Capability gaps (Slice 0b)

Spec geometry is already airfield-relative. These helpers are Channel-hardcoded:

| Gap | Where |
|-----|--------|
| Invent locked to Channel | `agent/prompts.py`, `agent/spec_schema.py` |
| Countries WWII-only | `allowlists.py`, `catalog/sync.py`, `models.py` defaults |
| Domain classifier always TheChannel | `channel_domain.py`; validation still calls it |
| Path clamp one Channel place | `agent/path_clamp.py` `french_coast_strike_belt` |
| Intercept spawn Hawkinge/Dover | `compiler/pydcs_compiler.py` `_HAWKINGE_*` |
| Join-up outbound 120° | same compiler |
| Strike units tagged Channel | `catalog/sync.py` |
| Places family `channel_place` | planning_options |
| Reweather / METAR Channel | `reweather.py`, `weather_metar.py` `EGMH` |
| Era warnings Channel-only | `agent/realism.py` |
| Stub LLM always Manston | `agent/llm.py` |
| Hermetic inventory Channel+Normandy | `tests/conftest.py` |
| Payloads / failures Spitfire-only | `data/era/wwii/payloads.yaml`, `aircraft_failures.yaml` |

## Hard ceiling

- No PyDCS terrain → cannot compile (`MarianaIslandsWWII`, `Kola`, `Iraq` as of R11).
- Player spawn is airfield-only (no FARP/carrier/helipad in Spec).
- No first-class modern mission types (AAR, SEAD, FAC, helo CAS, carrier recovery).

## Already generic (do not rebuild)

Spec `schema_version: "1"`; validate/compile pipeline; catalog join
`known ∧ available ∧ planner_supported`; native ME triggers; player.flight;
install probe without auto-promote.
