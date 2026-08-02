## ADDED Requirements

### Requirement: Ground-attack mission type in planning options
The packaged planning-option catalog SHALL include `mission_type` id `ground_attack` marked
`supported`, describing Channel ground-attack / strike planning with targets and payload
selection.

#### Scenario: List supported mission types includes ground_attack
- **WHEN** a caller lists planning options for family `mission_type` with support `supported`
- **THEN** results MUST include `ground_attack` in addition to `free_flight`, `intercept`,
  and `cap`

### Requirement: Payload families are Spec-backed for ground attack
Planning options in family `payload_family` SHALL include at least the named Spitfire bomb
presets agreed in design (including a Channel-crossing preset with slipper tank), marked
`supported` (or `advisory` with `meta.payload` mapping) so agents can map them onto
ground-attack Spec `player.payload`. They MUST NOT be presented as compile-backed for
free_flight when the Spec forbids player payloads.

#### Scenario: Payload options no longer future-only
- **WHEN** catalog sync runs after this change
- **THEN** packaged `payload_family` entries MUST NOT all remain `future`; at least the
  Spitfire bomb and slipper-tank presets MUST be discoverable as non-`future` support
