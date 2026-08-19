## MODIFIED Requirements

### Requirement: Spec schema tool accepts Caucasus
`get_mission_spec_schema` SHALL accept theatre `Caucasus`. When mission type
is `free_flight`, the derived example MUST follow the Batumi envelope (not
Manston or NeedsOarPoint) with player `SpitfireLFMkIX` and notes MUST NOT
concatenate Channel/Normandy template bundles (Manston YAML paths, Spitfire
failure shelves, `channel_place` as templates to copy). When mission type is
`cap`, `ground_attack`, `intercept`, or `escort`, the derived example MUST
follow the Batumi envelope (not Manston) with player SpitfireLFMkIX. When
mission type is `recon`, the tool MUST NOT return a Channel or Normandy
combat skeleton.

#### Scenario: Caucasus free_flight schema uses Batumi
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Caucasus`
- **THEN** the example MUST use `Batumi`, `SpitfireLFMkIX`, and `Georgia`

#### Scenario: Caucasus combat schema has no Manston skeleton
- **WHEN** a caller requests a cap or intercept schema with theatre
  `Caucasus`
- **THEN** the result MUST NOT present a Manston or NeedsOarPoint example as
  the template to copy
