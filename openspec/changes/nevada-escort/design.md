## Context

Escort compile already uses the player airfield (`airport.position.point_from_heading`).
No intercept-spawn recipe table is required. Channel escort is a mid-Channel
package transit (120° / 55 km from Manston). Nevada CAP/intercept already
station at 350° / 40 km land (`nellis_north_range_cap`). Reusing that station
keeps geometry measured and avoids copying Manston 120/55, Incirlik 180/40,
Batumi 270/40, or Cherbourg 180/63.

## Goals / Non-Goals

**Goals:**

- Validate + compile a Nellis escort with USA Su-25T package + Russia Su-25T
  bounce on the north-range corridor (same 350/40 as CAP).
- Invent/chat may emit Nevada `escort` every turn; GA and recon still refuse.
- Channel escort goldens stay bit-identical.

**Non-Goals:**

- Domain classifier, GA/recon, path clamp, new unit ids, Instant Action as
  merge gate.
- Compiler escort rewrite or intercept_spawn edits.
- Raw map x/y in the Spec (Nellis coords are research only).

## Decisions

1. **Package destination = 350° / 40 km / 4000 m** from Nellis — same land
   station as CAP/intercept. Spec uses bearing/distance, never raw map x/y.
   Do not copy 120/55, 180/40, 270/40, or 180/63.

2. **Reuse `nellis_north_range_cap`.** Add `escort` to `mission_types`. Keep
   the CAP example path on that row. Extend `nellis_home` too. Do not invent
   a second place. Do not add an inland strike place.

3. **Modern aircraft only:** player, package, and bounce are `Su-25T` at
   251.0 MHz. Package country **USA** blue (`PackageFlight` defaults to UK).
   Bounce country **Russia** red (`EnemyFlight` defaults to ThirdReich).
   `usaaf` is voice only. Date 2024-06-06, 09:00, `sunny_clear` (not intercept
   dawn 06:00). Omit `player.payload`.

4. **Dedicated `_NEVADA_ESCORT_NOTES`.** Do not concatenate Channel `_TYPE_NOTES`
   (Manston 120/55). Schema loads `nellis_north_range_escort.yaml`. Stub LLM
   stays Manston. Drop escort from `_NEVADA_UNSUPPORTED_COMBAT` (GA + recon stay).

5. **Tests:** validate+compile new example (airdromeId 4, Su-25T, Escort task,
   start_time 32400, frequency 251.0, theatre Nevada). Invent: escort allowed;
   GA/recon still refused. Channel escort goldens unchanged.

## Open Questions

- None.
