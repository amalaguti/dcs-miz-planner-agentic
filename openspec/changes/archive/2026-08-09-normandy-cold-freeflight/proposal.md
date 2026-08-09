## Why

The Channel is the only planner-supported map. Normandy 2.0 is installed, PyDCS-bound
(38 airfields), and next on the definitive fleet promote order — we need a Manston-
equivalent smoke so multi-theatre is real, not aspirational.

## What Changes

- Bind Spec theatre id `Normandy` to PyDCS `Normandy` terrain.
- Registry: list `Normandy` as supported; add curated airfield key `NeedsOarPoint`
  (airdromeId 28 / Needs Oar Point).
- Example Spec + hermetic validate/compile path for cold freeflight Spitfire at
  Needs Oar Point (sunny morning, UK blue).
- Inventory fixtures / tests treat Normandy as available + planner_supported when
  exercising that Spec.
- Docs: definitive map fleet note; README status mentions Normandy smoke.

## Non-goals

- Full Normandy airfield catalog, GA shelves, places, or invent multi-theatre cues.
- Syria / Marianas WWII / Kola / Iraq planner support.
- Changing Channel Manston acceptance or invent Channel-only behaviour.
- Auto-promoting every PyDCS Normandy airport into YAML.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: supported theatres include `Normandy`; NeedsOarPoint airfield.
- `miz-compiler`: compile Normandy free_flight cold parking at NeedsOarPoint.
- `mission-validation`: accept Normandy Spec when registry + inventory agree.
- `mission-spec`: Normandy freeflight example Shape (theatre/airfield).
- `golden-fixtures`: hermetic Normandy compile coverage (structure asserts or fixture).
- `installed-theatres` / `agent-catalog` / `agent-tools`: Normandy offerable when
  known + available + planner_supported.

## Impact

`theatre_terrain.py`, Channel package YAML (`theatres.yaml`, `airfields.yaml`),
examples, `fixtures_support`, tests, catalog sync expectations, README/BACKLOG.
Acceptance: open compiled `.miz` in DCS ME Instant Action on Normandy 2.0.
