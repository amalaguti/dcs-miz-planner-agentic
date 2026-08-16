## MODIFIED Requirements

### Requirement: Known countries and aircraft are era-filtered
Shared validation SHALL resolve known countries and known aircraft using the
Spec theatre’s packaged era (`era_for_theatre`). A WWII theatre MUST reject
`Georgia` / `Turkey` / `Su-25T`. A modern theatre MUST accept
`SpitfireLFMkIX` (dual-era). It MUST still reject modern-only countries on
WWII theatres.

#### Scenario: Channel rejects Georgia
- **WHEN** a TheChannel Mission Spec sets player country `Georgia`
- **THEN** validation MUST fail with an unknown-country error

#### Scenario: Caucasus accepts Spitfire
- **WHEN** a Caucasus Mission Spec sets player aircraft `SpitfireLFMkIX`
- **THEN** validation MUST succeed when the rest of the Spec is well-formed

### Requirement: Syria freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Syria`
and airfield `Incirlik` when the packaged registry supports Syria, a terrain
binding exists, and the install inventory reports `Syria` as available and
planner-supported.

#### Scenario: Valid Incirlik freeflight passes
- **WHEN** the checked-in Syria cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Syria` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Syria accepts Spitfire
- **WHEN** a Syria Mission Spec sets player aircraft `SpitfireLFMkIX`
- **THEN** validation MUST succeed when the rest of the Spec is well-formed

### Requirement: Nevada freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Nevada`
and airfield `Nellis` when the packaged registry supports Nevada, a terrain
binding exists, and the install inventory reports `Nevada` as available and
planner-supported.

#### Scenario: Valid Nellis freeflight passes
- **WHEN** the checked-in Nevada cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Nevada` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Nevada accepts Spitfire
- **WHEN** a Nevada Mission Spec sets player aircraft `SpitfireLFMkIX`
- **THEN** validation MUST succeed when the rest of the Spec is well-formed

### Requirement: Falklands freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Falklands`
and airfield `MountPleasant` when the packaged registry supports Falklands, a
terrain binding exists, and the install inventory reports `Falklands` as
available and planner-supported.

#### Scenario: Valid Mount Pleasant freeflight passes
- **WHEN** the checked-in Falklands cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Falklands` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Falklands accepts Spitfire
- **WHEN** a Falklands Mission Spec sets player aircraft `SpitfireLFMkIX`
- **THEN** validation MUST succeed when the rest of the Spec is well-formed

## ADDED Requirements

### Requirement: Batumi Spitfire freeflight validates
Shared validation SHALL accept `examples/batumi_spitfire_freeflight.yaml`
when inventory agrees.

#### Scenario: Batumi Spitfire validates
- **WHEN** that example is validated against offerable Caucasus inventory
- **THEN** validation MUST succeed
