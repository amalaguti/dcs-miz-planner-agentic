## MODIFIED Requirements

### Requirement: Spec schema tool accepts theatre
`get_mission_spec_schema` SHALL accept an optional theatre id. When theatre is
`Caucasus` and mission type is `free_flight`, the derived example MUST follow
the Batumi envelope (not Manston). When theatre is `Caucasus` and mission type
is `cap`, the derived example MUST follow the Batumi Black Sea CAP envelope
(not Manston 135/25, not Cherbourg 180/63). When theatre is `Caucasus` and
mission type is `intercept`, `ground_attack`, `escort`, or `recon`, the tool
MUST NOT return a Channel or Normandy combat skeleton.

#### Scenario: Caucasus CAP schema uses Batumi
- **WHEN** a caller requests the cap Spec schema with theatre `Caucasus`
- **THEN** the example MUST use `Batumi`, `Su-25T`, CAP 270° / 40 km, and
  MUST NOT use Manston or NeedsOarPoint CAP stations

#### Scenario: Caucasus intercept schema has no Manston skeleton
- **WHEN** a caller requests an intercept schema with theatre `Caucasus`
- **THEN** the result MUST NOT present a Manston or NeedsOarPoint combat
  example as the template to copy
