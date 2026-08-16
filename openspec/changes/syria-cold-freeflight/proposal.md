## Why

Syria is installed and PyDCS-bound, but the planner only supports Channel,
Normandy, and Caucasus. Stage A needs a Manston-class smoke: one airfield, one
modern country (Turkey), reused Su-25T, terrain bind, and a compiling
free-flight Spec — without copying WWII ids or Manston/Batumi skeletons onto
the map.

## What Changes

- Bind Spec theatre `Syria` to PyDCS `Syria`. Package
  `data/theatres/Syria/` with `Incirlik: 16` only (do not dump all 59 fields).
- Add `Turkey` to era `modern` countries alongside Georgia. Reuse `Su-25T` at
  251.0 MHz. Do not put Turkey in `era/wwii`. Era-filter validate so
  Channel/Normandy stay UK / ThirdReich.
- Ship `examples/incirlik_cold_freeflight.yaml` (2024-06-06, `sunny_clear`,
  Turkey blue, cold parking).
- Invent: Syria is **free_flight only**. Schema `theatre=Syria` uses the
  Incirlik example; combat types raise with no Manston/NeedsOarPoint/Batumi
  skeleton. Dedicated `_SYRIA_FF_NOTES` (do not concatenate Channel note
  bundles). Infer theatre from `Incirlik`. Repair must not hardcode
  Caucasus or Normandy.

## Non-goals

- Extra airfields, places, CAP/GA/intercept examples, domain classifier,
  intercept spawn, strike dual-tag, paid jets, USA, modern
  payloads/failures, `theatre_place` rename.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: Syria package; Incirlik 16; Turkey in modern era.
- `mission-validation`: Syria Incirlik smoke validates; Channel+Turkey
  unknown.
- `miz-compiler`: Syria terrain; Incirlik cold FF compile.
- `nl-agent`: invent table; Syria FF only; repair must not inject
  Manston/Normandy/Caucasus.
- `agent-tools`: schema theatre=Syria FF example; combat raise; Syria-only notes.
- `agent-catalog`: catalog lists Syria + Incirlik after sync.

## Impact

`theatre_terrain.py`, invent schema/session/planner, modern countries YAML,
Syria theatre YAML, Incirlik example + N1 tests. Channel goldens stay green.
Acceptance: hermetic pytest + compile the Incirlik example. ME Instant Action
is do-soon after merge.
