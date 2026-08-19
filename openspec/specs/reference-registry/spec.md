# Reference Registry

## Purpose

Queryable Channel Map reference data (airfields, aircraft, weather presets, radio
defaults, optional payload CLSIDs) with a stable Python lookup API. Exact DCS
identifiers only — packaged YAML under `data/era/`, `data/shared/`, and
`data/theatres/<SpecId>/` is the source of truth.

## Requirements

### Requirement: Channel reference registry data
The system SHALL provide committed Channel reference data covering airfields
(display name → `airdromeId` for theatre `TheChannel`), aircraft type ids with
default radio frequency (MHz), supported theatre id `TheChannel`, and named
weather presets used by the Mission Spec. Data MUST use verified DCS
identifiers only. Channel airfields MUST live in the `TheChannel` theatre
package; WWII aircraft, radios, and weather presets MAY be shared era/shared
packages consumed by TheChannel.

#### Scenario: Manston is registered
- **WHEN** the Channel registry is queried for airfield `Manston`
- **THEN** it MUST return `airdromeId` 5

#### Scenario: Spitfire radio default
- **WHEN** the Channel registry is queried for aircraft `SpitfireLFMkIX`
- **THEN** it MUST expose the default group radio frequency 124.0 MHz (Allied
  VHF, matching stock Channel missions)

### Requirement: Registry lookup API
The system SHALL expose a Python lookup API over the packaged registry for
airfield id resolution, aircraft/radio lookup, static planner theatre support,
and weather preset existence so the compiler and later tools share one source
of truth. Static theatre membership MUST remain separate from the user-local
SQLite installation inventory; callers that offer mission options MUST require
both planner support and a currently available local theatre (from the cached
inventory, refreshed on demand).

#### Scenario: Unknown airfield fails clearly
- **WHEN** a caller requests an airfield name not present for the requested
  theatre (or, if unscoped, not present in the packaged registry)
- **THEN** the API MUST raise an error that identifies the unknown name and
  lists known airfields (or equivalent clear diagnostics)

#### Scenario: Supported theatre
- **WHEN** a caller checks theatre `TheChannel`
- **THEN** the registry MUST treat it as supported

#### Scenario: Supported but not locally available
- **WHEN** `TheChannel` is supported by the packaged registry but the (cached
  or freshly refreshed) installation inventory does not report it as available
- **THEN** callers MUST NOT offer `TheChannel` as currently compilable for that
  installation

#### Scenario: Installed but unsupported
- **WHEN** the installation inventory reports a theatre that is absent from the
  packaged registry
- **THEN** callers MUST identify it as locally available but
  planner-unsupported

### Requirement: Packaged registry packages
The packaged reference registry SHALL load from theatre packages under
`data/theatres/<SpecId>/` plus shared and era YAML (WWII aircraft, payloads,
failures, ground/sea units, weather presets, planning options). The loader MUST
walk packaged `theatre.yaml` files and treat each `id:` as a planner-supported
theatre. The registry MUST NOT invent DCS identifiers. The single
`data/channel/` package MUST NOT remain the source of truth.

#### Scenario: Both bound theatres load from packages
- **WHEN** the packaged registry is loaded
- **THEN** it MUST treat `TheChannel` and `Normandy` as supported theatres
  sourced from per-theatre packages (not a combined `data/channel/theatres.yaml`
  list)

#### Scenario: Shared weather still resolves
- **WHEN** the packaged registry is queried for weather preset `sunny_clear`
- **THEN** it MUST resolve that preset without a Normandy-local weather file

### Requirement: Theatre-scoped airfield lookup
Airfield → `airdromeId` lookup SHALL be scoped to a Spec theatre. Airdrome ids
MUST NOT be treated as global. When `theatre` is provided, unknown names MUST
error with that theatre’s known airfields. When `theatre` is omitted, a name
that maps uniquely MAY resolve; a name present in more than one theatre MUST
fail as ambiguous.

