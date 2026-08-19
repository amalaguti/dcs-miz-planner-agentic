## Why

Compiled Channel Spitfire missions set group frequency 124 MHz (flyable) but
leave the unit Radio A–E bank as PyDCS airframe defaults (105 / 124 / 131 /
139 / 108.9). Cockpit channel clicks then disagree with stock ED Channel
missions (A=124, B=40, C=41, D=42, E=108.9). The owner flies only the
Spitfire; this is cockpit immersion they can actually use.

## What Changes

- Packaged WWII aircraft YAML records the verified ED Channel Spitfire A–E
  bank on `SpitfireLFMkIX` and `SpitfireLFMkIXCW`.
- Registry exposes `radio_channels_mhz` so the compiler does not hard-code
  frequencies.
- Compiler writes unit `Radio[1].channels` for those types after setting
  group frequency. It MUST NOT call PyDCS `set_frequency()`, which flips
  `radioSet` and overwrites presets. `radioSet` stays false (stock Channel).
- Hermetic tests assert A–E; Manston goldens refresh if Radio tables appear.

## Non-goals

- P-51 / Mosquito / German radio banks.
- F10 comms menus (already shipped).
- `#22` Lua snippet library.
- Agent invent of free-form frequencies.
- ME Instant Action as merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: Spitfire A–E channel bank on packaged WWII aircraft.
- `miz-compiler`: emit unit Radio presets for Spitfire LF Mk IX / CW.

## Impact

Registry YAML + lookup, PyDCS compiler emit, Manston goldens, hermetic tests,
lessons. Acceptance: pytest; Instant Action channel clicks are human do-soon.
