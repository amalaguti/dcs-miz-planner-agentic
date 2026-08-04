## Context

Narrative dispatch already supports CAP and intercept. Escort Specs include nested
`escort` (airfield-relative destination) and `package`; the Manston example also has a
bounce `enemies` flight — enough for a CAP-like zone + unit_dead win pack.

## Goals / Non-Goals

**Goals:**

- Escort pack: push message; destination zone + player-coalition-in-zone callout;
  first-enemy dead → message + win.
- Same guards: empty zones/triggers; clear errors for unsupported types / missing fields.
- Example + tests + ME acceptance.

**Non-Goals:**

- GA pack; Lua; package-group death conditions; escort-without-enemies win path in v1.

## Decisions

1. **Require `escort`, non-empty `package`, and non-empty `enemies`** for escort narrative
   (win needs `unit_dead`). Pure escort-without-bounce stays hand-triggers or a later pack.
2. **Zone `escort_destination`** from `escort.bearing_deg` / `distance_km` (radius ~5000 m),
   same pattern as CAP station.
3. **Beats:** `narrative_push` (time ~120s); `narrative_with_package` (coalition in zone);
   `narrative_bandits_down` (unit_dead 0 → message + win).
4. **Refactor:** add `_apply_escort_pack`; extend unsupported-type message to include escort.

## Risks / Trade-offs

- [Risk] Win on bounce dead, not “package reached destination” → Mitigation: document;
  destination callout still fires; true package-success needs later Spec hooks.
- [Risk] Escort Specs without enemies cannot enable narrative → Mitigation: clear error;
  example includes bounce.

## Migration Plan

- Additive. Rollback: remove escort branch + example.

## Open Questions

- None blocking. GA narrative after escort accept.
