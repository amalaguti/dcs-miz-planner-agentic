## Context

Known Channel registry stays small and verified. User wants discovery of local installs and
an ad-hoc way to grow known later — without treating SQLite as authoring SoT.

## Goals / Non-Goals

**Goals:**

- Known `catalog_*` sync from YAML + Spec enums.
- Discovery visibility: theatres from install inventory; clear `known` / `installed` /
  `offerable` (known ∧ available ∧ planner_supported).
- Documented ad-hoc path to add known rows (edit YAML → verify in DCS → sync catalog).
- CLI list with filters (e.g. known-only vs include discovered theatres).

**Non-Goals:**

- Auto-discover all aircraft into known; NL agent; prefs/history; Normandy compile.

## Decisions

1. **Two layers, one DB family**
   - `catalog_*` = known sync from package.
   - Install tables unchanged; catalog API joins for theatres.
   - Discovered-only theatres appear in list with `planner_supported=false` / `known=false`.

2. **Aircraft discovery deferred as stub**
   - v1: no module harvest into catalog.
   - Design note + optional empty `discovered_aircraft` placeholder or backlog follow-up
     (`catalog-discover-modules`) — do not fake rows from install in this change.

3. **Ad-hoc known maintenance (documented, not automated promotion)**
   - Expand `data/channel/*.yaml` (and Spec enums when needed) via normal PR/change.
   - Acceptance: in-game compile for that asset when it becomes compile-supported.
   - Run `dcs-miz catalog sync` after YAML change.
   - Never “save from discovery UI → known YAML” in v1 (avoids silent SoT corruption).

4. **Sync + CLI** as before (`sync`, `list [--type] [--json]`, offerable helper).

## Risks / Trade-offs

- [User expects full aircraft discovery now] → Explicit stub + follow-up item; list messaging.
- [YAML drift] → Sync version/checksum; tests.

## Migration Plan

1. Schema + known sync + theatre join + CLI + docs (ad-hoc promote workflow).
2. Accept via CLI list (known Channel + discovered theatres from local inventory).
3. Next: `agent-tools-surface`; later discovery expansion as its own change.

Open Questions — resolved at apply: share `inventory.sqlite` (least friction; separate table namespaces).
