# Backlog & Roadmap

Ordered candidate work. One item is promoted to an OpenSpec change at a time.

**Item names are the OpenSpec change name** (and therefore the git branch name).

Status: `idea` → `proposed` (OpenSpec change exists) → `building` → `done` (archived)

Rule: only **one** item in `building` unless items are genuinely independent.

---

## M0 — Foundations ✅ done

Toolchain (Python 3.12, Git, Node LTS, uv, pre-commit), GitHub repo, OpenSpec init,
Cursor hooks + skills (branch protection, README upkeep), research on `.miz` internals.

Research record: `research/FINDINGS.md` (gitignored, local only).

---

## M1 — First playable `.miz`

The whole point of M1: prove the pipeline end-to-end on the simplest possible mission.

| # | Item | Goal | Status |
|---|------|------|--------|
| 1 | `manston-cold-freeflight` | Spitfire cold on Manston parking, 09:00, sunny, Channel — compiles and loads in DCS | `done` (accepted in-game 2026-07-26) |

Scope note: intentionally folds the `uv` project skeleton, a minimal Mission Spec, and the
PyDCS compile path into one vertical slice. Split only if the proposal gets fat.

**Exit criteria:** a spec file in the repo compiles to a `.miz` that opens in the DCS Mission
Editor and is flyable, reproducibly, from a single command.

---

## M2 — Harden the contract and data

**Next promote / in proposal:** (see M6 — prefer `trigger-model-spec`)

| # | Item | Goal | Status |
|---|------|------|--------|
| 2 | `mission-spec-schema` | Formalize Mission Spec (free flight + extension points for combat) | `done` (accepted in-game 2026-07-26) |
| 7 | `dev-module-map` | Checked-in architecture diagram + short module relationship doc (`docs/ARCHITECTURE.md`); refreshed manually, push hook reminds when `src/` changes | `done` (2026-07-26) |
| 3 | `reference-registry-channel` | Queryable Channel registry (YAML tables + Python API as product SoT; SQLite reserved for user-local install cache in `#4`): airfields, aircraft, weather presets, payload CLSIDs | `done` (accepted in-game 2026-07-26) |
| 4 | `installed-theatres-probe` | User-local SQLite install inventory (install/remove + enable/disable); refresh on demand; YAML registry stays product SoT; only offer maps both available and planner-supported | `done` (CLI accepted 2026-07-26; registry Path discovery) |
| 5 | `validation-engine` | Structural + DCS-exists + semantic validation with clear errors (shared API + `dcs-miz validate`; compile uses same engine) | `done` (accepted in-game 2026-07-26) |
| 6 | `golden-fixtures-tests` | pytest regression: spec → `.miz` structural asserts | `done` (accepted 2026-07-26; suite green) |

---

## M3 — Agent layer

The AI arrives only once compilation is trustworthy.

**Catalog & memory direction:** agent-facing lookups prefer a **local SQLite catalog**
(synced from YAML registry + Spec enums + install inventory — not a second DCS-id SoT).
Same DB family may hold **user preferences**, **generation history**, and **satisfaction /
feedback** so the agent can learn tastes over time. Compile/validate still use registry + Spec.

| # | Item | Goal | Status |
|---|------|------|--------|
| 8 | `agent-tools-surface` | Tools: `find_airfield`, `get_aircraft_details`, `list_mission_options`, `validate_mission_spec`, `compile_mission` (query catalog SQLite where appropriate; validate/compile stay registry-backed) | `done` (API/CLI accepted 2026-08-01) |
| 9 | `mission-option-catalog` | Enumerate planning knobs the agent can ask about / suggest (start type, weather, time, opposition density, ROE seeds, payload families); load into SQLite catalog for list/ask | `done` (catalog/tool accepted 2026-08-01; Normandy not required) |
| 8a | `agent-catalog-sqlite` | Sync YAML registry + mission types/options into queryable SQLite tables for agent/UI; keep install inventory schema distinct (`catalog_*` vs install tables); theatre discovery join; aircraft module harvest deferred | `done` (CLI accepted 2026-07-26) |
| 8a.1 | `catalog-discover-modules` | Optional: harvest installed aircraft modules for discovery-only listing (never auto-promote into known YAML) | `done` (2026-08-05; cache on theatres --refresh) |
| 8a.2 | `install-maintenance-slash` | Host `/maintenance` (or extend `/catalog`): read-only install summary (scan time, theatres, known aircraft installed/missing, discovered-only folders); optional refresh. Not default LLM invent tools — slash/CLI only | `idea` (parked 2026-08-05) |
| 8c | `agent-strike-target-catalog` | **Prebuilt** SQLite catalog of Channel strike/recon **unit targets** (land + sea) for agent suggestion — sync from registry YAML (`ground_units.yaml` + `ships.yaml`) at `dcs-miz catalog sync` time (same async path as `#8a`/`#9`); agent **queries SQLite only** during invent/chat (never scan YAML/PyDCS mid-turn). Tool e.g. `list_strike_targets(domain?, class?, q?)` → exact DCS ids + labels + domain for recon contacts / GA targets. Join or tag with `strike_target_class` / `channel_place` shelves. Compile/validate stay registry SoT. Pairs with `#15a`/`#15f` so “search/recon” can recommend e.g. `Uboat_VIIC`. Feeds **`#8d`** invent heuristics. | `done` (CLI/API accepted 2026-08-08; ME not required) |
| 8d | `agent-target-option-heuristics` | Make invent/chat **smart at picking targets + motion + `#15h` AI presets** from pilot intent (not free-form Opt*). Decision table / tool guidance: place (`channel_place`) × class (`strike_target_class`) × ask type (convoy / flak / U-boat / harbour) → unit ids (via `#8c`), `motion`, `ai_preset` / `move_formation`. Enrich planning_options + prompts/schema so the model calls catalog tools then emits only allowlisted fields. Optional: few-shot invent tests (“truck column inland” → Blitz + path + `convoy_transit`). **Depends on** `#15h` shelf + preferably `#8c` query tool. **Non-goals:** dumping ME Options; inventing DCS ids; learning from flight telemetry. | `done` (CLI/API accepted 2026-08-08; no ME) |
| 8e | `theatre-target-promote-checklist` | Durable **human/agent checklist** for adding a new theatre slice and/or expanding strike/recon target shelves (not auto-scrape). See [`docs/THEATRE_TARGET_PROMOTE.md`](THEATRE_TARGET_PROMOTE.md). Feeds R11 + registry growth after `#8d`/`#8g`. | `done` (docs 2026-08-08) |
| 8h | `channel-unit-shelf-expand` | First curated Channel strike/recon **unit shelf expand** (soft + AAA + harbour/coastal sea) following `#8e` checklist — verified PyDCS ids only; class shelves + motion + AAA AI allowlist; examples. **Non-goals:** armor/troops/radar classes; ME scrape. | `done` (CLI/API 2026-08-08; ME do-soon) |
| 8i | `channel-shelf-halftracks` | Promote **halftracks_apc** class + verified ids (`Sd_Kfz_251`, `Sd_Kfz_7`, `M2A1_halftrack`) per `#8e`: YAML, class shelf, motion halftrack band, invent cues, example. Reuses convoy_transit (soft AI). | `done` (CLI/API 2026-08-08; ME do-soon) |
| 8j | `channel-shelf-armor` | Promote **armor** class + verified AFVs (`Pz_IV_H`, `Stug_III`, `Cromwell_IV`, `M4_Sherman`) per `#8e`. Reuses convoy_transit (soft AI); motion armor band; invent cues; example GA. | `done` (CLI/API 2026-08-08; ME do-soon) |
| 8k | `channel-shelf-troops` | Promote **troops** class + verified WWII infantry (`soldier_mauser98`, `soldier_wwii_br_01`, `soldier_wwii_us`) per `#8e`. Troops motion band; invent cues; example GA. Reuses convoy_transit. | `done` (CLI/API 2026-08-08; ME do-soon) |
| 8l | `channel-shelf-radar-c3` | Promote **radar_c3** static shelf (`FuMG-401`, `FuSe-65`) per `#8e` — emplaced only; invent cues for radar/C3 hunts. Soft AI (not aaa_alert). | `done` (CLI/API 2026-08-08; ME do-soon) |
| 8m | `channel-shelf-trains` | Promote **trains** class + verified loco/wagons (`Locomotive`, `German_covered_wagon_G10`, `German_tank_wagon`, `DR_50Ton_Flat_Wagon`) + curated `french_coast_rail_corridor` place (path deltas only; **no** rail-mesh snap) per `#8e` / `#15g`. | `done` (CLI/API 2026-08-08; ME do-soon) |

