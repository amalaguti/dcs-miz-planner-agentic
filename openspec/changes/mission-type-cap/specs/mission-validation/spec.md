## ADDED Requirements

### Requirement: Validate CAP Specs
The shared validation engine SHALL accept CAP Mission Specs that satisfy CAP schema rules
and registry/install checks, including a valid `cap` block, `patrol` objective, and — when
present — known enemy aircraft ids. It MUST still reject free-flight Specs with non-empty
extension points, MUST reject CAP Specs missing required `cap` fields or using unknown
engagement/pattern values, and MUST reject non-empty `triggers` for all schema_version `"1"`
types covered by this change.

#### Scenario: Valid CAP example passes validate
- **WHEN** the checked-in CAP example is validated with Channel available inventory
- **THEN** `validate_mission_spec` / `dcs-miz validate` MUST succeed

#### Scenario: Unknown CAP enemy aircraft fails
- **WHEN** a CAP Spec names an enemy aircraft absent from the Channel registry
- **THEN** validation MUST fail with an unknown-aircraft (or equivalent) error identifying
  the enemies path

#### Scenario: Invalid engagement fails
- **WHEN** a CAP Spec sets an engagement value outside the closed set
- **THEN** validation or Spec load MUST fail before compile
