## Context

Syria Stage A+B are on master. Invent is still free_flight only at Incirlik.
CAP on a valid Syria airfield already validates and compiles (airfield-relative).
Domain and intercept spawn fail closed off Channel/Normandy/Caucasus.

Live PyDCS from Incirlik (id 16, x=221207.773438, y=-35240.347656): curated
inland/Levant AFs lie 121–185° (Aleppo 121°, Palmyra 137°, Bassel Al-Assad
167°, Damascus 168°, Beirut 181°, Ramat David 185°). Due south 180° / 40 km
stays nearest Incirlik (Gulf of Iskenderun); 270° / 40 km is nearer Adana
Şakirpaşa (land). Not Batumi 270/40, not Cherbourg 180/63.

## Goals / Non-Goals

**Goals:** two places, one CAP example, invent CAP only.

**Non-Goals:** domain, intercept spawn, GA, extra countries.

## Decisions

1. **CAP-only.** Station 180° / 40 km / 4000 m from Incirlik (south, Gulf of
   Iskenderun). Leave domain fail-closed. Leave intercept fail-closed.

2. **Keep family `channel_place`.** Rows `incirlik_home` and
   `incirlik_iskenderun_cap` with `meta.theatre: Syria`.

3. **Smoke identity.** Player Turkey + Su-25T blue; enemies country `Syria` +
   Su-25T red at 251.0 MHz. Spec MUST set `enemies[].country: Syria`.

4. **Dedicated `_SYRIA_CAP_NOTES`.** Do not concatenate `_TYPE_NOTES`.

## Open Questions

- None.