#### Scenario: Manston on TheChannel
- **WHEN** the registry is queried for airfield `Manston` with theatre
  `TheChannel`
- **THEN** it MUST return `airdromeId` 5

#### Scenario: Manston on Normandy fails
- **WHEN** the registry is queried for airfield `Manston` with theatre
  `Normandy`
- **THEN** it MUST raise an error that identifies the unknown name and lists
  known Normandy airfields (or equivalent clear diagnostics)

#### Scenario: NeedsOarPoint on TheChannel fails
- **WHEN** the registry is queried for airfield `NeedsOarPoint` with theatre
  `TheChannel`
- **THEN** it MUST raise an error that identifies the unknown name and lists
  known TheChannel airfields (or equivalent clear diagnostics)

#### Scenario: NeedsOarPoint on Normandy
- **WHEN** the registry is queried for airfield `NeedsOarPoint` with theatre
  `Normandy`
- **THEN** it MUST return `airdromeId` 28

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

### Requirement: Channel R13 shelf promote
Packaged Channel registry SHALL include R13-promoted land ids `flak41`,
`M45_Quadmount`, `QF_37_AA`, `Allies_Director`, `Tiger_I`, `SturmPzIV`,
`Pz_V_Panther_G`, `JagdPz_IV`, `Jagdpanther_G1`, `Coach cargo`,
`Coach cargo open`, and sea ids `LST_Mk2`, `USS_Samuel_Chase`.

#### Scenario: flak41 resolvable
- **WHEN** the registry is queried for flak41
- **THEN** it MUST return a land-domain strike unit

#### Scenario: LST_Mk2 resolvable
- **WHEN** the registry is queried for LST_Mk2
- **THEN** it MUST return a sea-domain strike unit

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

### Requirement: Normandy theatre in packaged registry
The packaged reference registry SHALL list Spec theatre id `Normandy` as
planner-supported alongside `TheChannel`. Data MUST use the verified DCS/PyDCS
theatre id only.

#### Scenario: Normandy is supported
- **WHEN** a caller checks theatre `Normandy`
- **THEN** the registry MUST treat it as supported

### Requirement: Needs Oar Point airfield registered
The packaged registry SHALL map curated airfield key `NeedsOarPoint` to DCS
`airdromeId` 28 (PyDCS Normandy airport Needs Oar Point) in the `Normandy`
theatre package.

#### Scenario: NeedsOarPoint resolves
- **WHEN** the registry is queried for airfield `NeedsOarPoint`
- **THEN** it MUST return `airdromeId` 28

### Requirement: Curated Normandy airfields beyond Needs Oar Point
The packaged `Normandy` theatre airfield table SHALL map these curated Spec
keys to DCS `airdromeId` values from PyDCS `Normandy.airport_list()` (never
invented): `NeedsOarPoint` 28, `Chailey` 27, `Funtington` 29, `Tangmere` 30,
`FordAF` 31 (PyDCS name `Ford_AF`), `Maupertus` 4, `SaintPierreduMont` 1,
`Carpiquet` 19. The registry MUST NOT dump every Normandy airport. Lookup MUST
remain theatre-scoped (Normandy id 4 is Maupertus, not Channel Abbeville).

#### Scenario: FordAF resolves on Normandy
- **WHEN** the registry is queried for airfield `FordAF` with theatre
  `Normandy`
- **THEN** it MUST return `airdromeId` 31

#### Scenario: Maupertus is not Channel Abbeville
- **WHEN** the registry is queried for `Maupertus` with theatre `Normandy`
- **THEN** it MUST return `airdromeId` 4 and MUST NOT treat that id as a
  TheChannel airfield

### Requirement: WWII countries in era package
The packaged registry SHALL list exact PyDCS country class names `UK`,
`ThirdReich`, and `USA` from era YAML (`data/era/wwii/countries.yaml`). `Germany` MUST
NOT be a known country id (hint to `ThirdReich` MAY remain). The registry MUST
NOT invent country strings. `usaaf` MUST NOT be a known country (`usaaf` is voice only).

