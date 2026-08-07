## ADDED Requirements

### Requirement: Brief honesty when failures armed
When `failures` is non-empty, generated briefing/voice text SHALL mention that
system failures may occur (training / keep-honest wording). Solo Specs without
failures MUST keep prior brief behaviour.

#### Scenario: Failures brief note
- **WHEN** briefing a Spec with at least one failure entry
- **THEN** Situation or Watch-outs MUST indicate possible aircraft system failures
