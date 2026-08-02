## MODIFIED Requirements

### Requirement: Optional guidance research
The system SHALL provide a research capability the planning agent can invoke to gather
short guidance notes on flight procedures, combat manoeuvres, pilot accounts, or
historical context relevant to the mission. Live mode MUST attempt web-backed retrieval
when enabled. Stub or offline mode MUST return fixture notes without network access. When
live research fails or returns no snippets, the system MUST soft-fail with a clear warning
and MAY fall back to fixtures; it MUST NOT present that fallback as successful live
retrieval. Research failures MUST NOT fail an otherwise successful Spec plan. Research
results MUST NOT be treated as a source of DCS type ids or Spec field authority.

#### Scenario: Stub research returns offline notes
- **WHEN** the research capability is invoked in stub/offline mode for an intercept-oriented
  query
- **THEN** it MUST return non-empty guidance notes without requiring network access

#### Scenario: Research failure soft-fails
- **WHEN** live research fails (timeout or provider error) after a Spec has already validated
- **THEN** the plan MUST still be able to succeed and MUST still be allowed to produce a
  brief without depending on live research notes

#### Scenario: Live research warning is visible to the agent path
- **WHEN** live research is requested and returns no usable live snippets
- **THEN** the research result MUST include a warning suitable for tool/CLI display stating
  that live research was unavailable