#### Scenario: UK, ThirdReich, and USA known
- **WHEN** the registry lists countries for era `wwii`
- **THEN** the set MUST include `UK`, `ThirdReich`, and `USA` and MUST NOT include
  `Germany` as a known id

### Requirement: Theatre era membership is retained
The packaged registry SHALL retain each theatre package’s `era:` (`wwii` for
TheChannel and Normandy; `modern` for Caucasus) so catalog/allowlists can
resolve era without a second hardcoded Channel list.

#### Scenario: Normandy era is wwii
- **WHEN** a caller asks the registry for the era of theatre `Normandy`
- **THEN** it MUST return `wwii`

#### Scenario: Caucasus era is modern
- **WHEN** a caller asks the registry for the era of theatre `Caucasus`
- **THEN** it MUST return `modern`

### Requirement: Caucasus theatre in packaged registry
The packaged registry SHALL list Spec theatre id `Caucasus` as
planner-supported. Folder name under `data/theatres/` MUST match the Spec id.
Era MUST be `modern`. Data MUST use the verified DCS/PyDCS theatre id only.

#### Scenario: Caucasus is supported
- **WHEN** a caller checks theatre `Caucasus`
- **THEN** the registry MUST treat it as supported and MUST report era
  `modern`

### Requirement: Batumi airfield registered
The packaged registry SHALL map curated airfield key `Batumi` to DCS
`airdromeId` 22 (PyDCS Caucasus airport Batumi) in the `Caucasus` theatre
package. It MUST NOT dump every Caucasus airport.

#### Scenario: Batumi resolves
- **WHEN** the registry is queried for airfield `Batumi` with theatre
  `Caucasus`
- **THEN** it MUST return `airdromeId` 22

### Requirement: Curated Caucasus airfields beyond Batumi
The packaged `Caucasus` theatre airfield table SHALL map these curated Spec
keys to DCS `airdromeId` values from PyDCS `Caucasus.airport_list()` (never
invented): `Batumi` 22, `Kobuleti` 24, `SenakiKolkhi` 23 (PyDCS name
`Senaki-Kolkhi`), `Kutaisi` 25, `TbilisiLochini` 29 (`Tbilisi-Lochini`),
`Vaziani` 31, `SochiAdler` 18 (`Sochi-Adler`), `Mozdok` 28. The registry
MUST NOT dump every Caucasus airport. Lookup MUST remain theatre-scoped
(Caucasus id 28 is Mozdok, not Normandy Needs Oar Point).

#### Scenario: Mozdok resolves on Caucasus
- **WHEN** the registry is queried for airfield `Mozdok` with theatre
  `Caucasus`
- **THEN** it MUST return `airdromeId` 28

#### Scenario: Mozdok is not Needs Oar Point
- **WHEN** the registry is queried for `Mozdok` with theatre `Caucasus`
- **THEN** it MUST return `airdromeId` 28 and MUST NOT treat that id as a
  Normandy airfield

### Requirement: Modern era countries and aircraft are era-keyed
The packaged registry SHALL load countries and aircraft from each
`data/era/<era>/` package (`wwii` and `modern`). Era `modern` SHALL include
PyDCS countries `Georgia`, `Turkey`, `USA`, `UK`, `Russia`, `Syria`,
`Argentina`, and `Norway`, aircraft `Su-25T` with group radio 251.0 MHz, and
dual-era `SpitfireLFMkIX` / `SpitfireLFMkIXCW` with group radio 124.0 MHz
(same refs as WWII). `UK` and those Spitfire types MUST remain in the WWII
era package as well. `USA` MAY appear in both era packages (WWII Channel/Normandy
P-51D; modern Nevada). It MUST NOT add Georgia/Turkey/Russia/Syria/
Argentina/Norway or `Su-25T` to the WWII era package. Known-country and
known-aircraft queries used for validation SHALL be filterable by era so
Channel/Normandy remain `UK` / `ThirdReich` / `USA` and WWII aircraft (including
Spitfire and `P-51D`) only for jets — `Su-25T` stays modern-only. `usaaf` MUST NOT be a
known country. `Germany` MUST NOT be a known country in any era. `Chile`
MUST NOT be a known country.

#### Scenario: WWII countries include USA
- **WHEN** the registry lists countries for era `wwii`
- **THEN** the set MUST be `UK`, `ThirdReich`, and `USA` and MUST NOT include
  `Georgia`, `Turkey`, `Russia`, `Syria`, `Argentina`, `Norway`, or
  `Germany`

#### Scenario: Modern smoke identity
- **WHEN** the registry lists countries and aircraft for era `modern`
- **THEN** countries MUST include `Georgia`, `Turkey`, `USA`, `UK`,
  `Russia`, `Syria`, `Argentina`, and `Norway` and aircraft MUST include
  `Su-25T` at 251.0 MHz and `SpitfireLFMkIX` at 124.0 MHz

#### Scenario: Spitfire is dual-era
- **WHEN** the registry lists aircraft for era `wwii` and era `modern`
- **THEN** both MUST include `SpitfireLFMkIX` and MUST NOT include `Su-25T`
  in `wwii`

### Requirement: Modern ground units and Su-25T payload in era package
The packaged registry SHALL load ground units and named payloads from each
`data/era/<era>/` package when those YAML files exist (`wwii` and `modern`).
Era `modern` SHALL include PyDCS vehicle ids `Ural-375`, `GAZ-66`, and
`ZIL-135` (domain land) and payload preset `su25t_2x_fab250` (aircraft
`Su-25T`, FAB-250 CLSID `{3C612111-C7AD-476E-8A8E-2485812F4E5C}` on inner
pylons 5 and 7). Duplicate ids across eras with differing refs MUST fail
load. WWII ground units and Spitfire payloads MUST remain in the WWII era
package. The registry MUST NOT invent vehicle ids or CLSIDs.

#### Scenario: Modern trucks registered
- **WHEN** the registry lists ground units
- **THEN** it MUST include `Ural-375`, `GAZ-66`, and `ZIL-135` and MUST still
  include WWII `Blitz_36-6700A`

#### Scenario: Su-25T FAB-250 preset resolves
- **WHEN** the registry is queried for `su25t_2x_fab250`
- **THEN** it MUST return aircraft `Su-25T` and FAB-250 CLSID on pylons 5 and 7

### Requirement: Syria theatre in packaged registry
The packaged registry SHALL list Spec theatre id `Syria` as
planner-supported. Folder name under `data/theatres/` MUST match the Spec id.
Era MUST be `modern`. Data MUST use the verified DCS/PyDCS theatre id only.

#### Scenario: Syria is supported
- **WHEN** a caller checks theatre `Syria`
- **THEN** the registry MUST treat it as supported and MUST report era
  `modern`

### Requirement: Incirlik airfield registered
The packaged registry SHALL map curated airfield key `Incirlik` to DCS
`airdromeId` 16 (PyDCS Syria airport Incirlik) in the `Syria` theatre
package. It MUST NOT dump every Syria airport.

#### Scenario: Incirlik resolves
- **WHEN** the registry is queried for airfield `Incirlik` with theatre
  `Syria`
- **THEN** it MUST return `airdromeId` 16

### Requirement: Curated Syria airfields beyond Incirlik
The packaged `Syria` theatre airfield table SHALL map these curated Spec
keys to DCS `airdromeId` values from PyDCS `Syria.airport_list()` (never
invented): `Incirlik` 16, `RamatDavid` 30 (PyDCS name `Ramat David`),
`Damascus` 7, `BeirutRaficHariri` 6 (`Beirut-Rafic Hariri`), `Aleppo` 27,
`BasselAlAssad` 21 (`Bassel Al-Assad`), `Palmyra` 28,
`KingHusseinAirCollege` 19 (`King Hussein Air College`). The registry
MUST NOT dump every Syria airport. Lookup MUST remain theatre-scoped
(Syria id 28 is Palmyra, not Caucasus Mozdok, not Normandy Needs Oar Point).

