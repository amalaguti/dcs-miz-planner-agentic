## ADDED Requirements

### Requirement: Kola invent is free_flight only
Invent/chat SHALL allow `free_flight` when the bound theatre is `Kola`
(home `Bodo`, `Su-25T`, `sunny_clear`, Norway blue). It SHALL refuse
`intercept`, `cap`, `ground_attack`, `escort`, and `recon` on Kola every
turn (never capture or write a refused Spec). Repair MUST nudge toward Bodo
free_flight or switching theatre to TheChannel — not MountPleasant, Nellis,
Incirlik, Batumi, NeedsOarPoint, or Manston.

#### Scenario: Kola free_flight invent allowed
- **WHEN** invent is asked for a Kola free-flight
- **THEN** the planner MUST be allowed to emit `theatre: Kola` with
  `airfield: Bodo`

#### Scenario: Kola CAP invent refused every turn
- **WHEN** invent is asked for a CAP on Kola
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward Bodo free_flight (or TheChannel combat)
