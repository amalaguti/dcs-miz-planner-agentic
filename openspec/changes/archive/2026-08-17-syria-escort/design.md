## Context

Escort compile already uses the player airfield (`airport.position.point_from_heading`).
No intercept-spawn recipe table is required. Channel escort is a mid-Channel
package transit (120° / 55 km from Manston), not an inland strike. Syria
CAP/intercept already station at 180° / 40 km sea (`incirlik_iskenderun_cap`).
Reusing that station keeps geometry measured and avoids copying Manston 120/55,
Cherbourg 180/63, or Batumi 270/40.

## Goals / Non-Goals

**Goals:**

- Validate + compile an Incirlik escort with Turkey Su-25T package + Syria
  Su-25T bounce on the Iskenderun corridor (same 180/40 as CAP).
- Invent/chat may emit Syria `escort` every turn; GA and recon still refuse.
- Channel escort goldens stay bit-identical.

**Non-Goals:**

- Domain classifier, GA/recon, path clamp, new unit ids, Instant Action as
  merge gate.
- Compiler escort rewrite or intercept_spawn edits.
- Raw map x/y in the Spec (Incirlik `221207.773438` / `-35240.347656` is
  research only).

## Decisions

1. **Package destination = 180° / 40 km / 4000 m** from Incirlik — same sea
   station as CAP/intercept. Channel analogue is over-water transit, not an
   inland strike. Spec uses bearing/distance, never raw map x/y. Bounce is
   compile-time destination + (2500, −1500) m. Do not copy 120/55, 180/63, or
   270/40.

2. **Reuse `incirlik_iskenderun_cap`.** Add `escort` to `mission_types`. Keep
   the CAP example path on that row. Extend `incirlik_home` too. Do not invent
   a second place. Do not add an inland strike place.

3. **Modern aircraft only:** player, package, and bounce are `Su-25T` at
   251.0 MHz. Package country **Turkey** blue (`PackageFlight` defaults to UK).
   Bounce country **Syria** red (`EnemyFlight` defaults to ThirdReich; theatre
   id `Syria` ≠ country `Syria`). MosquitoFBMkVI / Bf-109K-4 are WWII-only.
   Date 2024-06-06, 09:00, `sunny_clear` (not intercept dawn 06:00). Omit
   `player.payload`.

4. **Dedicated `_SYRIA_ESCORT_NOTES`.** Do not concatenate Channel `_TYPE_NOTES`
   (Manston 120/55). Schema loads `incirlik_iskenderun_escort.yaml`. Stub LLM
   stays Manston. Drop escort from `_SYRIA_UNSUPPORTED_COMBAT` (GA + recon stay).

5. **Tests:** validate+compile new example (airdromeId 16, Su-25T, Escort task,
   start_time 32400, frequency 251.0, theatre Syria). Invent: escort allowed;
   GA/recon still refused. Channel escort goldens unchanged.

## Risks / Trade-offs

- [Package over land vs sea] → 180/40 is already classified sea (Gulf of
  Iskenderun). West of Incirlik is nearer uncurated Adana Şakirpaşa (id 2).
- [Invent copies 120/55 or 270/40] → schema/place/prompts name Incirlik 180/40.
- [Omitted country defaults] → example MUST set Turkey / Syria.

## Migration Plan

Implement on `syria-escort`. Rollback = revert the branch. Channel goldens
must stay green.

## Open Questions

None — Instant Action is do-soon after merge, not a gate.