#### Scenario: Palmyra resolves on Syria
- **WHEN** the registry is queried for airfield `Palmyra` with theatre
  `Syria`
- **THEN** it MUST return `airdromeId` 28

#### Scenario: Palmyra is not Mozdok
- **WHEN** the registry is queried for `Palmyra` with theatre `Syria`
- **THEN** it MUST return `airdromeId` 28 and MUST NOT treat that id as a
  Caucasus or Normandy airfield

### Requirement: Nevada theatre in packaged registry
The packaged registry SHALL list Spec theatre id `Nevada` as
planner-supported. Folder name under `data/theatres/` MUST match the Spec id.
Era MUST be `modern`. Data MUST use the verified DCS/PyDCS theatre id only.

#### Scenario: Nevada is supported
- **WHEN** a caller checks theatre `Nevada`
- **THEN** the registry MUST treat it as supported and MUST report era
  `modern`

### Requirement: Nellis airfield registered
The packaged registry SHALL map curated airfield key `Nellis` to DCS
`airdromeId` 4 (PyDCS Nevada airport Nellis) in the `Nevada` theatre
package. It MUST NOT dump every Nevada airport.

#### Scenario: Nellis resolves
- **WHEN** the registry is queried for airfield `Nellis` with theatre
  `Nevada`
- **THEN** it MUST return `airdromeId` 4

### Requirement: Curated Nevada airfields beyond Nellis
The packaged `Nevada` theatre airfield table SHALL map these curated Spec
keys to DCS `airdromeId` values from PyDCS `Nevada.airport_list()` (never
invented): `Nellis` 4, `GroomLake` 2 (PyDCS name `Groom Lake`), `Creech` 1,
`TonopahTestRange` 18 (`Tonopah Test Range`), `NorthLasVegas` 15
(`North Las Vegas`), `HendersonExecutive` 8 (`Henderson Executive`),
`BoulderCity` 6 (`Boulder City`), `Mesquite` 13. The registry MUST NOT dump
every Nevada airport. Lookup MUST remain theatre-scoped (Nevada id 2 is
Groom Lake, not Falklands Mount Pleasant, not Channel Merville Calonne).

#### Scenario: GroomLake resolves on Nevada
- **WHEN** the registry is queried for airfield `GroomLake` with theatre
  `Nevada`
- **THEN** it MUST return `airdromeId` 2

#### Scenario: GroomLake is not MountPleasant
- **WHEN** the registry is queried for `GroomLake` with theatre `Nevada`
- **THEN** it MUST return `airdromeId` 2 and MUST NOT treat that id as a
  Falklands or Channel airfield

### Requirement: Falklands theatre in packaged registry
The packaged registry SHALL list Spec theatre id `Falklands` as
planner-supported. Folder name under `data/theatres/` MUST match the Spec id.
Era MUST be `modern`. Data MUST use the verified DCS/PyDCS theatre id only.

#### Scenario: Falklands is supported
- **WHEN** a caller checks theatre `Falklands`
- **THEN** the registry MUST treat it as supported and MUST report era
  `modern`

### Requirement: Mount Pleasant airfield registered
The packaged registry SHALL map curated airfield key `MountPleasant` to DCS
`airdromeId` 2 (PyDCS Falklands airport Mount Pleasant) in the `Falklands`
theatre package. It MUST NOT dump every Falklands airport. The Spec key MUST
be `MountPleasant`, not `Mount_Pleasant`.

#### Scenario: MountPleasant resolves
- **WHEN** the registry is queried for airfield `MountPleasant` with theatre
  `Falklands`
