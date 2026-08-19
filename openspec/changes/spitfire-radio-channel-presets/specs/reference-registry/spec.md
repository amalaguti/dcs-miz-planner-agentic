## ADDED Requirements

### Requirement: Spitfire Channel A–E radio bank
Packaged WWII aircraft entries for `SpitfireLFMkIX` and `SpitfireLFMkIXCW`
SHALL include a five-channel `radio_channels_mhz` list copied from stock ED
Channel Spitfire missions: 124, 40, 41, 42, 108.9 MHz. Channel A MUST equal
the aircraft `radio_mhz` (124.0). The registry lookup API SHALL expose this
list. Other aircraft MAY omit the list.

#### Scenario: Spitfire LF Mk IX Channel bank
- **WHEN** the registry is queried for `SpitfireLFMkIX` radio channels
- **THEN** it MUST return 124.0, 40.0, 41.0, 42.0, 108.9

#### Scenario: Spitfire CW uses the same bank
- **WHEN** the registry is queried for `SpitfireLFMkIXCW` radio channels
- **THEN** it MUST return the same five frequencies as `SpitfireLFMkIX`
