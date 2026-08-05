## ADDED Requirements

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
