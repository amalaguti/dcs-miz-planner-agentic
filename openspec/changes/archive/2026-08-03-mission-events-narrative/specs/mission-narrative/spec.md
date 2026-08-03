## ADDED Requirements

### Requirement: Opt-in narrative expands to typed triggers
The system SHALL support an optional Mission Spec `narrative` object with
`enabled` (boolean, default false). When `enabled` is true for `mission_type: cap`,
the system MUST expand a curated CAP narrative pack into typed `zones` and `triggers`
using only the existing v1 condition/action vocabulary (no Lua). Expansion MUST run
before shared validation and compile so the emitted `.miz` contains the resulting rules.

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
than `cap` in v1. It MUST reject CAP narrative when `cap` is missing or `enemies` is empty.

#### Scenario: Hand-written triggers block narrative
- **WHEN** `narrative.enabled` is true and `triggers` is non-empty
- **THEN** validation or expansion MUST fail with a clear conflict error

#### Scenario: Non-CAP narrative rejected
- **WHEN** `mission_type` is not `cap` and `narrative.enabled` is true
- **THEN** validation or expansion MUST fail identifying unsupported mission type

### Requirement: Narrative messages use squadron voice
Expanded message texts MUST follow the selected squadron voice (`raf` | `usaaf` |
`neutral`, same resolution as briefing). Templates MUST be human-authored; the LLM MUST
NOT author trigger Lua or free-form script fields.

#### Scenario: Voice selects message copy
- **WHEN** narrative CAP is expanded with voice `raf`
- **THEN** message action texts MUST use the RAF template strings for that pack
