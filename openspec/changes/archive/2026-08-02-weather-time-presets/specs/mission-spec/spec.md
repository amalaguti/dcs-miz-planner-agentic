## ADDED Requirements

### Requirement: Dawn and marginal VFR weather presets
The Mission Spec SHALL support weather preset values `dawn_clear` and `marginal_vfr` in
addition to `sunny_clear` under schema_version `"1"`. These values MUST be registered in
the Channel weather preset registry with human-readable descriptions.

#### Scenario: Dawn clear Spec is valid
- **WHEN** a Mission Spec sets `weather: dawn_clear` with an otherwise valid free-flight
  Channel payload
- **THEN** structural load and shared validation MUST accept the Spec

#### Scenario: Marginal VFR Spec is valid
- **WHEN** a Mission Spec sets `weather: marginal_vfr` with an otherwise valid free-flight
  Channel payload
- **THEN** structural load and shared validation MUST accept the Spec

### Requirement: Dawn and marginal example Specs
The repository SHALL include checked-in example Mission Specs demonstrating dawn
(`dawn_clear` with a dawn-appropriate `start_time`) and marginal VFR (`marginal_vfr`)
Channel free-flight (or equivalent minimal) sorties usable as validate/compile input.

#### Scenario: Dawn example present
- **WHEN** a developer lists Channel weather examples
- **THEN** a dawn example Spec MUST be present and compile under Channel inventory

#### Scenario: Marginal VFR example present
- **WHEN** a developer lists Channel weather examples
- **THEN** a marginal VFR example Spec MUST be present and compile under Channel inventory
