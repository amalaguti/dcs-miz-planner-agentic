## ADDED Requirements

### Requirement: Derived Spec shape for planning prompts
The NL agent system prompt SHALL include a short always-on reminder of Mission Spec
anti-patterns (nested `player`, `date` as `{year,month,day}`, top-level `objectives`,
no flat `airfield`/`aircraft`) and MUST instruct the model to obtain the type-specific
example via `get_mission_spec_schema` (or an equivalent host-injected derived fragment)
before emitting Spec JSON. The prompt MUST NOT rely on a hand-maintained full CAP (or
other mission-type) JSON skeleton as the sole Spec shape authority.

#### Scenario: Composed prompt points at schema tool or derived shape
- **WHEN** the system prompt is composed for one-shot or chat planning
- **THEN** it MUST mention `get_mission_spec_schema` (or clearly state that the host
  provides the derived Spec example) and MUST include anti-pattern guidance for nested
  `player` and object `date`

### Requirement: Host repair uses derived Spec example
When the host rejects assistant Spec JSON during one-shot planning or chat, the repair
nudge MUST include a derived compact Spec example for the relevant `mission_type`
(inferred from the rejected JSON when present) rather than only a prose error string.

#### Scenario: Parse failure nudge includes example
- **WHEN** the model emits Spec-like JSON that fails Mission Spec validation
- **THEN** the next host repair message MUST include a derived example Spec (or
  equivalent fragment) for a supported mission type alongside the error
