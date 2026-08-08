## Context

`#8a` catalog sync already replaces `catalog_*` tables from Channel YAML + Spec
enums via `build_snapshot_from_registry` → `CatalogStore.replace_snapshot`.
Strike units exist only on `ChannelRegistry` (`list_strike_units` /
`get_strike_unit`). Agent sees curated ids only inside
`strike_target_class` meta (`unit_ids` / `ship_ids`).

## Goals / Non-Goals

**Goals:**

- `catalog_strike_units` rows: `unit_id`, `label`, `domain`, `theatre`, optional
  `class_ids` (JSON list), synced on every catalog replace.
- Tool + CLI list path reading SQLite only.
- Class tags: invert planning_options `strike_target_class` meta (not new YAML
  fields required for v1).

**Non-Goals:** Upsert-only path (keep full replace); multi-theatre registries;
expanding packaged unit YAML; `#8d` full heuristics.

## Decisions

1. **Replace snapshot** — add table to `_KNOWN_TABLES` and bump
   `CATALOG_SCHEMA_VERSION` so `ensure_synced` rebuilds (match existing pattern;
   ignore BACKLOG “upsert” wording).
2. **Class tagging** — when building snapshot, scan planning_options with
   `family=strike_target_class`; map each `unit_ids`/`ship_ids` entry → class id.
   Units with no class still sync (domain+label only).
3. **Tool** — `list_strike_targets(domain?: land|sea, class_id?: str, q?: str)`
   → `{ok, units:[{unit_id,label,domain,class_ids,theatre}]}`. Case-insensitive
   substring `q` on id/label.
4. **CLI** — `catalog list --type strike_units` (or `strike_targets`) with optional
   filters if cheap; sync summary prints count.
5. **Invent** — prompt/schema one-liner: call tool before inventing GA/recon
   `targets[]`; prefer returned ids.

## Risks / Trade-offs

- [Stale class tags if planning_options drift] → Same sync pass as options; tests
  pin Uboat + Blitz class membership.
- [Agent skips tool] → Prompt/schema note; `#8d` later hardens.

## Migration Plan

- Schema version bump forces resync on next `ensure_synced` / `catalog sync`.
- Additive tool; omit = prior invent behaviour (weaker).

## Open Questions

- CLI type name: `strike_units` vs `strike_targets` (prefer `strike_units` to
  match table).
