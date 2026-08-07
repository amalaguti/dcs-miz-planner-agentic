## 1. Spec model and validation

- [x] 1.1 Add `player.flight.discipline` model (radius_m, soft_after_s, hard_after_s, hard enum) with defaults; omit = off
- [x] 1.2 Validation: wingman + join_up only; curated hard ids; radius/time bounds
- [x] 1.3 Planning-options family + schema notes for discipline

## 2. Compiler emit

- [x] 2.1 Emit moving zone on AI lead + `UnitOutsideMovingZone` soft/hard progressive triggers (flags 820+)
- [x] 2.2 Airborne gate so parking/taxi does not fire; soft message ± rejoin flag 801 when orders include rejoin
- [x] 2.3 Hard actions: `message_end` | `mission_end` | `section_rtb`

## 3. Example and tests

- [x] 3.1 Example Spec: Manston CAP wingman + join_up + discipline (+ rejoin order preferred)
- [x] 3.2 Unit tests: validation rejects; compile asserts outside-moving-zone / soft message; omit = no pack
- [x] 3.3 Brief mentions discipline when armed

## 4. Docs and smoke

- [x] 4.1 Update ARCHITECTURE / BACKLOG `#15e`; lessons + `dcs-dev-player-flight` if ME moving-zone pitfalls
- [x] 4.2 Manual Instant Action: take off, leave section → soft rejoin warn; optional hard beat once
  (Accepted 2026-08-07: ME triggers + `section_discipline_bubble` OK.
  Airborne soft/hard deferred — BACKLOG M4 do-soon.)
