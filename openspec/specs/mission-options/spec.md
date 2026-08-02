# Mission Options

## Purpose

Packaged Channel planning-option catalog with support levels so agents and users can
discover creative mission knobs without inventing DCS ids or claiming unsupported
fields compile.

## Requirements

### Requirement: Packaged planning option catalog
The system SHALL maintain packaged planning-option definitions for Channel mission
planning (families of knobs with ids, human labels, descriptions, and a support level of
`supported`, `advisory`, or `future`). Definitions MUST NOT invent DCS type ids.
`future` options MUST NOT be treated as compile-supported.

#### Scenario: Sync loads planning options
- **WHEN** catalog sync runs
- **THEN** the local catalog MUST contain planning options including at least weather and
  start-type entries marked `supported`

### Requirement: Query planning options
The system SHALL allow listing planning options (CLI and/or agent tool) filtered by family
and/or support level, returning structured rows suitable for agent reasoning.

#### Scenario: List supported weather options
- **WHEN** a caller lists planning options for family weather with support supported
- **THEN** results MUST include `sunny_clear` (or the packaged weather preset id)

#### Scenario: Future options are labeled
- **WHEN** a caller lists options that include a `future` entry
- **THEN** each such row MUST report support `future`

### Requirement: Honest support levels for the agent
Agent-facing option listing MUST expose support levels so planners can prefer `supported`
and `advisory` values and avoid claiming `future` knobs as compile-backed.

#### Scenario: list_mission_options includes enriched options
- **WHEN** `list_mission_options` is called after sync
- **THEN** the result MUST include an enriched options collection (or equivalent) with
  family, id, and support fields in addition to any legacy enum lists

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
