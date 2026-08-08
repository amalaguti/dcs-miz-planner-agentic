## 1. Catalog sync

- [x] 1.1 Add `catalog_strike_units` model + schema; bump catalog schema version;
      include in replace/load/`_KNOWN_TABLES`
- [x] 1.2 Build rows in `build_snapshot_from_registry` from registry strike units;
      attach class tags from `strike_target_class` planning_options meta
- [x] 1.3 CLI list `--type strike_units` (+ sync summary count); tests assert
      Uboat sea + Blitz land after sync

## 2. Agent tool

- [x] 2.1 Implement `list_strike_targets` in tools (SQLite only; domain/class/q)
- [x] 2.2 Register in `tool_bridge` TOOL_DEFINITIONS + dispatch; export
- [x] 2.3 Tool/dispatch tests for sea filter and aaa_guns class

## 3. Invent guidance + docs

- [x] 3.1 Prompts + schema notes: call tool before inventing targets[]
- [x] 3.2 README / ARCHITECTURE / BACKLOG `#8c` building→done; LESSONS if needed
- [x] 3.3 Ruff + full pytest green
- [x] 3.4 Accept: CLI/API — sync + list_strike_targets shows Uboat_VIIC (no ME)
