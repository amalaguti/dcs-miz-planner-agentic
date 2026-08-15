# DCS AI Mission Planner

Natural-language → validated Mission Spec → deterministic `.miz` compiler for DCS World.

**Principle:** the AI plans; software compiles. No LLM-authored DCS Lua.

## Status

Channel Spitfire MVP through M6: Mission Spec (`schema_version: "1"`, unknown fields
rejected) covers free_flight, intercept, CAP, ground_attack, escort, and recon, plus native ME
triggers (zones, flags, radio, late activation, sound, markers, altitude/speed gates).
Manston cold free flight was the first accepted-in-game slice. **Normandy 2.0** is
planner-bound for the same cold freeflight smoke at Needs Oar Point
(`examples/needs_oar_point_cold_freeflight.yaml`; Spec theatre id `Normandy`).
Invent/chat may use any offerable theatre; Normandy invent is **free_flight only**
until place recipes ship. Land/sea domain, intercept spawn, and Channel path clamp
fail closed or skip off TheChannel. Optional
`player.flight` (size 2–4, role lead|wingman) emits a multi-ship player section
(accepted ME 2026-08-07; `examples/manston_freeflight_flight_lead.yaml` /
`manston_freeflight_flight_wingman.yaml`; wingman `join_up` Follow/shared route
`#15c`, CAP example `manston_cap_flight_wingman.yaml`; optional `orders` F10
Section menus `#15d`, example `manston_cap_flight_orders.yaml`; optional
`discipline` fail-to-follow `#15e`, example `manston_cap_flight_discipline.yaml`). Optional Spec `failures`
(curated Spitfire ME Set Failure ids; example `manston_freeflight_magneto_failure.yaml`).
Channel DCS facts
(airfields, aircraft, radio, weather presets incl. `showers_scattered`) live in packaged YAML under
`src/dcs_miz_planner/data/` (`era/wwii/`, `shared/`, `theatres/<SpecId>/`). Commander briefs include an offline synthetic
METAR (`EGMH` + `RMK SIM` for TheChannel; other theatres omit a fake ICAO) from invent weather — never live meteo APIs.
Packaged tables are queried via `registry.py`. Local map
availability is cached in SQLite (`%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite`);
refresh with `dcs-miz theatres --refresh` (caches theatres **and** aircraft module
folders). Known agent catalog (`catalog_*` tables in the
same DB) syncs from packaged YAML + Spec enums via `dcs-miz catalog sync` (airfields,
aircraft, planning options, **strike/recon units**). Shared validation
(`dcs-miz validate` / compile) checks registry + local theatre inventory.
Manston compile structure is pinned by golden fixtures under `tests/fixtures/`
(refresh: `uv run python tests/refresh_manston_golden.py`; trigger-rich examples:
`uv run python tests/refresh_trigger_rich_goldens.py`). Intercept Spec
(`examples/manston_dawn_intercept.yaml`) places Bf-109K-4s on a Hawkinge/Dover
approach corridor. CAP Spec (`examples/manston_cap.yaml`) orbits a station SE of
Manston with engagement/ROE (accepted in-game 2026-08-01). Ground-attack Spec
(`examples/manston_ground_attack.yaml`) crosses the Channel with 2×250 lb + slipper
tank against enemy trucks inland near Dunkirk (accepted in-game 2026-08-02). Escort Spec
(`examples/manston_escort.yaml`) covers a Mosquito package SE of Manston with optional
Bf-109 bounce (accepted in-game 2026-08-02). Recon Spec (`examples/manston_recon.yaml`)
observes an AOI inland near Dunkirk with optional truck contacts (no bombs; find beat).
Surfaced U-boat mid-Channel pair: `examples/manston_uboat_recon.yaml` /
`manston_uboat_hunt.yaml` (locate then bomb while surfaced — not ASW; accepted ME
2026-08-08; patrol motion under way; accepted ME 2026-08-08). Soft truck convoy path:
`examples/manston_ground_attack_convoy.yaml` (Off Road + Disperse Under Fire +
`convoy_transit` AI; ME accepted 2026-08-08; airborne disperse do-soon). Emplaced
Flak alert: `examples/manston_ground_attack_flak_alert.yaml` (`aaa_alert`). Optional
target AI presets / `move_formation` (`#15h`; ME smoke do-soon).
Compile writes squadron-commander briefing text
into `.miz` `l10n` (Sortie / Description / Task; `dcs-miz compile --voice`; accepted in-game
2026-08-02). Weather presets: `sunny_clear`, `dawn_clear`, `marginal_vfr`, plus campaign-seeded
gallery patterns (`light_scattered_vfr`, `high_scattered`, `broken_channel`,
`overcast_low`, `rain_overcast`, `scattered_summer`, `sea_fog`; examples
`manston_broken_channel.yaml` / `manston_rain_overcast.yaml` /
`manston_dawn_fog_burnoff.yaml` with Spec `fog_dynamics`). Seeded Spec rerolls:
`dcs-miz randomize <spec> --seed N` (weather/time/geometry/opposition; same seed → same Spec).
Interactive multi-turn
chat (`dcs-miz chat`) plans Specs with `/accept` before write (accepted CLI 2026-08-01).
Opt-in CAP / intercept / escort / ground-attack narrative (`narrative.enabled`;
`examples/manston_cap_narrative.yaml`, `manston_dawn_intercept_narrative.yaml`,
`manston_escort_narrative.yaml`, `manston_ground_attack_narrative.yaml`) expands to
native ME triggers (accepted through GA 2026-08-04). Opt-in Spec `dynamics`
(`fixed`/`live`/`choose`/`hybrid` + pools; XOR with narrative) expands play-time
dice/F10/activate graphs (`examples/manston_dawn_intercept_dynamics_live.yaml`,
`manston_dawn_intercept_dynamics_hybrid.yaml`). F10 radio + late activation
(`examples/manston_dawn_intercept_radio.yaml`) for difficulty spawn options (accepted
in ME 2026-08-04). Curated `sound` + numeric flags
(`examples/manston_freeflight_sound_flags.yaml`; accepted in-game 2026-08-04).
Native Set Flag Random (`examples/manston_freeflight_flag_random.yaml`; 2026-08-05).
`group_life_less` partial-damage beats
(`examples/manston_ground_attack_life_less.yaml`; accepted in ME 2026-08-04).
`mark` / `smoke` zone markers
(`examples/manston_ground_attack_markers.yaml`; accepted in ME 2026-08-04).
Player altitude/speed gates with flag cooldown re-warn
(`examples/manston_freeflight_altitude_speed_gates.yaml`; accepted in ME 2026-08-04;
re-warn polish 2026-08-05). Trigger-rich examples above are also pinned by structural
goldens (not string-smoke only).
Agent capability catalog: `mission_behaviour` / `mission_inspiration` planning options,
mission-designer shelves (`dynamics_mode` → Spec `dynamics`, `strike_target_class`,
`channel_place` with Manston-relative geometry recipes and invent path clamp),
`research_guidance(focus=mission_design)`, and `list_installed_campaigns` (local
`Mods/campaigns` `.miz` / `.cmp` / Doc PDFs — filenames by default; opt-in
`include_doc_text` for short cached PDF excerpts) for creative planning inspiration.
Creative decisions persist in generation
`detail.creative`; feedback + history bias later invents.
Module map: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

