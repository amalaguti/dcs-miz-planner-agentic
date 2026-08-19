## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: Modern era countries and aircraft are era-keyed
The packaged registry SHALL load countries and aircraft from each
`data/era/<era>/` package (`wwii` and `modern`). Era `modern` SHALL include
PyDCS countries `Georgia`, `Turkey`, `USA`, `UK`, `Russia`, `Syria`,
`Argentina`, and `Norway`, aircraft `Su-25T` with group radio 251.0 MHz, and
dual-era `SpitfireLFMkIX` / `SpitfireLFMkIXCW` with group radio 124.0 MHz
(same refs as WWII). `UK` and those Spitfire types MUST remain in the WWII
era package as well. It MUST NOT add Georgia/Turkey/USA/Russia/Syria/
Argentina/Norway or `Su-25T` to the WWII era package. Known-country and
known-aircraft queries used for validation SHALL be filterable by era so
Channel/Normandy remain `UK` / `ThirdReich` and WWII aircraft (including
Spitfire) only for jets — `Su-25T` stays modern-only. `usaaf` MUST NOT be a
known country. `Germany` MUST NOT be a known country in any era. `Chile`
MUST NOT be a known country.

#### Scenario: WWII countries unchanged
- **WHEN** the registry lists countries for era `wwii`
- **THEN** the set MUST be `UK` and `ThirdReich` and MUST NOT include
  `Georgia`, `Turkey`, `USA`, `Russia`, `Syria`, `Argentina`, `Norway`, or
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
