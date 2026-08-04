## ADDED Requirements

### Requirement: Ground-attack narrative pack
When `narrative.enabled` is true and `mission_type` is `ground_attack`, the system MUST
expand a ground-attack narrative pack into typed zones/triggers using only the v1
vocabulary (including `target_dead`; no Lua). The pack MUST include a time-based push
message, a strike-area zone derived from the Spec `strike` block with a coalition-in-zone
ingress callout, and a `target_dead` (first target) path that messages and ends the
mission as a win. Expansion MUST run before validate/compile. Preconditions: empty
`zones`/`triggers`, nested `strike`, non-empty `targets`.

#### Scenario: Ground-attack narrative expands
- **WHEN** a valid ground_attack Spec has `narrative.enabled: true`, empty zones/triggers,
  strike + targets
- **THEN** expansion MUST add a strike-area zone and trigger rules for push, ingress, and
  targets-down win

#### Scenario: Ground-attack narrative without targets fails
- **WHEN** ground_attack narrative is enabled and `targets` is empty
- **THEN** expansion or validation MUST fail with a clear error

## MODIFIED Requirements

### Requirement: Opt-in narrative expands to typed triggers
The system SHALL support an optional Mission Spec `narrative` object with
`enabled` (boolean, default false). When `enabled` is true for `mission_type: cap`,
`intercept`, `escort`, or `ground_attack`, the system MUST expand the matching curated
narrative pack into typed `zones` and/or `triggers` using only the existing v1
condition/action vocabulary (no Lua). Expansion MUST run before shared validation and
compile so the emitted `.miz` contains the resulting rules.

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
than `cap`, `intercept`, `escort`, and `ground_attack` in this capability revision.
Pack-specific preconditions (CAP: `cap` + enemies; intercept: enemies; escort: `escort` +
package + enemies; ground_attack: `strike` + targets) MUST fail clearly when missing.

#### Scenario: Hand-written triggers block narrative
- **WHEN** `narrative.enabled` is true and `triggers` is non-empty
- **THEN** validation or expansion MUST fail with a clear conflict error

#### Scenario: Unsupported mission type narrative rejected
- **WHEN** `mission_type` is not `cap`, `intercept`, `escort`, or `ground_attack` and
  `narrative.enabled` is true
- **THEN** validation or expansion MUST fail identifying unsupported mission type
