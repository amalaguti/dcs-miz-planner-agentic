## Why

Falklands (South Atlantic) is installed and PyDCS-bound, but the planner only
supports Channel, Normandy, Caucasus, Syria, and Nevada. Stage A needs a
Manston-class smoke: one airfield, UK in modern era, reused Su-25T, terrain
bind, and a compiling free-flight Spec — without copying WWII aircraft or
prior-map skeletons onto the islands.

## What Changes

- Bind Spec theatre `Falklands` to PyDCS `Falklands`. Package
  `data/theatres/Falklands/` with `MountPleasant: 2` only (do not dump all 27
  fields). Spec key is `MountPleasant`; PyDCS name is `Mount Pleasant`.
- Add `UK` to era `modern` countries alongside Georgia, Turkey, and USA.
  Keep UK in `era/wwii`. Reuse `Su-25T` at 251.0 MHz. Spitfire stays wwii-only.
- Ship `examples/mount_pleasant_cold_freeflight.yaml` (2024-06-06,
  `sunny_clear`, UK blue, cold parking).
- Invent: Falklands is **free_flight only**. Schema `theatre=Falklands` uses
  the Mount Pleasant example; combat types raise with no prior-map skeleton.
  Dedicated `_FALKLANDS_FF_NOTES`. Infer theatre from `MountPleasant`.
- Retarget `test_unsupported_installed_map` off Falklands onto **Kola**.

## Non-goals

- Extra airfields, places, CAP/GA/intercept, Argentina/Chile countries,
  paid jets, modern payloads/failures, `theatre_place` rename.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: Falklands package; MountPleasant 2; UK in modern era.
- `mission-validation`: Falklands smoke validates; Falklands+Spitfire unknown.
- `miz-compiler`: Falklands terrain; Mount Pleasant cold FF compile.
- `nl-agent`: invent table; Falklands FF only; repair must not inject prior maps.
- `agent-tools`: schema theatre=Falklands FF example; combat raise; dedicated notes.
- `agent-catalog`: catalog lists Falklands + MountPleasant after sync.

## Impact

`theatre_terrain.py`, invent schema, modern countries YAML, Falklands theatre
YAML, example + N1 tests. Channel goldens stay green. Acceptance: hermetic
pytest + compile the Mount Pleasant example. ME Instant Action is do-soon
after merge.
