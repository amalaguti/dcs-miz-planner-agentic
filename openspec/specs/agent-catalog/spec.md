# Agent Catalog

## Purpose

Local SQLite known-catalog tables for agent/UI queries, synced from packaged Channel YAML
and Mission Spec enums. YAML/Spec remain the compile source of truth; install inventory
stays a separate discovery layer (joined for theatre offerability).

## Requirements

### Requirement: Synced known agent catalog
The system SHALL maintain local SQLite `catalog_*` tables for **known** planner resources
synced from the packaged Channel YAML registry and Mission Spec enums. Known rows MUST NOT
invent DCS identifiers. The catalog MUST NOT replace YAML/Spec as the compile source of truth.

#### Scenario: Sync populates known Channel resources
- **WHEN** a catalog sync runs against the packaged Channel registry
- **THEN** the catalog MUST contain known Channel airfields (including Manston), aircraft
  (including SpitfireLFMkIX and Bf-109K-4), theatre `TheChannel`, and Spec mission types
  `free_flight` and `intercept`

### Requirement: Discovery join for local theatres
The catalog query layer SHALL combine known theatres with the user-local install inventory so
callers can distinguish known-only, discovered-installed, and **offerable** theatres
(known AND install `available` AND `planner_supported`). Discovery MUST NOT auto-insert
install-only theatres into known YAML.

#### Scenario: Offerable Channel when installed
- **WHEN** TheChannel is known and the install inventory reports it available and
  planner-supported
- **THEN** an offerable-theatre query MUST include TheChannel

#### Scenario: Discovered unsupported theatre visible
- **WHEN** the install inventory reports a theatre that is not in the known catalog
- **THEN** a catalog list mode that includes discovery MUST be able to surface it as
  installed-but-not-known (or equivalent), without treating it as compile-supported

### Requirement: Catalog enumeration API and CLI
The system SHALL provide a query API and CLI to sync and list catalog objects (human + JSON),
including filters for type and known vs discovery-inclusive theatre listing.

#### Scenario: List known airfields
- **WHEN** a user lists airfields after sync
- **THEN** output MUST include Manston and other known Channel airfields

### Requirement: Catalog sync includes planning options
Catalog sync from packaged Channel data SHALL also replace planning-option rows from the
packaged planning-options source so agent/UI queries stay aligned with the product package.

#### Scenario: Sync refreshes planning options idempotently
- **WHEN** catalog sync runs twice without package changes
- **THEN** planning-option query results MUST remain equivalent (same ids and support levels)

### Requirement: Ad-hoc growth of known catalog
Expanding what the planner can compile MUST be done by updating packaged known sources
(YAML / Spec enums) through the normal change process, then re-running catalog sync.
The system MUST document this workflow. Automatic promotion from discovery into known
sources is out of scope for this capability.

#### Scenario: Documented promote path
- **WHEN** a developer adds a new verified airfield or aircraft to Channel YAML and syncs
- **THEN** the catalog MUST list the new known row after sync without requiring hand-edited SQL
