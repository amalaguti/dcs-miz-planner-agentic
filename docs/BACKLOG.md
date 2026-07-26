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

Only after M1 produces a file.

| # | Item | Goal | Status |
|---|------|------|--------|
| 2 | `mission-spec-schema` | Formalize Mission Spec (free flight + extension points for combat) | `idea` |
| 3 | `reference-registry-channel` | Generated registry: Channel airfields (Manston=5…), aircraft ids, weather presets, payload CLSIDs | `idea` |
| 4 | `validation-engine` | Structural + DCS-exists + semantic validation with clear errors | `idea` |
| 5 | `golden-fixtures-tests` | pytest regression: spec → `.miz` structural asserts | `idea` |

---

## M3 — Agent layer

The AI arrives only once compilation is trustworthy.

| # | Item | Goal | Status |
|---|------|------|--------|
| 6 | `agent-tools-surface` | Tools: `find_airfield`, `get_aircraft_details`, `validate_mission_spec`, `compile_mission` | `idea` |
| 7 | `nl-to-spec-agent` | Natural language → Mission Spec via structured outputs + tool calling | `idea` |

---

## M4 — Mission types

Each is a thin slice on top of a working compiler + validator.

| # | Item | Goal | Status |
|---|------|------|--------|
| 8 | `mission-type-intercept` | Dawn Manston intercept vs Bf-109K-4 (the concept doc's example) | `idea` |
| 9 | `mission-type-cap` | Patrol station, engagement rules | `idea` |
| 10 | `mission-type-ground-attack` | Ground targets, payload selection | `idea` |
| 11 | `mission-type-escort` | Escort a friendly package | `idea` |

---

## M5 — Immersion & replayability

| # | Item | Goal | Status |
|---|------|------|--------|
| 12 | `briefing-generation` | AI briefing text into `l10n` dictionary (sortie, description, tasks) | `idea` |
| 13 | `weather-time-presets` | Named presets verified in-game (sunny/dawn/marginal VFR) | `idea` |
| 14 | `mission-randomization` | Seeded variation for replayability | `idea` |
| 15 | `spitfire-radio-channel-presets` | Match ED stock Spitfire radio bank (A=124, B=40, C=41, D=42, E=108.9), not only group frequency | `idea` |

---

## Later / research (not scheduled)

- **VEAF MCP** (`veaf-tools mcp`) — optional Cursor install as a research lab; steal the
  catalog/oracle patterns. Never the product compiler.
- **dcs-world-schema** — vendor EmmyLua/JSON schema only if we start authoring embedded mission Lua.
- **Normandy expansion** — reuse Spitfire campaigns (Fight or Die, Big Show, Epsom) as references.
- **Historical validation** — date → plausible aircraft/opposition.
- Multiplayer, dynamic campaign, radio VO generation, native Lua compiler (replacing PyDCS).

---

## Pending decisions

Resolve these inside the relevant proposal, not here.

| Question | Affects |
|----------|---------|
| Mission date (year/month/day) for the free flight | M1 |
| Output path: `Saved Games\DCS\Missions\` vs `./out/` | M1 |
| CLI (`compile spec.yaml`) vs library entrypoint only | M1 |
| Clipped-wing `SpitfireLFMkIXCW` ever in scope | M2 |
| How much of `research/FINDINGS.md` becomes committed main specs | M2 |

---

## Working agreement

- Off `master`/`main` for all work; branch name = change name (enforced by Cursor hook + pre-commit).
- Specs before code: no implementation until a change is apply-ready and approved.
- Keep `README.md` brief and current; this file holds the sequencing detail.
