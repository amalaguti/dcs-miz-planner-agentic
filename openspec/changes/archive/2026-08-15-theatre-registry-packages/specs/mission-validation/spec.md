## ADDED Requirements

### Requirement: Player airfield belongs to Spec theatre
Validation SHALL reject a Mission Spec whose player airfield is not registered
for the Spec theatre, even if the same Spec key exists on another packaged
theatre. Diagnostics MUST identify the airfield field and list known airfields
for that theatre (or equivalent clear diagnostics).

#### Scenario: Channel airfield on Normandy fails
- **WHEN** a Mission Spec sets theatre `Normandy` and airfield `Manston`
- **THEN** validation MUST fail with an error that identifies the airfield
  field and lists known Normandy airfields (or equivalent clear diagnostics)

#### Scenario: Normandy airfield on Channel fails
- **WHEN** a Mission Spec sets theatre `TheChannel` and airfield
  `NeedsOarPoint`
- **THEN** validation MUST fail with an error that identifies the airfield
  field and lists known TheChannel airfields (or equivalent clear diagnostics)

## MODIFIED Requirements

### Requirement: Shared Mission Spec validation API
The system SHALL expose a Python validation API that accepts a loaded
free-flight `MissionSpec` and returns a structured result indicating success
or one or more errors. Each error MUST include a stable machine-oriented code,
a human-readable message, and a field path when applicable. Independent checks
SHOULD be reported together rather than stopping at the first failure when
practical.

#### Scenario: Valid Manston free-flight passes
- **WHEN** the checked-in Manston cold free-flight Mission Spec is loaded and
  validated against the packaged registry and a local inventory that reports
  `TheChannel` as available and planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Unknown airfield is reported clearly
- **WHEN** a Mission Spec names an airfield absent from the packaged registry
  for the Spec theatre
- **THEN** validation MUST fail with an error that identifies the airfield
  field and lists known airfields for that theatre (or equivalent clear
  diagnostics)

#### Scenario: Multiple independent errors collected
- **WHEN** a Mission Spec uses both an unknown aircraft id and an unknown
  weather preset
- **THEN** the validation result MUST include errors for both problems in one
  response
