## ADDED Requirements

### Requirement: Validate escort Specs
The shared validation engine SHALL accept escort Mission Specs that satisfy escort schema
rules and registry checks, including a valid `escort` block, non-empty same-coalition
`package` with known aircraft ids, `escort_package` objective, and — when present — known
opposing `enemies`. It MUST reject escort Specs with opposing-coalition package entries,
unknown package/enemy aircraft, missing required `escort` fields, misuse of
`strike`/`targets`/`payload` on escort, and non-empty `triggers` for schema_version `"1"`.

#### Scenario: Valid escort example passes validate
- **WHEN** the checked-in escort example is validated with Channel available inventory
- **THEN** `validate_mission_spec` / `dcs-miz validate` MUST succeed

#### Scenario: Unknown package aircraft fails
- **WHEN** an escort Spec names a package aircraft absent from the Channel registry
- **THEN** validation MUST fail with an unknown-aircraft (or equivalent) error identifying
  the package path

#### Scenario: Friendly package coalition mismatch fails
- **WHEN** an escort Spec includes a package entry whose coalition differs from
  `player.coalition`
- **THEN** validation or Spec load MUST fail before compile
