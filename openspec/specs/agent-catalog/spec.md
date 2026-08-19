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

### Requirement: Known catalog includes Normandy
After catalog sync from the packaged registry, known theatres MUST include
`Normandy` and known airfields MUST include `NeedsOarPoint`.

#### Scenario: Sync populates Normandy
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain theatre `Normandy` and airfield
  `NeedsOarPoint`

### Requirement: Catalog lists curated Normandy airfields
After catalog sync from the packaged registry, known airfields for theatre
`Normandy` MUST include the curated keys `NeedsOarPoint`, `Chailey`,
`Funtington`, `Tangmere`, `FordAF`, `Maupertus`, `SaintPierreduMont`, and
`Carpiquet` with their packaged `airdromeId` values.

#### Scenario: Sync populates FordAF
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain airfield `FordAF` with theatre `Normandy`
  and `airdromeId` 31

### Requirement: Offerable Normandy when installed
An offerable-theatre query MUST include `Normandy` when it is known and the
install inventory reports it available and planner-supported.

#### Scenario: Offerable Normandy when installed
- **WHEN** Normandy is known and the install inventory reports it available and
  planner-supported
- **THEN** an offerable-theatre query MUST include Normandy

### Requirement: Catalog countries come from era YAML
Catalog sync SHALL load known country ids from the packaged WWII era countries
table (`UK`, `ThirdReich` only). It MUST NOT invent country ids. `Germany`
MUST NOT appear as a known catalog country.

#### Scenario: Sync lists UK and ThirdReich
- **WHEN** catalog sync runs after the WWII countries package is present
- **THEN** catalog country listing MUST include `UK` and `ThirdReich` and
  MUST NOT include `Germany` as a known id

### Requirement: Strike units carry era_id and stay Channel-tagged
After catalog sync, WWII strike-unit rows SHALL expose `era_id` `wwii` and
SHALL keep stored combat `theatre_id` `TheChannel`. Sync MUST NOT stamp
`theatre_id` `Normandy` on those WWII rows. Modern land trucks SHALL expose
`era_id` `modern` and `theatre_id` `Caucasus`. `list_strike_targets(theatre="Normandy")`
MUST still return WWII **land** units (query-time offer). Sea-domain rows
MUST NOT be returned for Normandy. `list_strike_targets(theatre="Caucasus")`
MUST return the modern trucks and MUST NOT return WWII Channel trucks.
`list_strike_targets(theatre="Syria")` SHALL dual-offer those modern **land**
rows (stored `theatre_id` remains `Caucasus`). `list_strike_targets(theatre="Nevada")`
SHALL dual-offer those same modern **land** rows (stored `theatre_id` remains
`Caucasus`). Channel MUST NOT receive Ural ids. Falklands MUST stay empty.

#### Scenario: Strike unit era and Channel tag
- **WHEN** catalog sync runs
- **THEN** a known land strike unit (e.g. Blitz) MUST have `era_id` `wwii`
  and `theatre_id` `TheChannel`

#### Scenario: Normandy filter offers land units
- **WHEN** `list_strike_targets` is called with theatre `Normandy` after sync
- **THEN** the listing MUST include Blitz (land) and MUST NOT include
  sea_craft

#### Scenario: Caucasus filter offers modern trucks
- **WHEN** catalog sync runs and `list_strike_targets` is called with theatre
  `Caucasus`
- **THEN** `Ural-375` MUST have `era_id` `modern` and `theatre_id` `Caucasus`
  and the listing MUST include it and MUST NOT include `Blitz_36-6700A`

#### Scenario: Syria query dual-offers Caucasus modern land trucks
- **WHEN** catalog lists strike units for theatre `Syria`
- **THEN** `Ural-375`, `GAZ-66`, and `ZIL-135` MUST be offerable without
  changing stored `theatre_id` away from `Caucasus`

#### Scenario: Nevada query dual-offers Caucasus modern land trucks
- **WHEN** catalog lists strike units for theatre `Nevada`
- **THEN** `Ural-375`, `GAZ-66`, and `ZIL-135` MUST be offerable without
  changing stored `theatre_id` away from `Caucasus`

### Requirement: Catalog lists Caucasus and Batumi
After catalog sync from the packaged registry, known theatres MUST include
`Caucasus` and known airfields MUST include `Batumi` with `airdromeId` 22
and theatre `Caucasus`. Known airfields MUST also include the other curated
Caucasus keys (`Kobuleti`, `SenakiKolkhi`, `Kutaisi`, `TbilisiLochini`,
`Vaziani`, `SochiAdler`, `Mozdok`). Known countries for era `modern` MUST
include `Russia`.

