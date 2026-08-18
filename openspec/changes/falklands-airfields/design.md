## Context

Stage A bound Falklands with MountPleasant=2, UK, Su-25T 251.0 MHz, invent
free_flight only. Live PyDCS `Falklands.airport_list()` has 27 airports
(ids 4 and 28 absent). Numeric ids collide (Rio Gallegos 5 vs Manston 5;
Mount Pleasant 2 vs Groom Lake 2 vs Merville Calonne 2). PyDCS country
`Argentina` (id 83) is not pre-parked on a coalition; extra-AF smoke still
uses Argentina red (Palmyra-style opposing host). Chile deferred.

## Goals / Non-Goals

**Goals:**

- Curate eight verified Falklands airfields (not all 27).
- Add country `Argentina` to era/modern only; keep Su-25T as the only
  modern player type.
- Compile a Rio Gallegos free-flight smoke (Argentina red) without lifting
  combat invent.
- Infer theatre from the eight Spec keys; keep `Mount_Pleasant`; lookup
  stays theatre-scoped. Port Stanley is findable, not a compile home.

**Non-Goals:**

- Places, CAP/GA, domain, intercept spawn, Chile, dual-offer, dump of 27
  fields, payloads, invent home change.

## Decisions

1. **Eight airfields, not 27.** Verified keys: `MountPleasant=2`,
   `PortStanley=1`, `SanCarlosFOB=3`, `RioGallegos=5`, `RioGrande=6`,
   `Ushuaia=7`, `PuntaArenas=9`, `SanJulian=11`. Skip Franco Bianco (thin)
   and the rest of the 27. Do not invent ids 4 or 28. Alternative (dump
   every AF) rejected — Caucasus/Syria/Nevada curated 8.

2. **Country Argentina modern, not WWII; player still Su-25T.** Era-keyed
   like Turkey/Russia/Syria. Adding the country makes it valid on
   Caucasus/Nevada/Syria too (same leak as Georgia). Channel+Argentina MUST
   fail unknown-country. Do not add Chile this slice.

3. **Rio Gallegos example is Argentina red.** Palmyra pattern (opposing
   continental host). Invent/schema stay MountPleasant UK blue. Stub LLM
   stays Manston. RioGallegos 5 is not Manston 5. Radio 251.0 (not ATC).
   Date 2024-06-06 so WWII realism no-ops.

4. **Port Stanley is lookup-only (heli).** Include the key for catalog /
   `find_airfield`. Do not ship a Su-25T compile example there. Extra-AF
   smoke is RioGallegos only.

5. **infer_theatre maps the eight camelCase keys** and keeps
   `Mount_Pleasant`. Combat refuse unchanged. Registry MUST reject
   `Port_Stanley`, `Rio_Gallegos`, `San_Carlos_FOB`, `Rio_Grande`,
   `Punta_Arenas`, `San_Julian`. Infer MUST return None for those
   underscore forms (same as `Groom_Lake`).

6. **N1-style Rio Gallegos contracts**, not a full golden. Assert
   `airdromeId=5` on Falklands theatre (not Channel Manston). Include
   country `Argentina`.

## Risks / Trade-offs

- [RioGallegos 5 confused with Manston] → theatre-scoped lookup + compile
  zip theatre Falklands, not TheChannel.
- [Argentina on Channel] → era filter; Channel+Argentina unknown_country.
- [Invent copies Rio Gallegos as home] → schema/notes stay MountPleasant.
- [Su-25T at Port Stanley] → no example; lookup-only.
- [Chile skipped] → PuntaArenas remains lookup this slice.

## Migration Plan

Implement on `falklands-airfields`. Rollback = revert the branch. Channel
goldens must stay green. After merge: `dcs-miz theatres --refresh`. Next
OpenSpec: `falklands-places` (Stage C CAP).

## Open Questions

None — Instant Action is do-soon after merge, not a gate.
