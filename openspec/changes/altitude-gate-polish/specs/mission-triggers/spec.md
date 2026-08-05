## ADDED Requirements

### Requirement: Altitude/speed gate example uses timed re-warn
The checked-in altitude/speed gates example Spec MUST demonstrate a cooldown pattern:
after an initial out-of-limits message, further messages for the same limit MUST be spaced
by a timed flag cooldown (e.g. `time_since_flag`) while the violation continues, and the
cooldown MUST clear when the player returns inside limits. Bare continuous
message-only gates without cooldown MUST NOT be the documented recommended recipe.

#### Scenario: Example includes cooldown flags
- **WHEN** the altitude/speed gates example Spec is loaded
- **THEN** it MUST include flag set/clear and `time_since_flag` (or equivalent) in the
  altitude and/or speed gate trigger graph alongside the unit altitude/speed conditions
