## MODIFIED Requirements

### Requirement: Extra Falklands airfields validate
Shared validation SHALL accept a well-formed Falklands free-flight Spec whose
player airfield is a curated extra Falklands key (e.g. `RioGallegos`) when
inventory agrees. Channel/Normandy MUST still reject country `Argentina` as
unknown-country. Ground_attack, escort, and recon invent on Falklands MUST
still be rejected.

#### Scenario: Rio Gallegos freeflight validates
- **WHEN** `examples/rio_gallegos_cold_freeflight.yaml` is validated against
  an inventory that includes offerable Falklands
- **THEN** validation MUST succeed

#### Scenario: Channel rejects country Argentina
- **WHEN** a TheChannel Mission Spec sets player country `Argentina`
- **THEN** validation MUST fail with an unknown-country error

### Requirement: Falklands CAP Specs validate
Shared validation SHALL accept a well-formed Falklands CAP Spec
(theatre `Falklands`, airfield `MountPleasant`, nested cap) when inventory
agrees. Domain checks MUST remain fail-closed on Falklands.

#### Scenario: Mount Pleasant CAP validates
- **WHEN** `examples/mount_pleasant_south_atlantic_cap.yaml` is validated
  against an inventory that includes offerable Falklands
- **THEN** validation MUST succeed

## ADDED Requirements

### Requirement: Falklands intercept Specs validate
Shared validation SHALL accept a well-formed Falklands intercept Spec
(theatre `Falklands`, airfield `MountPleasant`) when inventory agrees.
Well-formed Falklands intercept Specs MUST NOT fail solely with
`intercept_unsupported_theatre`. Domain checks MUST remain fail-closed.

#### Scenario: Mount Pleasant intercept validates
- **WHEN** `examples/mount_pleasant_dawn_intercept.yaml` is validated against
  an inventory that includes offerable Falklands
- **THEN** validation MUST succeed

### Requirement: Intercept unsupported hint lists recipe theatres
When intercept spawn is not packaged for a theatre, the
`intercept_unsupported_theatre` hint SHALL list every key in
`INTERCEPT_SPAWN_RECIPES` (not a hardcoded Channel/Normandy/Caucasus-only
string).

#### Scenario: Unbound theatre intercept hint lists current recipes
- **WHEN** an intercept Spec uses a theatre without an intercept spawn recipe
- **THEN** validation MUST fail with `intercept_unsupported_theatre` and the
  hint MUST include every current `INTERCEPT_SPAWN_RECIPES` key

### Requirement: Domain unsupported hint lists domain theatres
When land/sea domain checks are not packaged for a theatre, the
`domain_unsupported_theatre` hint SHALL list every entry in `DOMAIN_THEATRES`
(not a hardcoded Channel/Normandy/Caucasus/Syria-only string that omits
Nevada). Falklands MUST remain absent from `DOMAIN_THEATRES` until a domain
recipe ships.

#### Scenario: Falklands domain hint lists current domain theatres
- **WHEN** a Falklands strike Spec is validated
- **THEN** validation MUST fail with `domain_unsupported_theatre` and the hint
  MUST include every current `DOMAIN_THEATRES` key including Nevada
