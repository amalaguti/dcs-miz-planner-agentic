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

### Requirement: Stable import surface
Agent-facing callers MUST be able to import the tool callables from a single package surface
(e.g. `dcs_miz_planner.tools`) without depending on unrelated internal modules for these
five operations.

#### Scenario: Import tools package
- **WHEN** a test imports the tools surface
- **THEN** the five named tools MUST be available for invocation
