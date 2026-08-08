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

### Requirement: Strike unit and theatre promote uses checklist
Expanding known strike/recon units or theatres in the catalog MUST follow the
checked-in theatre/target promote checklist (curated YAML → catalog sync). The
system MUST NOT auto-promote discovery-only install folders or ME scrapes into
known catalog sources.

#### Scenario: Promote path points at checklist
- **WHEN** a developer adds a verified ground/ship id to Channel registry YAML
  and runs catalog sync
- **THEN** the catalog MUST list the new strike unit after sync, and project
  docs MUST point at the promote checklist for the required steps (class shelf,
  motion/AI, examples, invent cues)

### Requirement: Catalog exposes mission behaviour and inspiration options
After catalog sync from packaged Channel data, planning-option queries MUST include
`mission_behaviour` and `mission_inspiration` family rows when present in the packaged
planning-options source, with the same support-level honesty as other planning options.

#### Scenario: Sync surfaces mission_behaviour
- **WHEN** catalog sync runs after packaged `mission_behaviour` options are added
- **THEN** listing planning options for family `mission_behaviour` MUST return those rows

#### Scenario: Sync surfaces mission_inspiration
- **WHEN** catalog sync runs after packaged `mission_inspiration` options are added
- **THEN** listing planning options for family `mission_inspiration` MUST return those rows

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

### Requirement: Catalog exposes mission-designer shelf options
After catalog sync from packaged Channel data, planning-option queries MUST include
`dynamics_mode`, `strike_target_class`, and `channel_place` family rows when present in
the packaged planning-options source, with the same support-level honesty as other
planning options.

#### Scenario: Sync surfaces dynamics_mode
- **WHEN** catalog sync runs after packaged `dynamics_mode` options are added
- **THEN** listing planning options for family `dynamics_mode` MUST return those rows

#### Scenario: Sync surfaces strike_target_class
- **WHEN** catalog sync runs after packaged `strike_target_class` options are added
- **THEN** listing planning options for family `strike_target_class` MUST return those rows

#### Scenario: Sync surfaces channel_place
- **WHEN** catalog sync runs after packaged `channel_place` options are added
- **THEN** listing planning options for family `channel_place` MUST return those rows

### Requirement: Catalog sync includes strike units
`dcs-miz catalog sync` (and `ensure_synced`) SHALL replace `catalog_strike_units`
rows from the Channel registry land + sea strike units, including `unit_id`,
`label`, `domain`, `theatre` (TheChannel), and optional class id tags derived from
packaged `strike_target_class` planning options. Compile/validate MUST continue to
use the registry as SoT.

#### Scenario: Sync includes U-boat
- **WHEN** catalog sync runs against packaged Channel data
- **THEN** `catalog_strike_units` MUST contain `Uboat_VIIC` with domain `sea`

#### Scenario: Sync includes soft truck
- **WHEN** catalog sync runs against packaged Channel data
- **THEN** `catalog_strike_units` MUST contain a known soft land unit (e.g. Blitz)
  with domain `land`

### Requirement: Catalog lists expanded strike units
After catalog sync, `list_strike_targets` / strike-unit listing SHALL return the
newly promoted Channel soft, AAA, and sea ids with correct domain and class tags.

#### Scenario: Sea filter includes HarborTug
- **WHEN** list_strike_targets is called with domain=sea after sync
- **THEN** results MUST include HarborTug

### Requirement: Catalog lists halftracks_apc strike units
After catalog sync, `list_strike_targets` with class_id `halftracks_apc` SHALL
return the promoted Channel halftrack unit ids.

#### Scenario: Filter by halftracks_apc
- **WHEN** list_strike_targets is called with class_id halftracks_apc
- **THEN** the result MUST include Sd_Kfz_251 among unit_ids

### Requirement: Catalog lists armor strike units
After catalog sync, `list_strike_targets` with class_id `armor` SHALL return the
promoted Channel armor unit ids.

#### Scenario: Filter by armor
- **WHEN** list_strike_targets is called with class_id armor
- **THEN** the result MUST include Pz_IV_H among unit_ids

### Requirement: Catalog lists troops strike units
After catalog sync, `list_strike_targets` with class_id `troops` SHALL return the
promoted Channel infantry unit ids.

#### Scenario: Filter by troops
- **WHEN** list_strike_targets is called with class_id troops
- **THEN** the result MUST include soldier_mauser98 among unit_ids

### Requirement: Catalog lists trains strike units
After catalog sync, `list_strike_targets` with class_id `trains` SHALL return the
promoted Channel train unit ids.

#### Scenario: Filter by trains
- **WHEN** list_strike_targets is called with class_id trains
- **THEN** the result MUST include Locomotive among unit_ids

### Requirement: Catalog lists radar_c3 strike units
After catalog sync, `list_strike_targets` with class_id `radar_c3` SHALL return
the promoted Channel radar unit ids.

#### Scenario: Filter by radar_c3
- **WHEN** list_strike_targets is called with class_id radar_c3
- **THEN** the result MUST include FuMG-401 among unit_ids

### Requirement: Catalog lists R13 promoted strike units
After catalog sync, list_strike_targets SHALL return R13-promoted ids under the
correct class filters.

#### Scenario: Armor filter includes Tiger_I
- **WHEN** list_strike_targets is called with class_id armor
- **THEN** results MUST include Tiger_I
