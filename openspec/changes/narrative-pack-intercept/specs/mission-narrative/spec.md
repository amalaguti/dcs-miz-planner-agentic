## ADDED Requirements

### Requirement: Intercept narrative pack
When `narrative.enabled` is true and `mission_type` is `intercept`, the system MUST
expand an intercept narrative pack into typed triggers using only the v1 vocabulary
(no Lua). The pack MUST include a time-based scramble/push message and a
`unit_dead` (first enemy) path that messages and ends the mission as a win. Expansion
MUST run before validate/compile. Preconditions: empty `zones`/`triggers`, non-empty
`enemies`.

#### Scenario: Intercept narrative expands
- **WHEN** a valid intercept Spec has `narrative.enabled: true`, empty zones/triggers,
  and at least one enemy
- **THEN** expansion MUST add trigger rules for scramble messaging and bandits-down win

#### Scenario: Intercept without enemies fails
- **WHEN** intercept narrative is enabled and `enemies` is empty
- **THEN** expansion or validation MUST fail with a clear error

## MODIFIED Requirements

### Requirement: Opt-in narrative expands to typed triggers
The system SHALL support an optional Mission Spec `narrative` object with
`enabled` (boolean, default false). When `enabled` is true for `mission_type: cap` or
`mission_type: intercept`, the system MUST expand the matching curated narrative pack
into typed `zones` and/or `triggers` using only the existing v1 condition/action
vocabulary (no Lua). Expansion MUST run before shared validation and compile so the
emitted `.miz` contains the resulting rules.

#### Scenario: CAP narrative expands
- **WHEN** a valid CAP Spec has `narrative.enabled: true`, empty `zones`/`triggers`, at
  least one enemy, and a `cap` block
- **THEN** expansion MUST add a station zone and trigger rules including a message and a
  bandit-down path that can end the mission as a win

#### Scenario: Narrative disabled leaves triggers empty
- **WHEN** `narrative` is omitted or `enabled` is false
- **THEN** the system MUST NOT inject narrative zones or triggers

### Requirement: Narrative conflicts and unsupported types fail clearly
When `narrative.enabled` is true, the system MUST reject Specs that already have
non-empty `zones` or `triggers`. It MUST reject `enabled: true` for mission types other
than `cap` and `intercept` in this capability revision. It MUST reject CAP narrative when
`cap` is missing or `enemies` is empty, and intercept narrative when `enemies` is empty.

#### Scenario: Hand-written triggers block narrative
- **WHEN** `narrative.enabled` is true and `triggers` is non-empty
- **THEN** validation or expansion MUST fail with a clear conflict error

#### Scenario: Unsupported mission type narrative rejected
- **WHEN** `mission_type` is not `cap` or `intercept` and `narrative.enabled` is true
- **THEN** validation or expansion MUST fail identifying unsupported mission type
