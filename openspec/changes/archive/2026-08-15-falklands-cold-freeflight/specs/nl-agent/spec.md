## ADDED Requirements

### Requirement: Falklands invent is free_flight only
Invent/chat SHALL allow `free_flight` when the bound theatre is `Falklands`
(home `MountPleasant`, `Su-25T`, `sunny_clear`, UK blue). It SHALL refuse
`intercept`, `cap`, `ground_attack`, `escort`, and `recon` on Falklands every
turn (never capture or write a refused Spec). Repair MUST nudge toward Mount
Pleasant free_flight or switching theatre to TheChannel — not Nellis,
Incirlik, Batumi, NeedsOarPoint, or Manston.

#### Scenario: Falklands free_flight invent allowed
- **WHEN** invent is asked for a Falklands free-flight
- **THEN** the planner MUST be allowed to emit `theatre: Falklands` with
  `airfield: MountPleasant`

#### Scenario: Falklands CAP invent refused every turn
- **WHEN** invent is asked for a CAP on Falklands
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward Mount Pleasant free_flight (or TheChannel combat)
