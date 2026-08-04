## MODIFIED Requirements

### Requirement: Validate typed triggers and zones
The shared validation engine SHALL accept Specs whose `triggers` and `zones` conform to the
mission-triggers vocabulary and reference rules, and MUST reject unknown types, duplicate
zone names, out-of-range `enemy_index` / `target_index`, missing zone references, empty
flag names, unknown `sound.asset_id` values, and invalid `group_life_less` (bad index XOR,
out-of-range index, or percent outside 1–100). Blanket refusal of any non-empty `triggers`
list MUST NOT apply once the typed model is in force.

#### Scenario: Out-of-range enemy_index fails
- **WHEN** `unit_dead.enemy_index` is 0 but `enemies` is empty
- **THEN** validation MUST fail

#### Scenario: Well-formed trigger passes validate
- **WHEN** a Spec with `time_more` → `message` trigger is validated
- **THEN** `validate_mission_spec` MUST succeed for trigger rules

#### Scenario: Unknown sound asset rejected
- **WHEN** a Spec uses `sound` with an unregistered `asset_id`
- **THEN** `validate_mission_spec` MUST fail with a clear error

#### Scenario: Invalid group_life_less rejected
- **WHEN** a Spec uses `group_life_less` with both indices set or percent outside 1–100
- **THEN** `validate_mission_spec` (or Spec load) MUST fail with a clear error
