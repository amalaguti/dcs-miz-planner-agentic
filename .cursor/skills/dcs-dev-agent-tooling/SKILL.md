---
name: dcs-dev-agent-tooling
description: >-
  NL agent, catalog, user memory, research, immersion floor, and aircraft-module
  cache pitfalls. Use when changing planner/tools/catalog/memory, invent prompts,
  research_guidance, or soft immersion / module warnings.
---

# Agent, catalog & research

## Read first

[`docs/lessons/agent-tooling.md`](../../../docs/lessons/agent-tooling.md)

## Hard rules

1. Agent Spec invent uses **derived schema examples**, not hand-maintained skeletons.
2. Tools return **structured dicts**; no dedicated research CLI required.
3. Catalog shares `inventory.sqlite` as query layer — Channel YAML remains SoT;
   schema bumps must clear `synced_at`. Strike units are a **curated** YAML shelf
   (`list_strike_targets`), not an ME/install dump. Before expanding theatres or
   target shelves, follow [`docs/THEATRE_TARGET_PROMOTE.md`](../../../docs/THEATRE_TARGET_PROMOTE.md)
   (`#8e`). Invent unit/preset cues ≠ geometry — use place recipes + invent path
   clamp (`#8f`/`#8g`). Trains use `french_coast_rail_corridor` path deltas only —
   **no** DCS rail-mesh snap (`#8m`).
4. User memory tables ≠ `catalog_*`.
5. Live research: Instant Answer alone is insufficient; cascade + fixture fallback.
6. Soft immersion floor for vague invent; soft-warn missing aircraft modules.
7. Campaign Doc PDF excerpts are cached; `.cmp` vs `Doc/` inspiration paths differ.
8. Squadron voice id is **usaaf** (not usaf).

## Code touchpoints

`agent/`, `catalog/`, `memory/`, `tools/`, `immersion.py`.
