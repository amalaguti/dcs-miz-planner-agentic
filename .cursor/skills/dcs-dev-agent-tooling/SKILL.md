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
   `list_strike_targets(theatre="Caucasus")` returns Ural-375 not Blitz.
   `list_strike_targets(theatre="Syria")` dual-offers those same modern **land**
   trucks at query time (stored `theatre_id` stays Caucasus).
   `list_strike_targets(theatre="Nevada")` dual-offers those same modern **land**
   trucks (same predicate). Falklands stay empty.
   Before expanding theatres or
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
   **all six types** (Batumi; CAP/intercept/escort
   270°/40 km west over the Black Sea; GA/recon AOI 43°/110 km inland past Kutaisi).
   Syria is **all six types**
   (Incirlik; CAP/intercept/escort 180°/40 km south over the Gulf of Iskenderun — not Cherbourg
   180/63, not Batumi 270/40, not Hawkinge, not escort 120/55; GA/recon AOI 121°/200 km inland past Aleppo —
   not CAP 180/40).    Nevada is **all six types** (Nellis;
   CAP/intercept/escort station 350°/40 km desert north-range — not Incirlik 180/40,
   not Batumi 270/40, not Cherbourg 180/63, not Channel escort 120/55, not Creech 303/40;
   GA/recon AOI 303°/85 km inland past Creech — not CAP 350/40).
   Falklands is **free_flight, CAP, intercept, or escort** (MountPleasant UK blue;
   CAP/intercept/escort station 150°/40 km South Atlantic sea — not Nellis 350/40,
   not Channel escort 120/55, not Hawkinge; Argentina enemies; Chile deferred; Port Stanley not CAP
   home). Extra Falklands AFs (`PortStanley`, `SanCarlosFOB`, `RioGallegos`,
   `RioGrande`, `Ushuaia`, `PuntaArenas`, `SanJulian`) are catalog/lookup;
   they MUST NOT replace the invent/schema home. Port Stanley is heli
   lookup-only. Country `Argentina` is modern-only; Channel+Argentina is
   unknown. Chile is deferred.
   Refused types refuse every turn
   (never a one-shot nudge that then captures/writes the Spec).    Host repair
   nudges MUST infer theatre from rejected JSON and pass it to
   `build_spec_schema` — do not hardcode `theatre="Normandy"`,
   `theatre="Caucasus"`, `theatre="Syria"`, or `theatre="Nevada"` on
   domain/intercept errors (Falklands must repair to Mount Pleasant FF, CAP,
   intercept, or escort 150/40 — not “switch to TheChannel for intercept”, not
   Nellis, Incirlik, Batumi, or NeedsOarPoint).
   Default Manston CAP 135/25 must
   not repair a Normandy CAP.    Domain-mismatch repair
   (`motion_domain_mismatch` / `strike_domain_mismatch`) MUST use inferred
   theatre: Channel 125/76; Caucasus Kutaisi 43/110; Normandy Maupertus
   180/133; Syria Aleppo 121/200; Nevada Creech 303/85 — never inject french_coast onto Batumi recon
   or Incirlik GA/recon, never copy CAP 180/40 onto Syria land strike or
   recon AOI, and never copy CAP 350/40 onto Nevada land strike or recon
   AOI.
   Caucasus/Syria/Nevada/Falklands `build_spec_schema` notes MUST NOT
   concatenate `_COMMON_NOTES` / `_TYPE_NOTES` (those cite Manston YAML,
   Spitfire failures, `channel_place`). Use a dedicated notes tuple
   (`_CAUCASUS_FF_NOTES` / `_CAUCASUS_CAP_NOTES` / `_CAUCASUS_GA_NOTES` /
   `_CAUCASUS_INTERCEPT_NOTES` / `_CAUCASUS_ESCORT_NOTES` /
   `_CAUCASUS_RECON_NOTES` /
   `_SYRIA_FF_NOTES` / `_SYRIA_CAP_NOTES` / `_SYRIA_INTERCEPT_NOTES` /
   `_SYRIA_ESCORT_NOTES` /    `_SYRIA_GA_NOTES` / `_SYRIA_RECON_NOTES` /
   `_NEVADA_FF_NOTES` / `_NEVADA_CAP_NOTES` / `_NEVADA_INTERCEPT_NOTES` /
   `_NEVADA_ESCORT_NOTES` /    `_NEVADA_GA_NOTES` / `_NEVADA_RECON_NOTES` /
   `_FALKLANDS_FF_NOTES` / `_FALKLANDS_CAP_NOTES` /
   `_FALKLANDS_INTERCEPT_NOTES` / `_FALKLANDS_ESCORT_NOTES`).
4. User memory tables ≠ `catalog_*`.
5. Live research: Instant Answer alone is insufficient; cascade + fixture fallback.
6. Soft immersion floor for vague invent is **TheChannel-only** (Manston
   behaviour YAML); skip `host_immersion_repair_nudge` on other theatres.
   Soft-warn missing aircraft modules.
7. Campaign Doc PDF excerpts are cached; `.cmp` vs `Doc/` inspiration paths differ.
8. Squadron voice id is **usaaf** (not usaf).

## Code touchpoints

`agent/`, `catalog/`, `memory/`, `tools/`, `immersion.py`.