| 8f | `agent-channel-geometry-invent` | Fix invent **placement**: `channel_place` numeric recipes (bearing/distance bands from Manston examples), path/patrol domain coherence, stronger validation **repair nudges** for `motion_domain_mismatch` / `strike_domain_mismatch`. Live invent eval 2026-08-08: unit/preset cues OK; inland convoy paths over water, harbour ~4 km from Manston, U-boat GA domain fails. **Before** shelf expand. | `done` (CLI/API 2026-08-08; live invent re-eval optional) |
| 8g | `agent-invent-path-harbour-harden` | After `#8f`: harden **land path invent** (short strike-relative path deltas + optional host clamp on invent validate) and **harbour→sea unit** binding (guidance + repair; no unit auto-swap). Live gaps: convoy path points over water; harbour coastal geometry with land trucks. **Before** `#8e` shelf expand. | `done` (CLI/API live invent 6/6 2026-08-08) |
| 8b | `user-prefs-and-history` | Store user preferences, mission-generation history (Spec path, outcome), and post-flight / post-gen satisfaction surveys; agent tools to read prefs and record feedback | `done` (CLI/API accepted 2026-08-01) |
| 10 | `nl-to-spec-agent` | Natural language → Mission Spec via structured outputs + tool calling (uses catalog + prefs/history tools) | `done` (stub Spec accepted 2026-08-01; live needs OPENAI_API_KEY) |
| 10a | `interactive-plan-repl` | Multi-turn CLI chat/REPL to plan missions interactively from scratch (stdin/stdout; explicit Spec accept) | `done` (CLI accepted 2026-08-01; CAP Spec via chat) |
| 10b | `agent-verbose-default-off` | After product polish: default agent `verbose` **off** (quiet CLI); keep `--verbose` / `/verbose on` for debugging | `done` (2026-08-05) |
| 10c | `agent-spec-schema-tool` | Derived Mission Spec shape for the agent (tool + prompt fragment); stop hand-maintaining JSON skeletons as mission types grow | `done` (CLI/API accepted 2026-08-01) |
| 10d | `fix-chat-research-live` | Make `/research` (and `research_guidance`) actually return useful live web notes; today live often yields nothing and silently falls back to fixtures | `done` (pytest/API 2026-08-02; Instant Answer + HTML cascade; clear soft-fail label) |
| 11 | `squadron-commander-voice` | Agent persona: USAAF or RAF squadron commander tone for questions, guidance, and briefings (configurable; may follow prefs); tactics/procedures/watch-outs brief + optional research | `done` (CLI/API accepted 2026-08-01) |

**`#10d` `fix-chat-research-live` — notes (resolved 2026-08-02):**

Live chat used to print fixture-only notes that looked like a successful web lookup when
DuckDuckGo Instant Answer returned empty JSON for multi-word queries. Fixed by cascading
to DuckDuckGo HTML results, enriching the query with Spec context, and labeling
`/research` output as offline fixture fallback whenever live returns empty/error.

**`#8c` `agent-strike-target-catalog` — draft (2026-08-07, categories 2026-08-08):**

Today the agent only *indirectly* sees target ids via `planning_options` meta on
`strike_target_class` (e.g. `sea_craft.ship_ids`) after catalog sync — incomplete for
recon contact suggestion, easy to miss, and not a queryable unit table. Registry already
has the SoT (`get_strike_unit` / `list_strike_units`); compile must keep using registry.

**Category spine (plan motion + invent around these; expand registry over time):**

| Class id (proposed) | Domain | Motion default | Registry today | Next / candidates |
|---------------------|--------|----------------|----------------|-------------------|
| `soft_vehicles` | land | path / patrol | Blitz, Kubel, Bedford, Sd_Kfz_2, Horch, Willys (`#8h`) | more soft as needed |
| `halftracks_apc` | land | path / patrol | Sd_Kfz_251, Sd_Kfz_7, M2A1 (`#8i`) | more APC as needed |
| `armor` | land | path / patrol (static if dug-in) | Pz_IV_H, Stug_III, Cromwell, Sherman (`#8j`) | heavies later |
| `troops` | land | path / patrol (static if dug-in) | soldier_mauser98, wwii_br/us (`#8k`) | more infantry via R13 |
| `aaa_guns` | land | **static** | flak18/30/36/37/38, Pak40, searchlight, KDO, bofors (`#8h`) | more AAA as needed |
| `artillery` | land | static (or rare relocate path) | — | verify before shelving |
| `radar_c3` | land | **static** | FuMG-401, FuSe-65 (`#8l`) | more C3 via R13 |
| `trains` | land | **path** on curated rail corridor | Locomotive + German wagons (`#8m` + `french_coast_rail_corridor`) | mesh snap still non-goal |
| `sea_craft` | sea | patrol / path; harbour → static | S-130, Uboat, Dry-cargo×2, HarborTug, Higgins (`#8h`) | LST/Castle later (era-filter) |
| `hard_infrastructure` | land | **static** | empty (`future`) | static objects / `#17b` |

Era caution: Channel Spitfire sorties ≠ dump every WWII id; prefer BoB/Channel-front
plausible Axis/Allied sets when promoting units into YAML.

Draft shape (for a future OpenSpec propose — do not implement until promoted):

1. **Sync (offline / CLI, not invent-time):** extend `catalog sync` to upsert
   `catalog_strike_units` (or equivalent) from Channel `ground_units.yaml` + `ships.yaml`:
   `unit_id`, `label`, `domain` (`land`|`sea`), optional `class_ids` / notes, theatre
   (`TheChannel`). Same DB as `#8a` (`catalog_*` tables). Refresh with existing
   `dcs-miz catalog sync` (and optionally after registry YAML edits in CI).
2. **Query at agent time:** read-only tool `list_strike_targets` (filter `domain`,
   optional text `q`, optional class) → rows from SQLite. Prompts: for recon/GA, call
   this before inventing `targets[]`; prefer returned ids only.
3. **Non-goals:** inventing DCS ids; scraping install UnitPayloads; building the table
   inside each LLM turn; replacing registry for validate/compile.
4. **Accept:** after sync, tool returns `Uboat_VIIC` under `domain=sea`; agent recon plan
   can suggest it without hardcoding.

Sequencing: full SQLite table + tool is `#8c`. Prefer `#8c` soon after `#15h`
accept so invent can query units; then **`#8d`** teaches *which* unit + motion +
`ai_preset` to pick. Category list above is the planning SoT until propose; grow
registry YAML class-by-class.

**`#8d` `agent-target-option-heuristics` — draft (2026-08-08):**

Today `#15h` ships presets (`convoy_transit`, `aaa_alert`, `ship_under_way`, …)
and prompts mention them, but invent still relies on the model remembering sparse
notes. Pilots expect “truck column inland” / “flak belt” / “U-boat under way” to
land on the right **unit id + motion + AI posture** without free-form Opt*.

**Goal:** decision guidance the agent can follow (tools + cards + optional table):

| Pilot / place cue | Class | Unit source | Motion | AI preset |
|-------------------|-------|-------------|--------|-----------|
| Truck / convoy inland | soft_vehicles | `#8c` soft ids | path (or patrol) | `convoy_transit` |
| Flak / AAA / guns | aaa_guns | flak*/Pak* | static | `aaa_alert` |
| Mid-Channel U-boat under way | sea_craft | `Uboat_VIIC` | patrol | `ship_under_way` |
| Harbour / dock shipping | sea_craft | sea ids | static | `harbour_static` |
| Emplaced only / dig-in | aaa / (later armor) | class ids | static | omit or alert |

**Ship as:**

1. Richer `ground_ai_preset` / `strike_target_class` / `channel_place` meta
   (preferred_motion, preferred_ai_preset, example Spec paths).
2. Invent prompt + schema: **call** `list_strike_targets` / `list_mission_options`
   before emitting `targets[]`; only allowlisted presets/fields.
3. Optional hermetic invent/fixture tests for 3–4 ask → Spec shape checks.
4. Brief language already partly covers under-way / alert — keep aligned.

**Depends on:** `#15h` (presets exist); **`#8c` preferred** so unit pick isn’t
hardcoded in prompts. Can thin-ship prompt table before `#8c` if needed.

**Non-goals:** ME Options dump; inventing DCS ids; RL from flight logs; air/helo
Option shelves.

**`#8e` `theatre-target-promote-checklist` — shipped as docs SoT:**

Full checklist: [`THEATRE_TARGET_PROMOTE.md`](THEATRE_TARGET_PROMOTE.md).
BACKLOG no longer owns the step list — edit the doc when process changes.
First unit-batch OpenSpec change uses that checklist (not this `#8e` item).

### Explicit non-goals for promote (reminder)

- Scraping full ME unit trees into the catalog.
- Auto-promoting discovered install folders into known YAML.
- Invent inventing Opt* or unit strings outside allowlists.

**`#8f` `agent-channel-geometry-invent` — draft (2026-08-08):**

Live invent suite after `#8d`: tools + unit/preset cues work; **geometry fails**.

| Failure | Example |
|---------|---------|
| Land path over water | Convoy Blitz + path → `motion_domain_mismatch` |
| Bad strike distance | Harbour shipping strike ~4 km from Manston |
| Sea/land strike mismatch | U-boat GA fails domain validation after repair |

**Ship as:**

1. Numeric recipes on `channel_place` meta (and/or thin helper): french coast /
   mid-Channel / harbour bands from accepted examples (e.g. inland ~125°/76 km;
   mid-Channel ~140°/40 km).
2. Prompts/schema: copy place geometry; land path near strike on land; sea on water.
3. Stronger `host_spec_repair_nudge` when codes are `motion_domain_mismatch` /
   `strike_domain_mismatch` (include recipe + example).
4. Re-run diverse invent suite; accept = validate + domain-coherent geometry.
5. Optional later: host clamp of path points (only if LLM repair still fails).

**Non-goals:** full terrain mesh; multi-theatre geometry; expanding unit shelves.

**`#8g` `agent-invent-path-harbour-harden` — draft (2026-08-08):**

After `#8f` recipes: convoy still invents path points over water; harbour may keep
coastal geometry but land soft units. Ship: short path invent (2–3 +
`path_point_deltas`), pasteable path repair YAML, invent/chat **host path clamp**
(not CLI validate), harbour→`list_strike_targets(domain=sea)` guidance + nudge.
Then `#8e` shelf expand.

**`#15g` `strike-target-motion` — draft (2026-08-08):**

