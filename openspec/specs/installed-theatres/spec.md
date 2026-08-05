# Installed Theatres

## Purpose

Read-only discovery of theatre modules in the local DCS installation, with
availability classification, SQLite-backed cache, on-demand refresh, and
CLI/API reporting. Exact DCS ids only; never execute DCS Lua.

## Requirements

### Requirement: Discover local DCS theatre installations
The system SHALL inspect a selected local DCS installation and return typed theatre records
containing the exact DCS theatre id, updater module id, installation root, and observed
availability state. The probe MUST NOT execute DCS Lua.

#### Scenario: Installed Channel theatre is discovered
- **WHEN** the selected DCS root contains `TheChannel` terrain metadata and
  `THECHANNEL_terrain` is present in the updater module list
- **THEN** the probe MUST report theatre id `TheChannel`, updater id `THECHANNEL_terrain`, and its
  observed availability state

#### Scenario: Untrusted entry file is treated as data
- **WHEN** a terrain `entry.lua` contains executable statements beyond the supported static fields
- **THEN** the probe MUST NOT execute the file and MUST extract only supported quoted metadata or
  report the record as `unknown`

### Requirement: Classify mutable availability without guessing
The system SHALL classify each discovered theatre as `available`, `disabled`, `incomplete`, or
`unknown` from current local evidence. It MUST preserve diagnostics when evidence is missing,
malformed, contradictory, or cannot establish a trustworthy state.

#### Scenario: Explicitly disabled theatre
- **WHEN** an installed terrain has a matching explicit false enablement override in the selected
  DCS Saved Games profile
- **THEN** the probe MUST report that theatre as `disabled` and MUST NOT offer it as currently
  available

#### Scenario: Enablement changes after a scan
- **WHEN** a user changes a matching theatre override from disabled to enabled and refreshes
- **THEN** the refreshed result MUST reflect the new state without requiring an application
  reinstall or editing packaged registry data

#### Scenario: Removal or partial update
- **WHEN** a theatre directory and the updater module list disagree
- **THEN** the probe MUST report `incomplete` with diagnostics rather than claiming the theatre is
  available

#### Scenario: Offline entitlement is not provable
- **WHEN** local installation evidence exists but current DCS license authorization cannot be
  established offline
- **THEN** the probe MUST describe only observed local availability and MUST NOT claim that online
  entitlement is verified

### Requirement: Cache inventory in SQLite; refresh on demand
The system SHALL persist a user-local theatre inventory in a SQLite database after a successful
scan and SHALL serve ordinary availability queries from that database. The default database path
MUST be under the user's local application data directory (Windows:
`%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite`) and MUST be overridable for tests. The system
MUST provide a Python refresh operation and a CLI `--refresh` option that re-read all selected DCS
installation and profile sources and replace the cached theatre rows. When no usable SQLite
inventory exists, the first query MUST perform one scan and populate the database. The inventory
MUST expose `scanned_at` so callers can tell cached from just-refreshed results. The packaged
Channel YAML registry MUST remain the committed product source of truth and MUST NOT be migrated
into this SQLite file by this change.

#### Scenario: Ordinary list uses SQLite cache
- **WHEN** a usable SQLite inventory already exists and the caller lists theatres without
  requesting refresh
- **THEN** the system MUST return the cached records from SQLite and MUST NOT require a full disk
  rescan

#### Scenario: Explicit refresh after install
- **WHEN** a theatre is installed after an inventory was cached and the caller requests refresh
- **THEN** the replacement SQLite inventory MUST include the newly installed theatre

#### Scenario: Explicit refresh after uninstall
- **WHEN** a theatre is uninstalled after an inventory was cached and the caller requests refresh
- **THEN** the replacement SQLite inventory MUST no longer offer that theatre as available

#### Scenario: First use with no database
- **WHEN** no usable SQLite inventory exists and the caller lists theatres
- **THEN** the system MUST scan local sources once, write the SQLite inventory, and return it

