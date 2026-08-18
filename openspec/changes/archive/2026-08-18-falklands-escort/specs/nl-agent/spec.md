## MODIFIED Requirements

### Requirement: Falklands invent is free_flight only
Invent/chat SHALL allow `free_flight`, `cap`, `intercept`, and `escort` when
the bound theatre is `Falklands` (home `MountPleasant`; escort destination on
the South Atlantic corridor 150° / 40 km — not Channel escort 120/55, not
Nellis 350/40, not Incirlik 180/40, not Batumi 270/40, not Cherbourg 180/63).
It SHALL refuse `ground_attack` and `recon` on Falklands every turn (never
capture or write a refused Spec). Repair MUST nudge toward Mount Pleasant
free_flight, CAP, intercept, or escort, or switching theatre to TheChannel —
not Nellis, Incirlik, Batumi, NeedsOarPoint, or Manston.

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

#### Scenario: Falklands intercept invent allowed
- **WHEN** invent is asked for an intercept on Falklands
- **THEN** the planner MUST be allowed to emit `theatre: Falklands` with
  `airfield: MountPleasant` (MUST NOT be required to emit TheChannel,
  Hawkinge, Nellis, Incirlik, Cherbourg, or Batumi spawn)

#### Scenario: Falklands escort invent allowed
- **WHEN** invent is asked for an escort on Falklands
- **THEN** the planner MUST be allowed to emit `theatre: Falklands` with
  `airfield: MountPleasant` (MUST NOT be required to emit TheChannel or
  Manston 120/55)
