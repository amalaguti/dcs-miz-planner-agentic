## MODIFIED Requirements

### Requirement: Caucasus invent is free_flight or CAP
Invent/chat SHALL allow `free_flight` and `cap` when the bound theatre is
`Caucasus` (home `Batumi`, `Su-25T`, `sunny_clear`, Georgia blue; CAP station
from Caucasus `channel_place` meta — 270° / 40 km west over the Black Sea —
not Manston 135/25, not Cherbourg 180/63). It SHALL refuse `intercept`,
`ground_attack`, `escort`, and `recon` on Caucasus every turn (never capture
or write a refused Spec). Repair for refused types MUST nudge toward Batumi
free_flight or CAP, or switching theatre to TheChannel. Invent MUST NOT copy
Channel or Normandy `channel_place` geometry onto Caucasus.

#### Scenario: Caucasus free_flight invent allowed
- **WHEN** invent is asked for a Caucasus free-flight
- **THEN** the planner MUST be allowed to emit `theatre: Caucasus` with
  `airfield: Batumi`

#### Scenario: Caucasus CAP invent allowed
- **WHEN** invent is asked for a CAP on Caucasus
- **THEN** the planner MUST be allowed to emit `theatre: Caucasus` with
  `airfield: Batumi` and CAP geometry from the Caucasus place/schema
  (MUST NOT be required to emit TheChannel, Manston 135/25, or Cherbourg 180/63)

#### Scenario: Caucasus intercept invent still refused every turn
- **WHEN** invent is asked for an intercept on Caucasus
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward Batumi free_flight or CAP (or TheChannel combat)
