## Context

Follow [`docs/THEATRE_TARGET_PROMOTE.md`](../../../docs/THEATRE_TARGET_PROMOTE.md)
section B. PyDCS ids verified: `Pz_IV_H`, `Stug_III`, `Cromwell_IV`,
`M4_Sherman` in `vehicle_map`. Motion profile `armor` already exists; unit map
stub was commented after `#8h`.

## Goals / Non-Goals

**Goals:** Promote armor class + four verified AFVs; motion wiring; invent cues;
example + hermetic tests.

**Non-Goals:** New AI Opt* / presets; troops/radar; ME scrape; heavy tanks
(Tiger/Panther) this batch.

## Decisions

1. **Class row** — New `strike_target_class` `armor`. Prefer path +
   `convoy_transit` (soft AI class covers non-AAA land). Dug-in static remains
   invent-optional via preferred_motion note, not a separate preset.

2. **Ids** — Axis `Pz_IV_H`, `Stug_III`; Allied practice `Cromwell_IV`,
   `M4_Sherman` (labels note UK-side / practice).

3. **Motion** — Map all four to existing `armor` profile (12–35 km/h).

4. **Place / invent** — Add `armor` to french_coast `related_classes`; cue:
   tank/armor/StuG → armor + path + convoy_transit.

5. **Accept** — Hermetic validate/compile + catalog; ME do-soon.

## Risks / Trade-offs

- [Era stretch Allied Sherman/Cromwell on Channel] → Practice/UK-side labels.
- [Soft AI for armor] → Acceptable until R12b; no new preset this change.
- [Heavy AFVs omitted] → Defer Tiger/Panther to a later expand if needed.

## Migration Plan

- Additive YAML + one example; catalog sync; no schema bump.

## Open Questions

- None.
