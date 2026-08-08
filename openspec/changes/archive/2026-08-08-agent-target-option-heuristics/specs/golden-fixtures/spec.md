## ADDED Requirements

### Requirement: Target invent heuristics covered by tests
Hermetic tests SHALL assert that packaged planning-option invent heuristics
(preferred motion / AI preset for soft, AAA, sea under way, harbour) remain
present after catalog sync, and that invent prompts or Spec schema notes
mention the cue mapping.

#### Scenario: Heuristic meta and prompt tests green
- **WHEN** catalog / agent invent tests run in CI
- **THEN** they MUST pass and fail if preferred_* meta or cue-table guidance
  regresses
