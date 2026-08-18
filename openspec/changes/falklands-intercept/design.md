## Context

Falklands Stage C CAP is on master (`mount_pleasant_south_atlantic_cap`,
150° / 40 km). Intercept spawn is still TheChannel / Normandy / Caucasus /
Syria / Nevada only.

Live PyDCS Mount Pleasant (id 2): x=73318.320312, y=47168.748047.
`point_from_heading(150, 40000)` → x=38677.30416062245, y=67168.748047
(offset −34641.016151377546, +20000.0). Same station as CAP. Not Nellis
350/40, not Incirlik 180/40, not Batumi 270/40, not Cherbourg 180/63, not
Hawkinge. Offset is not axis-aligned ±40000,0.

## Goals / Non-Goals

**Goals:** spawn recipe, dawn intercept example, invent intercept, derive
validation hint from recipe keys.

**Non-Goals:** domain, GA, escort, recon, Chile, Port Stanley as home.

## Decisions

1. **Reuse CAP station.** 150° / 40 km SSE of Mount Pleasant (South Atlantic
   sea). Leave domain fail-closed. Do not edit `channel_domain.py`.

2. **Store literals.** Do not recompute Hawkinge from `airport_list()`. Offset
   is not axis-aligned (unlike Incirlik −40000, 0). Live `offset_y` repr is
   exactly `20000.0`.

3. **Country Argentina** on enemies (model default is ThirdReich). Player UK
   blue. Do not put UK on red. Chile deferred.

4. **Dedicated `_FALKLANDS_INTERCEPT_NOTES`.** Do not concatenate `_TYPE_NOTES`.
   FF schema example stays `mount_pleasant_cold_freeflight.yaml`. CAP example
   stays `mount_pleasant_south_atlantic_cap.yaml`. Dawn intercept is 06:00
   (`start_time` 21600), not CAP 09:00.

5. **Hint from `INTERCEPT_SPAWN_RECIPES` keys.** After this slice the hint MUST
   list TheChannel, Normandy, Caucasus, Syria, Nevada, and Falklands. Tests
   MUST assert keys, not a frozen string.

## Risks / Trade-offs

- [Hardcoded hint lags again] → Derive from recipe dict; add a Kola (or other
  unbound) intercept Spec test that every key appears.
- [Copying 150/40 onto later GA] → Later inland slice MUST pick a different
  station (same pitfall as Nevada 350/40 vs Creech 303/85).

## Open Questions

- None.
