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

---

## M4 — Mission types

**Next promote / in proposal:** (see M6 — prefer narrative events / snippets as needed)

| # | Item | Goal | Status |
|---|------|------|--------|
| 12 | `mission-type-intercept` | Dawn Manston intercept vs Bf-109K-4 (the concept doc's example) | `done` (accepted in-game 2026-07-26; ThirdReich/red) |
| 13 | `mission-type-cap` | Patrol station, engagement rules | `done` (accepted in-game 2026-08-01) |
| 14 | `mission-type-ground-attack` | Ground targets, payload selection | `done` (accepted in-game 2026-08-02; Dunkirk inland + slipper) |
| 15 | `mission-type-escort` | Escort a friendly package | `done` (accepted in-game 2026-08-02; Mosquito package + bounce) |
| 15a | `mission-type-recon` | Locate / observe a place or contact (GA-like geometry + marks/zones) **without** strike/payload attack; win on find/RTB rather than destroy | `idea` (after `#30e`/`#30f`; may stay GA+behaviours until Spec needs a distinct type) |

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
| 17c | `weather-in-flight-fog` | Optional mid-sortie **fog** evolution (foggy→clear / clear→fog) via curated `world.weather.setFogAnimation` snippets — **not** sunny→rainy cloud swaps (no DCS API). After `#17a`; needs `#22` or fog-only snippet slice. Full in-flight cloud/rain deferred until ED APIs exist | `idea` (feasibility 2026-08-06; fog-only) |
| 17d | `weather-reweather-miz` | Agent + CLI: change weather on an **existing** `.miz` (named pattern / NL → recipe) and **overwrite** the same path — same sortie (groups/triggers), new static weather. Write Spec YAML alongside `.miz`; agent finds sibling or takes an explicit path. Prefer Spec recompile when YAML exists; else PyDCS `load_file` → apply invent snapshot → `save`. Not mid-flight. After `#17a`/`#17e` | `done` (accepted ME smoke 2026-08-06; rain_overcast → Overcast and Rain 2) |
| 17e | `weather-invent-jitter` | **Always-on** seeded invent variation around `#17a` patterns. **Hybrid priors:** (1) **within-family gallery preference** weighted by Spec **date/season** (+ start **time** where useful, e.g. morning fog risk) — pick among allowed `PresetN`/`RainyPresetN` for that pattern class, never silent cross-family swaps; (2) **soft nudge** on temp/QNH/wind layers/turb/fog/base after gallery pick; (3) seeded jitter for day-to-day noise. Climatology from `research/weather.md` (Channel seasonal — **no per-place bias**). Distinct from ME Dynamic cyclones and `#17c`. Goldens pin seed. Spec: `weather` enum + `weather_opts.seed` (auto-write if omitted) | `done` (accepted ME smoke 2026-08-06; seed42 vs seed99 broken) |

---

## M6 — Mission enrichment: triggers & Lua

**Next promote / in proposal:** `#22` only if native insufficient; R8 when bumping pydcs; R1/R2 deep `.miz` audits

Goal: missions get *behaviour*, not just placement — events, radio calls, objectives that
succeed or fail. This is where Lua legitimately enters the product, as **compiler output and
curated snippets**, never as free-form LLM text.

The rule that keeps this safe: the agent chooses *which* behaviour and *what parameters*;
the trigger/script text itself is human-authored, versioned, and tested.

| # | Item | Goal | Status |
|---|------|------|--------|
| 20 | `trigger-model-spec` | Mission Spec gains a backend-agnostic condition → action model (zones, flags, time, unit state); no Lua in the Spec | `done` (2026-08-02; validate OK, compile deferred to `#21`) |
| 21 | `trigger-compiler-native` | Compile the declared trigger model into native `.miz` trigger tables via PyDCS; golden-fixture asserts on emitted structure | `done` (accepted in-game 2026-08-02; sample message ~T+120) |
| 22 | `script-snippet-library` | Curated, parameterised Lua snippets (human-written, tested, version-pinned) that the compiler injects for behaviour PyDCS triggers can't express; agent may only select + fill declared params | `idea` |
| 22a | `trigger-flag-random` | Spec action for ME Set Flag Random (`a_set_flag_random`) so “dynamic” raid dice stay native (R1 Version_2 / community BoB) — prefer before Mist/`#22` | `done` (2026-08-05) |
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

Audit checklist for R1 / R2 / R5 (per mission, stay in `research/`):

- Has `triggers` / zones / flags?
- Inline `a_do_script` vs embedded `l10n/.../*.lua` vs external Mist/MOOSE?
- What behaviour is scripted (spawn, messages, win/fail, radio, cockpit)?
- Anything reusable as a parameterised snippet vs better as a native trigger?

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
- **Normandy / multi-theatre** — after Channel registry pattern is solid; campaigns above are inspiration, not shipping content.
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
| ME weather panel / static objects / scenery depth for richer Channel sorties | **Research** R10 `research-me-mission-content` → promote `#17a` / `#17b` (or new ideas) |
| ME weather templates + real meteo for Channel pattern cards | **Research** R10 (+ R3 weather mentions); notes in `research/weather.md` |
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
| Embedded Lua snippets: `.miz` script member vs `DO SCRIPT` trigger action | M6 `#22` — R5 Training uses DictKey + `a_do_script`, not zip-root `.lua` |
| Whether to pin Mist/MOOSE as optional runtime deps (from R5 findings) | M6 `#22` — **default no** (stock Channel); revisit after R1–R2 |
| When to install VEAF MCP locally (R6) vs wait until first snippet work | R6 — **at first `#22` snippet authoring**, not during M2 |
| Re-weather existing `.miz`: overwrite vs sibling file | **M5 `#17d` — decided: overwrite same path** (reload in ME after); Spec sidecar recompile preferred when YAML exists |
| Invent weather jitter always-on vs only via `randomize` / Spec flag | **M5 `#17e` — decided: always jitter** (seeded for reproducibility; goldens pin seed). Pattern class preserved |
| Spec sidecar for re-weather | **M5 `#17d` — decided: write YAML alongside `.miz`**; agent discovers sibling path or accepts explicit Spec/`.miz` path |
| Season/date → climatology priors for weather numerics | **M5 `#17e` — decided: hybrid** — within-family gallery pick weighted by date/season (+ time-of-day cues) **plus** soft numeric nudge, then always-on seeded jitter. No silent cross-family gallery swaps (agent changes `weather` pattern for that). **Place bias (Dover vs Cotentin etc.) — out of scope**; date/time + jitter enough |
| Spec shape for weather seed | **M5 `#17e` — decided:** `weather` enum + optional `weather_opts.seed`; **auto-write seed into sidecar YAML when omitted**. If reproducibility ever feels wrong, **re-weather with a new seed** (simple recovery; not a big deal). Re-weather that changes pattern also draws a new seed by default |

---

## Working agreement

- Off `master`/`main` for all work; branch name = change name (enforced by Cursor hook + pre-commit).
- Specs before code: no implementation until a change is apply-ready and approved.
- Keep `README.md` brief and current; this file holds the sequencing detail.