#### Scenario: Sync populates Batumi
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain theatre `Caucasus` and airfield `Batumi`
  with `airdromeId` 22

#### Scenario: Sync populates Mozdok and Russia
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain airfield `Mozdok` with `airdromeId` 28
  and theatre `Caucasus`, and country `Russia`

### Requirement: Caucasus CAP places sync into catalog
After `dcs-miz catalog sync`, `channel_place` rows `batumi_home` and
`batumi_black_sea_cap` SHALL be queryable with theatre `Caucasus`.

#### Scenario: Batumi CAP place listed
- **WHEN** catalog planning options are queried after sync
- **THEN** `batumi_black_sea_cap` MUST appear with theatre Caucasus and CAP
  meta 270° / 40 km

### Requirement: Catalog lists Syria and Incirlik
After catalog sync from the packaged registry, known theatres MUST include
`Syria` and known airfields MUST include `Incirlik` with `airdromeId` 16
and theatre `Syria`.

#### Scenario: Sync populates Incirlik
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain theatre `Syria` and airfield `Incirlik`
  with `airdromeId` 16

### Requirement: Catalog lists extra Syria airfields and Syria country
After `dcs-miz catalog sync`, known airfields MUST include `Palmyra` with
`airdromeId` 28 and theatre `Syria`, and known countries MUST include
`Syria` (modern).

#### Scenario: Sync populates Palmyra
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain airfield `Palmyra` with `airdromeId` 28
  and theatre `Syria`, and country `Syria`

### Requirement: Catalog lists Nevada and Nellis
After catalog sync from the packaged registry, known theatres MUST include
`Nevada` and known airfields MUST include `Nellis` with `airdromeId` 4
and theatre `Nevada`.

#### Scenario: Sync populates Nellis
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain theatre `Nevada` and airfield `Nellis`
  with `airdromeId` 4

### Requirement: Catalog lists extra Nevada airfields
After catalog sync from the packaged registry, known airfields MUST include
`GroomLake` with `airdromeId` 2 and theatre `Nevada` (and the other curated
Nevada keys besides `Nellis`).

#### Scenario: GroomLake is a known Nevada airfield
- **WHEN** catalog sync runs after the Nevada Stage B airfield table is present
- **THEN** airfield listing MUST include `GroomLake` with theatre `Nevada`
  and `airdromeId` 2

### Requirement: Catalog lists Falklands and MountPleasant
After catalog sync from the packaged registry, known theatres MUST include
`Falklands` and known airfields MUST include `MountPleasant` with
`airdromeId` 2 and theatre `Falklands`.

#### Scenario: Sync populates MountPleasant
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain theatre `Falklands` and airfield
  `MountPleasant` with `airdromeId` 2

### Requirement: Catalog lists extra Falklands airfields and Argentina country
After catalog sync from the packaged registry, known airfields MUST include
`RioGallegos` with `airdromeId` 5 and theatre `Falklands` (and the other
curated keys besides `MountPleasant`), and known countries MUST include
`Argentina` (modern). `list_strike_targets(theatre=Falklands)` MUST dual-offer
Caucasus modern land trucks (same query-time predicate as Syria/Nevada).
Stored `theatre_id` MUST remain `Caucasus`. Channel MUST NOT receive Ural ids.

#### Scenario: Sync populates RioGallegos
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain airfield `RioGallegos` with `airdromeId` 5
  and theatre `Falklands`, and country `Argentina`

#### Scenario: Falklands strike listing dual-offers modern land trucks
- **WHEN** catalog/tools list strike units for theatre `Falklands`
- **THEN** `Ural-375`, `GAZ-66`, and `ZIL-135` MUST be present and Channel
  WWII trucks MUST be absent

### Requirement: Catalog lists Kola and Bodo
After catalog sync from the packaged registry, known theatres MUST include
`Kola` and known airfields MUST include `Bodo` with `airdromeId` 7 and
theatre `Kola`.

#### Scenario: Sync populates Bodo
- **WHEN** a catalog sync runs against the packaged registry after this
  change
- **THEN** the catalog MUST contain theatre `Kola` and airfield `Bodo` with
  `airdromeId` 7
