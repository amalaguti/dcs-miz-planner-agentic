---
name: dcs-dev-triggers-me
description: >-
  Native ME triggers, Failures panel, fog scripts, radio/late-activation, and
  Channel trigger research pitfalls. Use when implementing or debugging Spec
  triggers, aircraft failures, fog_dynamics, narrative/dynamics expand, Mist vs
  native ME, or compiling trigger-rich .miz files.
---

# DCS / ME triggers & failures

## Read first

Skim [`docs/lessons/triggers-me.md`](../../../docs/lessons/triggers-me.md) (newest
entries). Index: [`docs/LESSONS_LEARNED.md`](../../../docs/LESSONS_LEARNED.md).

## Hard rules

1. **Prefer native ME** over Mist/MOOSE/zip-root Lua for Channel combat behaviour
   (stock Instant Action / R1–R5 research).
2. **No LLM-authored Lua.** Curated snippets only (`DoScriptFile` / map resources).
3. **Aircraft failures** → mission-root **Failures panel** table
   (`mission.failures`: `enable` / After `hh`+`mm` / Within `mmint` / `prob`).
   - ME **Within (mm) = minutes**. Within `0` never fires; emit `mmint >= 1`.
   - Do **not** rely on trigger `a_set_failure` for Spitfire (stock unused; Within=0 pitfall).
   - Options → Misc → Random System Failures is **separate** MTBF noise.
   - Acceptance: cockpit feel + Debriefing Event `failure` (e.g. Magneto No. 1).
4. **Fog mid-sortie yes; clouds/rain/wind mid-sortie no** — use curated
   `setFogAnimation` via `DoScriptFile`, not `DoScript(mission.string(...))`
   (DictKey empty → Lua parse error). Prefer `sea_fog` for demos.
5. **Narrative XOR dynamics** expand before validate/compile; empty hand triggers.

## Code touchpoints

`compiler/triggers_emit.py`, `compiler/failures_emit.py`, `compiler/fog_emit.py`,
`narrative.py`, `dynamics.py`, `models.py` zones/triggers.