Today GA/recon `targets[]` are placed once (static) at the strike/AOI point.
Motion should apply to **land and sea** when it makes sense; static remains the
default and the right choice for fixed sites.

**When motion fits (agent + examples):**

| Kind | Prefer | Notes |
|------|--------|--------|
| Mid-Channel / open-sea craft | `patrol` or short `path` | Surfaced U-boat, coastal shipping under way |
| Harbour / dock / port ships | `static` | Tied up alongside |
| Soft vehicles / trucks / light cars | `path` (convoy) or `patrol` | Road-ish legs near strike/AOI |
| Tanks / AFVs / troops (when in registry) | `path` or `patrol` | Advancing / sweeping — not dug-in |
| AAA / AT guns / flak | `static` | Emplaced batteries |
| Trains | `path` along **curated rail corridor** | Not free-form; needs Channel rail shelf (v2 / registry) |

**Draft Spec shape** (promote via OpenSpec — do not implement until proposed):

1. **Per-target motion:** `motion: static` (default/omit) | `patrol` +
   `patrol_radius_m` | `path` + short airfield-relative
   `{bearing_deg, distance_km}` waypoints (loop). Same fields for land + sea.
2. **Compiler:** emit native ME waypoints / go-to loop on ship **or** vehicle
   groups; curated speeds by domain/class. Static = today’s placement only.
3. **Agent heuristics:** shipping places → sea motion; soft_vehicles / mobile
   land classes → path/patrol; aaa_guns / harbour → static. Never invent rail
   geometry — only named corridors once registry/planning_options expose them.
4. **Examples:** mid-Channel U-boat with patrol; inland truck convoy path;
   keep flak/static harbour Specs as-is.
5. **Non-goals (v1):** crash-dive/ASW; Mist/MOOSE; LLM free-form routes;
   auto-snap to real DCS rail mesh (trains = later curated corridor, not v1).
6. **Accept:** ME shows moving sea craft + moving truck group; static Specs
   unchanged.

**Registry note:** Channel land shelf today is soft vehicles + AAA (`ground_units.yaml`).
Tanks/troops/trains need unit ids + classes before examples; motion Spec can
ship first for trucks + ships.

**`#15h` `ground-target-ai-options` — draft (2026-08-08):**

DCS splits AI options by domain (`AI.Option.Air` / `.Ground` / `.Naval` — Hoggit
`DCS_enum_AI`). ME shows a mixed list; **not every Opt applies to every unit**.

| Domain | Documented option ids (adopt filter) |
|--------|--------------------------------------|
| **Ground** | ROE (0), Formation (5), Disperse on attack (8), Alarm state (9), Engage air weapons (20), AC engagement range (24), Restrict AAA min/max (27/29), Restrict targets (28), Formation interval (30), Evasion of ARM (31) |
| **Air** | ROE, React on threat, Radar, Flare, Formation, RTB bingo/ammo, Silence, ECM, Prohibit AA/AG/jett/AB, Missile attack, radio usage, jett empty tanks, forced attack, prefer vertical, formation side swap, … |
| **Naval** | **ROE only** in published enum (as of Hoggit page) — thin surface; **research** whether ships get more options in current DCS / ME than the wiki lists |

ME WP **options** (not triggers) — PyDCS `Opt*` keys vs domain:

| Adopt? | ME / behaviour | Domain | PyDCS | Notes |
|--------|----------------|--------|-------|--------|
| **yes (shipped `#15g`)** | Disperse Under Fire | ground | `OptDisparseUnderFire` (8) | Moving land default 180s |
| **yes** | ROE | ground (+ air/naval variants) | `OptROE` (0) | Soft hold vs AAA return/open fire |
| **yes** | Alarm State | ground | `OptAlarmState` (9) | Convoy green in transit / red when set |
| **yes** | Engage air weapons | ground | `OptEngageAirWeapons` (20) | Flak/SAM columns |
| **yes** | Restrict targets | ground | `OptRestrictTargets` (28) | Narrow engage set |
| **yes** | Interception / AC engage range | ground | `OptInterceptionRange` (24) | Commit distance |
| **maybe** | Formation interval; AAA alt restrict; ARM evade | ground | confirm PyDCS | Spacing / AAA belts |
| **research** | On Road / Off Road / Rank·Cone·Vee… | ground PointAction | `PointAction.*` | v1 = Off Road only |
| **research** | Naval options beyond ROE | **sea** | ? | Ships/U-boat: wiki naval = ROE only — verify in ME on Channel ships |
| **skip for ground targets** | React on threat, radar, chaff, RTB bingo, ECM, afterburner, jettison, AA missile range, radio usage… | **air** | various | Aircraft-centric; don’t dump on trucks |

Draft Spec: optional `targets[].ai` or named presets (`convoy_transit`, `aaa_alert`) →
allowlisted options on WP0 **filtered by unit domain**. Catalog family e.g.
`ground_ai_preset` (+ later `naval_ai_preset` if ME exposes more). **R12 desk
notes** (`research/ai-options-domain.md`): Naval published = ROE only; ground
formation is PointAction not air `OptFormation`; PyDCS missing Opt* for AAA
alt / formation interval / ARM evade (ids 27/29/30/31). Promote `#15h` after ME
smoke checklist in that file.

---

## M4 — Mission types

**Next promote / in proposal:** Full-catalog campaign **M7** (Slice F4
`nevada-cold-freeflight`) from Agents Window
(`/full-catalog-orchestrate`). ME Instant Action smokes below stay do-soon and
do not block that campaign. Follow
[`THEATRE_TARGET_PROMOTE.md`](THEATRE_TARGET_PROMOTE.md). Definitive map fleet
recorded under R11 (2026-08-09). Normandy freeflight bind shipped
(`normandy-cold-freeflight`).

**Do soon (not blocking next promote) — prefer sooner:**
- **Normandy 2.0 ME accept:** Instant Action
  `out/needs_oar_point_cold_freeflight.miz` (or recompile
  `examples/needs_oar_point_cold_freeflight.yaml`) — cold Spitfire at Needs Oar
  Point on Normandy. Compile+pytest done 2026-08-09; **ME Instant Action still
  needed** before calling the map fully accepted.
- `#15h` ME smoke: Instant Action
  `out/manston_ground_attack_convoy.miz` — Alarm Green / Return Fire / Off Road /
  Disperse; `out/manston_ground_attack_flak_alert.miz` — aaa_alert options;
  `out/manston_uboat_hunt.miz` — ship_under_way ROE/Alarm. Deferred from `#15h`
  finalize 2026-08-08.
- `#15c` join-up: Instant Action `out/manston_cap_flight_wingman.miz` (or recompile
  `examples/manston_cap_flight_wingman.yaml`) — after takeoff, confirm AI lead flies
  CAP and player Follow/join works. Deferred from `#15c` accept 2026-08-07.
- `#15d` section orders: Instant Action `out/manston_cap_flight_orders.miz` (or
  recompile `examples/manston_cap_flight_orders.yaml`) — **take off**, then exercise
  F10 `Section: Rejoin` and `Section: Engage` (Orbit/RTB/Break optional) while
  airborne so Follow/ROE packs are visible in flight. ME + cold-start F10/ack
  accepted 2026-08-07; airborne smoke deferred.
- `#15e` discipline: Instant Action `out/manston_cap_flight_discipline.miz` (or
  recompile `examples/manston_cap_flight_discipline.yaml`) — **take off**, leave
  section bubble → soft rejoin warn (~45 s), optional hard `message_end` (~120 s).
  ME triggers/zone accepted 2026-08-07; airborne smoke deferred.
- `#15g` convoy fly: Instant Action `out/manston_ground_attack_convoy.miz` (or
  recompile `examples/manston_ground_attack_convoy.yaml`) — ME OK 2026-08-08 (trucks
  moving Off Road + Disperse Under Fire on WP options). **Later:** airborne attack
  pass — confirm disperse / scatter under fire; optional On Road follow-up via `#15h`.

