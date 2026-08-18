## Context

Falklands Stage A+B are on master. Invent is still free_flight only at
Mount Pleasant. CAP on a valid Falklands airfield already validates and
compiles (airfield-relative). Domain and intercept spawn fail closed off
Channel/Normandy/Caucasus/Syria/Nevada.

Live PyDCS 0.15.0 from Mount Pleasant (id 2, x=73318.320312 y=47168.748047):
Port Stanley 71.41° / 49.27 km; San Carlos FOB 311.83° / 51.91 km; Goose Green
268.80° / 36.01 km (uncurated); Gull Point 213.43° / 48.56 km (uncurated).
SSE 150° / 40 km stays nearest Mount Pleasant (South Atlantic sea; station
x=38677.3 y=67168.7). 180° / 40 km is nearer Gull Point; 270° / 40 km is
4.06 km from Goose Green; 350° / 40 km is nearer San Carlos; 090° / 40 km is
nearer Port Stanley. Not Manston 135/25, not Cherbourg 180/63, not Incirlik
180/40, not Batumi 270/40, not Nellis 350/40.

## Goals / Non-Goals

**Goals:** two places, one CAP example, invent CAP only.

**Non-Goals:** domain, intercept spawn, GA, extra countries, Chile, Port Stanley
as invent home.

## Decisions

1. **CAP-only.** Station 150° / 40 km / 4000 m from Mount Pleasant (South
   Atlantic sea). Leave domain fail-closed. Leave intercept fail-closed.

2. **Keep family `channel_place`.** Rows `mount_pleasant_home` and
   `mount_pleasant_south_atlantic_cap` with `meta.theatre: Falklands`.
   Advisory `domain: sea`. Home `mission_types: [free_flight, cap]`; CAP
   place `[cap]` only.

3. **Smoke identity.** Player UK + Su-25T blue; enemies country `Argentina` +
   Su-25T red at 251.0 MHz. Spec MUST set `enemies[].country: Argentina`. Do
   not put UK on red. Do not use Chile. `usaaf` is voice only.

4. **Dedicated `_FALKLANDS_CAP_NOTES`.** Do not concatenate `_TYPE_NOTES`.
   FF schema example stays `mount_pleasant_cold_freeflight.yaml`.

## Risks / Trade-offs

- [Advisory `domain: sea` without a classifier] → Catalog colour only; validation
  MUST NOT call `classify_domain` for Falklands CAP. Domain stay fail-closed.
- [Copying 150/40 onto later GA] → Later inland slice MUST pick a different
  station (same pitfall as Nevada 350/40 vs Creech 303/85).

## Open Questions

- None.
