## Context

Theatre probe uses `autoupdate.cfg` + `Mods/terrains`. Aircraft live under
`Mods/aircraft/<id>` and/or `CoreMods/WWII Units/<folder>` (FW-190 folders use hyphens).
Updater ids (`SPITFIRE-MKIX`) do not match Spec type ids — folder presence is the
reliable soft check.

## Goals / Non-Goals

**Goals:** Soft-warn missing known Channel aircraft packs; hermetic tests; no YAML writes.

**Non-Goals:** `#8a.1` discovery listing; hard errors; non-Channel theatres.

## Decisions

1. **Static map in code** (committed, not harvested) from Spec id → relative folder
   candidates. CW Spitfire shares SpitfireLFMkIX folders.
2. **Presence** = any candidate path is a directory under any existing inventory
   `dcs_roots` entry. Skip entirely when no roots resolve on disk (CI without DCS).
3. **`ValidationResult.warnings`** — `tuple[ValidationError, ...]`; `ok` ignores
   warnings. Code `aircraft_module_missing`.
4. **Do not** treat missing module as compile-blocking.

## Risks / Trade-offs

- [Folder rename by ED] → Update static map; warn is advisory.
- [False skip when roots are fake paths] → Only probe existing directories; tests use
  tmp roots.
