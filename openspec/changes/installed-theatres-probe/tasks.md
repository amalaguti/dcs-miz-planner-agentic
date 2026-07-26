## 1. Probe model and constrained readers

- [x] 1.1 Add typed installation, theatre-record, availability-state, and diagnostic models
- [x] 1.2 Implement explicit/environment/Windows DCS-root and Saved Games profile discovery with clear missing/multiple-root diagnostics
- [x] 1.3 Parse `autoupdate.cfg` and terrain `entry.lua` static identity fields as untrusted data without executing Lua
- [x] 1.4 Parse exact boolean overrides from `pluginsEnabled.lua`; classify available/disabled/incomplete/unknown with evidence

## 2. SQLite cache, refresh, and planner support

- [x] 2.1 Implement user-local SQLite inventory (`%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite`, overridable) with `scan_meta` + `theatres`; ordinary reads query DB; `refresh()` rescans and replaces in a transaction; first read scans if empty/missing
- [x] 2.2 Add helper/output fields that intersect exact local theatre ids with static YAML registry support without mutating registry data or copying YAML into SQLite
- [x] 2.3 Ensure missing, malformed, moved, and multiple installations remain scoped and diagnostic rather than silently empty/merged

## 3. CLI surface

- [x] 3.1 Add `dcs-miz theatres` with `--dcs-root`, `--saved-games`, `--refresh`, and `--json` (default = SQLite-backed list)
- [x] 3.2 Preserve existing `dcs-miz <spec.yaml> [-o ...]` compile behavior and exit codes
- [x] 3.3 Format human/JSON output with state, planner support, roots, `scanned_at`, evidence, and diagnostics

## 4. Automated verification

- [x] 4.1 Build synthetic DCS install/profile fixtures and a temp SQLite path; never read the developer's real install or real app-data DB in unit tests
- [x] 4.2 Test Channel discovery, exact ids, no Lua execution, SQLite cache hit without rescan, disabled/enabled + install/uninstall via explicit refresh, and partial/malformed evidence
- [x] 4.3 Test explicit/custom roots, missing roots, multiple installs, unsupported installed maps, and stable JSON output
- [x] 4.4 Test both the legacy compile CLI and the new theatre CLI; run Ruff and the full pytest suite

## 5. Documentation and acceptance

- [x] 5.1 Update README usage, `docs/ARCHITECTURE.md`, and `docs/BACKLOG.md`; document YAML registry vs SQLite install cache, default DB path, and `--refresh` / API refresh
- [x] 5.2 Run the CLI against an explicitly selected local DCS install and confirm it reports `TheChannel` with exact ids and planner support (accepted 2026-07-26: `TheChannel` / `THECHANNEL_terrain` / available / planner_supported)
- [x] 5.3 Confirm default list uses SQLite cache, and `--refresh` updates the DB after a synthetic install/remove or enable/disable change (unit tests + live CLI `from_cache: true` after refresh)
