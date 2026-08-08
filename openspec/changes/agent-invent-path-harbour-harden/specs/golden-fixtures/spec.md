## ADDED Requirements

### Requirement: Path and harbour harden covered by tests
Hermetic tests SHALL assert french_coast path_point_deltas, harbour sea-only
guidance text, path-domain repair YAML snippet, and host land-path clamp
behaviour (when implemented).

#### Scenario: Path harbour harden tests green
- **WHEN** catalog / agent / validation tests run in CI
- **THEN** they MUST pass and fail if path deltas, harbour sea guidance, repair
  path example, or clamp behaviour regresses
