---
name: full-catalog-orchestrator
description: >-
  Orchestrates sequential full-catalog OpenSpec slices so the NL agent can plan
  missions on all PyDCS-bound installed maps. Use when the user runs
  /full-catalog-orchestrate, starts theatre-registry-packages or
  theatre-agnostic-planning, expands a map beyond Channel, or works in Agents
  Window on the multi-theatre catalog campaign.
---

# Full-catalog orchestrator

Parent agent in Agents Window (or chat) coordinates specialists. **You** do not
spawn a seventh “orchestrator” subagent.

Baseline: tag `v0.4_the_channel`. Channel is complete; Normandy has FF + CAP + GA + intercept + escort + recon smoke (all six types). Caucasus Stage C: Batumi places + Black Sea CAP (270°/40 km); invent FF+CAP. Caucasus GA: Batumi inland strike 43°/110 km past Kutaisi; invent FF+CAP+GA. Caucasus intercept: Batumi dawn intercept on the Black Sea corridor (270°/40 km); invent FF+CAP+GA+intercept; escort/recon still refuse.

## Read

- `docs/THEATRE_TARGET_PROMOTE.md` — promote checklist (`#8e`)
- `docs/BACKLOG.md` — campaign table (M7)
- [reference.md](reference.md) — resource taxonomy + Channel-hardcoded gaps
- Subagents: `.cursor/agents/*.md`

## Hard rules

1. One OpenSpec change = one git branch = one writer (`implementer`).
2. Never invent DCS ids. Never auto-promote discovery into YAML.
3. Merge gate: ruff + `uv run pytest -q` + compile new examples + Agent Review.
   ME Instant Action is human **do-soon after merge**.
4. **Slice 0b gate:** no Stage C combat (places + intercept/GA/etc.) on a new
   map until `theatre-agnostic-planning` is on master.
5. No PyDCS terrain → no Spec bind (today: `MarianaIslandsWWII`, `Kola`, `Iraq`).
6. Do not `/in-cloud` two theatres. Optional `/babysit` on the current PR only.
7. OpenSpec CLI: `npx openspec` (not `uv openspec`).

## Campaign order

1. `theatre-registry-packages` (Slice 0) — split `data/channel/` into per-theatre
   packages; registry loader walks them; Channel goldens + Normandy smoke stay green.
2. `theatre-agnostic-planning` (Slice 0b) — unhardcode domain, invent, countries,
   intercept spawn, path clamp, strike-unit tags, reweather/METAR.
3. Refresh `dcs-miz theatres --refresh`. Then sequential maps:
   - Normandy deepen (WWII, already bound)
   - Caucasus → Syria → Nevada → Falklands (`Falklands`)
   - Unbound terrains stay discovered-only

Per-map stages (separate OpenSpecs):

| Stage | Exit |
|-------|------|
| A Bind + smoke | theatre + terrain + 1 AF + 1 country/aircraft/radio + weather + freeflight example + pytest |
| B Geography + identity | more AFs; era countries; player aircraft; catalog offerable |
| C Places + 1 combat type | `theatre_place` + domain + one combat example (**needs 0b**) |
| D Units + invent | shelves, payloads, strike classes, invent cues |

## Loop (every slice)

1. Branch = change name (`openspec-git-branch`). Not `master`/`main`.
2. Built-in **Explore** for code that will move.
3. `/theatre-researcher` (and `/catalog-units` / `/mission-catalog` as needed).
4. `/planner` → `/opsx-propose` until apply-ready.
5. `/implementer` (only writer; may consult readonly specialists).
6. `/verifier` — `uv sync --frozen --group dev`; ruff check/format `--check`;
   `uv run pytest -q`; compile new example Spec.
7. **Agent Review** `/agent-review`: Deep if registry/compiler/validation;
   Quick if docs-only.
8. `openspec-finish-change`: docs → impl commit → archive+spec sync commit →
   **ask merge**.
9. Pause until master has the merge.

## Parallelism

- **Forbidden:** two implementers; two map branches touching `registry.py`,
  `theatre_terrain.py`, catalog sync, `tests/conftest.py`, or `openspec/specs/`
  at once.
- **Allowed:** readonly Explore + theatre-researcher on map N+1 writing only
  gitignored `research/theatres/`.

## Specialists

| Subagent | Owns |
|----------|------|
| `planner` | One-change technical plan |
| `implementer` | Only code/YAML writer |
| `verifier` | Skeptical ruff/pytest/compile |
| `theatre-researcher` | Map id, PyDCS, AFs/FARPs, places, domain |
| `catalog-units` | Countries, air/helo/ground/sea, payloads, failures, radios |
| `mission-catalog` | Invent, places-as-planning, examples, weather-as-planning |

Handoff fields (every subagent): `slice`, `change_name`, `branch`,
`findings` or `files_touched`, `verified_ids`, `tests_run`, `blockers`,
`next_agent`.

## Target vs non-goals

**Target:** existing six mission types on every **installed + PyDCS-bound** map.

**Not this campaign:** AAR/SEAD/helo/carrier spawn types; ME unit-tree dumps;
liveries as Spec ids; LLM Lua; auto-promote; terrains without PyDCS.