- **THEN** it MUST return `airdromeId` 2

### Requirement: Curated Falklands airfields beyond MountPleasant
The packaged `Falklands` theatre airfield table SHALL map these curated Spec
keys to DCS `airdromeId` values from PyDCS `Falklands.airport_list()` (never
invented): `MountPleasant` 2 (PyDCS name `Mount Pleasant`), `PortStanley` 1
(`Port Stanley`), `SanCarlosFOB` 3 (`San Carlos FOB`), `RioGallegos` 5
(`Rio Gallegos`), `RioGrande` 6 (`Rio Grande`), `Ushuaia` 7, `PuntaArenas` 9
(`Punta Arenas`), `SanJulian` 11 (`San Julian`). The registry MUST NOT dump
every Falklands airport. It MUST NOT invent airdrome ids 4 or 28. Lookup MUST
remain theatre-scoped (Falklands id 5 is Rio Gallegos, not Channel Manston).
Spec keys MUST be camelCase without underscores (`RioGallegos` ≠
`Rio_Gallegos`; `PortStanley` ≠ `Port_Stanley`).

#### Scenario: RioGallegos resolves on Falklands
- **WHEN** the registry is queried for airfield `RioGallegos` with theatre
  `Falklands`
- **THEN** it MUST return `airdromeId` 5

#### Scenario: RioGallegos is not Manston
- **WHEN** the registry is queried for `RioGallegos` with theatre `Falklands`
- **THEN** it MUST return `airdromeId` 5 and MUST NOT treat that id as a
  Channel airfield

### Requirement: Argentina country in modern era
The packaged modern country table SHALL include PyDCS country class
`Argentina`. WWII country tables MUST NOT include `Argentina`. Chile MUST
NOT be added in this change.

#### Scenario: Argentina is a known modern country
- **WHEN** the registry lists countries for era `modern`
- **THEN** `Argentina` MUST be present and MUST NOT appear in era `wwii`

### Requirement: Kola theatre in packaged registry
The packaged registry SHALL list Spec theatre id `Kola` as planner-supported.
Folder name under `data/theatres/` MUST match the Spec id. Era MUST be
`modern`. Data MUST use the verified DCS/PyDCS theatre id only.

#### Scenario: Kola is supported
- **WHEN** a caller checks theatre `Kola`
- **THEN** the registry MUST treat it as supported and MUST report era
  `modern`

### Requirement: Bodo airfield registered
The packaged registry SHALL map curated airfield key `Bodo` to DCS
`airdromeId` 7 (PyDCS Kola airport Bodo) in the `Kola` theatre package. It
MUST NOT dump every Kola airport.

#### Scenario: Bodo resolves
- **WHEN** the registry is queried for airfield `Bodo` with theatre `Kola`
- **THEN** it MUST return `airdromeId` 7

### Requirement: WWII P-51D aircraft and payload
The packaged WWII aircraft table SHALL include exact PyDCS type `P-51D` with
group radio 124.0 MHz. A named payload `p51d_2x_anm64` MUST place verified
CLSID `{AN-M64}` on pylons 4 and 7. The registry MUST NOT list a Typhoon type
id (absent from PyDCS `plane_map`).

#### Scenario: P-51D radio and bombs resolve
- **WHEN** the registry is queried for aircraft `P-51D` and payload `p51d_2x_anm64`
- **THEN** radio MUST be 124.0 MHz and pylons MUST be 4 and 7 with `{AN-M64}`

### Requirement: WWII static object ids
The packaged WWII statics table SHALL list exact PyDCS `fortification_map` keys
used for Channel scenery (`Hangar A`, `Revetment_x4`, `Tent01`, `Belgian gate`,
`Shelter`). Lookup MUST fail clearly for unknown ids.

#### Scenario: Hangar A is known
- **WHEN** the registry lists statics
- **THEN** it MUST include `Hangar A`

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
