## MODIFIED Requirements

### Requirement: Caucasus invent is free_flight or CAP
Invent/chat SHALL allow `free_flight`, `cap`, and `ground_attack` when the
bound theatre is `Caucasus` (home `Batumi`, `Su-25T`, `sunny_clear`, Georgia
blue; CAP station from Caucasus `channel_place` meta — 270° / 40 km west over
the Black Sea — not Manston 135/25, not Cherbourg 180/63; GA strike from
Caucasus inland place meta — 43° / 110 km inland past Kutaisi — not CAP
270/40). It SHALL refuse `intercept`, `escort`, and `recon` on Caucasus every
turn (never capture or write a refused Spec). Repair for refused types MUST
nudge toward Batumi free_flight, CAP, or ground_attack, or switching theatre
to TheChannel. Invent MUST NOT copy Channel or Normandy `channel_place`
geometry onto Caucasus.

#### Scenario: Caucasus free_flight invent allowed
- **WHEN** invent is asked for a Caucasus free-flight
- **THEN** the planner MUST be allowed to emit `theatre: Caucasus` with
  `airfield: Batumi`

#### Scenario: Caucasus CAP invent allowed
- **WHEN** invent is asked for a CAP on Caucasus
- **THEN** the planner MUST be allowed to emit `theatre: Caucasus` with
  `airfield: Batumi` and CAP geometry from the Caucasus place/schema
  (MUST NOT be required to emit TheChannel, Manston 135/25, or Cherbourg 180/63)

#### Scenario: Caucasus ground_attack invent allowed
- **WHEN** invent is asked for a ground attack on Caucasus
- **THEN** the planner MUST be allowed to emit `theatre: Caucasus` with
  `airfield: Batumi` and strike geometry from the Caucasus inland place/schema
  (MUST NOT be required to emit TheChannel, Manston 125/76, or CAP 270/40)

#### Scenario: Caucasus intercept invent still refused every turn
- **WHEN** invent is asked for an intercept on Caucasus
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward Batumi free_flight, CAP, or ground_attack (or TheChannel combat)
