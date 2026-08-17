## MODIFIED Requirements

### Requirement: Syria invent is free_flight only
Invent/chat SHALL allow `free_flight`, `cap`, `intercept`, `escort`, and
`ground_attack` when the bound theatre is `Syria` (home `Incirlik`, `Su-25T`,
`sunny_clear`, Turkey blue; CAP/intercept/escort station 180° / 40 km south
over the Gulf of Iskenderun — not Cherbourg 180/63, not Batumi 270/40, not
Hawkinge, not escort 120/55; GA strike 121° / 200 km inland past Aleppo —
not CAP 180/40). It SHALL refuse `recon` on Syria every turn (never capture
or write a refused Spec). Repair MUST nudge toward Incirlik free_flight,
CAP, intercept, escort, or ground_attack, or switching theatre to TheChannel —
not Batumi, NeedsOarPoint, or Manston. Invent MUST NOT copy Channel, Normandy,
or Caucasus `channel_place` geometry onto Syria.

#### Scenario: Syria free_flight invent allowed
- **WHEN** invent is asked for a Syria free-flight
- **THEN** the planner MUST be allowed to emit `theatre: Syria` with
  `airfield: Incirlik`

#### Scenario: Syria CAP invent allowed
- **WHEN** invent is asked for a CAP on Syria
- **THEN** the planner MUST be allowed to emit `theatre: Syria` with
  `airfield: Incirlik` and CAP geometry from the Syria place/schema
  (MUST NOT be required to emit TheChannel, Cherbourg 180/63, or Batumi 270/40)

#### Scenario: Syria intercept invent allowed
- **WHEN** invent is asked for an intercept on Syria
- **THEN** the planner MUST be allowed to emit `theatre: Syria` with
  `airfield: Incirlik` (MUST NOT be required to emit TheChannel, Hawkinge,
  Cherbourg, or Batumi spawn)

#### Scenario: Syria escort invent allowed
- **WHEN** invent is asked for an escort on Syria
- **THEN** the planner MUST be allowed to emit `theatre: Syria` with
  `airfield: Incirlik` (MUST NOT be required to emit TheChannel or Manston
  120/55)

#### Scenario: Syria ground_attack invent allowed
- **WHEN** invent is asked for a ground attack on Syria
- **THEN** the planner MUST be allowed to emit `theatre: Syria` with
  `airfield: Incirlik` and strike geometry from the Syria inland place/schema
  (MUST NOT be required to emit TheChannel, Manston 125/76, CAP 180/40, or
  Kutaisi 43/110)

#### Scenario: Syria recon invent still refused every turn
- **WHEN** invent is asked for recon on Syria
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward Incirlik free_flight, CAP, intercept, escort, or ground_attack (or
  TheChannel combat)
