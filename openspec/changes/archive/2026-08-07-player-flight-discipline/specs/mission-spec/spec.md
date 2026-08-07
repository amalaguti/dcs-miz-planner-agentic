## ADDED Requirements

### Requirement: Optional flight discipline
The Mission Spec SHALL allow an optional `player.flight.discipline` object. When
omitted, the compiler MUST NOT emit fail-to-follow discipline behaviour. When
present (including empty object using defaults), discipline MUST be considered
armed and MUST only apply with `role: wingman` and `join_up: true`. Fields SHALL
include radius and soft/hard timing plus a curated `hard` action id
(`message_end` | `mission_end` | `section_rtb`).

#### Scenario: Discipline object on wingman join_up accepted
- **WHEN** a Spec sets `player.flight` with `role: wingman`, `join_up: true`, and
  `discipline: {}`
- **THEN** structural load MUST succeed

#### Scenario: Omit discipline means off
- **WHEN** a Spec has `player.flight` but omits `discipline`
- **THEN** the Spec MUST remain valid without fail-to-follow emit from this feature
