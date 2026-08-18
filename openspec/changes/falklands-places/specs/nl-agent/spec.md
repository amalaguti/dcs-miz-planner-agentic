## MODIFIED Requirements

### Requirement: Falklands invent is free_flight only
Invent/chat SHALL allow `free_flight` and `cap` when the bound theatre is
`Falklands` (home `MountPleasant`; CAP station 150° / 40 km SSE over the
South Atlantic — not Manston 135/25, not Cherbourg 180/63, not Incirlik
180/40, not Batumi 270/40, not Nellis 350/40). It SHALL refuse `intercept`,
`ground_attack`, `escort`, and `recon` on Falklands every turn (never capture
or write a refused Spec). Repair MUST nudge toward Mount Pleasant free_flight
or CAP, or switching theatre to TheChannel — not Nellis, Incirlik, Batumi,
NeedsOarPoint, or Manston.

#### Scenario: Falklands free_flight invent allowed
- **WHEN** invent is asked for a Falklands free-flight
- **THEN** the planner MUST be allowed to emit `theatre: Falklands` with
  `airfield: MountPleasant`

#### Scenario: Falklands CAP invent allowed
- **WHEN** invent is asked for a CAP on Falklands
- **THEN** the planner MUST be allowed to emit `theatre: Falklands` with
  `airfield: MountPleasant` and CAP geometry from the Falklands place/schema
  (MUST NOT be required to emit TheChannel, Manston 135/25, Cherbourg 180/63,
  Batumi 270/40, Incirlik 180/40, or Nellis 350/40)

#### Scenario: Falklands intercept invent refused every turn
- **WHEN** invent is asked for an intercept on Falklands
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward Mount Pleasant free_flight or CAP (or TheChannel combat)
