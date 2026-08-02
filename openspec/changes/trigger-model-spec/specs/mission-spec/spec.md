## ADDED Requirements

### Requirement: Trigger and zone reference validation
The shared validation engine SHALL validate trigger/zone graphs: every `coalition_in_zone`
zone name MUST exist in `zones`; every `unit_dead.enemy_index` MUST be in range for
`enemies`; flag names on `flag_is` / `set_flag` MUST be non-empty. Well-formed non-empty
`triggers`/`zones` MUST pass validation (compile may still refuse until native emit exists).

#### Scenario: Missing zone reference fails
- **WHEN** a condition references zone `alpha` but `zones` has no such name
- **THEN** validation MUST fail with a clear missing-zone error

#### Scenario: Valid trigger graph passes validate
- **WHEN** a Spec with a consistent zone and `coalition_in_zone` / `message` trigger is
  validated
- **THEN** validation MUST succeed for the trigger/zone rules

## MODIFIED Requirements

### Requirement: Reserved extension points for future combat and triggers
The Mission Spec MAY include optional top-level keys `enemies`, `objectives`, `triggers`,
`targets`, `package`, and `zones`. For free-flight missions combat keys MUST be absent or
empty per existing free-flight rules. `triggers` and `zones` MAY be non-empty when they
conform to the typed mission-triggers model. Free-form or Lua-bearing trigger payloads
MUST be rejected. The system MUST NOT silently drop unsupported non-empty values.

#### Scenario: Free flight with absent extensions compiles
- **WHEN** a free-flight Mission Spec omits `enemies`, `objectives`, `triggers`,
  `targets`, `package`, and `zones`
- **THEN** the Spec SHALL be structurally valid and the compiler MUST proceed as for free
  flight

#### Scenario: Typed triggers allowed on free flight
- **WHEN** a free-flight Spec includes a well-typed `time_more` → `message` trigger and
  empty combat extensions
- **THEN** structural load and shared validation MUST succeed
