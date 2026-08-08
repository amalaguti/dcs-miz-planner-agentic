## Context

Validate already rejects land-on-water / sea-on-land (`motion_domain_mismatch`,
`strike_domain_mismatch`). `#8d` shelves help unit/preset pick. `channel_place`
only has `geometry_hint` strings. Accepted examples encode the real recipes
(e.g. Manston → Dunkirk inland 125°/76 km; mid-Channel ~140°/40 km).

## Goals / Non-Goals

**Goals:**

- Document copy-paste geometry bands on place cards.
- Tell invent to use them; strengthen repair when domain codes fire.
- Tests pin meta + nudge wording.

**Non-Goals:** Host auto-clamp of Spec coordinates; new maps; unit shelf growth.

## Decisions

1. **Meta recipes on `channel_place`** — Add structured fields, e.g.:
   - `strike_bearing_deg`, `strike_distance_km` (or `aoi_*` for recon)
   - `path_offsets` optional short list of relative deltas for soft path
   - `domain`: land|sea (already present)
   - `notes`: one-liner (water if distance too short inland)
   Seed from `examples/manston_ground_attack*.yaml`, `manston_uboat_*.yaml`.
   Add or enrich a harbour/coastal place if missing (static sea near coast —
   use an accepted coastal band, not 4 km from Manston).

2. **Repair nudge enrichment** — When `parse_err` / validation JSON contains
   `motion_domain_mismatch` or `strike_domain_mismatch`, append Channel place
   recipes + “land path waypoints must stay on land near strike; sea targets
   need water geometry (mid-Channel ~40 km, not UK field pattern).”

3. **Prompts/schema** — Short geometry rules next to cue table; point at
   `channel_place` meta numbers.

4. **No new tool v1** — `list_mission_options` already returns meta; optional
   later `suggest_channel_geometry(place_id)`.

## Risks / Trade-offs

- [Recipes drift from map] → Pin to checked-in examples; comment source Spec.
- [Harbour geometry ambiguous] → Prefer one documented coastal/harbour band;
  still better than 4 km Manston.

## Migration Plan

- Additive YAML + prompt text; catalog sync picks up planning_options.

## Open Questions

- None blocking — harbour place id name (`coastal_harbour` vs extend mid-Channel
  harbour_* keys only).
