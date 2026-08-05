## Why

`PyDCSCompiler` always builds `Mission(terrain=TheChannel())` regardless of
`spec.theatre`. Adding a theatre to registry/inventory without a compiler binding would
compile false-confidence Channel missions (adversarial B6). Before any second theatre,
binding must be explicit and unbound theatres must fail closed.

## What Changes

- Add a committed Spec theatre id → PyDCS terrain factory map (Channel only for now).
- Compiler constructs terrain via that map; raises a clear error if unbound.
- `channel_domain` (and any other Channel terrain use) goes through the same helper.
- Validation MAY fail with `theatre_terrain_unbound` when registry theatre lacks a binding
  (parity with theatres.yaml).
- Tests: Channel binds; unbound id fails; registry theatres ⊆ binding keys.

## Non-goals

- Shipping a second theatre (Normandy, etc.).
- Changing Channel airfield/geometry behaviour.
- Auto-discovering PyDCS terrain classes from disk.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `miz-compiler`: Compile MUST resolve Spec theatre via explicit terrain binding; fail if
  unbound.
- `mission-validation`: Unbound but registry-listed theatre MUST fail validation (or be
  impossible via parity — prefer explicit validate error).

## Impact

- New binding module; `pydcs_compiler.py`, `channel_domain.py`; tests; docs/BACKLOG `#39`.