#### Scenario: CLI without refresh keeps prior SQLite rows
- **WHEN** a user changes installed or enabled modules and then runs the theatre-list CLI without
  `--refresh`
- **THEN** the command MAY still report the previous SQLite inventory until an explicit refresh (or
  a missing-inventory first scan) updates it

#### Scenario: Registry YAML stays separate
- **WHEN** the install inventory is stored in SQLite
- **THEN** Channel airfield/aircraft/weather product facts MUST continue to come from the packaged
  YAML registry, not from the install inventory database

### Requirement: Discover roots and expose ambiguity
The system SHALL accept explicit DCS install and Saved Games roots and SHALL support conservative
Windows discovery when they are omitted. Missing or multiple plausible installations MUST be
reported clearly and MUST NOT be silently interpreted as an empty inventory or collapsed into one
installation.

#### Scenario: Explicit custom install path
- **WHEN** a user supplies a valid custom DCS root
- **THEN** the probe MUST inspect that root without requiring DCS to be installed in a default
  location

#### Scenario: Windows registry install path
- **WHEN** no explicit root is given and the Windows registry contains
  `SOFTWARE\Eagle Dynamics\DCS World` `Path` pointing at a valid install
- **THEN** the probe MUST discover that installation (including non-Program-Files locations)

#### Scenario: DCS root cannot be found
- **WHEN** neither an explicit root nor a discoverable installation is available
- **THEN** the probe MUST return a clear diagnostic and the CLI MUST exit non-zero

#### Scenario: Multiple DCS installations
- **WHEN** stable and open-beta or other distinct DCS roots are discovered
- **THEN** the probe MUST keep results scoped by installation and MUST NOT silently choose or merge
  them

### Requirement: Report theatres through CLI and API
The system SHALL expose current theatre records through a Python API suitable for later user/agent
requests and a CLI command supporting human-readable and JSON output. Each record MUST indicate
both local availability and whether this planner currently supports compilation for its exact
theatre id.

#### Scenario: Installed but unsupported map
- **WHEN** the probe discovers an available theatre not listed by the project reference registry
- **THEN** output MUST show it as locally available but planner-unsupported and MUST NOT offer it
  for compilation

#### Scenario: Channel is installed and supported
- **WHEN** `TheChannel` is locally available and listed by the project reference registry
- **THEN** output MUST show it as both locally available and planner-supported

#### Scenario: Machine-readable refresh result
- **WHEN** the user requests JSON output with refresh
- **THEN** the CLI MUST emit records, source roots, scan timestamp, and diagnostics in a stable
  machine-readable structure

### Requirement: Cache discovered aircraft module folders
Inventory refresh MUST scan each discovered DCS root for aircraft module folders under
at least `Mods/aircraft`, `CoreMods/WWII Units`, and `CoreMods/aircraft`, persist them
in the same SQLite inventory database as theatres, and serve them from cache until the
next explicit refresh. Shared non-aircraft directories under `WWII Units` (e.g. Encyclopedia,
Weapons, l10n) MUST NOT be listed as aircraft modules. Discovery MUST NOT write into
packaged Channel YAML or known `catalog_aircraft` rows.

#### Scenario: Refresh caches aircraft folders
- **WHEN** a fake DCS tree contains `Mods/aircraft/SpitfireLFMkIX` and the caller
  refreshes inventory
- **THEN** the cached inventory MUST include that aircraft module folder

#### Scenario: Cache served without rescan
- **WHEN** inventory was refreshed earlier and the caller reads inventory without refresh
- **THEN** aircraft module rows MUST come from SQLite (from_cache) matching the last scan

#### Scenario: Non-aircraft WWII Units dirs skipped
- **WHEN** `CoreMods/WWII Units/Weapons` exists beside a real aircraft folder
- **THEN** refresh MUST NOT list `Weapons` as an aircraft module
