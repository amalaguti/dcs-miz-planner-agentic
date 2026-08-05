## ADDED Requirements

### Requirement: Discovery join for local aircraft modules
The agent catalog MUST join known Channel aircraft (from YAML sync) with cached install
aircraft module discovery. Listing MUST distinguish known vs discovered-only modules and
MUST NOT claim discovered-only folders are planner Spec ids. Automatic promotion from
discovery into known YAML MUST NOT occur. The deferred “aircraft discovery not
implemented” stub note MUST NOT be the catalog aircraft list behaviour once discovery
is shipped.

#### Scenario: Known installed aircraft marked installed
- **WHEN** catalog aircraft includes `SpitfireLFMkIX` and inventory cache has that module
  folder
- **THEN** an aircraft discovery-inclusive list MUST show it as known and installed

#### Scenario: Discovered-only folder surfaced
- **WHEN** inventory cache has a folder not present in known Channel aircraft YAML
- **THEN** discovery-inclusive listing MUST be able to show it as not known (discovered-only)

#### Scenario: Known-only omits discovered-only
- **WHEN** the caller requests known-only aircraft listing
- **THEN** rows MUST be limited to known catalog aircraft (install flags may still reflect cache)
