## Context

Escort compile already uses the player airfield (`airport.position.point_from_heading`).
No intercept-spawn recipe table is required. Channel escort is a mid-Channel
package transit (120° / 55 km from Manston), not an inland strike. Caucasus
CAP/intercept already station at 270° / 40 km sea (`batumi_black_sea_cap`).
Reusing that station keeps geometry measured and avoids copying Manston 120/55
or Cherbourg 180/63.

## Goals / Non-Goals

**Goals:**

- Validate + compile a Batumi escort with Georgia Su-25T package + Russia
  Su-25T bounce on the Black Sea corridor (same 270/40 as CAP).
- Invent/chat may emit Caucasus `escort` every turn; recon still refuses.
- Channel escort goldens stay bit-identical.

**Non-Goals:**

- Recon, path clamp, new unit ids, Instant Action as merge gate.
- Compiler escort rewrite or intercept_spawn edits.

## Decisions

1. **Package destination = 270° / 40 km / 4000 m** from Batumi — same sea
   station as CAP/intercept. Channel analogue is over-water transit, not Kutaisi
   inland 43/110. Spec uses bearing/distance, never raw map x/y. Bounce is
   compile-time destination + (2500, −1500) m. Do not copy 120/55 or 180/63.

2. **Reuse `batumi_black_sea_cap`.** Add `escort` to `mission_types`. Keep the
   CAP example path on that row. Extend `batumi_home` too. Do not invent a
   second place. Do not add escort to `kutaisi_inland_strike`.

3. **Modern aircraft only:** player, package, and bounce are `Su-25T` at
   251.0 MHz. Package country **Georgia** blue (`PackageFlight` defaults to UK).
   Bounce country **Russia** red (`EnemyFlight` defaults to ThirdReich).
   MosquitoFBMkVI / Bf-109K-4 are WWII-only. Date 2024-06-06, 09:00,
   `sunny_clear` (not intercept dawn 06:00). Omit `player.payload`.

4. **Dedicated `_CAUCASUS_ESCORT_NOTES`.** Do not concatenate Channel
   `_TYPE_NOTES` (Manston 120/55). Schema loads `batumi_black_sea_escort.yaml`.
   Stub LLM stays Manston. Drop escort from `_CAUCASUS_UNSUPPORTED_COMBAT`
   (recon stays).

5. **Tests:** validate+compile new example (airdromeId 22, Su-25T, Escort task,
   start_time 32400, frequency 251.0, theatre Caucasus). Invent: escort allowed;
   recon still refused. Channel escort goldens unchanged.

## Risks / Trade-offs

- [Package over land vs sea] → 270/40 is already classified sea.
- [Invent copies 120/55] → schema/place/prompts name Batumi 270/40.
- [Omitted country defaults] → example MUST set Georgia / Russia.

## Migration Plan

Implement on `caucasus-escort`. Rollback = revert the branch. Channel goldens
must stay green.

## Open Questions

None — Instant Action is do-soon after merge, not a gate.
