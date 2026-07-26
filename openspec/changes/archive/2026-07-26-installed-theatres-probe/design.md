## Context

`ChannelRegistry.has_theatre()` answers a static product question: does this build know how to
compile for a theatre? It does not answer the user-specific question: can this DCS installation
load that theatre now?

Local DCS evidence is spread across:

- `<DCS root>/autoupdate.cfg`: updater module ids currently installed.
- `<DCS root>/Mods/terrains/*/entry.lua`: static theatre id, updater id, and plugin metadata.
- `<Saved Games>/DCS*/Config/pluginsEnabled.lua`: explicit plugin enable/disable overrides when
  present.

These files can change independently when DCS updates, modules are installed/removed, profiles
change, or plugins are enabled/disabled. They are untrusted input and must be read without
executing Lua.

## Goals / Non-Goals

**Goals:**

- Produce a typed inventory of local theatre availability with evidence and diagnostics.
- Persist that inventory in a user-local **SQLite** database; ordinary reads hit SQLite; rescan
  only on explicit refresh or when no usable DB exists (maps/modules change infrequently).
- Keep static planner support (YAML registry) separate from mutable local installation state
  (SQLite cache).
- Support explicit roots, normal Windows discovery, multiple DCS variants, and clear ambiguity.
- Expose refresh through both Python and CLI surfaces for later user/agent requests.
- Test entirely with synthetic directory fixtures and a temp SQLite path; never depend on the
  developer's DCS install or real app-data DB.

**Non-Goals:**

- Mutating DCS, checking online licenses, or bypassing DCS authorization.
- General-purpose Lua parsing/execution.
- Adding compiler support or reference data for newly discovered maps.
- TTL / background auto-refresh.
- Migrating packaged Channel YAML into SQLite, or building a full agent-facing landmark/weapon
  inventory product in this change (SQLite schema may leave room for later tables).

## Decisions

1. **Separate static support from dynamic availability**
   - `ChannelRegistry` remains packaged YAML — the committed product source of truth.
   - A new install-probe module returns `TheatreInstallation` records and stores them in SQLite.
   - A caller may intersect `registry.list_theatres()` with rows whose state is `available`.
   - Alternative: inject local state into registry YAML — rejected because installation state is
     user-specific, mutable, and must never be committed.

2. **Resolve install/profile roots explicitly and conservatively**
   - Precedence: explicit API/CLI path, environment override, Windows DCS install metadata/common
     locations.
   - Saved Games roots use an explicit override or discovered `Saved Games/DCS*` profiles.
   - Multiple plausible installs are reported separately (with variant/root); no silent winner.
   - A missing root is a clear probe diagnostic and non-zero CLI result, not an empty “nothing
     installed” success.

3. **Use corroborated local evidence and a typed state**
   - Read `autoupdate.cfg` as JSON and scan `Mods/terrains/*/entry.lua`.
   - Extract only quoted static assignments for `id`, `update_id`, `state`, and plugin id; never
     execute or import Lua.
   - Read `pluginsEnabled.lua` only as a constrained table of string-to-boolean overrides.
   - States: `available`, `disabled`, `incomplete`, and `unknown`.
     - `available`: terrain metadata exists, updater id is present in `autoupdate.cfg`, and no
       explicit disable override applies.
     - `disabled`: an explicit matching plugin override is false.
     - `incomplete`: filesystem and updater evidence disagree (common during removal/update).
     - `unknown`: required metadata is malformed, unreadable, or contradictory.
   - Absence from a prior result is not a tombstone row; refresh replaces the theatre set for the
     scanned roots. Callers comparing successive refreshes can report additions/removals.
   - DCS entitlement/login metadata may be exposed as evidence, but this offline probe does not
     claim to prove a current online license.

4. **SQLite cache by default; refresh on demand**
   - Default DB path: `%LOCALAPPDATA%\dcs-miz-planner\inventory.sqlite` on Windows (override via
     env/API for tests). Never commit the file; keep it under a gitignored / app-data location.
   - Schema (minimal for this change; extensible later):
     - `scan_meta` — `scanned_at`, selected `dcs_root`(s), `saved_games_root`(s), diagnostics blob
     - `theatres` — `theatre_id`, `update_id`, `dcs_root`, `state`, `planner_supported`, path /
       evidence fields
   - Ordinary reads (`get_inventory()` / `dcs-miz theatres`) query SQLite when populated.
   - `refresh()` / `--refresh` rescans disk and replaces theatre rows in a transaction (or via
     atomic file replace) and updates `scanned_at`.
   - If the DB is missing or has no usable theatre inventory, the first read performs one scan and
     populates SQLite.
   - Use stdlib `sqlite3` only — no new package dependency.
   - Alternative: JSON/YAML snapshot file — rejected in favor of SQLite so a later agent can query
     with SQL and we can add aircraft/module tables without inventing a second cache format.
   - Alternative: put Channel registry facts into the same DB — rejected; committed product data
     stays reviewable YAML (`reference-registry-channel` decision unchanged).
   - Alternative: fresh-scan every call — rejected (cost vs rare module changes).
   - Alternative: TTL background refresh — deferred; explicit refresh is clearer.

5. **CLI uses a subcommand without breaking compile**
   - Evolve `dcs-miz` to subcommands while preserving legacy `dcs-miz <spec.yaml>` behavior.
   - Add `dcs-miz theatres [--dcs-root PATH] [--saved-games PATH] [--refresh] [--json]`.
   - Default `theatres` lists the SQLite inventory (or scans once if empty/missing).
   - `--refresh` forces a full rescan and updates the DB; output should show `scanned_at` so
     callers know whether they are looking at a cached or just-refreshed result.
   - Human output shows DCS id, updater id, state, planner support, root, and diagnostics.

## Risks / Trade-offs

- [DCS changes local file formats] → Constrained parsers fail to `unknown` with source diagnostics;
  fixture tests lock known formats without executing Lua.
- [Plugin keys differ from theatre ids] → Match only exact extracted plugin/theatre ids and preserve
  unmatched overrides as diagnostics; never fuzzy-match names.
- [A physically installed module lacks current entitlement] → Do not equate the offline result with
  online license authorization; report only observed local availability evidence.
- [Multiple installs/profiles disagree] → Keep records scoped to their install/profile and require
  callers to select rather than merging silently.
- [CLI compatibility regression] → Add parser tests for both legacy compile syntax and the new
  theatre command.
- [SQLite schema churn as probes expand] → Keep a small versioned schema; migrate in place or
  recreate on incompatible version during refresh.

## Migration Plan

1. Add typed records, root locator, constrained readers, and synthetic fixture tests.
2. Add SQLite inventory store + on-demand refresh API and static-support intersection helper.
3. Add CLI reporting (cache by default, `--refresh` to rescan) while retaining compile syntax.
4. Document SQLite path, cache vs refresh, and YAML-vs-SQLite split; update the architecture map.
5. Roll back by removing the probe/CLI subcommand and deleting the local DB; registry YAML and
   compiler remain unchanged.

## Open Questions

- Whether a later agent service should diff successive refreshed SQLite snapshots to notify users
  that a map was added/removed.
- Whether aircraft and asset-pack probing should add tables to the same `inventory.sqlite` in a
  separate change (recommended yes; not in this change’s scope).
