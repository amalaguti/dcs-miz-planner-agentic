## ADDED Requirements

### Requirement: Creative bias from history and feedback
The system SHALL provide a deterministic helper (callable from tests and planning hosts)
that, given recent generation history rows (with optional `creative` detail) and
linked satisfaction feedback, returns soft `prefer` and `avoid` lists of
`mission_behaviour` ids for an optional mission type filter. Higher scores and
liked-style tags MUST bias toward prefer; low scores and avoid-style tags toward
avoid. Empty history MUST yield empty prefer/avoid lists.

#### Scenario: High score with behaviours prefers them
- **WHEN** a success generation detail lists behaviours and feedback score is high
- **THEN** the bias helper MUST include at least one of those behaviours in prefer
  (for matching mission type when filtered)

#### Scenario: Empty history yields no bias
- **WHEN** no generations exist
- **THEN** prefer and avoid MUST be empty

### Requirement: Agent tools document creative detail and bias
Tool descriptions and/or planning guidance MUST state that `record_generation` detail
MAY carry `creative` inspiration/behaviour ids, and that `list_generation_history`
(plus feedback when available) SHOULD inform creative picks on vague asks.

#### Scenario: record_generation description mentions creative detail
- **WHEN** tool definitions are inspected
- **THEN** `record_generation` guidance MUST mention optional creative decision detail
  (or an equivalent documented host convention tested in prompts)
