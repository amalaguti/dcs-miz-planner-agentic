## Why

The first R13 shelf (`channel-shelf-r13-promote`) took the high-count campaign
ids (Flak 41, Quadmount, heavies, LST, cargo coaches). A rescan of the 60
installed Spitfire Channel campaign `.miz` files still finds WWII PyDCS
vehicles that are not on the Channel shelf: V-1 ski, SK C/28 coastal gun, and
tank/platform coaches. Invent cannot name those targets until they are
curated via `#8e`.

## What Changes

Promote verified leftovers only (campaign-present + `vehicle_map`):

| Class | New ids |
|-------|---------|
| artillery | `v1_launcher`, `SK_C_28_naval_gun` |
| trains | `Coach a tank yellow`, `Coach a tank blue`, `Coach a platform` |

Wire YAML, class shelves, train motion, invent cues, Manston GA examples, hermetic tests, BACKLOG.

## Non-goals

- Modern leftovers (`M978 HEMTT Tanker`, …).
- Scenery/statics (`Cow`, `m1_vla`, hangars, FARP).
- Helos (none in corpus). `Essex` carrier.
- New strike classes; rail-mesh snap; auto-YAML from campaign scan.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: leftover land ids.
- `mission-options`: artillery + trains shelves and French-coast cues.
- `agent-catalog`: `list_strike_targets` returns the new ids.
- `golden-fixtures`: V-1 / coastal-gun examples compile.

## Impact

Registry YAML, planning_options, target_motion, examples, tests, BACKLOG.
Acceptance: pytest. ME Instant Action is human do-soon.
