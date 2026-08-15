## ADDED Requirements

### Requirement: Invent uses offerable theatres
Natural-language invent/chat SHALL set Spec theatre from offerable theatres
(`known ∧ available ∧ planner_supported`). It MUST NOT lock theatre to
`TheChannel` only. It MUST NOT invent theatre ids.

#### Scenario: Normandy free_flight invent allowed
- **WHEN** Normandy is offerable and the user asks for a Normandy free-flight
- **THEN** the planner MUST be allowed to emit `theatre: Normandy` with
  `airfield: NeedsOarPoint` (and MUST NOT be required to emit TheChannel)

### Requirement: Normandy invent is free_flight only
Until Normandy place recipes exist, invent/chat SHALL refuse combat mission
types (`intercept`, `cap`, `ground_attack`, `escort`, `recon`) when the bound
theatre is `Normandy`. Repair MUST nudge toward NeedsOarPoint free_flight or
switching theatre to TheChannel. Invent MUST NOT copy `channel_place` geometry
(french coast belts, Hawkinge/Dunkirk bearings) onto Normandy.

#### Scenario: Normandy intercept invent refused
- **WHEN** invent is asked for an intercept on Normandy
- **THEN** it MUST NOT emit a combat Mission Spec and MUST surface a repair
  that free_flight at NeedsOarPoint (or TheChannel combat) is the supported path

### Requirement: Channel place cues stay Channel-only
Invent prompts, schema notes, harbour immersion nudges, and land-path host
clamp SHALL apply `channel_place` recipes only when Spec theatre is
`TheChannel`.

#### Scenario: Path clamp skipped on Normandy
- **WHEN** a Normandy Spec would otherwise receive `french_coast_strike_belt`
  path deltas
- **THEN** the host MUST NOT rewrite those Channel deltas onto the Spec
