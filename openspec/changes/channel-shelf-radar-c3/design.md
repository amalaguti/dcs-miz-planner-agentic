## Context

Follow [`docs/THEATRE_TARGET_PROMOTE.md`](../../../docs/THEATRE_TARGET_PROMOTE.md)
section B. PyDCS ids verified: `FuMG-401`, `FuSe-65` in `vehicle_map` (vehicle
groups, not fortification statics).

## Goals / Non-Goals

**Goals:** Promote radar_c3 class + two WWII radar ids; static preferred;
invent cues; example + hermetic tests.

**Non-Goals:** Modern radars; new AI presets; `#17b` scenery; AAA class membership.

## Decisions

1. **Class** — `radar_c3`; preferred_motion **static**; preferred_ai_preset
   `convoy_transit` (soft AI — not aaa_alert; radars are not guns).

2. **Ids** — Axis `FuMG-401`, `FuSe-65` only.

3. **Motion** — No `target_motion.yaml` unit map (static like AAA).

4. **Place / invent** — Add to french_coast `related_classes`; cue:
   radar/C3/Freya/Würzburg → radar_c3 + static + convoy_transit.

5. **Accept** — Hermetic; ME do-soon.

## Risks / Trade-offs

- [Vehicle-group radar vs scenery] → Accept vehicle_map ids for strike shelf;
  scenery props stay `#17b`.
- [Soft AI on radar] → Prefer Quiet/hold later via R12b if needed; v1 soft OK.

## Migration Plan

- Additive YAML + example; catalog sync; no schema bump.

## Open Questions

- None.
