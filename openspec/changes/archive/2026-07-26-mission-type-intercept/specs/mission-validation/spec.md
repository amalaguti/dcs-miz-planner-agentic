## ADDED Requirements

### Requirement: Validate intercept Specs
The shared validation engine SHALL accept intercept Mission Specs that satisfy intercept
schema rules and registry/install checks, including non-empty `enemies` with known aircraft
ids. It MUST still reject free-flight Specs with non-empty extension points and MUST reject
non-empty `triggers` for all schema_version `"1"` types covered by this change.

#### Scenario: Valid intercept example passes validate
- **WHEN** the checked-in intercept example is validated with Channel available inventory
- **THEN** `validate_mission_spec` / `dcs-miz validate` MUST succeed

#### Scenario: Unknown enemy aircraft fails
- **WHEN** an intercept Spec names an enemy aircraft absent from the Channel registry
- **THEN** validation MUST fail with an unknown-aircraft (or equivalent) error identifying
  the enemies path
