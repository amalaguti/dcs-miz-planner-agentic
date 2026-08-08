## Context

Follow [`docs/THEATRE_TARGET_PROMOTE.md`](../../../docs/THEATRE_TARGET_PROMOTE.md)
section B. PyDCS ids verified: `soldier_mauser98`, `soldier_wwii_br_01`,
`soldier_wwii_us` in `vehicle_map`. Motion profile `troops` already exists;
unit map stub was commented.

## Goals / Non-Goals

**Goals:** Promote troops class + three WWII infantry ids; motion wiring;
invent cues; example + hermetic tests.

**Non-Goals:** Modern infantry; new AI presets; radar/trains; R13 harness.

## Decisions

1. **Class row** — New `strike_target_class` `troops`. Prefer path +
   `convoy_transit` (soft AI). Dug-in static invent-optional.

2. **Ids** — Axis `soldier_mauser98`; Allied practice `soldier_wwii_br_01`,
   `soldier_wwii_us` (labels note UK-side / practice). Skip modern Soldier_* /
   Infantry AK.

3. **Motion** — Map all three to existing `troops` profile (3–8 km/h).

4. **Place / invent** — Add `troops` to french_coast `related_classes`; cue:
   infantry/troops/patrol → troops + path + convoy_transit.

5. **Accept** — Hermetic validate/compile + catalog; ME do-soon.

## Risks / Trade-offs

- [Infantry as Spit GA targets] → Soft/area targets; bombs still OK for
  training; prefer path so they aren’t invisible static dots.
- [Soft AI for troops] → Acceptable until R12b.

## Migration Plan

- Additive YAML + one example; catalog sync; no schema bump.

## Open Questions

- None.
