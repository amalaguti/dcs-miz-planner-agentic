## MODIFIED Requirements

### Requirement: Nevada invent is free_flight only
Invent/chat SHALL allow `free_flight`, `cap`, `intercept`, `escort`, and
`ground_attack` when the bound theatre is `Nevada` (home `Nellis`, `Su-25T`,
`sunny_clear`, USA blue; CAP/intercept/escort station 350° / 40 km north over
desert north-range land — not Cherbourg 180/63, not Batumi 270/40, not Incirlik
180/40, not Manston escort 120/55; GA strike 303° / 85 km inland past Creech —
not CAP 350/40). It SHALL refuse `recon` on Nevada every turn (never capture
or write a refused Spec). Repair MUST nudge toward Nellis free_flight, CAP,
intercept, escort, or ground_attack, or switching theatre to TheChannel — not
Incirlik, Batumi, NeedsOarPoint, or Manston. Invent MUST NOT copy Channel,
Normandy, Caucasus, or Syria `channel_place` geometry onto Nevada.

#### Scenario: Nevada free_flight invent allowed
- **WHEN** invent is asked for a Nevada free-flight
- **THEN** the planner MUST be allowed to emit `theatre: Nevada` with
  `airfield: Nellis`

#### Scenario: Nevada CAP invent allowed
- **WHEN** invent is asked for a CAP on Nevada
- **THEN** the planner MUST be allowed to emit `theatre: Nevada` with
  `airfield: Nellis` and CAP geometry from the Nevada place/schema
  (MUST NOT be required to emit TheChannel, Cherbourg 180/63, Batumi 270/40,
  or Incirlik 180/40)

#### Scenario: Nevada intercept invent allowed
- **WHEN** invent is asked for an intercept on Nevada
- **THEN** the planner MUST be allowed to emit `theatre: Nevada` with
  `airfield: Nellis` (MUST NOT be required to emit TheChannel, Hawkinge,
  Incirlik, Cherbourg, or Batumi spawn)

#### Scenario: Nevada escort invent allowed
- **WHEN** invent is asked for an escort on Nevada
- **THEN** the planner MUST be allowed to emit `theatre: Nevada` with
  `airfield: Nellis` (MUST NOT be required to emit TheChannel or Manston
  120/55)

#### Scenario: Nevada ground_attack invent allowed
- **WHEN** invent is asked for a ground attack on Nevada
- **THEN** the planner MUST be allowed to emit `theatre: Nevada` with
  `airfield: Nellis` and strike geometry from the Nevada inland place/schema
  (MUST NOT be required to emit TheChannel, Manston 125/76, CAP 350/40,
  Aleppo 121/200, or Kutaisi 43/110)

#### Scenario: Nevada recon invent still refused every turn
- **WHEN** invent is asked for recon on Nevada
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward Nellis free_flight, CAP, intercept, escort, or ground_attack (or
  TheChannel combat)
