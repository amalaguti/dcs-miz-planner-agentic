## ADDED Requirements

### Requirement: Optional aircraft failures list
The Mission Spec SHALL allow an optional top-level `failures` list. When omitted or
empty, no Failures panel rows MUST be implied. When present, each entry MUST declare
`id` (string), `start_after_s` (non-negative integer seconds, floored to ME After
minutes on emit), and MAY declare `probability` (0–100, default 100) and
`random_pause_s` (non-negative integer, default 0; maps to Within minutes with
minimum 1). Failure `id` values MUST be exact curated DCS failure identifiers for
the player aircraft — not free-form prose.

#### Scenario: Scheduled magneto failure accepted
- **WHEN** a Spec sets `failures` to one entry with a catalog Spitfire id and
  `start_after_s: 120`
- **THEN** structural load MUST succeed

#### Scenario: Omit failures means none
- **WHEN** a Spec omits `failures`
- **THEN** the Spec MUST remain valid without failure behaviour
