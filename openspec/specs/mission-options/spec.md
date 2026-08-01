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
