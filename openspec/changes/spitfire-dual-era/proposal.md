## Why

DCS lets you fly the Spitfire on Caucasus (and other modern maps). The planner
era-filters `SpitfireLFMkIX` to WWII only, so a valid DCS combination fails
validation. The product rule should match DCS: if the module flies on the map,
the Spec may use it.

## What Changes

- Add `SpitfireLFMkIX` (and `SpitfireLFMkIXCW`) to `era/modern` with the same
  124.0 MHz radio as WWII so the id does not collide across eras.
- Keep `Su-25T` WWII-unknown. Channel/Normandy still reject Frogfoot.
- Ship `examples/batumi_spitfire_freeflight.yaml` (Batumi, UK, Spitfire).
  Invent/schema default stays Su-25T Georgia.
- Flip era-filter tests: modern theatres accept Spitfire; Channel still
  rejects Su-25T.

## Non-goals

- Putting Su-25T on Channel/WWII. Paid FC3 jets. Combat invent on Caucasus.
- Dual-era Mosquito / Bf-109 / FW-190 unless asked.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: Spitfire is dual-era (like UK).
- `mission-validation`: modern theatres accept Spitfire; WWII still rejects Su-25T.
- `miz-compiler`: Batumi Spitfire free-flight compiles.

## Impact

`data/era/modern/aircraft.yaml`, Batumi Spitfire example + tests. Channel
goldens stay green. Acceptance: hermetic pytest + compile the new example.
ME Instant Action is do-soon after merge.
