## ADDED Requirements

### Requirement: Known countries and aircraft are era-filtered
Shared validation SHALL resolve known countries and known aircraft using the
Spec theatre’s packaged era (`era_for_theatre`). A WWII theatre MUST reject
`Georgia` / `Su-25T`. A modern Caucasus Spec MUST reject `UK` /
`SpitfireLFMkIX`.

#### Scenario: Channel rejects Georgia
- **WHEN** a TheChannel Mission Spec sets player country `Georgia`
- **THEN** validation MUST fail with an unknown-country error

#### Scenario: Caucasus rejects Spitfire
- **WHEN** a Caucasus Mission Spec sets player aircraft `SpitfireLFMkIX`
- **THEN** validation MUST fail with an unknown-aircraft error

### Requirement: Caucasus freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Caucasus`
and airfield `Batumi` when the packaged registry supports Caucasus, a terrain
binding exists, and the install inventory reports `Caucasus` as available and
planner-supported.

#### Scenario: Valid Batumi freeflight passes
- **WHEN** the checked-in Caucasus cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Caucasus` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors
