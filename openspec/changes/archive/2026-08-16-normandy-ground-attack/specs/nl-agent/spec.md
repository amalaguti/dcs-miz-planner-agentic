## MODIFIED Requirements

### Requirement: Normandy invent is free_flight or CAP
Invent/chat SHALL allow `free_flight`, `cap`, and `ground_attack` when the
bound theatre is `Normandy` (home `NeedsOarPoint`, CAP station from Normandy
`channel_place` meta — 180° / 63 km — not Manston 135/25; GA strike from
Normandy inland place meta — 180° / 133 km — not Manston 125/76). It SHALL
refuse `intercept`, `escort`, and `recon` on Normandy every turn (never
capture or write a refused Spec). Repair for refused types MUST nudge toward
NeedsOarPoint free_flight, CAP, or ground_attack, or switching theatre to
TheChannel. Invent MUST NOT copy Channel `channel_place` geometry (french
coast belts, Hawkinge/Dunkirk bearings) onto Normandy.

#### Scenario: Normandy CAP invent allowed
- **WHEN** invent is asked for a CAP on Normandy
- **THEN** the planner MUST be allowed to emit `theatre: Normandy` with
  `airfield: NeedsOarPoint` and CAP geometry from the Normandy place/schema
  (MUST NOT be required to emit TheChannel or Manston 135/25)

#### Scenario: Normandy ground_attack invent allowed
- **WHEN** invent is asked for a ground attack on Normandy
- **THEN** the planner MUST be allowed to emit `theatre: Normandy` with
  `airfield: NeedsOarPoint` and strike geometry from the Normandy inland
  place/schema (MUST NOT be required to emit TheChannel or Manston 125/76)

#### Scenario: Normandy intercept invent still refused every turn
- **WHEN** invent is asked for an intercept on Normandy
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward NeedsOarPoint free_flight, CAP, or ground_attack (or TheChannel
  combat)
