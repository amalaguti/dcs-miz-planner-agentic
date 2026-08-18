## MODIFIED Requirements

### Requirement: Extra Falklands airfields validate
Shared validation SHALL accept a well-formed Falklands free-flight Spec whose
player airfield is a curated extra Falklands key (e.g. `RioGallegos`) when
inventory agrees. Channel/Normandy MUST still reject country `Argentina` as
unknown-country. Recon invent on Falklands MUST still be rejected.

#### Scenario: Rio Gallegos freeflight validates
- **WHEN** `examples/rio_gallegos_cold_freeflight.yaml` is validated against
  an inventory that includes offerable Falklands
- **THEN** validation MUST succeed

#### Scenario: Channel rejects country Argentina
- **WHEN** a TheChannel Mission Spec sets player country `Argentina`
- **THEN** validation MUST fail with an unknown-country error

### Requirement: Domain unsupported hint lists domain theatres
When land/sea domain checks are not packaged for a theatre, the
`domain_unsupported_theatre` hint SHALL list every entry in `DOMAIN_THEATRES`
(including Falklands after this change). Unbound theatres such as `Kola` MUST
still fail closed.

#### Scenario: Falklands domain hint lists current domain theatres
- **WHEN** a Kola (or other unbound) strike Spec is validated
- **THEN** validation MUST fail with `domain_unsupported_theatre` and the hint
  MUST include every current `DOMAIN_THEATRES` key including Falklands

## ADDED Requirements

### Requirement: Falklands land/sea domain
Shared validation SHALL classify Falklands strike/recon map points using
Syria-style seaward windows on classifier AFs `{1,2,3,24,29}`. Near a
classifier AF MUST be land. CAP 150/40 MUST be sea. GA 269/21 MUST be land.
MUST NOT run other-theatre chords or Nevada desert-default. MUST NOT promote
Goose Green 24 or Gull Point 29 as Spec keys.

#### Scenario: Falklands CAP station is sea
- **WHEN** domain is classified at the Mount Pleasant 150° / 40 km CAP station
- **THEN** the result MUST be sea

#### Scenario: Falklands GA station is land
- **WHEN** domain is classified at the Mount Pleasant 269° / 21 km strike
- **THEN** the result MUST be land

### Requirement: Falklands ground_attack Specs validate
Shared validation SHALL accept a well-formed Falklands ground_attack Spec
(theatre `Falklands`, airfield `MountPleasant`, nested strike) when inventory
agrees. Recon invent MUST still be rejected.

#### Scenario: Mount Pleasant ground_attack validates
- **WHEN** `examples/mount_pleasant_east_falkland_ground_attack.yaml` is
  validated against an inventory that includes offerable Falklands
- **THEN** validation MUST succeed
