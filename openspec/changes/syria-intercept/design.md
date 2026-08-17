## Context

Syria Stage C CAP is on master (`incirlik_iskenderun_cap`, 180° / 40 km).
Intercept spawn is still TheChannel / Normandy / Caucasus only.

Live PyDCS Incirlik (id 16): x=221207.773438, y=-35240.347656.
`point_from_heading(180, 40000)` → x=181207.773438, y=-35240.347656
(offset −40000, 0). Same station as CAP. Not Cherbourg 180/63, not Batumi 270/40.

## Goals / Non-Goals

**Goals:** spawn recipe, dawn intercept example, invent intercept.

**Non-Goals:** domain, GA, escort, recon.

## Decisions

1. **Reuse CAP station.** 180° / 40 km south of Incirlik (Gulf of Iskenderun).
2. **Store literals.** Do not recompute Hawkinge from `airport_list()`.
3. **Country Syria** on enemies (model default is ThirdReich).
4. **Dedicated `_SYRIA_INTERCEPT_NOTES`.** Do not concatenate `_TYPE_NOTES`.

## Open Questions

- None.
