## ADDED Requirements

### Requirement: Caucasus invent is free_flight only
Invent/chat SHALL allow `free_flight` when the bound theatre is `Caucasus`
(home `Batumi`, `Su-25T`, `sunny_clear`, Georgia blue). It SHALL refuse
`intercept`, `cap`, `ground_attack`, `escort`, and `recon` on Caucasus every
turn (never capture or write a refused Spec). Repair MUST nudge toward
Batumi free_flight or switching theatre to TheChannel — not NeedsOarPoint or
Manston. Invent MUST NOT copy Channel or Normandy `channel_place` geometry
onto Caucasus.

#### Scenario: Caucasus free_flight invent allowed
- **WHEN** invent is asked for a Caucasus free-flight
- **THEN** the planner MUST be allowed to emit `theatre: Caucasus` with
  `airfield: Batumi`

#### Scenario: Caucasus CAP invent refused every turn
- **WHEN** invent is asked for a CAP on Caucasus
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward Batumi free_flight (or TheChannel combat)