**Intentional limits:** Channel theatre is the complete product surface today
(Normandy is a freeflight smoke). Multi-theatre catalog expand is queued as
backlog **M7** (`/full-catalog-orchestrate`); campaign `.miz` files are listed for
inspiration, not imported as Spec; stub LLM + offline research fixtures keep tests
hermetic.

**MVP acceptance:** Spitfire LF Mk IX, Channel map, cold start free flight at Manston, 09:00, sunny.
**Release:** **v0.3** is the pre–mission-designer baseline (immersion floor, R1/R2 audits,
`set_flag_random`, hermetic GitHub Actions CI). Designer shelves (`#30e`) and Spec
`dynamics` expand (`#30f`), Channel weather patterns (`#17a`), invent weather
jitter (`#17e`), re-weather overwrite (`#17d`), and mid-sortie fog dynamics
(`#17c` / `fog_dynamics` + `sea_fog` example) are done. Optional later: `#15a`
recon. `#22b` aircraft failures accepted (Failures panel; magneto example).
See [`docs/BACKLOG.md`](docs/BACKLOG.md).
## Stack

- Python 3.12 + uv
- Mission Spec (Pydantic) → shared validation → compiler via PyDCS (behind `CompilerInterface`)
- OpenSpec (`npx openspec`; npm `@fission-ai/openspec` — not `uv openspec`) for SDD
- GitHub Actions CI (Ubuntu): ruff + hermetic pytest on PR/push — no DCS install or Windows
  runner required (`tests/conftest.py` fake inventory; liveries stripped from goldens)
