## Why

The package is still small but growing (Spec → loader → registry → compiler → CLI, plus OpenSpec and hooks). New contributors and agents need a checked-in map of modules and relationships before we add registry/validation churn. Doing that now matches the ideas backlog and reduces orientation cost.

## What Changes

- Add a short checked-in architecture doc with a module relationship diagram (ASCII or Mermaid) covering the runtime path and key repo areas.
- Link it from `README.md` Docs (keep README brief).
- Add a lightweight reminder (Cursor hook and/or skill note) to refresh the diagram when package layout or public compile flow changes — not a heavy CI generator.
- No change to Mission Spec or compile behaviour; Manston `.miz` acceptance is unchanged and not re-required for this docs change.

## Non-goals

- Auto-generated UML from every commit or Graphviz CI pipeline.
- Documenting gitignored `research/` dumps or every OpenSpec archive.
- Implementing the Channel registry, agent layer, or Lua enrichment.
- Replacing `DCS_AI_Mission_Planner.md` concept essay — this is the *code* module map.

## Capabilities

### New Capabilities

- `dev-docs`: Maintained developer-facing module map and relationship diagram for the mission planner package and supporting repo layout.

### Modified Capabilities

- (none — no product Spec/compiler requirement changes)

## Impact

- New doc under `docs/` (e.g. `docs/ARCHITECTURE.md`); README Docs link.
- Optional `.cursor/hooks` reminder on push when `src/` layout changed (same pattern as README reminder).
- Unblocks clearer review of upcoming `reference-registry-channel` and later layers.
