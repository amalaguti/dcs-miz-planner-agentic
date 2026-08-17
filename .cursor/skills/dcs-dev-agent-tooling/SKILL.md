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
   (`list_strike_targets`), not an ME/install dump. Schema v6: WWII rows
   `era_id=wwii` and combat `theatre_id=TheChannel`. Modern trucks
   `era_id=modern` / `theatre_id=Caucasus`. `list_strike_targets(theatre="Normandy")`
   returns WWII **land** units (sea_craft stay Channel-only).
   `list_strike_targets(theatre="Caucasus")` returns Ural-375 not Blitz. Before expanding theatres or
   target shelves, follow [`docs/THEATRE_TARGET_PROMOTE.md`](../../../docs/THEATRE_TARGET_PROMOTE.md)
   (`#8e`). Local gitignored `research/` QAG HTML is `research_guidance` colour
   only — never ship those pages, never auto-promote QAG UI names into catalog
   YAML. Invent unit/preset cues ≠ geometry — use place recipes + invent path
   clamp (`#8f`/`#8g`) **only when Spec theatre is TheChannel**. Trains use
   `french_coast_rail_corridor` path deltas only —
   **no** DCS rail-mesh snap (`#8m`).    Invent may use offerable theatres; Normandy is **all six types**
   (NeedsOarPoint; CAP/intercept/escort 180°/63 km Cherbourg
   corridor, not Hawkinge, not Manston escort 120/55; GA/recon AOI 180°/133 km
   inland of Maupertus). Caucasus is
   **free_flight, CAP, ground_attack, or intercept** (Batumi; CAP/intercept
   270°/40 km west over the Black Sea; GA 43°/110 km inland past Kutaisi;
   escort/recon refused).
   Syria is **free_flight only**
   (Incirlik; CAP refused). Nevada is **free_flight only** (Nellis; CAP
   refused). Falklands is **free_flight only** (MountPleasant; CAP refused).
   Refused types refuse every turn
   (never a one-shot nudge that then captures/writes the Spec). Host repair
   nudges MUST infer theatre from rejected JSON and pass it to
   `build_spec_schema` — do not hardcode `theatre="Normandy"`,
   `theatre="Caucasus"`, `theatre="Syria"`, or `theatre="Nevada"` on
   domain/intercept errors (Falklands must repair to Mount Pleasant FF, not
   Nellis, Incirlik, Batumi, or NeedsOarPoint).
   Default Manston CAP 135/25 must
   not repair a Normandy CAP. Caucasus/Syria/Nevada/Falklands `build_spec_schema` notes MUST NOT
   concatenate `_COMMON_NOTES` / `_TYPE_NOTES` (those cite Manston YAML,
   Spitfire failures, `channel_place`). Use a dedicated notes tuple
   (`_CAUCASUS_FF_NOTES` / `_CAUCASUS_CAP_NOTES` / `_CAUCASUS_GA_NOTES` /
   `_SYRIA_FF_NOTES` / `_NEVADA_FF_NOTES` / `_FALKLANDS_FF_NOTES`).
4. User memory tables ≠ `catalog_*`.
5. Live research: Instant Answer alone is insufficient; cascade + fixture fallback.
6. Soft immersion floor for vague invent is **TheChannel-only** (Manston
   behaviour YAML); skip `host_immersion_repair_nudge` on other theatres.
   Soft-warn missing aircraft modules.
7. Campaign Doc PDF excerpts are cached; `.cmp` vs `Doc/` inspiration paths differ.
8. Squadron voice id is **usaaf** (not usaf).

## Code touchpoints

`agent/`, `catalog/`, `memory/`, `tools/`, `immersion.py`.
