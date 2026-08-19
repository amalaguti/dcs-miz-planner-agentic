## 1. Registry bank

- [x] 1.1 Add verified `radio_channels_mhz` to SpitfireLFMkIX and SpitfireLFMkIXCW in WWII aircraft YAML (A=124 B=40 C=41 D=42 E=108.9)
- [x] 1.2 Extend `AircraftRef` + parser + `radio_channels_mhz()` lookup; channel A must match `radio_mhz`

## 2. Compiler emit

- [x] 2.1 Helper: set group frequency, init radio if missing, write A–E; do not call `set_frequency()`
- [x] 2.2 Apply to player Spitfire groups (lead + player) and any other emitted Spitfire groups

## 3. Tests, goldens, docs

- [x] 3.1 Hermetic tests: registry bank; Manston compile A–E; radioSet remains false
- [x] 3.2 Refresh Manston goldens if Radio tables appear
- [x] 3.3 BACKLOG #19, README Status, lessons + dcs-dev-channel-ids / pydcs-compile; ruff + pytest
