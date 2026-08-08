## Why

R13 scanned Spitfire Channel campaigns and listed high-frequency units not yet
on the Channel shelf (`flak41`, Quadmount, heavies, LST/Chase, Coach wagons).
Incorporate that shortlist via `#8e` so invent matches ED campaign target mix.

## What Changes

- Promote verified R13 candidates into `ground_units.yaml` / `ships.yaml`.
- Extend class shelves (aaa / armor / trains / sea), motion maps, AAA AI
  allowlist; invent cues; examples + hermetic tests; BACKLOG note.

**Batch (verified PyDCS):**

| Class | New ids |
|-------|---------|
| aaa_guns | `flak41`, `M45_Quadmount`, `QF_37_AA`, `Allies_Director` |
| armor | `Tiger_I`, `SturmPzIV`, `Pz_V_Panther_G`, `JagdPz_IV`, `Jagdpanther_G1` |
| trains | `Coach cargo`, `Coach cargo open` |
| sea_craft | `LST_Mk2`, `USS_Samuel_Chase` |

## Capabilities

### New Capabilities

- *(none)*

### Modified Capabilities

- `reference-registry`, `mission-options`, `agent-catalog`, `golden-fixtures`
  (and AAA allowlist behaviour as needed).

## Impact

- Registry YAML, planning_options, target_motion, target_ai, examples/, tests,
  BACKLOG.

## Non-goals

- Modern leftovers (HEMTT, Sandbox); scenery bunkers; auto-YAML from R13.
- New classes; rail-mesh snap; helo shelf.

## Acceptance

New ids validate/compile in examples; catalog lists them by class; AAA new ids
get aaa_alert class; hermetic pytest green. ME do-soon optional.
