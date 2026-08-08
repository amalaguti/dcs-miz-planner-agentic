## Why

Channel strike shelves are thin (few soft/AAA/sea ids). Invent and pilots need
more era-plausible options without dumping the ME. `#8e` checklist is in place —
first curated expand batch for soft, AAA, and harbour/coastal sea craft.

## What Changes

- Promote verified PyDCS ids into `ground_units.yaml` / `ships.yaml`.
- Extend `strike_target_class` unit/ship lists + cues; `target_motion.yaml`
  profiles; `#15h` AAA allowlist ids.
- At least one new (or updated) example Spec exercising new units; hermetic
  catalog/compile tests.
- BACKLOG class spine / `#8e` next-promote note; LESSONS if needed.

**First batch (verified in PyDCS vehicle_map / ship_map):**

| Domain | Class | New ids |
|--------|-------|---------|
| land | soft_vehicles | `Sd_Kfz_2`, `Horch_901_typ_40_kfz_21`, `Willys_MB` |
| land | aaa_guns | `flak30`, `flak37`, `flak38`, `Flakscheinwerfer_37`, `KDO_Mod40`, `bofors40` |
| sea | sea_craft | `Dry-cargo ship-2`, `HarborTug`, `Higgins_boat` |

## Capabilities

### New Capabilities

- *(none)*

### Modified Capabilities

- `reference-registry`: new Channel strike unit/ship ids.
- `mission-options`: class shelves list new ids / cues.
- `agent-catalog`: sync surfaces new strike units.
- `golden-fixtures`: examples/tests for new shelf members.
- `miz-compiler` / `mission-validation`: only as needed for AAA class id set.

## Impact

- Registry YAML, planning_options, target_motion, target_ai AAA frozenset,
  examples/, tests, BACKLOG.

## Non-goals

- New classes (armor, troops, halftracks_apc, radar) — follow-on.
- ME scrape / Assets Pack dump; invent free-form ids.
- Multi-theatre; train corridors.

## Acceptance

New ids validate + compile in at least one example; `list_strike_targets`
returns them after sync; AAA new flak ids get aaa_alert allowlist behaviour;
hermetic pytest green. ME Instant Action optional do-soon.
