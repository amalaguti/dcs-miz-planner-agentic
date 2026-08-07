## ADDED Requirements

### Requirement: Schema documents failures list
Agent Spec schema notes SHALL document optional `failures` (`id`, `start_after_s`,
`probability`, `random_pause_s`) and that ids must come from the catalog / tools.

#### Scenario: Schema mentions failures
- **WHEN** requesting Spec shape for invent
- **THEN** notes MUST mention optional `failures` and curated ids