- Local pre-commit: blocks `master`/`main`; runs Ruff lint + format (`pre-commit install`)

## Validate and compile examples

```bash
uv sync
uv run dcs-miz validate examples/manston_cold_freeflight.yaml
uv run dcs-miz examples/manston_cold_freeflight.yaml
# -> out/manston_cold_freeflight.miz

uv run dcs-miz validate examples/manston_dawn_intercept.yaml
uv run dcs-miz examples/manston_dawn_intercept.yaml
# -> out/manston_dawn_intercept.miz

uv run dcs-miz validate examples/manston_cap.yaml
uv run dcs-miz examples/manston_cap.yaml
# -> out/manston_cap.miz

uv run dcs-miz validate examples/manston_ground_attack.yaml
uv run dcs-miz examples/manston_ground_attack.yaml
# -> out/manston_ground_attack.miz

uv run dcs-miz validate examples/manston_escort.yaml
uv run dcs-miz examples/manston_escort.yaml
# -> out/manston_escort.miz

uv run dcs-miz validate examples/manston_recon.yaml
uv run dcs-miz examples/manston_recon.yaml
# -> out/manston_recon.miz

uv run dcs-miz validate examples/manston_uboat_recon.yaml
uv run dcs-miz examples/manston_uboat_recon.yaml
# -> out/manston_uboat_recon.miz
uv run dcs-miz validate examples/manston_uboat_hunt.yaml
uv run dcs-miz examples/manston_uboat_hunt.yaml
# -> out/manston_uboat_hunt.miz

# Seeded reroll (same seed → same Spec), then compile:
uv run dcs-miz randomize examples/manston_cap.yaml --seed 42
uv run dcs-miz compile out/manston_cap_seed42.yaml -o out/manston_cap_seed42.miz

# Typed triggers (native ME emit):
uv run dcs-miz validate examples/manston_freeflight_trigger_sample.yaml
uv run dcs-miz compile examples/manston_freeflight_trigger_sample.yaml
# -> out/manston_freeflight_trigger_sample.miz  (message ~T+120 in Instant Action)

# Sound + numeric flags (beep ~T+10s + flag chain):
uv run dcs-miz validate examples/manston_freeflight_sound_flags.yaml
uv run dcs-miz compile examples/manston_freeflight_sound_flags.yaml
# -> out/manston_freeflight_sound_flags.miz

# Group life less (partial-damage beat on ground targets):
uv run dcs-miz validate examples/manston_ground_attack_life_less.yaml
uv run dcs-miz compile examples/manston_ground_attack_life_less.yaml
# -> out/manston_ground_attack_life_less.miz

# Mark + smoke on strike zone (~T+15s F10 mark + red smoke):
uv run dcs-miz validate examples/manston_ground_attack_markers.yaml
uv run dcs-miz compile examples/manston_ground_attack_markers.yaml
# -> out/manston_ground_attack_markers.miz

# Altitude + speed gates (continuous after T+30s; AGL + km/h):
uv run dcs-miz validate examples/manston_freeflight_altitude_speed_gates.yaml
uv run dcs-miz compile examples/manston_freeflight_altitude_speed_gates.yaml
# -> out/manston_freeflight_altitude_speed_gates.miz

# CAP with opt-in narrative (push / on-station / bandits-down→win):
uv run dcs-miz validate examples/manston_cap_narrative.yaml
uv run dcs-miz compile examples/manston_cap_narrative.yaml --voice raf
# -> out/manston_cap_narrative.miz

# Intercept with opt-in narrative (scramble / bandits-down→win):
uv run dcs-miz validate examples/manston_dawn_intercept_narrative.yaml
uv run dcs-miz compile examples/manston_dawn_intercept_narrative.yaml --voice raf
# -> out/manston_dawn_intercept_narrative.miz

# Escort with opt-in narrative (push / with-package / bounce-down→win):
uv run dcs-miz validate examples/manston_escort_narrative.yaml
uv run dcs-miz compile examples/manston_escort_narrative.yaml --voice raf
# -> out/manston_escort_narrative.miz

# Ground attack with opt-in narrative (push / ingress / targets-down→win):
uv run dcs-miz validate examples/manston_ground_attack_narrative.yaml
uv run dcs-miz compile examples/manston_ground_attack_narrative.yaml --voice raf
# -> out/manston_ground_attack_narrative.miz

# Intercept with live dynamics (raid die → late pools):
uv run dcs-miz validate examples/manston_dawn_intercept_dynamics_live.yaml
uv run dcs-miz compile examples/manston_dawn_intercept_dynamics_live.yaml
# -> out/manston_dawn_intercept_dynamics_live.miz

# Intercept with hybrid dynamics (F10 Auto + Easy/Medium/Hard):
uv run dcs-miz validate examples/manston_dawn_intercept_dynamics_hybrid.yaml
uv run dcs-miz compile examples/manston_dawn_intercept_dynamics_hybrid.yaml
# -> out/manston_dawn_intercept_dynamics_hybrid.miz
```
Open the result in the DCS Mission Editor, or copy it into
`Saved Games\DCS\Missions\` to fly it from Instant Action / Load Mission.

## List local theatres

```bash
uv run dcs-miz theatres                 # SQLite cache (scans once if empty)
uv run dcs-miz theatres --refresh       # rescan DCS install + update cache
uv run dcs-miz theatres --json          # machine-readable
uv run dcs-miz theatres --dcs-root "S:/DCS World"
```

Product theatre ids stay in YAML; the SQLite file is only a user-local install inventory.

## Agent catalog (known + discovery)

```bash
uv run dcs-miz catalog sync              # replace catalog_* from packaged YAML + Spec enums
uv run dcs-miz catalog list              # theatres: known vs installed vs offerable
uv run dcs-miz catalog list --known-only
uv run dcs-miz catalog list --type aircraft --json   # known + discovered folders (after --refresh)
uv run dcs-miz catalog list --type aircraft --known-only
uv run dcs-miz catalog list --type planning_options --json
uv run dcs-miz catalog list --type planning_options --family weather --support supported
uv run dcs-miz catalog list --type planning_options --family mission_behaviour --support supported
uv run dcs-miz catalog list --type planning_options --family mission_inspiration
uv run dcs-miz catalog list --type strike_units --json
```

To grow **known** entries: edit packaged YAML under `src/dcs_miz_planner/data/`
(`era/wwii/`, `shared/`, `theatres/<SpecId>/`) and Spec enums when needed, accept in DCS
when compile-supported, then `catalog sync`. Planning knobs live
in `planning_options.yaml` with support levels (`supported` / `advisory` / `future`), including
`mission_behaviour` (Spec recipes) and `mission_inspiration` (advisory patterns). Strike/recon
target units sync into `catalog_strike_units` from `ground_units.yaml` + `ships.yaml` (class
tags from `strike_target_class`). Deep
community/campaign `.miz` audits remain R1/R2; live research snippets and local campaign
`Doc/` listing are lighter inspiration channels.
Discovered install theatres are listed with `known=false` and are not auto-promoted.
Normandy (or other maps) is not required for the planning-option catalog.

## Agent tools (Python API)

Import from `dcs_miz_planner.tools` (no dedicated tools CLI — pytest is the acceptance path):

- `find_airfield(query)` / `get_aircraft_details(aircraft_id)` — known catalog
- `get_mission_spec_schema(mission_type)` — compact Spec example + notes (from `examples/`)
- `list_mission_options()` — Spec enums + enriched planning options + offerable theatres
  (includes `mission_behaviour` / `mission_inspiration` capability cards)
- `list_strike_targets(domain?, class_id?, q?)` — known land/sea strike units from SQLite
  (prefer before inventing GA/recon `targets[]`)
- `list_installed_campaigns(include_doc_text=False)` — local `Mods/campaigns` names,
  `.miz` files, `Doc/` PDFs (filenames by default; set `include_doc_text=true` for
  short excerpts cached by mtime/size). Inspiration only; no `.miz`→Spec import
- `get_user_prefs` / `set_user_prefs` / `list_generation_history` / `record_generation` /
  `record_feedback` — local user memory
- `research_guidance(query, …, focus=)` — tactics/procedures/history notes for commander
  briefs; `focus=mission_design` biases live search toward User Files / mission repos /
  ME patterns (offline fixtures by default; set `DCS_MIZ_RESEARCH_LIVE=1` or chat
  `/research` for best-effort web: DuckDuckGo Instant Answer, then HTML results;
  soft-fail warns and labels offline fixtures — research is never Spec/DCS-id authority)
- `validate_mission_spec(path)` / `compile_mission(path, output)` — wrap existing engines

Results are JSON-friendly dicts with an `ok` flag for later LLM tool calling.

## User prefs and history

Same SQLite file as install/catalog (`%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite`):

```bash
uv run dcs-miz prefs set preferred_airfield Manston
uv run dcs-miz prefs set squadron_voice raf   # raf | usaaf | neutral
uv run dcs-miz prefs list --json
uv run dcs-miz prefs history --json
uv run dcs-miz feedback --score 5 --note "good sortie"
```

The NL planner records generation history on success/failure; prefs are never wiped by
`catalog sync`.

## Plan a mission (natural language)

Offline stub (no API key — canned Manston free flight):

```bash
uv run dcs-miz plan "cold Spitfire free flight at Manston" --stub -o out/planned.yaml
uv run dcs-miz plan "..." --stub --voice usaaf --compile -o out/planned.yaml
```

### Interactive chat (multi-turn REPL)

```bash
uv run dcs-miz chat --stub --voice raf -o out/planned.yaml
# live: set OPENAI_API_KEY in .env (see .env.example) or in the shell, then:
# uv run dcs-miz chat --voice raf -o out/planned.yaml --compile
```

Slash commands: `/help`, `/quit`, `/show`, `/accept`, `/compile`, `/briefing`,
`/research [query]`, `/catalog`, `/voice`, `/prefs`, `/clear`, `/verbose on|off`. Spec YAML
is written only on `/accept` (not when the model merely prints JSON). `/research` prefers
live web (Instant Answer, then DuckDuckGo HTML results); on empty/error it prints a clear
warning and labels offline fixture fallback (sources still shown on each note).
**Verbose is off by default**; use `--verbose` or `/verbose on` for LLM rounds + tool
calls on stderr.

The planner speaks as a squadron commander (default **raf**; override with `--voice` or
pref `squadron_voice`). On success it prints a short commander brief: situation, tactics,
procedures, and watch-outs. Spec YAML stays plain machine fields.

Live (OpenAI-compatible):

```bash
# Option A: local .env (gitignored) — copy .env.example → .env and set OPENAI_API_KEY=
# Option B: PowerShell for this session
$env:OPENAI_API_KEY = "sk-..."
# optional: $env:DCS_MIZ_LLM_MODEL = "gpt-4o-mini"
# optional: $env:DCS_MIZ_RESEARCH_LIVE = "1"  # web-backed research_guidance
uv run dcs-miz plan "dawn intercept from Manston vs Bf-109s" -o out/planned.yaml --compile
```

The agent may call catalog tools, then writes Mission Spec YAML; `--compile` uses PyDCS.
Never put API keys in the repo or SQLite — use a local `.env` (gitignored) or the
environment; shell env wins over `.env`.
Dates should fit the history you want (WWII Channel content usually 1939–1945; modern
or other eras are allowed). A mismatched Channel date still succeeds but prints a
**Warning** on stderr.

## Setup notes

```bash
uv tool install pre-commit
pre-commit install
```

Agent work stays off `master`/`main` (Cursor hook + skill). Commits are also blocked there by pre-commit. Every commit runs Ruff (`ruff-check --fix` + `ruff-format`) via pre-commit.

## Docs

- Concept: [`DCS_AI_Mission_Planner.md`](DCS_AI_Mission_Planner.md)
- Architecture / module map: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- Theatre / target promote checklist: [`docs/THEATRE_TARGET_PROMOTE.md`](docs/THEATRE_TARGET_PROMOTE.md)
- Full-catalog campaign (multi-theatre): [`docs/BACKLOG.md`](docs/BACKLOG.md) M7;
  Agents Window: `/full-catalog-orchestrate` (skill
  `.cursor/skills/full-catalog-orchestrator/`)
- Roadmap / backlog: [`docs/BACKLOG.md`](docs/BACKLOG.md)
- Agent lessons index + topic files: [`docs/LESSONS_LEARNED.md`](docs/LESSONS_LEARNED.md)
  (skills: `dcs-dev-*` under `.cursor/skills/`)
- OpenSpec config: [`openspec/config.yaml`](openspec/config.yaml)
- Local research samples are gitignored (`research/`)
