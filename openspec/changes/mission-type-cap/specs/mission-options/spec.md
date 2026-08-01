## ADDED Requirements

### Requirement: CAP mission type in planning options
The packaged planning-option catalog SHALL include `mission_type` id `cap` marked
`supported`, describing Channel CAP / patrol planning.

#### Scenario: List supported mission types includes cap
- **WHEN** a caller lists planning options for family `mission_type` with support `supported`
- **THEN** results MUST include `cap` in addition to `free_flight` and `intercept`

### Requirement: ROE seeds are Spec-backed for CAP
Planning options in family `roe_seed` (`weapons_hold`, `weapons_free`, and any other
packaged ROE ids agreed in design) SHALL be marked `supported` (or `advisory` with
`meta.engagement` mapping) so agents can map them onto CAP Spec `cap.engagement`. They
MUST NOT be presented as free-floating compile fields for free_flight.

#### Scenario: ROE options no longer future-only
- **WHEN** catalog sync runs after this change
- **THEN** packaged `roe_seed` entries MUST NOT all remain `future`; at least the CAP-mapped
  engagement values MUST be discoverable as non-`future` support
