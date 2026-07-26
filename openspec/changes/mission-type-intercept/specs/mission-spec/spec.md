## ADDED Requirements

### Requirement: Intercept mission type
The Mission Spec SHALL support `mission_type` value `intercept` in addition to `free_flight`.
An intercept Spec MUST include a non-empty `enemies` collection using verified DCS aircraft
ids and a positive count. Free-flight Specs MUST continue to require empty `enemies`,
`objectives`, and `triggers`.

#### Scenario: Intercept with Bf-109K-4 enemies accepted
- **WHEN** a Mission Spec sets `mission_type` to `intercept`, player `SpitfireLFMkIX` at
  Manston, and `enemies` containing at least one entry with aircraft `Bf-109K-4` and count ≥ 1
- **THEN** the Spec MUST load as structurally valid for intercept compilation

#### Scenario: Free flight still refuses enemies
- **WHEN** a Mission Spec sets `mission_type` to `free_flight` with a non-empty `enemies` list
- **THEN** loading or validation MUST fail with a clear not-supported / empty-extensions error

### Requirement: Minimal intercept objective
An intercept Mission Spec MUST declare a minimal objective indicating enemy interception
(structured field agreed in design). Unknown objective types MUST be rejected. Non-empty
`triggers` MUST still be rejected in this change.

#### Scenario: intercept_enemy objective accepted
- **WHEN** an intercept Spec includes the supported intercept objective shape and empty
  `triggers`
- **THEN** validation MUST accept the Spec (subject to other intercept rules)

#### Scenario: Non-empty triggers still refused
- **WHEN** an intercept Spec sets a non-empty `triggers` list
- **THEN** validation MUST fail stating triggers are not supported yet

### Requirement: Checked-in intercept example Spec
The repository SHALL include a checked-in example Mission Spec for the Manston dawn-style
intercept (early start time, Channel, Spitfire player, Bf-109K-4 enemies) usable as validate
and compile input.

#### Scenario: Example present
- **WHEN** a developer clones the repository
- **THEN** an intercept example Spec MUST be present and loadable under schema_version `"1"`
