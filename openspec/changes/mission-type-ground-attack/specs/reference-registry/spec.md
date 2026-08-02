## ADDED Requirements

### Requirement: Named payload presets in Channel registry
The Channel reference registry SHALL include named payload presets with verified DCS weapon
CLSIDs for supported aircraft (at least SpitfireLFMkIX bomb presets used by ground-attack).
Lookup MUST fail clearly for unknown preset names. Presets MUST declare the aircraft they
apply to and the pylon/CLSID pairs. The registry MUST NOT invent CLSID strings.

#### Scenario: spitfire bomb preset resolves
- **WHEN** the registry is queried for a packaged SpitfireLFMkIX bomb payload preset
- **THEN** it MUST return meta including matching aircraft id and at least one verified bomb
  CLSID on a Spitfire pylon

#### Scenario: spitfire Channel-crossing slipper preset resolves
- **WHEN** the registry is queried for the packaged SpitfireLFMkIX Channel-crossing preset
- **THEN** it MUST return meta that includes wing bomb CLSIDs and the verified
  `SPITFIRE_45GAL_SLIPPER_TANK` CLSID on the centreline pylon

#### Scenario: Unknown payload fails clearly
- **WHEN** a caller requests a payload name absent from the registry
- **THEN** the API MUST raise an error that identifies the unknown name and lists known
  payloads (or equivalent clear diagnostics)

### Requirement: Ground unit type ids in Channel registry
The Channel reference registry SHALL include a curated set of WWII ground unit type ids used
by ground-attack land targets (exact DCS / PyDCS id strings) with domain `land`. Lookup MUST
fail clearly for unknown unit ids. The registry MUST NOT invent alternate spellings.

#### Scenario: German soft target registered
- **WHEN** the Channel registry lists ground units
- **THEN** it MUST include at least one verified soft-target id usable on The Channel (e.g.
  a German truck type present in PyDCS vehicles)

#### Scenario: Unknown ground unit fails clearly
- **WHEN** a caller requests a ground unit id absent from the registry
- **THEN** the API MUST raise an error that identifies the unknown id and lists known ground
  units (or equivalent clear diagnostics)

### Requirement: Ship type ids for over-water strike targets
The Channel reference registry SHALL include curated WWII ship/boat type ids for mid-Channel
or coastal-water strike targets (exact DCS / PyDCS id strings) with domain `sea`. Land
vehicle ids MUST NOT be used as sea targets. Lookup MUST fail clearly for unknown ship ids.

#### Scenario: Schnellboot registered
- **WHEN** the Channel registry lists ships
- **THEN** it MUST include at least one verified Axis boat/ship id (e.g. Schnellboot)

#### Scenario: Strike unit resolves domain
- **WHEN** a caller resolves a registered land truck vs a registered Schnellboot
- **THEN** the registry MUST report domain `land` and `sea` respectively
