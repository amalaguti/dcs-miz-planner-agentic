## ADDED Requirements

### Requirement: Planner may emit CAP Specs
The NL planning rules SHALL allow Mission Spec `mission_type` `cap` with a nested `cap`
block (airfield-relative bearing/distance, altitude, pattern, engagement) and MUST NOT
instruct the model to invent raw map coordinates or unsupported mission types beyond the
allow-list. CAP Specs MUST still pass host validation before acceptance.

#### Scenario: Stub or documented allow-list includes cap
- **WHEN** planning rules / system prompt are composed for Channel MVP planning
- **THEN** `cap` MUST be listed among supported mission types alongside `free_flight` and
  `intercept`
