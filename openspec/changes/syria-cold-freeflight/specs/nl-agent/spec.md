## ADDED Requirements

### Requirement: Syria invent is free_flight only
Invent/chat SHALL allow `free_flight` when the bound theatre is `Syria`
(home `Incirlik`, `Su-25T`, `sunny_clear`, Turkey blue). It SHALL refuse
`intercept`, `cap`, `ground_attack`, `escort`, and `recon` on Syria every
turn (never capture or write a refused Spec). Repair MUST nudge toward
Incirlik free_flight or switching theatre to TheChannel — not Batumi,
NeedsOarPoint, or Manston. Invent MUST NOT copy Channel, Normandy, or
Caucasus `channel_place` geometry onto Syria.

#### Scenario: Syria free_flight invent allowed
- **WHEN** invent is asked for a Syria free-flight
- **THEN** the planner MUST be allowed to emit `theatre: Syria` with
  `airfield: Incirlik`

#### Scenario: Syria CAP invent refused every turn
- **WHEN** invent is asked for a CAP on Syria
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward Incirlik free_flight (or TheChannel combat)
