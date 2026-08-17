## Context

Intercept spawn is a theatre-keyed recipe table. TheChannel (Hawkinge + Dover
offset) and Normandy (NeedsOarPoint + 180° / 63 km) are populated. Caucasus CAP
already stations at 270° / 40 km from Batumi (`batumi_black_sea_cap`, domain sea).
Ground-attack inland of Kutaisi is 43/110 (land). Enemy intercept inflight belongs
on the sea station, not on Kutaisi or Hawkinge.

## Goals / Non-Goals

**Goals:**

- Validate + compile a Batumi dawn intercept with Russia Su-25T on the Black Sea
  corridor (same 270/40 as CAP).
- Invent/chat may emit Caucasus `intercept` every turn; escort/recon still refuse.
- Channel Hawkinge goldens stay bit-identical.

**Non-Goals:**

- Escort/recon, path clamp, new unit ids, Instant Action as merge gate.

## Decisions

1. **Spawn = Batumi + 270° / 40 km**, measured with PyDCS `point_from_heading`.
   Batumi (id 22) = `-355810.6875, 617386.1875`. Offset `(0, -40000)`.
   Enemy = `-355810.6875, 577386.1875`. Store these literals (same pattern as
   Hawkinge / Cherbourg). Do not call `airport_list()` at compile time. Domain of
   the station is **sea** (west-of-coast recipe). Do not copy Cherbourg
   `(-63000, 0)` or Hawkinge.

2. **Keep Channel field aliases.** Recipe storage stays `anchor_*` / `offset_*`
   with `hawkinge_*` / `dover_offset_*` properties so existing Channel tests stay
   green.

3. **Reuse `batumi_black_sea_cap`** for intercept cues (add `intercept` to
   `mission_types`). Do not invent a second place with the same numbers.

4. **Dawn 06:00** like Manston/Normandy intercept, not 09:00 CAP. Same date/weather
   as other Caucasus smokes. Enemies: Su-25T, country **Russia** red (model default
   is ThirdReich).

5. **Dedicated `_CAUCASUS_INTERCEPT_NOTES`.** Do not concatenate Channel
   `_TYPE_NOTES` (Hawkinge / Manston radio example). Schema loads
   `batumi_dawn_intercept.yaml`. Stub LLM stays Manston.

6. **Tests:** validate+compile new example (airdromeId 22, Su-25T, Russia, theatre
   Caucasus, enemy at `-355810.6875, 577386.1875`). Channel intercept recipe
   literals unchanged. Invent: intercept allowed; escort still refused. Fail-closed
   intercept moves to Syria.

## Risks / Trade-offs

- [Enemy over land] → 270/40 is already classified sea.
- [Invent copies Hawkinge] → schema/place/prompts name Batumi 270/40.

## Migration Plan

Implement on `caucasus-intercept`. Rollback = revert the branch. Channel goldens
must stay green.

## Open Questions

None — Instant Action is do-soon after merge, not a gate.
