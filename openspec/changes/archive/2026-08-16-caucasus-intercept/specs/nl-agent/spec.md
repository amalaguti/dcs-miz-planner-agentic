## MODIFIED Requirements

### Requirement: Caucasus invent is free_flight or CAP
Invent/chat SHALL allow `free_flight`, `cap`, `ground_attack`, and `intercept`
when the bound theatre is `Caucasus` (home `Batumi`, `Su-25T`, `sunny_clear`,
Georgia blue; CAP/intercept station from Caucasus `channel_place` meta —
270° / 40 km west over the Black Sea — not Manston 135/25, not Cherbourg
180/63, not Hawkinge; GA strike 43° / 110 km inland past Kutaisi). It SHALL
refuse `escort` and `recon` on Caucasus every turn (never capture or write a
refused Spec). Repair for refused types MUST nudge toward Batumi free_flight,
CAP, ground_attack, or intercept, or switching theatre to TheChannel. Invent
MUST NOT copy Channel or Normandy `channel_place` geometry onto Caucasus.

#### Scenario: Caucasus intercept invent allowed
- **WHEN** invent is asked for an intercept on Caucasus
- **THEN** the planner MUST be allowed to emit `theatre: Caucasus` with
  `airfield: Batumi` (MUST NOT be required to emit TheChannel or Hawkinge spawn)

#### Scenario: Caucasus escort invent still refused every turn
- **WHEN** invent is asked for an escort on Caucasus
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  toward Batumi free_flight, CAP, ground_attack, or intercept (or TheChannel
  combat)
