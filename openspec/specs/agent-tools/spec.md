# Agent Tools

## Purpose

Stable, agent-facing callables over the known catalog and the existing validate/compile
path. Results are structured for later LLM tool calling. No LLM or MCP wiring in this
capability.

## Requirements

### Requirement: Catalog lookup tools
The system SHALL expose callable tools `find_airfield` and `get_aircraft_details` that query
the known agent catalog (after ensuring it is synced). Results MUST be structured and MUST NOT
invent DCS identifiers absent from the known catalog.

#### Scenario: Find Manston
- **WHEN** `find_airfield` is called with a query that matches Manston
- **THEN** the result MUST include airfield name Manston and its known airdrome id

#### Scenario: Aircraft details for Spitfire
- **WHEN** `get_aircraft_details` is called for `SpitfireLFMkIX`
- **THEN** the result MUST include that aircraft id and its known radio frequency

#### Scenario: Unknown aircraft
- **WHEN** `get_aircraft_details` is called for an id not in the known catalog
- **THEN** the result MUST indicate failure without inventing aircraft data

### Requirement: List mission options tool
The system SHALL expose `list_mission_options` that returns known planning enumerations from
the catalog (at least mission types, start types, weather presets) and offerable theatres
from the catalog/install join, **and** an enriched planning-options collection with family,
id, description, and support level (`supported` | `advisory` | `future`).

#### Scenario: Options include free flight and intercept
- **WHEN** `list_mission_options` is called after catalog sync
- **THEN** the result MUST include mission types `free_flight` and `intercept`

#### Scenario: Offerable theatres reflected
- **WHEN** TheChannel is offerable on the local machine
- **THEN** `list_mission_options` MUST list TheChannel among offerable theatres

#### Scenario: Enriched planning options present
- **WHEN** `list_mission_options` is called after catalog sync
- **THEN** the result MUST include planning option rows with support levels for agent use

### Requirement: Validate and compile tools
The system SHALL expose `validate_mission_spec` and `compile_mission` tools that wrap the
existing shared validation engine and PyDCS compiler. Validate/compile MUST remain
registry- and install-backed; tools MUST NOT bypass those engines or emit LLM-authored Lua.

#### Scenario: Validate Manston free flight Spec
- **WHEN** `validate_mission_spec` is given the checked-in Manston cold free-flight Spec path
- **THEN** the result MUST report ok (valid)

#### Scenario: Compile Manston free flight Spec
- **WHEN** `compile_mission` is given that Spec path and an output path
- **THEN** the tool MUST write a `.miz` at the output path (or a clear structured failure)

### Requirement: Prefs and history tools
The system SHALL expose callable tools `get_user_prefs`, `set_user_prefs`,
`record_generation`, `record_feedback`, and `list_generation_history` that read and write
user-memory tables. Results MUST be structured `{ok: …}` dicts consistent with other
agent tools. These tools MUST NOT invent DCS identifiers or bypass validation/compile.

#### Scenario: Get prefs when empty
- **WHEN** `get_user_prefs` is called with no prefs stored
- **THEN** the result MUST report ok and an empty prefs map

#### Scenario: Set and get prefs
- **WHEN** `set_user_prefs` writes a preference and `get_user_prefs` is called
- **THEN** the result MUST include that preference

#### Scenario: List recent history
- **WHEN** at least one generation has been recorded and `list_generation_history` is called
- **THEN** the result MUST include that generation in the recent list

### Requirement: Research guidance tool
The system SHALL expose a callable `research_guidance` tool that returns short notes on
flight procedures, combat manoeuvres, pilot accounts, or historical context for commander
briefs. Offline/stub mode MUST use fixtures without network access. Live mode MUST attempt
web-backed retrieval (best-effort free providers; no research API key required). When live
retrieval succeeds, notes MUST include at least one non-fixture source. When live was
requested and retrieval fails or returns no snippets, the result MUST still be structured
ok with fixture notes AND MUST include a clear `warning` stating that live research was
unavailable and fixtures are being used. Failures MUST soft-fail and MUST NOT invent DCS
identifiers or Spec field authority. Live fetch queries MUST incorporate available
`mission_type`, `theatre`, and `aircraft` context when provided.

#### Scenario: Offline research returns notes
- **WHEN** `research_guidance` is called in offline mode for an intercept-oriented query
- **THEN** the result MUST report ok with non-empty notes and MUST NOT require network access

