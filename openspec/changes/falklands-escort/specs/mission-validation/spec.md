## MODIFIED Requirements

### Requirement: Extra Falklands airfields validate
Shared validation SHALL accept a well-formed Falklands free-flight Spec whose
player airfield is a curated extra Falklands key (e.g. `RioGallegos`) when
inventory agrees. Channel/Normandy MUST still reject country `Argentina` as
unknown-country. Ground_attack and recon invent on Falklands MUST still be
rejected.

#### Scenario: Rio Gallegos freeflight validates
- **WHEN** `examples/rio_gallegos_cold_freeflight.yaml` is validated against
  an inventory that includes offerable Falklands
- **THEN** validation MUST succeed

#### Scenario: Channel rejects country Argentina
- **WHEN** a TheChannel Mission Spec sets player country `Argentina`
- **THEN** validation MUST fail with an unknown-country error

## ADDED Requirements

### Requirement: Falklands escort Specs validate
Shared validation SHALL accept a well-formed Falklands escort Spec
(theatre `Falklands`, airfield `MountPleasant`, nested escort) when inventory
agrees. Ground_attack invent MUST still be rejected. Domain checks MUST remain
fail-closed on Falklands.

#### Scenario: Mount Pleasant escort validates
- **WHEN** `examples/mount_pleasant_south_atlantic_escort.yaml` is validated
  against an inventory that includes offerable Falklands
- **THEN** validation MUST succeed
