## Why

Nevada is installed and PyDCS-bound, but the planner only supports Channel,
Normandy, Caucasus, and Syria. Stage A needs a Manston-class smoke: one
airfield, one modern country (USA at Nellis), reused Su-25T, terrain bind,
and a compiling free-flight Spec — without copying WWII ids or prior-map
skeletons onto the desert.

## What Changes

- Bind Spec theatre `Nevada` to PyDCS `Nevada`. Package
  `data/theatres/Nevada/` with `Nellis: 4` only (do not dump all 17 fields).
- Add `USA` to era `modern` countries alongside Georgia and Turkey. Reuse
  `Su-25T` at 251.0 MHz. Do not put USA in `era/wwii`. `usaaf` stays voice
  only. Era-filter validate so Channel/Normandy stay UK / ThirdReich.
- Ship `examples/nellis_cold_freeflight.yaml` (2024-06-06, `sunny_clear`,
  USA blue, cold parking).
- Invent: Nevada is **free_flight only**. Schema `theatre=Nevada` uses the
  Nellis example; combat types raise with no Manston/NeedsOarPoint/Batumi/
  Incirlik skeleton. Dedicated `_NEVADA_FF_NOTES`. Infer theatre from
  `Nellis`. Repair must not hardcode Syria/Caucasus/Normandy.
- Retarget `test_unsupported_installed_map` off Nevada onto **Falklands**
  (next unbound Stage A).

## Non-goals

- Extra airfields, places, CAP/GA/intercept examples, domain classifier,
  intercept spawn, strike dual-tag, paid jets, extra countries, modern
  payloads/failures, `theatre_place` rename.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: Nevada package; Nellis 4; USA in modern era.
- `mission-validation`: Nevada Nellis smoke validates; Channel+USA unknown.
- `miz-compiler`: Nevada terrain; Nellis cold FF compile.
- `nl-agent`: invent table; Nevada FF only; repair must not inject prior maps.
- `agent-tools`: schema theatre=Nevada FF example; combat raise; Nevada-only notes.
- `agent-catalog`: catalog lists Nevada + Nellis after sync.

## Impact

`theatre_terrain.py`, invent schema, modern countries YAML, Nevada theatre
YAML, Nellis example + N1 tests. Channel goldens stay green. Acceptance:
hermetic pytest + compile the Nellis example. ME Instant Action is do-soon
after merge.