| # | Item | Goal | Status |
|---|------|------|--------|
| 12 | `mission-type-intercept` | Dawn Manston intercept vs Bf-109K-4 (the concept doc's example) | `done` (accepted in-game 2026-07-26; ThirdReich/red) |
| 13 | `mission-type-cap` | Patrol station, engagement rules | `done` (accepted in-game 2026-08-01) |
| 14 | `mission-type-ground-attack` | Ground targets, payload selection | `done` (accepted in-game 2026-08-02; Dunkirk inland + slipper) |
| 15 | `mission-type-escort` | Escort a friendly package | `done` (accepted in-game 2026-08-02; Mosquito package + bounce) |
| 15a | `mission-type-recon` | Locate / observe a place or contact (GA-like geometry + marks/zones) **without** strike/payload attack; win on find/RTB rather than destroy | `done` (accepted ME 2026-08-07; Reconnaissance + AOI find beat) |
| 15f | `channel-uboat-recon-hunt` | Channel **surfaced** U-boat locate + hunt on top of `#15a` recon + existing GA `sea_craft` / `Uboat_VIIC`: mid-Channel recon example (sea contacts, observe/find, weapons hold), GA U-boat strike example (bomb payload while surfaced; mid-Channel or harbour geometry), catalog `mission_inspiration` + place/class cards, agent briefs that say “bomb on the surface / before crash-dive.” Prefer two Specs (recon then GA) and optional late-act/radio drama via existing `#25`/`#30f`. **Non-goals:** true ASW (submerged detect, depth charges, sonobuoys — DCS bombs vanish underwater); new `asw` mission type; armed recon / find-then-kill in one Spec (defer to a later change if wanted). Agent target *suggestion* from full unit catalog → **`#8c`** (SQLite). Moving sea contacts → **`#15g`**. | `done` (accepted ME 2026-08-08; surfaced Uboat_VIIC recon + hunt) |
| 15g | `strike-target-motion` | Optional **motion** on `targets[]` / recon contacts (land **and** sea): default **static** (harbour/dock, emplaced AAA/AT, dug-in). Prefer **patrol** (radius) or short looping **path** (airfield-relative waypoints) for ships under way, truck/vehicle convoys, and (when registry has them) tanks/troops. Trains later via curated Channel rail corridors — not free-form. Compiler: native ME waypoints on ship/vehicle groups (no Lua). Agent heuristics by place/class. Applies to GA + recon. **Non-goals v1:** ASW/crash-dive; auto rail-mesh snap; LLM free routes. Ground AI option shelf → **`#15h`**. | `done` (accepted ME 2026-08-08; U-boat patrol + convoy path + Disperse Under Fire; airborne disperse do-soon) |
| 15h | `ground-target-ai-options` | Spec shelf for **ground/sea target WP AI options** (curated ids → PyDCS `Opt*`, not free-form). After `#15g` + **R12 done**: expose useful ME options beyond Disperse — ROE, Alarm State, Engage air weapons, Restrict targets; interception **by class** (AAA yes, soft truck no); sea = ROE+Alarm(+optional engage/intercept); **On Road** vs Off Road + formation PointActions as separate knobs. Defaults/presets by class. Planning_options + validate allowlist. **Non-goals:** Lua AI; dumping full air Opt* on targets; assuming ME list = capability (Spit ECM lesson). See `research/ai-options-domain.md`. | `done` (2026-08-08; compile+pytest; **ME do-soon**) |
| 15b | `player-flight-squadron` | Break solo-only player sorties: Spec + compiler support for a **player flight** (2–4 Spits) so the human can fly as **flight lead** (AI wingmen) or as a **wingman** in an AI-led section. Placement + skills + brief; join-up/Follow deferred to `#15c`. Escort `package` remains friendly AI only, not the player’s section. | `done` (accepted ME smoke 2026-08-07; lead 4-ship + wingman 4-ship via separate AI lead group) |
| 15c | `player-flight-joinup` | After `#15b`: **Follow / join-up** and shared route so the section flies as a squadron — wingman Follow AI lead; put CAP/GA/escort tasking on the AI lead when `role: wingman` + `join_up`. Prefer native ME Follow + waypoints; no LLM Lua. | `done` (accepted 2026-08-07; **do-soon smoke:** `manston_cap_flight_wingman` after takeoff) |
| 15d | `player-flight-orders` | Curated **section orders** the player (or Spec triggers) can issue: rejoin/form up, engage, cover, orbit, RTB, break, etc. Prefer stock DCS lead→wingman radio when `role: lead` (same group); extend with F10 / flag→AI-task packs for wingman separate groups and scripted beats. Spec selects named orders only — no free-form chat→Lua. After `#15b`; pairs with `#15c` for cohesion. | `done` (accepted 2026-08-07; ME + F10/ack; **do-soon:** airborne Rejoin/Engage on `manston_cap_flight_orders`) |
| 15e | `player-flight-discipline` | Opt-in **fail-to-follow** consequences when wingman+join_up: if the player stays outside a section bubble (distance/time) after takeoff — soft radio “rejoin”, then stronger beats (flag / message / abort or RTB / mission_end). Prefer native zones+flags+messages; curated snippet only if range-to-group needs Lua. After `#15c`; pairs with `#15d` rejoin orders. | `done` (accepted 2026-08-07; ME triggers/zone OK; **do-soon:** airborne soft/hard on `manston_cap_flight_discipline`) |
| N1 | `normandy-cold-freeflight` | First multi-theatre smoke: Normandy 2.0 cold freeflight Spitfire at Needs Oar Point (Spec theatre `Normandy`, airfield `NeedsOarPoint` / airdromeId 28). Bind + registry + example + hermetic tests. | `done` (2026-08-09; compile+pytest; **ME do-soon** `out/needs_oar_point_cold_freeflight.miz`) |

---

## M5 — Immersion & replayability

**M5 core done** (briefings, weather trio, randomization). Remaining items are optional polish.

| # | Item | Goal | Status |
|---|------|------|--------|
| 16 | `briefing-generation` | AI briefing text into `l10n` dictionary (sortie, description, tasks); uses squadron-commander voice when enabled | `done` (accepted in-game 2026-08-02; Sortie/Description/Task in ME) |
| 17 | `weather-time-presets` | Named presets verified in-game (sunny/dawn/marginal VFR) | `done` (accepted in-game 2026-08-02; meteo brief phrasing) |
| 17a | `weather-presets-expand` | Expand Channel Spec weather beyond the trio: curated **named patterns** seeded from Spitfire campaign `.miz` weather (cloud gallery + wind/fog/turb), pilot-facing brief text, SoT parity (`weather_sot`). Prefer recipes over raw ME knobs / live METAR. Invent jitter deferred to `#17e`. Research: R10 campaign scan (2026-08-06) | `done` (accepted ME smoke 2026-08-06; broken + rain examples) |
| 18 | `mission-randomization` | Seeded Spec→Spec variation for replayability (CLI + tool; compiler stays deterministic) | `done` (accepted 2026-08-02; seed42 vs seed99 CAP) |
| 19 | `spitfire-radio-channel-presets` | Match ED Channel Spitfire unit Radio bank (A=124, B=40, C=41, D=42, E=108.9) for cockpit channel clicks; group frequency 124 already correct | `idea` (parked 2026-08-02 — immersion only; not required to fly; revisit if cockpit radio parity matters or M6 radio menus need it) |
| 17b | `static-objects-placement` | Place ME static objects / scenery (hangars, vehicles-as-static, props) from Spec for Channel immersion — promote only after **R10** ranks PyDCS + Channel type ids | `idea` (blocked on R10) |
| 17c | `weather-in-flight-fog` | Optional mid-sortie **fog** evolution (foggy→clear / clear→fog) via curated `world.weather.setFogAnimation` snippets — **not** sunny→rainy cloud swaps (no DCS API). Fog-only DoScriptFile slice (full `#22` later) | `done` (accepted ME smoke 2026-08-06; sea_fog burn-off at Manston) |
| 17d | `weather-reweather-miz` | Agent + CLI: change weather on an **existing** `.miz` (named pattern / NL → recipe) and **overwrite** the same path — same sortie (groups/triggers), new static weather. Write Spec YAML alongside `.miz`; agent finds sibling or takes an explicit path. Prefer Spec recompile when YAML exists; else PyDCS `load_file` → apply invent snapshot → `save`. Not mid-flight. After `#17a`/`#17e` | `done` (accepted ME smoke 2026-08-06; rain_overcast → Overcast and Rain 2) |
| 17e | `weather-invent-jitter` | **Always-on** seeded invent variation around `#17a` patterns. **Hybrid priors:** (1) **within-family gallery preference** weighted by Spec **date/season** (+ start **time** where useful, e.g. morning fog risk) — pick among allowed `PresetN`/`RainyPresetN` for that pattern class, never silent cross-family swaps; (2) **soft nudge** on temp/QNH/wind layers/turb/fog/base after gallery pick; (3) seeded jitter for day-to-day noise. Climatology from `research/weather.md` (Channel seasonal — **no per-place bias**). Distinct from ME Dynamic cyclones and `#17c`. Goldens pin seed. Spec: `weather` enum + `weather_opts.seed` (auto-write if omitted) | `done` (accepted ME smoke 2026-08-06; seed42 vs seed99 broken) |
| 17f | `weather-brief-metar-showers` | Offline synthetic METAR line in commander/compile briefs from invent `WeatherSnapshot` (`EGMH` + `RMK SIM`; no live METAR APIs). New `showers_scattered` pattern using rainy light gallery (`RainyPreset4`–`6` / `NEWRAINPRESET4`) via packaged `weather_gallery.yaml` (PyDCS enum lacks those ids — construct `CloudPreset` for emit). R10 taxonomy in gitignored `research/weather.md` | `done` (accepted ME smoke 2026-08-07; showers + synthetic METAR) |

---

## M6 — Mission enrichment: triggers & Lua

**Next promote / in proposal:** (see M4 — squadron `#15e` done); `#22` only if native insufficient; R8 when bumping pydcs

Goal: missions get *behaviour*, not just placement — events, radio calls, objectives that
succeed or fail. This is where Lua legitimately enters the product, as **compiler output and
curated snippets**, never as free-form LLM text.

The rule that keeps this safe: the agent chooses *which* behaviour and *what parameters*;
the trigger/script text itself is human-authored, versioned, and tested.

| # | Item | Goal | Status |
|---|------|------|--------|
| 20 | `trigger-model-spec` | Mission Spec gains a backend-agnostic condition → action model (zones, flags, time, unit state); no Lua in the Spec | `done` (2026-08-02; validate OK, compile deferred to `#21`) |
| 21 | `trigger-compiler-native` | Compile the declared trigger model into native `.miz` trigger tables via PyDCS; golden-fixture asserts on emitted structure | `done` (accepted in-game 2026-08-02; sample message ~T+120) |
| 22 | `script-snippet-library` | Curated, parameterised Lua snippets (human-written, tested, version-pinned) that the compiler injects for behaviour PyDCS triggers can't express; agent may only select + fill declared params. **Grow on demand** (see Pending decisions) — do not pre-build a speculative library | `idea` |
| 22a | `trigger-flag-random` | Spec action for ME Set Flag Random (`a_set_flag_random`) so “dynamic” raid dice stay native (R1 Version_2 / community BoB) — prefer before Mist/`#22` | `done` (2026-08-05) |
| 22b | `aircraft-failures` | Optional player aircraft **failures** (engine, controls, etc.): omit = none; **fixed** schedule via ME Failures panel table (`enable`/`hh`/`mm`/`mmint`/`prob`); Within minutes (min 1). Curated Channel Spitfire ids only — no free-form strings, no LLM Lua. | `done` (accepted Instant Action 2026-08-07; magneto drill Mag2 OFF + Mag1 panel) |
| 23 | `mission-events-narrative` | Use 20–22 for immersion: bandit callouts, tasking updates, RTB clearance, success/failure outcomes — in squadron-commander voice | `done` (accepted in-game 2026-08-03; ME shows three CAP narrative rules) |
| 23a | `narrative-pack-ground-attack` | Opt-in GA narrative (push / ingress / targets-down via `target_dead`) | `done` (accepted in-game 2026-08-04; ME shows three GA narrative rules) |
| 25 | `trigger-radio-late-activation` | F10 radio menu items + late-activated enemy/target groups (Dawn Raid–style difficulty / spawn options); native ME only | `done` (accepted in-game 2026-08-04; ME radio + late activation) |
| 26 | `trigger-sound-flags` | Native `sound` action (curated `asset_id`) + richer flags (`flag_equals` / `flag_more` / `flag_less` / `time_since_flag`, `inc_flag` / `set_flag_value`) | `done` (accepted in-game 2026-08-04; beep + flag chain) |
| 27 | `group-life-less` | Spec condition for remaining group life % (`enemy_index`/`target_index` + `percent`) → PyDCS `GroupLifeLess`; partial-damage objective beats | `done` (accepted in ME 2026-08-04; GROUP LIFE LESS @ 50%) |
| 28 | `trigger-markers` | Spec actions `mark` (F10 map mark) + `smoke` (ME Smoke Marker) on Spec zones → PyDCS `MarkToAll` / `ExplodeWPMarker` | `done` (accepted in ME 2026-08-04; Mark To All id 1 + red Smoke Marker) |
| 29 | `altitude-speed-gates` | Spec player conditions `unit_altitude_*` / `unit_speed_*` → PyDCS UnitAltitude* / UnitSpeed* (ingress discipline) | `done` (accepted in ME 2026-08-04; continuous AGL + speed gates) |
| 30 | `agent-capability-catalog` | Packaged `mission_behaviour` / `mission_inspiration` cards; mission-design `research_guidance`; local `Mods/campaigns` + Doc index for assertive creative planning | `done` (2026-08-04; catalog + tools + prompts) |
| 30a | `creative-decision-memory` | Record inspiration/behaviour choices in generation `detail` + feedback → prompt bias over time | `done` (2026-08-04; detail.creative + bias helper) |
| 30b | `eval-agent-creativity` | Periodic live vague-ask harness (Cursor skill) to regression creative agent behaviour → LESSONS / OpenSpec | `done` (skill + prompt catalog; re-run after agent changes) |
| 30c | `agent-assertive-behaviours` | Close live-eval + adversarial gaps for *agent behaviour*: vague free_flight applies 1–2 behaviours; fix `SPEC_SHAPE_REMINDER` “triggers must be []”; schema examples include immersion variants; complete radio+late-act recipes (pair with `#32`); prefer campaigns/Doc *filenames* until `#40`; discourage randomize-as-authoring; stop `infer_creative` rewarding half-recipes; optional hard behaviour floor when immersion unspecified | `done` (2026-08-05) |
| 30d | `agent-immersion-floor` | Soft host immersion nudge + immersion-first schema examples + drop invent `randomize_mission` (live eval 2026-08-05 follow-up) | `done` (2026-08-05) |
| 30e | `mission-designer-catalog` | Catalog shelves for mission-designer co-authoring: dynamics modes (live/choose/hybrid/fixed), strike target classes ↔ payload/domain, curated Channel places; agent prompts query catalog then recommend | `done` (2026-08-05; shelves + co-author prompts; `#30f` consumes) |
| 30f | `mission-dynamics-pack` | Spec `dynamics` expand pack (pools + modes) emitting set_flag_random / F10 / activate_group — follows `#30e` palette | `done` (2026-08-06; live/hybrid ME smoke accepted) |
| 24 | `cockpit-state-triggers` | Optional interactive/training missions driven by Spitfire cockpit arguments (promotes research R4 once verified in-game) | `idea` |

Sequencing note: 20–21 need `mission-spec-schema` (M2 `#2`), `validation-engine` (M2 `#5`) and
`golden-fixtures-tests` (M2 `#6`) first — an unvalidated trigger graph is how missions silently
break. 22 stays optional: prefer native triggers whenever they suffice. **R5 (stock Channel) is done:**
model zones/flags/time/unit-dead/radio/messages first; Mist/MOOSE default **off** until R1–R2 say otherwise.
Still useful to revisit R5 after user-file audits.

---

## M7 — Full catalog (multi-theatre)

**Next promote / in proposal:** `nevada-cold-freeflight` (F4). Trigger from
Agents Window with `/full-catalog-orchestrate`. Cursor agents + skill live under
`.cursor/agents/` and `.cursor/skills/full-catalog-orchestrator/`.

**Goal:** NL agent can plan the existing six mission types (free_flight, intercept,
CAP, ground_attack, escort, recon) on every **installed map that PyDCS can bind**.
Not every DCS mission kind; not terrains without a PyDCS module.

**Process:** sequential OpenSpec slices (one branch at a time). Merge gate =
hermetic tests + compile + Agent Review. ME Instant Action is human do-soon after
merge. Checklist: [`THEATRE_TARGET_PROMOTE.md`](THEATRE_TARGET_PROMOTE.md). Playbook:
`.cursor/skills/full-catalog-orchestrator/SKILL.md`.

**Do not:** invent DCS ids; auto-promote install discovery; parallel map writers;
Stage C combat on a new map before Slice 0b is on master.

| # | Item | Goal | Status |
|---|------|------|--------|
| F0 | `theatre-registry-packages` | Split `data/channel/` into per-theatre packages; registry loader walks them; shared/era shelves for WWII units used by Channel+Normandy; Channel goldens + Normandy smoke stay green | `done` (CLI/API 2026-08-15; ME Instant Action do-soon) |
| F0b | `theatre-agnostic-planning` | Unhardcode Channel helpers before new-map combat: domain classifier, invent prompts, country allowlists, intercept spawn recipes, path clamp, strike-unit theatre tags, reweather/METAR. **Gate** for Stage C on any non-Channel map | `done` (CLI/API 2026-08-15; ME Instant Action do-soon) |
| F1 | `normandy-airfields-places` | Deepen Normandy (already bound): more AFs, places, CAP invent at Needs Oar Point (stages B–C). After 0 + 0b | `done` (CLI/API 2026-08-15; ME Instant Action do-soon) |
| F2 | `caucasus-cold-freeflight` | Caucasus Stage A: bind + smoke freeflight (modern countries/aircraft). After 0 + 0b | `done` (CLI/API 2026-08-15; ME Instant Action do-soon) |
| F3 | `syria-cold-freeflight` | Syria Stage A bind + smoke. After F2 pattern | `done` (CLI/API 2026-08-15; ME Instant Action do-soon) |
| F4 | `nevada-cold-freeflight` | Nevada Stage A bind + smoke | `idea` |
| F5 | `falklands-cold-freeflight` | South Atlantic (`Falklands`) Stage A bind + smoke | `idea` |

Further per-map stages B–D (geography, places+combat, units+invent) are named at
promote time (`<theatre>-airfields`, `<theatre>-places`, …). Refresh
`dcs-miz theatres --refresh` before promoting. **No Spec bind** for
`MarianaIslandsWWII` / `Kola` / `Iraq` until PyDCS terrain exists (R8).

---

## Adversarial review track (2026-08-05) — challenge & work

**Source:** [`docs/adversarial-review-2026-08-05.md`](adversarial-review-2026-08-05.md)
(interactive board: project canvas `adversarial-review-2026-08-05.canvas.tsx`).

**How to use:** these are *challengeable* findings — promote one OpenSpec change at a time after
agreeing the item is real, in-scope, and not better folded into an existing idea. Do **not**
treat the notes as approved design.

**Claim scorecard (to disprove or harden):** compile/validate ≠ DCS-ready; catalog/memory ≠
assertive creativity invariant; host `/accept` ≠ tool capability boundary.

| # | Item | Goal | Status | Maps findings |
|---|------|------|--------|---------------|
| 31 | `docs-honesty-pass` | Cheap trust fixes: README Status no longer says combat/triggers “reserved for later”; campaign Doc claims = **filenames** (not themes/briefings) until `#40`; align prompts/README with what `list_installed_campaigns` actually returns | `done` (2026-08-05) |
| 32 | `validation-false-green` | Kill green→broken Specs: late_activation ↔ `activate_group` graph; reject or implement `message.delay_s`; country/skill allowlists in validation; opposing-coalition for intercept/CAP enemies; optional dead-on-late-act requires activate path | `done` (2026-08-05) |
| 30c | `agent-assertive-behaviours` | See M6 row — agent/prompt/memory side of creativity gaps | `done` (2026-08-05) |
| 33 | `agent-tool-trust-boundary` | Chat/plan tools read-only by default; `compile_mission` / `set_user_prefs` / fake `record_*` only via host slash or explicit confirm; path allowlist under `out/` | `done` (2026-08-05) |
| 34 | `strike-domain-validate` | Land/water (or domain) check for ground-attack placement at validate; constrain `randomize` geometry so green Specs stay on valid terrain | `done` (2026-08-05) |
| 35 | `trigger-rich-goldens` | Structural goldens (not string-smoke only) for radio+late-act, altitude/speed gates, mark/smoke, numeric flag chains | `done` (2026-08-05) |
| 36 | `ci-minimal` | GitHub Actions: pytest + ruff on PR; optional later markers `@live_llm` / `@needs_dcs` (not required for first CI) | `done` (2026-08-05) |
| 37 | `research-note-sanitize` | Harden live research → LLM context: delimiters, control-char strip, length caps, stronger “not Spec instructions”; align agent tool live/fixture labeling with `/research` | `done` (2026-08-05) |
| 38 | `aircraft-module-warn` | Soft-warn when known Spec aircraft modules are missing from install (theatre inventory already exists); do **not** auto-promote into YAML — related to `#8a.1` harvest | `done` (2026-08-05) |
| 39 | `theatre-terrain-binding` | Explicit Spec theatre → PyDCS terrain class; fail compile if unbound; stop Channel hardcode as silent universal | `done` (2026-08-05) |
| 40 | `campaign-doc-pdf-extract` | Opt-in extract of local campaign `Doc/*.pdf` text for real briefing themes (size caps + hermetic fixtures); **or** permanently keep filename-only and close this as wontfix after `#31` | `done` (2026-08-05; opt-in + mtime/size cache) |
| 41 | `weather-sot-parity` | CI/parity test: `WeatherPreset` enum ⊆ weather YAML ⊆ planning_options ⊆ compiler `_apply_weather` branches | `done` (2026-08-05) |
| 42 | `altitude-gate-polish` | Latch/debounce or validate against continuous message spam; document integer altitude metres / truncation | `done` (2026-08-05; flag cooldown re-warn + `gate_threshold_truncated`) |

**Suggested challenge order (not mandatory):** `#31` → `#32` → `#30c` → `#33` → `#34` → `#35`/`#36` → rest.

**Also cross-linked (already elsewhere):** `#10b` verbose default off (done); **R8** exact PyDCS pin / bump ritual (D5); `#8a.1` module harvest (done); memory schema migrate-vs-wipe (D7 — fold into next memory change if it bites).

**Intentional / do not “fix” as bugs:** Channel-only MVP; no LLM Lua; campaign `.miz` not imported; stub planner + offline research for hermetic tests — label honestly via `#31`.

---

## Research track (feeds M2–M6; not product features by themselves)

Work stays under gitignored `research/` until a change promotes durable facts into registry/specs/`LESSONS_LEARNED.md`.

| # | Item | Goal | Status |
|---|------|------|--------|
| R1 | `research-spitfire-user-missions` | Download/track Spitfire single missions ([DCS User Files filter](https://files.digitalcombatsimulator.com/en/files/filter/type-is-single/game-is-world_2.9/unit-is-spitfire_lf_mk.ix/apply/)); note map/aircraft reqs; extract mission-design patterns for M4; **also open each `.miz` and note how triggers / `DO SCRIPT` / embedded `.lua` are used** | `done` (2026-08-05; Channel priority set audited — see `research/spitfire-user-missions.md`; Mist rare; native radio/late-act + flag-random) |
| R2 | `research-spitfire-campaigns` | Same for campaigns ([filter](https://files.digitalcombatsimulator.com/en/files/filter/type-is-campaign/unit-is-spitfire_lf_mk.ix/apply/)); track each file; learn campaign structure; **same Lua/trigger audit as R1 across campaign missions** | `done` (2026-08-05; installed Beware/FoD/Epsom/Big Show = 60× no Mist/triggers; UF Channel facet 0 — see `research/spitfire-campaigns.md`) |
| R3 | `research-historical-spitfire-sorties` | Web research of real historical Spitfire sorties usable as mission templates (feeds intercept/CAP/escort + historical validation). **Also:** note weather/visibility mentions for Channel/SE England pattern cards (feeds `#17a` / R10 meteo) | `idea` |
| R4 | `research-spitfire-cockpit-args` | Keep [cockpit args list](https://files.digitalcombatsimulator.com/en/files/3349460/) as trigger/training reference only (see `LESSONS_LEARNED.md`); re-verify on DCS version bumps; promote only when an interactive-mission change needs it | `idea` |
| R5 | `research-lua-usage-patterns` | Stock Channel Spitfire IA + Training + Beware campaign audited; findings in `research/lua-usage-patterns.md` | `done` (2026-07-26; R1 singles + **R2 campaigns 2026-08-05** — ED campaigns stay trigger-empty) |
| R6 | `research-lua-ide-tooling` | Recipe in `research/lua-ide-tooling.md`: pin dcs-world-schema EmmyLua + LuaLS lab; VEAF MCP only at first `#22` snippet work | `done` (notes only; lab vendor not installed) |
| R7 | `research-pydcs-issues` | Review open issues on [pydcs/dcs](https://github.com/pydcs/dcs/issues); assess impact on our compiler / Channel Specs; promote durable notes into `LESSONS_LEARNED.md` or specs when they affect us | `done` (2026-08-04; notes in `research/pydcs-issues.md`; LESSONS updated — stay on 0.15.0 + keep payload/theatre workarounds) |
| R8 | `deps-upgrade-review` | Periodically check latest PyDCS and other project-related libraries; decide whether an upgrade is recommended (pin notes in LESSONS / pyproject when we bump) | `idea` |
| R9 | `research-dcs-user-manual-me` | Inventory ME features we could map into Spec/compiler/agent; notes under `research/`; promote durable gaps into backlog / LESSONS. **Sources (use together):** (1) local `docs/DCS_User_Manual_EN_2020.pdf` (gitignored; [official EN download](https://www.digitalcombatsimulator.com/en/downloads/documentation/dcs-user_manual_en/) — still the 2020 file for DCS **2.5**; ME chapter ToC ~p.83 / Set Rules for Triggers — *baseline only*); (2) community [TEMPEST.114 Mission Editor Manual](https://forum.dcs.world/topic/347082-mission-editor-manual-most-of-all-me-how-do-i-do-this-are-solvable-with-this-little-pdf-it-has-lots-of-info-not-clear-in-the-ui-hope-it-helps/) (ED Forums, 2024 — clearer ME how-tos than the UI/ED PDF); (3) [Hoggit ME wiki](https://wiki.hoggitworld.com/view/DCS_editor_triggerBasics) ([conditions](https://wiki.hoggitworld.com/view/DCS_editor_conditions), actions, [AI tasking](https://wiki.hoggitworld.com/view/DCS_editor_AITasking)); (4) [Hoggit Scripting Engine docs](https://wiki.hoggitworld.com/view/Simulator_Scripting_Engine_Documentation) (for M6 `#22` Lua, not day-to-day Spec compile); (5) [ED changelogs](https://www.digitalcombatsimulator.com/en/news/changelog/) + newsletters for post-2020 ME features; (6) in-game ME + stock Channel IA/Training (cross-check with R5) | `done` (2026-08-04; ranked candidates in `research/me-enrichment-candidates.md` — next product: `#26` sound + richer flags) |
| R10 | `research-me-mission-content` | **ME content-depth pass** (in-editor + PyDCS + campaign corpus + optional meteo): (1) **Weather** — mine installed Spitfire campaign `.miz` weather tables (Beware/FoD/Epsom/Big Show; 60 scanned 2026-08-06) + research samples; ME weather templates optional; PyDCS `CloudPreset` (30 ids); defer dynamic cyclones. (2) Optional Channel climatology to refine briefs. (3) **Static objects**. Notes in `research/weather.md`; promote `#17a` / `#17b` | `idea` (2026-08-06; campaign weather scan done — enough to seed `#17a` recipes) |
| R11 | `research-theatre-content-expand` | **Per-map content audit** for multi-theatre expand: install vs PyDCS vs planner bind; Normandy/Syria/MarianasWWII notes; promote order. Notes: gitignored `research/theatres/` + harness `research/audit_theatres_r11.py`. **Do not** auto-promote. | `done` (2026-08-08; see notes below) |

**`R11` `research-theatre-content-expand` — done (2026-08-08; fleet refresh 2026-08-09):**

Desk probe + notes under `research/theatres/`. **Definitive owned map fleet**
(install inventory 2026-08-09 — product names → Spec/probe ids):

| Product / pilot name | Inventory / Spec theatre id | State | PyDCS 0.15 | Planner |
|----------------------|-----------------------------|-------|------------|---------|
| The Channel | `TheChannel` | available | yes | **yes** |
| Normandy 2.0 | `Normandy` | available | yes (38 AF) | smoke shipped; ME do-soon |
| Syria | `Syria` | available | yes | planner smoke |
| Marianas WWII | `MarianaIslandsWWII` | available | **no module** | no |
| Nevada | `Nevada` | available | yes | no |
| South Atlantic | `Falklands` | available | yes | no |
| Caucasus | `Caucasus` | available | yes | planner smoke |
| Kola | `Kola` | available | **no module** | no |
| Iraq | `Iraq` | available | **no module** | no |

Also on disk but **disabled**: modern `MarianaIslands` (not in definitive list).

- **Assets:** WWII Units + M3 PTO present. Campaigns: Channel Spitfire only.
- **Promote order:** (1) **Normandy 2.0** freeflight smoke (`normandy-cold-freeflight`),
  (2) Syria later, (3) Marianas WWII / Kola / Iraq after PyDCS/R8.

**`R12` `research-ai-options-by-domain` — done (ME 2026-08-08):**
| R12b | `research-ai-options-unit-matrix` | Expand R12 beyond Channel smoke samples: ME WP Options matrix for **representative units** across airplanes, helicopters (same Air enum — verify ME), ships (E-boat / cargo / warship), and ground classes (armor, infantry, radar/SAM, soft, AAA). Record ME list vs meaningful capability (Spit ECM lesson). Append to `research/ai-options-domain.md`. **Not blocking `#15h`.** Promote when helo / armor / multi-theatre shelves need allowlists. | `idea` (draft 2026-08-08) |
| R13 | `research-campaign-unit-inventory` | Mine installed **Spitfire Channel campaign** `.miz` (Beware / FoD / Epsom / Big Show; 60 missions) for **ground / AAA / sea / helo** unit `type` frequencies. Notes: gitignored `research/campaign-units.md` + harness `research/audit_campaign_units_r13.py`. Feed `#8e` promote candidates. **Do not** auto-promote. | `done` (2026-08-08; see notes below) |

**`R13` `research-campaign-unit-inventory` — done (2026-08-08):**

Scanned 60 Spitfire Channel campaign `.miz` (regex on `mission` Lua; PyDCS load
failed on `zones`). Headlines:

- **Helos:** none — no Channel MVP helo shelf from this corpus.
- **Already shelved well:** soft / halftrack / most AAA / troops / common sea
  (Blitz, Sd_Kfz_251, flak30/37/38, KDO, Bedford, U-boat, E-boat, …).
- **Top promote candidates (verify + `#8e`):** `flak41`, `M45_Quadmount`,
  `QF_37_AA`, `Allies_Director`, `Tiger_I`, `SturmPzIV`, `Pz_V_Panther_G`,
  `JagdPz_IV` / `Jagdpanther_G1`; sea `LST_Mk2`, `USS_Samuel_Chase` (Allied
  landing — era OK, not Axis coastal default).
- **Absent from campaigns but shelved:** `FuMG-401` / `FuSe-65`, `Stug_III`,
  German loco/wagons (campaigns use sparse `Coach *` instead).
- **Skip:** modern leftovers (`M978 HEMTT Tanker`, …).

Follow-on shelf expand: **done** as OpenSpec `channel-shelf-r13-promote`
(`flak41`, Quadmount/QF/Allies_Director, Tiger/Panther/Jagd*, Coach cargo*,
LST_Mk2, USS_Samuel_Chase). Modern leftovers still skipped.

Desk + ME WP Options smoke (truck convoy, Flak 18, Uboat_VIIC, Spitfire). Notes in
`research/ai-options-domain.md`. Headlines:

- Options differ by **domain and unit class** (soft truck ≠ flak ≠ U-boat ≠ Spit).
- Naval ≠ ROE-only in current ME (U-boat: ROE, Alarm, Engage air, Interception range).
- ME can list **useless** options (Spit ECM / Chaff-Flare) — curate by unit, don’t
  mirror the full enum.
- Soft truck lacks Interception range + ARM evade; Flak has both.
- PyDCS gaps remain for AAA alt / formation interval Opt* (ME shows them).
- Full per-unit matrix → **R12b** (helo, armor, more ships); not needed for `#15h` v1.

**`R12b` `research-ai-options-unit-matrix` — draft (2026-08-08):**

Scripting only has Air / Ground / Naval (helos share Air). R12 sampled one airplane,
two ground classes, one ship. R12b collects ME Option lists for a small matrix of
representatives so future shelves don’t assume “all ground = truck” or “all air =
Spit.” Do when expanding registry classes or theatres — not before `#15h` propose.

---

## Later / deferred

- **Install maintenance slash** — M3 `#8a.2` `install-maintenance-slash`:
  parked 2026-08-05 after `#8a.1` cache. Host `/maintenance` (or richer `/catalog`)
  for read-only install status + optional refresh; keep out of default LLM invent
  tool list so the agent does not treat discovered-only modules as Spec ids.
- **Spitfire Channel radio A–E bank** — M5 `#19` `spitfire-radio-channel-presets`:
  parked 2026-08-02; group frequency 124 already flyable; unit Radio bank is cockpit
  immersion only (ED Channel A=124/B=40/C=41/D=42/E=108.9).
- **Agent verbose default off** — M3 `#10b` `agent-verbose-default-off`: **done**
  2026-08-05; default quiet, `--verbose` / `/verbose on` for traces. Reinforced by
  adversarial review **C3** (screenshot/log leakage).
- **Chat research live fetch** — M3 `#10d` `fix-chat-research-live`: **done** (Instant
  Answer + HTML cascade; clear soft-fail label). Revisit only if DDG HTML is blocked.
- **Lua enrichment** — scheduled as **M6**; still never LLM-authored mission Lua.
- **Lua IDE / MCP tooling** — see research **R5–R6**. Schema + LSP for writing snippets; VEAF MCP as a lab only. A future *project-owned* MCP that exposes *our* snippet catalog (`list` / `validate_params` / API docs) is optional once M6 `#22` exists. Native Lua compiler replacing PyDCS remains far-horizon.
- **Normandy / multi-theatre** — **M7** full-catalog campaign (`nevada-cold-freeflight` next after F3). R11 audit done; campaigns remain inspiration, not Spec import.
- **Historical validation engine** — date → plausible aircraft/opposition (productized form of R3).
- **PyDCS issue watch** — research **R7**: **done** 2026-08-04 (`research/pydcs-issues.md` + LESSONS); re-run on R8 bumps / before `#22`.
- **Dependency upgrade cadence** — research **R8**: check PyDCS + related libs; bump only when recommended.
- **ED / ME docs pass** — research **R9**: **done** 2026-08-04 (`research/me-enrichment-candidates.md` + LESSONS); promoted `#25` radio + late activation.
- **ME mission-content depth** — research **R10**: Spitfire campaign `.miz`
  weather mined (60 missions; gallery presets ranked); ME templates optional;
  promote `#17a` / `#17b` (`research/weather.md`).
- Multiplayer, dynamic campaign, radio VO generation.

---

## Ideas → backlog map

Source: `ideas-concepts.txt` (updated 2026-08-02).

| Raw idea | Disposition |
|----------|-------------|
| Module diagram + relationship docs on update | **M2** `#7` `dev-module-map` |
| SQLite inventory (airports, aircraft, weapons, landmarks…) for user + agent | **M2** `#3` YAML product SoT; **M2** `#4` install SQLite; **M3** `#8a` agent **catalog** SQLite synced from YAML/enums (query layer, not second SoT) |
| Mission types catalog in SQLite (for agent / UI listing) | **M3** `#8a` / `#9` — intended |
| User preferences, gen history, satisfaction survey | **M3** `#8b` `user-prefs-and-history` — intended |
| Detect installed maps | **M2** `#4` `installed-theatres-probe` |
| Agent narrates as US/RAF Squadron Commander | **M3** `#11` `squadron-commander-voice` (+ M5 briefings) |
| Agent knows / offers all planning options | **M3** `#9` `mission-option-catalog` + tools on `#8` |
| Agent knows Mission Spec JSON shape per mission type | **M3** `#10c` `agent-spec-schema-tool` (derived from Pydantic; not SQLite SoT) |
| Chat `/research` should fetch real web notes | **M3** `#10d` `fix-chat-research-live` |
| Lua integration? | **M6** `#20`–`#23` — enrich missions with triggers/scripts as compiler output; LLM still never authors mission Lua |
| Spitfire cockpit arguments (User Files 3349460) | **Research** R4 → **M6** `#24` once verified in-game |
| Download Spitfire campaigns / singles as inspiration | **Research** R1–R2 (+ Lua/trigger audit) → **R5** synthesis for M6 |
| Lua IDE / MCP for developing scripts | **Research** R6 (`dcs-world-schema` + LuaLS; optional VEAF MCP lab) |
| Historical Spitfire missions from the web | **Research** R3 → later historical validation |
| Review [pydcs/dcs issues](https://github.com/pydcs/dcs/issues); assess impact for LESSONS / specs | **Research** R7 `research-pydcs-issues` |
| Check latest PyDCS / project libs; recommend upgrades | **Research** R8 `deps-upgrade-review` |
| Mine ED User Manual ME chapter for richer mission content | **Research** R9 `research-dcs-user-manual-me` (2020 PDF + TEMPEST ME manual + Hoggit + changelogs) |
| More weather beyond sunny / dawn / marginal VFR | **M5** `#17a` `weather-presets-expand` — curated patterns after **R10**; invent-time jitter OK; not live METAR |
| Same mission file, change weather after fly/ME load | **M5** `#17d` `weather-reweather-miz` — overwrite `.miz` (Spec recompile or weather-table patch) |
| Within-pattern variance (wind/fog/turb not identical every time) | **M5** `#17e` `weather-invent-jitter` — seeded; climatology bands; not ME Dynamic |
| Mid-flight weather story (sunny→rain / fog burn-off) | **M5** `#17c` fog-only via curated Lua (`#22`); cloud/rain mid-mission **not** feasible (no DCS API) |
| Fly with a squadron / as lead or wingman (not solo only) | **M4** `#15b` done; cohesion `#15c`; orders `#15d`; **fail-to-follow discipline** → `#15e` `player-flight-discipline` |
| Spitfire Channel U-boat recon / “sub hunt” (surfaced only; not true ASW) | **M4** `#15f` `channel-uboat-recon-hunt` — builds on `#15a` recon + GA `sea_craft` / `Uboat_VIIC` |
| Sea/land targets move on a path / patrol; harbour & emplaced stay static | **M4** `#15g` `strike-target-motion` — optional `targets[].motion` → ME waypoints (ships, trucks; trains later) |
| Ground/sea target WP AI options shelf (ROE, Alarm, Disperse, …) | **M4** `#15h` `ground-target-ai-options` — curated Opt* + On Road research |
| Agent suggests recon/GA targets from a full unit list (U-boat, trucks, …) | **M3** `#8c` `agent-strike-target-catalog` — **done** (SQLite + `list_strike_targets`) |
| Agent smart-picks unit + motion + AI preset from pilot ask | **M3** `#8d` `agent-target-option-heuristics` — after `#15h` (+ `#8c`) |
| Optional engine / control / systems failures (fixed or random) | **M6** `#22b` `aircraft-failures` — ME Failures panel table; curated ids; opt-in Spec (**done** 2026-08-07) |
| ME weather panel / static objects / scenery depth for richer Channel sorties | **Research** R10 `research-me-mission-content` → promote `#17a` / `#17b` (or new ideas) |
| ME weather templates + real meteo for Channel pattern cards | **Research** R10 (+ R3 weather mentions); notes in `research/weather.md` |
| Audit owned maps (Normandy, Syria, Marianas, …) for multi-theatre expand | **Research R11 done**; product expand → **M7** (Slice 0 + 0b + F1 + F2 + F3 done; `nevada-cold-freeflight` next) |
| Which AI options apply to air vs ground vs ships | **Research** R12 `research-ai-options-by-domain` → `#15h` allowlists (**done**) |
| Full ME Options matrix (helo, armor, more ships, …) | **Research** R12b `research-ai-options-unit-matrix` — not blocking `#15h` |
| Which AAA / ground / sea / helo types ED campaigns actually use | **Research** R13 `research-campaign-unit-inventory` — promote via `#8e`; never auto-YAML |
| Adversarial “prove it wrong” findings (false-green validate, tool trust, docs honesty, CI…) | **Adversarial review track** `#31`–`#42` + expand `#30c`; notes in `docs/adversarial-review-2026-08-05.md` |

---

## Pending decisions

Resolve these inside the relevant proposal, not here.

| Question | Affects |
|----------|---------|
| Mission date (year/month/day) for the free flight | M1 (mostly settled by accepted slice) |
| Output path: `Saved Games\DCS\Missions\` vs `./out/` | M1 (default `out/` shipped) |
| CLI (`compile spec.yaml`) vs library entrypoint only | M1 (CLI shipped) |
| Clipped-wing `SpitfireLFMkIXCW` ever in scope | M2 |
| Registry storage: SQLite vs JSON/YAML tables vs both | **YAML = compile SoT**; **SQLite install** = theatres cache (`#4`); **SQLite catalog** = agent/UI queries synced from YAML (`#8a`); prefs/history in same local DB family (`#8b`) |
| Install inventory cache format / path | M2 `#4` — **decided: `%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite`; refresh on demand** |
| How much of `research/FINDINGS.md` becomes committed main specs | M2 |
| Auto-refresh of `dev-module-map` (manual vs hook on push) | M2 `#7` — **decided: hand-written doc + non-blocking push reminder; no CI generator** |
| Default squadron voice: RAF vs USAAF vs user pick | M3 `#11` — **decided: default `raf`; CLI `--voice` / pref `squadron_voice`** |
| Spec shape for LLM: hand prompt skeleton vs tool vs structured outputs | M3 `#10c` — **direction: derive from `MissionSpec` / examples; tool + small prompt reminder; structured outputs optional follow-on; SQLite cache only, never schema SoT** |
| Trigger model expressiveness: minimal condition/action set vs full DCS trigger surface | M6 `#20` — seed from R5 recurring native patterns |
| Embedded Lua snippets: `.miz` script member vs `DO SCRIPT` trigger action | M6 `#22` — **decided (after `#17c`):** prefer **`DoScriptFile` + `l10n/DEFAULT/*.lua` resource** for curated snippets; avoid DictKey `DoScript` (empty lookup → DCS executes the key name). R5 Training used DictKey inline — historical only |
| Whether to pin Mist/MOOSE as optional runtime deps (from R5 findings) | M6 `#22` — **default no** (stock Channel); revisit after R1–R2 |
| When to install VEAF MCP locally (R6) vs wait until first snippet work | R6 — **at first `#22` snippet authoring**, not during M2 |
| How / when to grow Lua snippets (`#22`) | **Decided 2026-08-06:** do **not** pre-populate a speculative catalog for agent “inspiration.” **Demand-driven:** (1) prefer native Spec triggers; (2) when a sortie need cannot be expressed natively, human or agent files a **snippet requirement** (intent, why native fails, params, ME acceptance); (3) human implements one curated template + Spec params + tests (pattern of `#17c` fog); (4) only then agent may **select + fill** that snippet. Agent never authors Lua. Optional later: chat/`needs_snippet` tool that emits the requirement brief — still no runtime Lua from the model. Inspiration for *what to build next* comes from R5/R9 gaps + real user asks, not a pile of unused scripts |
| Re-weather existing `.miz`: overwrite vs sibling file | **M5 `#17d` — decided: overwrite same path** (reload in ME after); Spec sidecar recompile preferred when YAML exists |
| Invent weather jitter always-on vs only via `randomize` / Spec flag | **M5 `#17e` — decided: always jitter** (seeded for reproducibility; goldens pin seed). Pattern class preserved |
| Spec sidecar for re-weather | **M5 `#17d` — decided: write YAML alongside `.miz`**; agent discovers sibling path or accepts explicit Spec/`.miz` path |
| Season/date → climatology priors for weather numerics | **M5 `#17e` — decided: hybrid** — within-family gallery pick weighted by date/season (+ time-of-day cues) **plus** soft numeric nudge, then always-on seeded jitter. No silent cross-family gallery swaps (agent changes `weather` pattern for that). **Place bias (Dover vs Cotentin etc.) — out of scope**; date/time + jitter enough |
| Spec shape for weather seed | **M5 `#17e` — decided:** `weather` enum + optional `weather_opts.seed`; **auto-write seed into sidecar YAML when omitted**. If reproducibility ever feels wrong, **re-weather with a new seed** (simple recovery; not a big deal). Re-weather that changes pattern also draws a new seed by default |
| Aircraft failures Spec shape (`#22b`) | **Closed 2026-08-07:** opt-in `failures[]` → ME Failures panel (`enable`/After/Within min 1/`prob`); curated Spitfire ids; brief honesty when armed |

| Section orders Spec shape (`#15d`) | **Closed 2026-08-07:** optional `player.flight.orders` curated ids → F10 `Section:…` + flags 800+ → `AITaskPush`/`GroupStop`; wingman→AI lead, lead→player group; example `manston_cap_flight_orders` |
| Section discipline Spec shape (`#15e`) | **Closed 2026-08-07:** optional `player.flight.discipline` (wingman+join_up); moving zone + soft/hard; flags 820+; hard `message_end`\|`mission_end`\|`section_rtb`; example `manston_cap_flight_discipline` |
| Strike/recon target catalog for agent (`#8c`) | **Done 2026-08-08:** `catalog_strike_units` + `list_strike_targets`; invent prompts prefer catalog ids; registry remains compile SoT |
| Agent target + option invent heuristics (`#8d`) | **Done 2026-08-08:** cue table + preferred_* meta + invent call order; hermetic tests |
| Channel invent geometry (`#8f`) | **Done 2026-08-08:** place recipes + domain repair nudges; coastal_harbour place |
| Invent path + harbour harden (`#8g`) | **Done 2026-08-08:** path clamp + harbour 120/68; live invent 6/6 |
| Theatre / target promote checklist (`#8e`) | **Done 2026-08-08:** [`THEATRE_TARGET_PROMOTE.md`](THEATRE_TARGET_PROMOTE.md) |
| Channel unit shelf expand (`#8h`) | **Done 2026-08-08:** soft + AAA + sea harbour ids; ME do-soon |
| Channel strike class shelves (`#8h`–`#8m`) | **Done** — soft/AAA/sea, halftracks, armor, troops, trains, radar |
| Normandy cold freeflight (`N1`) | **Done 2026-08-09:** bind+compile; **ME do-soon** `out/needs_oar_point_cold_freeflight.miz` |
| Campaign unit frequency inventory | **Research R13 done** — shortlist in BACKLOG; notes gitignored `research/campaign-units.md` |
| Target motion Spec shape (`#15g`) | **Closed in proposal `strike-target-motion`:** default static; optional `patrol` / short `path`; sea + soft land; harbour + AAA static; trains later; Bombing stays at strike point v1; speed bands in `target_motion.yaml` + seeded cruise / waypoint jitter; threat stop/escape deferred |
| Target threat reaction under fire (`#15g`) | **Closed for disperse:** moving land → ME Disperse Under Fire (option 8, default 180s). Further stop/dash scripting still deferred |
| Ground waypoint actions: On Road vs Off Road + formations | Folded into **`#15h`** draft (with ROE/Alarm/Engage air/…) |
| Ground target AI options Spec shelf (`#15h`) | **Done 2026-08-08:** presets + class allowlists; ME smoke do-soon |
| AI options Air vs Ground vs Naval parity | **R12 done** 2026-08-08 — feeds `#15h`; broader unit matrix → **R12b** |

---

## Working agreement

- Off `master`/`main` for all work; branch name = change name (enforced by Cursor hook + pre-commit).
- Specs before code: no implementation until a change is apply-ready and approved.
- Keep `README.md` brief and current; this file holds the sequencing detail.
