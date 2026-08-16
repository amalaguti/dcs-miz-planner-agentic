## ADDED Requirements

### Requirement: Nevada invent is free_flight only
Invent/chat SHALL allow `free_flight` when the bound theatre is `Nevada`
(home `Nellis`, `Su-25T`, `sunny_clear`, USA blue). It SHALL refuse
`intercept`, `cap`, `ground_attack`, `escort`, and `recon` on Nevada every
turn (never capture or write a refused Spec). Repair MUST nudge toward
Nellis free_flight or switching theatre to TheChannel — not Incirlik,
Batumi, NeedsOarPoint, or Manston. Invent MUST NOT copy Channel, Normandy,
Caucasus, or Syria `channel_place` geometry onto Nevada.

#### Scenario: Nevada free_flight invent allowed
- **WHEN** invent is asked for a Nevada free-flight
- **THEN** the planner MUST be allowed to emit `theatre: Nevada` with
  `airfield: Nellis`

#### Scenario: Nevada CAP invent refused every turn
- **WHEN** invent is asked for a CAP on Nevada
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward Nellis free_flight (or TheChannel combat)
