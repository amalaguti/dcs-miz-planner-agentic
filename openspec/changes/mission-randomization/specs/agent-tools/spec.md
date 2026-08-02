## ADDED Requirements

### Requirement: Randomize mission tool
The system SHALL expose a callable tool `randomize_mission` that accepts a Mission Spec
(path or structured body), an integer `seed`, and optional `axes`, and returns a
structured result containing the randomized Spec (as data), the seed, and the axes
applied. The tool MUST use the shared seeded Spec→Spec transform and MUST NOT compile a
`.miz` itself. On failure (invalid Spec, unknown axis, validation failure of output) the
result MUST indicate failure with a clear message and MUST NOT invent DCS identifiers.

#### Scenario: Tool returns a Spec dict
- **WHEN** `randomize_mission` is called with a valid free-flight Spec path and seed `42`
- **THEN** the result MUST report ok and include a Spec-shaped payload whose
  `player.airfield` matches the base Spec

#### Scenario: Unknown axis fails cleanly
- **WHEN** `randomize_mission` is called with an unknown axis name
- **THEN** the result MUST report failure without writing files or inventing Spec fields
