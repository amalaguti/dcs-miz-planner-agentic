## ADDED Requirements

### Requirement: Mission Spec schema tool
The system SHALL expose `get_mission_spec_schema` that, given a supported
`mission_type` (`free_flight`, `intercept`, or `cap`), returns a compact Mission Spec
example JSON object plus human-readable notes and anti-patterns for that type. The
example MUST validate as a `MissionSpec` under the shared schema. The payload MUST be
derived from packaged examples and/or the Pydantic Spec model — not from a hand-edited
SQLite schema as source of truth. Unsupported or unknown `mission_type` MUST return a
structured error without inventing a Spec.

#### Scenario: CAP schema example validates
- **WHEN** `get_mission_spec_schema` is called with `mission_type` `cap` after the tool
  is registered
- **THEN** the result MUST be ok and MUST include an `example` object that validates as
  Mission Spec `schema_version` `"1"` with `mission_type` `cap`

#### Scenario: Unknown mission type errors
- **WHEN** `get_mission_spec_schema` is called with an unsupported `mission_type`
- **THEN** the result MUST not be ok and MUST include a clear error (no fabricated Spec)

#### Scenario: Tool available on bridge
- **WHEN** the standard agent tool definitions are listed
- **THEN** `get_mission_spec_schema` MUST be among the registered function tools
