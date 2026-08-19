## ADDED Requirements

### Requirement: Modern-theatre schema player is Spitfire
`get_mission_spec_schema` / `build_spec_schema` for theatres `Caucasus`,
`Syria`, `Nevada`, `Falklands`, and `Kola` MUST return example
`player.aircraft` `SpitfireLFMkIX`. Station geometry, airfield, and country
MUST stay the theatre envelope. Escort `package` and combat `enemies` MAY
remain Su-25T for Cold War defaults. Ground-attack example `player.payload`
MUST be a Spitfire preset (`spitfire_2x250_slipper`), not a Su-25T FAB load.
Notes MUST state the Spitfire player rule and MUST NOT copy Channel 135/25
onto these maps. Packaged compile YAML MAY still show Su-25T as map-smoke.

#### Scenario: Caucasus free_flight schema player is Spitfire
- **WHEN** a caller requests the free_flight Spec schema with theatre `Caucasus`
- **THEN** the example MUST use `Batumi`, `SpitfireLFMkIX`, and `Georgia`
  (MUST NOT use Su-25T in `player.aircraft`)

#### Scenario: Syria ground_attack schema payload matches Spitfire
- **WHEN** a caller requests the ground_attack Spec schema with theatre `Syria`
- **THEN** the example MUST use `player.aircraft` SpitfireLFMkIX and
  `player.payload` spitfire_2x250_slipper at Incirlik (geometry 121° / 200 km)

#### Scenario: Kola free_flight schema player is Spitfire
- **WHEN** a caller requests the free_flight Spec schema with theatre `Kola`
- **THEN** the example MUST use `Bodo` and `SpitfireLFMkIX`

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
