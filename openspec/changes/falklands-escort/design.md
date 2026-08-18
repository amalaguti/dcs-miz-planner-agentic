## Context

Escort compile already uses the player airfield (`airport.position.point_from_heading`).
No intercept-spawn recipe table is required. Channel escort is a mid-Channel
package transit (120° / 55 km from Manston). Falklands CAP/intercept already
station at 150° / 40 km sea (`mount_pleasant_south_atlantic_cap`). Reusing that
station keeps geometry measured and avoids copying Manston 120/55, Nellis
350/40, Incirlik 180/40, Batumi 270/40, or Cherbourg 180/63.

## Goals / Non-Goals

**Goals:** validate + compile a Mount Pleasant escort; invent escort; Channel
escort goldens stay bit-identical.

**Non-Goals:** domain, GA/recon, intercept_spawn edits, Instant Action as merge
gate.

## Decisions

1. **Package destination = 150° / 40 km / 4000 m** from Mount Pleasant — same
   sea station as CAP/intercept. Spec uses bearing/distance. Do not copy
   120/55, 350/40, 180/40, 270/40, or 180/63.

2. **Reuse `mount_pleasant_south_atlantic_cap`.** Add `escort` to
   `mission_types`. Keep the CAP example path on that row. Extend
   `mount_pleasant_home` too. Do not invent a second place.

3. **Modern aircraft only:** player, package, and bounce are `Su-25T` at
   251.0 MHz. Package country **UK** blue (`PackageFlight` defaults to UK —
   still set explicitly). Bounce country **Argentina** red (`EnemyFlight`
   defaults to ThirdReich). Date 2024-06-06, 09:00, `sunny_clear` (not intercept
   dawn 06:00). Omit `player.payload`.

4. **Dedicated `_FALKLANDS_ESCORT_NOTES`.** Do not concatenate Channel
   `_TYPE_NOTES` (Manston 120/55). Schema loads
   `mount_pleasant_south_atlantic_escort.yaml`. Drop escort from
   `_FALKLANDS_UNSUPPORTED_COMBAT` (GA + recon stay).

## Open Questions

- None.
