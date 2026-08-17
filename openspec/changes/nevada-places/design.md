## Context

Nevada Stage A+B are on master. Invent is still free_flight only at Nellis.
CAP on a valid Nevada airfield already validates and compiles (airfield-relative).
Domain and intercept spawn fail closed off Channel/Normandy/Caucasus/Syria.

Live PyDCS from Nellis (id 4, x=-398195.375 y=-17233.236816): Creech 302.86° /
69.47 km; Groom Lake 327.57° / 129.84 km; North Las Vegas 259.46° / 14.74 km
(urban); Henderson Executive 196.14° / 30.35 km (urban south); Echo Bay
(uncurated) 79.32° / 51.83 km (Lake Mead). Due north-by-west 350° / 40 km stays
nearest Nellis (Desert NWR / north range land). 180° / 40 km is nearer Henderson;
270° / 40 km is nearer North Las Vegas; 79° / 40 km is Echo Bay water. Not
Incirlik 180/40, not Batumi 270/40, not Cherbourg 180/63, not Manston 135/25.

## Goals / Non-Goals

**Goals:** two places, one CAP example, invent CAP only.

**Non-Goals:** domain, intercept spawn, GA, extra countries.

## Decisions

1. **CAP-only.** Station 350° / 40 km / 4000 m from Nellis (north-range desert).
   Leave domain fail-closed. Leave intercept fail-closed.

2. **Keep family `channel_place`.** Rows `nellis_home` and
   `nellis_north_range_cap` with `meta.theatre: Nevada`. Advisory `domain: land`.
   Home `mission_types: [free_flight, cap]`; CAP place `[cap]` only.

3. **Smoke identity.** Player USA + Su-25T blue; enemies country `Russia` +
   Su-25T red at 251.0 MHz. Spec MUST set `enemies[].country: Russia`. Do not
   put USA on red. Do not use country Syria. `usaaf` is voice only.

4. **Dedicated `_NEVADA_CAP_NOTES`.** Do not concatenate `_TYPE_NOTES`.
   FF schema example stays `nellis_cold_freeflight.yaml`.

## Open Questions

- None.
