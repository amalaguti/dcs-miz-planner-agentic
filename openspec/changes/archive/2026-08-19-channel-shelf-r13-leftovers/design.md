## Context

Rescanned 60 Channel Spitfire campaign `.miz` (2026-08-19). First R13 promote
already covers flak41 / Quadmount / heavies / LST / cargo coaches. Remaining
**vehicle_map** hits not on the shelf: `v1_launcher`, `SK_C_28_naval_gun`,
`Coach a tank yellow`, `Coach a tank blue`, `Coach a platform`.

`m1_vla` and `Cow` appear often but are **not** in PyDCS vehicle/ship/fort maps
— skip. `M978 HEMTT Tanker` is modern — skip.

## Goals / Non-Goals

**Goals:** `#8e` promote those five ids; artillery static (V-1 + coastal gun);
train motion for the three coaches; invent cues (noball / ski / coastal gun).

**Non-Goals:** new classes; scenery; Essex; auto-promote.

## Decisions

1. **Artillery, not AAA** — SK C/28 is a 15 cm naval gun (surface). V-1 ski is
   an emplaced launcher. Both static + `convoy_transit` (soft), not `aaa_alert`.
2. **V-1 stays a vehicle id** — `v1_launcher` is in `vehicle_map`, so it belongs
   in `ground_units.yaml`, not scenery.
3. **Coach names keep spaces** — same pattern as `Coach cargo`.
4. **Geometry** — reuse French-coast strike belt / rail corridor; add cues only.

## Risks / Trade-offs

- [V-1 era/place stretch] → Campaigns spawn it; Pas-de-Calais ski sites are
  Channel-plausible. Label as Noball / ski.
- [SK C/28 as artillery] → If ME treats it as AAA, a later allowlist tweak is
  cheap; do not guess aaa_alert now.
