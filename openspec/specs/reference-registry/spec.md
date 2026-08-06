# Reference Registry

## Purpose

Queryable Channel Map reference data (airfields, aircraft, weather presets, radio
defaults, optional payload CLSIDs) with a stable Python lookup API. Exact DCS
identifiers only — YAML tables under `data/channel/` are the source of truth.

## Requirements

### Requirement: Channel reference registry data
The system SHALL provide committed Channel reference data covering airfields (display name → `airdromeId`), aircraft type ids with default radio frequency (MHz), supported theatre id `TheChannel`, and named weather presets used by the Mission Spec. Data MUST use verified DCS identifiers only.

#### Scenario: Manston is registered
- **WHEN** the Channel registry is queried for airfield `Manston`
- **THEN** it MUST return `airdromeId` 5

#### Scenario: Spitfire radio default
- **WHEN** the Channel registry is queried for aircraft `SpitfireLFMkIX`
- **THEN** it MUST expose the default group radio frequency 124.0 MHz (Allied VHF, matching stock Channel missions)

### Requirement: Registry lookup API
The system SHALL expose a Python lookup API over the Channel registry for airfield id resolution,
aircraft/radio lookup, static planner theatre support, and weather preset existence so the compiler
and later tools share one source of truth. Static theatre membership MUST remain separate from the
user-local SQLite installation inventory; callers that offer mission options MUST require both
planner support and a currently available local theatre (from the cached inventory, refreshed on
demand).

#### Scenario: Unknown airfield fails clearly
- **WHEN** a caller requests an airfield name not present in the Channel registry
- **THEN** the API MUST raise an error that identifies the unknown name and lists known airfields
  (or equivalent clear diagnostics)

#### Scenario: Supported theatre
- **WHEN** a caller checks theatre `TheChannel`
- **THEN** the registry MUST treat it as supported

#### Scenario: Supported but not locally available
- **WHEN** `TheChannel` is supported by the packaged registry but the (cached or freshly
  refreshed) installation inventory does not report it as available
- **THEN** callers MUST NOT offer `TheChannel` as currently compilable for that installation

#### Scenario: Installed but unsupported
- **WHEN** the installation inventory reports a theatre that is absent from the packaged registry
- **THEN** callers MUST identify it as locally available but planner-unsupported

### Requirement: No invented DCS identifiers
The Channel registry SHALL NOT invent alternate spellings for theatres, aircraft, or airfields. Only verified ids already established for this project (and documented expansions via explicit data updates) MAY appear.

#### Scenario: Known WWII aircraft set
- **WHEN** the registry lists aircraft
- **THEN** it MUST include at least `SpitfireLFMkIX`, `Bf-109K-4`, `FW-190A8`, and `FW-190D9` with exact DCS type strings

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

### Requirement: Package aircraft in Channel registry
The Channel reference registry SHALL expose exact DCS aircraft type ids usable as escort
package aircraft, including at least `MosquitoFBMkVI` with a documented Allied VHF group
radio default. Keys MUST match PyDCS plane ids; the registry MUST NOT invent spellings.

#### Scenario: Mosquito lookup
- **WHEN** a caller requests aircraft `MosquitoFBMkVI` from the Channel registry
- **THEN** the registry MUST return the aircraft reference including a radio frequency in
  the Allied VHF band

### Requirement: Channel registry lists dawn and marginal weather
The Channel reference registry SHALL expose weather preset ids `dawn_clear` and
`marginal_vfr` (in addition to `sunny_clear`) from packaged YAML, with descriptions
suitable for catalog/agent listing and pilot-facing briefs.

#### Scenario: Registry lists new presets
- **WHEN** a caller lists Channel weather presets
- **THEN** the result MUST include `sunny_clear`, `dawn_clear`, and `marginal_vfr`

### Requirement: Weather recipes package cloud presets
Packaged Channel weather YAML SHALL describe each WeatherPreset with a
pilot-facing description and a compile recipe that MAY include a modern ME
`cloud_preset` id (`PresetN` / `RainyPresetN`) plus numeric fields (base,
visibility, fog, temperature, QNH, turbulence, ground wind) used by the compiler.

#### Scenario: Gallery recipe declared
- **WHEN** catalog/registry loads weather presets after this change
- **THEN** at least one expanded pattern MUST declare a non-empty `cloud_preset`
  matching a PyDCS-known gallery id
