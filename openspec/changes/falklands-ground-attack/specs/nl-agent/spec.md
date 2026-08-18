## MODIFIED Requirements

### Requirement: Falklands invent is free_flight only
Invent/chat SHALL allow `free_flight`, `cap`, `intercept`, `escort`, and
`ground_attack` when the bound theatre is `Falklands` (home `MountPleasant`;
CAP/intercept/escort 150° / 40 km South Atlantic sea; GA strike 269° / 21 km
inland short of Goose Green — not CAP 150/40, not 269/36, not 269/51, not
Nevada 303/85, not Aleppo 121/200, not Kutaisi 43/110, not Channel 125/76).
It SHALL refuse `recon` on Falklands every turn (never capture or write a
refused Spec). Repair MUST nudge toward Mount Pleasant free_flight, CAP,
intercept, escort, or ground_attack, or switching theatre to TheChannel.

#### Scenario: Falklands free_flight invent allowed
- **WHEN** invent is asked for a Falklands free-flight
- **THEN** the planner MUST be allowed to emit `theatre: Falklands` with
  `airfield: MountPleasant`

#### Scenario: Falklands CAP invent allowed
- **WHEN** invent is asked for a CAP on Falklands
- **THEN** the planner MUST be allowed to emit `theatre: Falklands` with
  `airfield: MountPleasant` and CAP geometry from the Falklands place/schema
  (MUST NOT be required to emit TheChannel or Nellis 350/40)

#### Scenario: Falklands intercept invent allowed
- **WHEN** invent is asked for an intercept on Falklands
- **THEN** the planner MUST be allowed to emit `theatre: Falklands` with
  `airfield: MountPleasant`

#### Scenario: Falklands escort invent allowed
- **WHEN** invent is asked for an escort on Falklands
- **THEN** the planner MUST be allowed to emit `theatre: Falklands` with
  `airfield: MountPleasant` (MUST NOT be required to emit Manston 120/55)

#### Scenario: Falklands ground_attack invent allowed
- **WHEN** invent is asked for a ground attack on Falklands
- **THEN** the planner MUST be allowed to emit `theatre: Falklands` with
  `airfield: MountPleasant` and strike geometry from the East Falkland inland
  place/schema (MUST NOT be required to emit TheChannel, Manston 125/76,
  CAP 150/40, Nevada 303/85, Aleppo 121/200, or Kutaisi 43/110)

#### Scenario: Falklands recon invent refused every turn
- **WHEN** invent is asked for recon on Falklands
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward Mount Pleasant free_flight, CAP, intercept, escort, or ground_attack
  (or TheChannel combat)
