## Context

Follow [`docs/THEATRE_TARGET_PROMOTE.md`](../../../docs/THEATRE_TARGET_PROMOTE.md)
section B + `#15g` train note. PyDCS ids verified: `Locomotive`,
`German_covered_wagon_G10`, `German_tank_wagon`, `DR_50Ton_Flat_Wagon`.

## Goals / Non-Goals

**Goals:** Promote trains class + four WWII-plausible rail units; curated
`french_coast_rail_corridor` place with path recipe; invent guidance; example.

**Non-Goals:** Rail-mesh snap; modern rolling stock; new AI presets; `#8l`.

## Decisions

1. **Class** — `strike_target_class` `trains`; preferred path + `convoy_transit`.

2. **Corridor place** — Separate from `french_coast_strike_belt` so invent does
   not put trucks on “rail” recipes or invent free train paths. Same proven land
   strike band (~125°/76 km) with **elongated colinear** `path_point_deltas`
   (advisory approximate corridor — not true rail alignment).

3. **Ids** — Steam `Locomotive` + German wagons / flat; skip Electric locomotive
   and modern Coach* / Boxcartrinity.

4. **Motion** — New `train` profile (~25–55 km/h).

5. **Accept** — Hermetic; ME do-soon for visual rail vs free path.

## Risks / Trade-offs

- [Trains off real rail mesh] → Document advisory corridor; ME smoke may show
  off-track motion — acceptable for v1 Spec shelf; mesh snap still non-goal.
- [Era stretch DR flat] → Keep if PyDCS id exists; Axis German wagons preferred.

## Migration Plan

- Additive YAML + place + example; catalog sync; no schema bump.

## Open Questions

- None for v1.
