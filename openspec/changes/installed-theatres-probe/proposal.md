## Why

The planner currently knows which theatres it supports, but not which ones the user can
actually launch. DCS modules can be installed, removed, enabled, or disabled after any prior
scan, so mission options must come from refreshable local-install evidence rather than a
permanent snapshot.

## What Changes

- Add a read-only DCS installation probe that discovers local theatre modules and reports their
  exact DCS theatre id, updater module id, installation path, and availability state.
- Distinguish planner support from local availability: an installed map is not automatically
  compilable until a project registry/compiler supports it.
- Cache a user-local inventory in **SQLite** after a successful scan; ordinary availability queries
  read that database (module changes are uncommon; full rescans need not run every time).
- Add explicit refresh through a CLI flag and a Python API suitable for a later user/agent
  request; refresh also runs automatically when no usable SQLite inventory exists yet.
- Detect install/uninstall changes and configured enable/disable state where DCS exposes
  trustworthy local metadata; report `unknown` with diagnostics instead of guessing when state
  cannot be established.
- Provide clear handling for missing, moved, malformed, or multiple DCS installations.

## Non-goals

- Installing, uninstalling, enabling, disabling, repairing, or licensing DCS modules.
- Adding compiler/registry support for every detected theatre; The Channel remains the product
  target in this change.
- Probing every aircraft, campaign, weapon, or asset-pack entitlement.
- Executing DCS Lua or importing arbitrary module code to discover metadata.
- Replacing the committed Channel **YAML** registry with SQLite (product facts stay in
  `data/channel/`; SQLite is only the mutable local install cache).

## Capabilities

### New Capabilities

- `installed-theatres`: Read-only discovery, availability classification, SQLite-backed cache,
  refresh behavior, and CLI/API reporting for theatre modules in local DCS installations.

### Modified Capabilities

- `reference-registry`: Separate static planner-supported theatre data from refreshable
  user-install availability so callers can safely intersect the two.

## Impact

- New probe module and tests using synthetic DCS directory fixtures; stdlib `sqlite3` only (no
  new dependency).
- CLI gains a theatre-list/refresh operation without breaking the existing compile command.
- User-local SQLite inventory under app data (`scanned_at`, theatre rows, diagnostics) with
  on-demand refresh; gitignored / never committed.
- Reads DCS `autoupdate.cfg`, terrain `entry.lua` metadata as data, and relevant Saved Games
  enable/disable metadata when available; never mutates the DCS installation.
