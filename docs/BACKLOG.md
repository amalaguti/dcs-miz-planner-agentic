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

Only after M1 produces a file. Next promote: `mission-spec-schema`.

| # | Item | Goal | Status |
|---|------|------|--------|
| 2 | `mission-spec-schema` | Formalize Mission Spec (free flight + extension points for combat) | `idea` |
| 3 | `reference-registry-channel` | Queryable Channel registry (SQLite or generated tables): airfields, aircraft, weather presets, payload CLSIDs, landmarks/cities as available; agent + validator share one source of truth | `idea` |
| 4 | `installed-theatres-probe` | Detect theatres/maps present in the local DCS install so generation only offers what the user can fly | `idea` |
| 5 | `validation-engine` | Structural + DCS-exists + semantic validation with clear errors | `idea` |
| 6 | `golden-fixtures-tests` | pytest regression: spec → `.miz` structural asserts | `idea` |
| 7 | `dev-module-map` | Checked-in architecture diagram + short module relationship doc; refresh on meaningful package/layout commits (hook or CI optional later) | `idea` |

---

## M3 — Agent layer

The AI arrives only once compilation is trustworthy.

| # | Item | Goal | Status |
|---|------|------|--------|
| 8 | `agent-tools-surface` | Tools: `find_airfield`, `get_aircraft_details`, `list_mission_options`, `validate_mission_spec`, `compile_mission` (backed by registry) | `idea` |
| 9 | `mission-option-catalog` | Enumerate planning knobs the agent can ask about / suggest (start type, weather, time, opposition density, ROE seeds, payload families) before NL→spec | `idea` |
| 10 | `nl-to-spec-agent` | Natural language → Mission Spec via structured outputs + tool calling | `idea` |
| 11 | `squadron-commander-voice` | Agent persona: USAAF or RAF squadron commander tone for questions, guidance, and briefings (configurable) | `idea` |

---

## M4 — Mission types

Each is a thin slice on top of a working compiler + validator. Inspiration inputs live under Research track (below).

