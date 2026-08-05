## Why

Theatre discovery is cached on refresh, but aircraft listing is YAML-only
(`AIRCRAFT_DISCOVERY_DEFERRED`). Installs rarely gain planes/maps, so folder harvest
belongs in the same SQLite inventory cache — discovery-only, never auto-promoted.

## What Changes

- Probe aircraft module folders under `Mods/aircraft`, `CoreMods/WWII Units`, and
  `CoreMods/aircraft` during inventory refresh; persist beside theatres in
  `inventory.sqlite`.
- `catalog list --type aircraft` joins known YAML aircraft with cached discovery
  (known vs discovered-only); drop the deferred note.
- Never write discovered folders into Channel YAML / `catalog_aircraft`.

## Non-goals

- Module Manager enable/disable classification for aircraft (folder presence only)
- Promoting Normandy or extra planes into planner-supported Specs
- Parsing full `entry.lua` aircraft metadata beyond presence heuristics
- A separate `dcs-miz aircraft` CLI (catalog list + theatres `--refresh` is enough)

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `installed-theatres`: Inventory refresh also caches aircraft module folders
- `agent-catalog`: Aircraft list joins discovery like theatres; no deferred stub

## Impact

- `install/models.py`, `probe.py`, `store.py`, `service.py`, `aircraft_modules.py`
- `catalog/service.py`, `catalog/models.py`, CLI catalog list
- Tests with fake DCS trees; BACKLOG `#8a.1`; README/LESSONS as needed
