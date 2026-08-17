## Context

Nevada Stage C CAP is on master (`nellis_north_range_cap`, 350° / 40 km).
Intercept spawn is still TheChannel / Normandy / Caucasus / Syria only.

Live PyDCS Nellis (id 4): x=-398195.375, y=-17233.236816.
`point_from_heading(350, 40000)` → x=-358803.06487951166,
y=-24179.163922677217 (offset +39392.31012048834, −6945.927106677216).
Same station as CAP. Not Incirlik 180/40, not Batumi 270/40, not Cherbourg
180/63, not Hawkinge.

## Goals / Non-Goals

**Goals:** spawn recipe, dawn intercept example, invent intercept.

**Non-Goals:** domain, GA, escort, recon.

## Decisions

1. **Reuse CAP station.** 350° / 40 km north of Nellis (desert north-range land).
2. **Store literals.** Do not recompute Hawkinge from `airport_list()`. Offset is
   not axis-aligned (unlike Incirlik −40000, 0).
3. **Country Russia** on enemies (model default is ThirdReich). Player USA blue.
   `usaaf` is voice only.
4. **Dedicated `_NEVADA_INTERCEPT_NOTES`.** Do not concatenate `_TYPE_NOTES`.

## Open Questions

- None.