#### Scenario: Live success returns web-sourced notes
- **WHEN** `research_guidance` is called with live enabled and the injectable/live fetch
  returns non-empty web notes
- **THEN** the result MUST report ok with at least one note whose source is not a fixture
  id, and MUST NOT set a live-unavailable warning

#### Scenario: Live empty soft-fails with warning
- **WHEN** `research_guidance` is called with live enabled and the live fetch returns no
  snippets
- **THEN** the result MUST report ok with fixture notes and MUST include a warning that live
  research returned no snippets (or equivalent live-unavailable wording)

#### Scenario: Live error soft-fails with warning
- **WHEN** `research_guidance` is called with live enabled and the live fetch raises a
  network or parse error
- **THEN** the result MUST report ok with fixture notes and MUST include a warning that
  mentions the live fetch failure

### Requirement: Mission Spec schema tool
The system SHALL expose `get_mission_spec_schema` that, given a supported
`mission_type` (`free_flight`, `intercept`, `cap`, or `ground_attack`), returns a compact
Mission Spec example JSON object plus human-readable notes and anti-patterns for that type.
The example MUST validate as a `MissionSpec` under the shared schema. The payload MUST be
derived from packaged examples and/or the Pydantic Spec model — not from a hand-edited
SQLite schema as source of truth. Unsupported or unknown `mission_type` MUST return a
structured error without inventing a Spec.

#### Scenario: CAP schema example validates
- **WHEN** `get_mission_spec_schema` is called with `mission_type` `cap` after the tool
  is registered
- **THEN** the result MUST be ok and MUST include an `example` object that validates as
  Mission Spec `schema_version` `"1"` with `mission_type` `cap`

#### Scenario: Ground-attack schema example validates
- **WHEN** `get_mission_spec_schema` is called with `mission_type` `ground_attack` after the
  tool is registered
- **THEN** the result MUST be ok and MUST include an `example` object that validates as
  Mission Spec `schema_version` `"1"` with `mission_type` `ground_attack`

#### Scenario: Unknown mission type errors
- **WHEN** `get_mission_spec_schema` is called with an unsupported `mission_type`
- **THEN** the result MUST not be ok and MUST include a clear error (no fabricated Spec)

#### Scenario: Tool available on bridge
- **WHEN** the standard agent tool definitions are listed
- **THEN** `get_mission_spec_schema` MUST be among the registered function tools

### Requirement: Escort schema via get_mission_spec_schema
The `get_mission_spec_schema` agent tool SHALL support `mission_type` `escort`, returning a
derived example shape consistent with the checked-in escort example (nested `escort`,
`package`, optional `enemies`, `escort_package` objective).

#### Scenario: Escort schema example validates
- **WHEN** an agent or test requests `get_mission_spec_schema` for `escort`
- **THEN** the returned example MUST load as a structurally valid escort Mission Spec
  (subject to registry checks)

### Requirement: Stable import surface
Agent-facing callers MUST be able to import the tool callables from a single package surface
(e.g. `dcs_miz_planner.tools`) without depending on unrelated internal modules for catalog
lookup, validate/compile, user-memory, and research-guidance operations.

#### Scenario: Import tools package
- **WHEN** a test imports the tools surface
- **THEN** the catalog, validate/compile, user-memory, and research guidance tools MUST be
  available for invocation

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

### Requirement: Spec schema notes include triggers
When `get_mission_spec_schema` (or equivalent prompt fragment) describes a mission type, it
MUST mention that optional typed `zones` / `triggers` may appear, MUST NOT encourage Lua or
script fields, and MUST note that validated non-empty triggers compile to native ME trigger tables.

#### Scenario: Schema notes mention triggers
- **WHEN** an agent requests the Spec schema for `free_flight` or `cap`
- **THEN** the notes or example guidance MUST reference optional triggers/zones without
  inventing unsupported condition types

### Requirement: Spec schema notes include narrative
When `get_mission_spec_schema` (or equivalent prompt fragment) describes combat mission
types, it MUST mention optional opt-in `narrative.enabled` for CAP (expands to typed
zones/triggers), MUST NOT encourage Lua, and MUST note that narrative conflicts with
hand-authored non-empty zones/triggers.

#### Scenario: Schema notes mention narrative
- **WHEN** an agent requests the Spec schema for `cap`
- **THEN** the notes MUST reference optional narrative without inventing unsupported
  trigger types
