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

### Requirement: Channel soft AAA sea shelf expand
Packaged Channel registry SHALL include the promoted soft, AAA, and sea craft
ids from the first shelf-expand batch (Sd_Kfz_2, Horch_901_typ_40_kfz_21,
Willys_MB, flak30/37/38, Flakscheinwerfer_37, KDO_Mod40, bofors40, Dry-cargo
ship-2, HarborTug, Higgins_boat), each with domain land or sea as appropriate.

#### Scenario: New soft land unit resolvable
- **WHEN** the registry is queried for Sd_Kfz_2
- **THEN** it MUST return a land-domain strike unit

#### Scenario: New sea harbour unit resolvable
- **WHEN** the registry is queried for HarborTug
- **THEN** it MUST return a sea-domain strike unit

### Requirement: Channel halftracks_apc shelf
Packaged Channel registry SHALL include land-domain halftrack ids `Sd_Kfz_251`,
`Sd_Kfz_7`, and `M2A1_halftrack`, each resolvable as a strike unit.

#### Scenario: Sd_Kfz_251 resolvable
- **WHEN** the registry is queried for Sd_Kfz_251
- **THEN** it MUST return a land-domain strike unit

#### Scenario: M2A1_halftrack resolvable
- **WHEN** the registry is queried for M2A1_halftrack
- **THEN** it MUST return a land-domain strike unit

### Requirement: Channel armor shelf
Packaged Channel registry SHALL include land-domain armor ids `Pz_IV_H`,
`Stug_III`, `Cromwell_IV`, and `M4_Sherman`, each resolvable as a strike unit.

#### Scenario: Pz_IV_H resolvable
- **WHEN** the registry is queried for Pz_IV_H
- **THEN** it MUST return a land-domain strike unit

#### Scenario: Stug_III resolvable
- **WHEN** the registry is queried for Stug_III
- **THEN** it MUST return a land-domain strike unit

### Requirement: Channel troops shelf
Packaged Channel registry SHALL include land-domain infantry ids
`soldier_mauser98`, `soldier_wwii_br_01`, and `soldier_wwii_us`, each resolvable
as a strike unit.

#### Scenario: soldier_mauser98 resolvable
- **WHEN** the registry is queried for soldier_mauser98
- **THEN** it MUST return a land-domain strike unit

#### Scenario: soldier_wwii_br_01 resolvable
- **WHEN** the registry is queried for soldier_wwii_br_01
- **THEN** it MUST return a land-domain strike unit

### Requirement: Channel trains shelf
Packaged Channel registry SHALL include land-domain train ids `Locomotive`,
`German_covered_wagon_G10`, `German_tank_wagon`, and `DR_50Ton_Flat_Wagon`, each
resolvable as a strike unit.

#### Scenario: Locomotive resolvable
- **WHEN** the registry is queried for Locomotive
- **THEN** it MUST return a land-domain strike unit

#### Scenario: German_covered_wagon_G10 resolvable
- **WHEN** the registry is queried for German_covered_wagon_G10
- **THEN** it MUST return a land-domain strike unit

### Requirement: Channel radar_c3 shelf
Packaged Channel registry SHALL include land-domain radar ids `FuMG-401` and
`FuSe-65`, each resolvable as a strike unit.

#### Scenario: FuMG-401 resolvable
- **WHEN** the registry is queried for FuMG-401
- **THEN** it MUST return a land-domain strike unit

#### Scenario: FuSe-65 resolvable
- **WHEN** the registry is queried for FuSe-65
- **THEN** it MUST return a land-domain strike unit

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

### Requirement: Weather patterns declare gallery families for invent
Packaged Channel weather data SHALL allow each gallery-backed WeatherPreset to
declare the set of allowed ME `cloud_preset` ids (within-family) used by invent
priors. Recipe centers remain the default numeric baseline.

#### Scenario: Broken pattern family non-empty
- **WHEN** registry loads weather presets after this change
- **THEN** the broken-channel pattern (or equivalent) MUST expose a non-empty
  allowed gallery family list of Broken-class preset ids

### Requirement: Channel aircraft failure catalog
The Channel reference data SHALL include a curated catalog of DCS failure ids for
supported player aircraft (at least `SpitfireLFMkIX` in v1), exposed via the registry
API for validation and agent listing. Catalog entries MUST use exact DCS ids from
verified Spitfire mission/ME sources.

#### Scenario: Spitfire magneto id known
- **WHEN** a client queries known failures for `SpitfireLFMkIX`
- **THEN** the catalog MUST include `ENG0_MAGNETO0` (and other curated v1 ids)

### Requirement: Showers scattered weather recipe and family
Packaged Channel weather YAML SHALL include `showers_scattered` with a
pilot-facing description and a gallery recipe whose default `cloud_preset` is a
light-rain ME gallery id (`RainyPreset4`, `NEWRAINPRESET4`, `RainyPreset5`, or
`RainyPreset6`). The pattern MUST declare a `gallery_family` that includes those
light-rain ids (and MUST NOT silently merge into `rain_overcast`’s
`RainyPreset1`–`3` family).

#### Scenario: Showers recipe declared
- **WHEN** the Channel registry loads weather presets after this change
- **THEN** `showers_scattered` MUST expose a non-empty gallery family containing
  at least `RainyPreset4` and MUST list a default `cloud_preset` from that family

### Requirement: Packaged gallery decode for synthetic METAR
Packaged Channel weather data SHALL provide a decode map from ME gallery
`cloud_preset` ids to METAR cloud coverage groups (and secondary layer bases)
sufficient to build offline synthetic METARs. The map MUST cover at least all
gallery ids used by packaged `gallery_family` lists, including rainy light ids.

#### Scenario: Decode covers rainy light presets
- **WHEN** the METAR decode map is loaded
- **THEN** entries for `RainyPreset4`, `RainyPreset5`, `RainyPreset6`, and
  `NEWRAINPRESET4` (if packaged in any family) MUST be present