| # | Item | Goal | Status |
|---|------|------|--------|
| 12 | `mission-type-intercept` | Dawn Manston intercept vs Bf-109K-4 (the concept doc's example) | `idea` |
| 13 | `mission-type-cap` | Patrol station, engagement rules | `idea` |
| 14 | `mission-type-ground-attack` | Ground targets, payload selection | `idea` |
| 15 | `mission-type-escort` | Escort a friendly package | `idea` |

---

## M5 — Immersion & replayability

| # | Item | Goal | Status |
|---|------|------|--------|
| 16 | `briefing-generation` | AI briefing text into `l10n` dictionary (sortie, description, tasks); uses squadron-commander voice when enabled | `idea` |
| 17 | `weather-time-presets` | Named presets verified in-game (sunny/dawn/marginal VFR) | `idea` |
| 18 | `mission-randomization` | Seeded variation for replayability | `idea` |
| 19 | `spitfire-radio-channel-presets` | Match ED stock Spitfire radio bank (A=124, B=40, C=41, D=42, E=108.9), not only group frequency | `idea` |

---

## M6 — Mission enrichment: triggers & Lua

Goal: missions get *behaviour*, not just placement — events, radio calls, objectives that
succeed or fail. This is where Lua legitimately enters the product, as **compiler output and
curated snippets**, never as free-form LLM text.

The rule that keeps this safe: the agent chooses *which* behaviour and *what parameters*;
the trigger/script text itself is human-authored, versioned, and tested.

| # | Item | Goal | Status |
|---|------|------|--------|
| 20 | `trigger-model-spec` | Mission Spec gains a backend-agnostic condition → action model (zones, flags, time, unit state); no Lua in the Spec | `idea` |
| 21 | `trigger-compiler-native` | Compile the declared trigger model into native `.miz` trigger tables via PyDCS; golden-fixture asserts on emitted structure | `idea` |
| 22 | `script-snippet-library` | Curated, parameterised Lua snippets (human-written, tested, version-pinned) that the compiler injects for behaviour PyDCS triggers can't express; agent may only select + fill declared params | `idea` |
| 23 | `mission-events-narrative` | Use 20–22 for immersion: bandit callouts, tasking updates, RTB clearance, success/failure outcomes — in squadron-commander voice | `idea` |
| 24 | `cockpit-state-triggers` | Optional interactive/training missions driven by Spitfire cockpit arguments (promotes research R4 once verified in-game) | `idea` |

Sequencing note: 20–21 need `mission-spec-schema` (M2 `#2`), `validation-engine` (M2 `#5`) and
`golden-fixtures-tests` (M2 `#6`) first — an unvalidated trigger graph is how missions silently
break. 22 stays optional: prefer native triggers whenever they suffice. Before designing `#20`–`#22`,
prefer having **R5** findings (from R1–R2 mission/campaign Lua audits) so the trigger model matches
real Spitfire content, not a theoretical API surface.

---

## Research track (feeds M2–M6; not product features by themselves)

Work stays under gitignored `research/` until a change promotes durable facts into registry/specs/`LESSONS_LEARNED.md`.

| # | Item | Goal | Status |
|---|------|------|--------|
| R1 | `research-spitfire-user-missions` | Download/track Spitfire single missions ([DCS User Files filter](https://files.digitalcombatsimulator.com/en/files/filter/type-is-single/game-is-world_2.9/unit-is-spitfire_lf_mk.ix/apply/)); note map/aircraft reqs; extract mission-design patterns for M4; **also open each `.miz` and note how triggers / `DO SCRIPT` / embedded `.lua` are used** | `idea` |
| R2 | `research-spitfire-campaigns` | Same for campaigns ([filter](https://files.digitalcombatsimulator.com/en/files/filter/type-is-campaign/unit-is-spitfire_lf_mk.ix/apply/)); track each file; learn campaign structure; **same Lua/trigger audit as R1 across campaign missions** | `idea` |
| R3 | `research-historical-spitfire-sorties` | Web research of real historical Spitfire sorties usable as mission templates (feeds intercept/CAP/escort + historical validation) | `idea` |
| R4 | `research-spitfire-cockpit-args` | Keep [cockpit args list](https://files.digitalcombatsimulator.com/en/files/3349460/) as trigger/training reference only (see `LESSONS_LEARNED.md`); re-verify on DCS version bumps; promote only when an interactive-mission change needs it | `idea` |
| R5 | `research-lua-usage-patterns` | Synthesize R1–R2 (+ a few ED stock Channel missions): classify Lua usage — none / native triggers only / Mist·MOOSE / custom scripts; list recurring trigger patterns worth modeling in M6 `#20`–`#22`; write a short findings note under `research/` | `idea` |
| R6 | `research-lua-ide-tooling` | Lab setup for snippet authoring: pin/vendor [dcs-world-schema](https://github.com/YoloWingPixie/dcs-world-schema) (or DCS-Scripting-Library) + LuaLS in Cursor; optional VEAF MCP (`veaf-tools mcp`) only to observe how scripts/triggers land in a `.miz` — never as product compiler | `idea` |

Audit checklist for R1 / R2 / R5 (per mission, stay in `research/`):

- Has `triggers` / zones / flags?
- Inline `a_do_script` vs embedded `l10n/.../*.lua` vs external Mist/MOOSE?
- What behaviour is scripted (spawn, messages, win/fail, radio, cockpit)?
- Anything reusable as a parameterised snippet vs better as a native trigger?

---

## Later / deferred

- **Lua enrichment** — scheduled as **M6**; still never LLM-authored mission Lua.
- **Lua IDE / MCP tooling** — see research **R5–R6**. Schema + LSP for writing snippets; VEAF MCP as a lab only. A future *project-owned* MCP that exposes *our* snippet catalog (`list` / `validate_params` / API docs) is optional once M6 `#22` exists. Native Lua compiler replacing PyDCS remains far-horizon.
- **Normandy / multi-theatre** — after Channel registry pattern is solid; campaigns above are inspiration, not shipping content.
- **Historical validation engine** — date → plausible aircraft/opposition (productized form of R3).
- Multiplayer, dynamic campaign, radio VO generation.

---

## Ideas → backlog map

Source: `ideas-concepts.txt` (2026-07-26).

| Raw idea | Disposition |
|----------|-------------|
| Module diagram + relationship docs on update | **M2** `#7` `dev-module-map` |
| SQLite inventory (airports, aircraft, weapons, landmarks…) for user + agent | **M2** `#3` `reference-registry-channel` (storage may be SQLite; shape matches concept registry) |
| Detect installed maps | **M2** `#4` `installed-theatres-probe` |
| Agent narrates as US/RAF Squadron Commander | **M3** `#11` `squadron-commander-voice` (+ M5 briefings) |
| Agent knows / offers all planning options | **M3** `#9` `mission-option-catalog` + tools on `#8` |
| Lua integration? | **M6** `#20`–`#23` — enrich missions with triggers/scripts as compiler output; LLM still never authors mission Lua |
| Spitfire cockpit arguments (User Files 3349460) | **Research** R4 → **M6** `#24` once verified in-game |
| Download Spitfire campaigns / singles as inspiration | **Research** R1–R2 (+ Lua/trigger audit) → **R5** synthesis for M6 |
| Lua IDE / MCP for developing scripts | **Research** R6 (`dcs-world-schema` + LuaLS; optional VEAF MCP lab) |
| Historical Spitfire missions from the web | **Research** R3 → later historical validation |

---

## Pending decisions

Resolve these inside the relevant proposal, not here.

| Question | Affects |
|----------|---------|
| Mission date (year/month/day) for the free flight | M1 (mostly settled by accepted slice) |
| Output path: `Saved Games\DCS\Missions\` vs `./out/` | M1 (default `out/` shipped) |
| CLI (`compile spec.yaml`) vs library entrypoint only | M1 (CLI shipped) |
| Clipped-wing `SpitfireLFMkIXCW` ever in scope | M2 |
| Registry storage: SQLite vs JSON/YAML tables vs both | M2 `#3` |
| How much of `research/FINDINGS.md` becomes committed main specs | M2 |
| Auto-refresh of `dev-module-map` (manual vs hook on push) | M2 `#7` |
| Default squadron voice: RAF vs USAAF vs user pick | M3 `#11` |
| Trigger model expressiveness: minimal condition/action set vs full DCS trigger surface | M6 `#20` |
| Embedded Lua snippets: `.miz` script member vs `DO SCRIPT` trigger action | M6 `#22` |
| Whether to pin Mist/MOOSE as optional runtime deps (from R5 findings) | M6 `#22` |
| When to install VEAF MCP locally (R6) vs wait until first snippet work | R6 |

---

## Working agreement

- Off `master`/`main` for all work; branch name = change name (enforced by Cursor hook + pre-commit).
- Specs before code: no implementation until a change is apply-ready and approved.
- Keep `README.md` brief and current; this file holds the sequencing detail.
