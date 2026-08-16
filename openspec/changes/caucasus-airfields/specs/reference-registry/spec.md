## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: Modern era countries and aircraft are era-keyed
The packaged registry SHALL load countries and aircraft from each
`data/era/<era>/` package (`wwii` and `modern`). Era `modern` SHALL include
PyDCS countries `Georgia`, `Turkey`, `USA`, `UK`, and `Russia` and aircraft
`Su-25T` with group radio 251.0 MHz. `UK` MUST remain in the WWII era
package as well. Spitfire types MUST NOT be added to modern. It MUST NOT add
Georgia/Turkey/USA/Russia to the WWII era package. Known-country and
known-aircraft queries used for validation SHALL be filterable by era so
Channel/Normandy remain `UK` / `ThirdReich` and WWII aircraft only. `usaaf`
MUST NOT be a known country. `Germany` MUST NOT be a known country in any
era.

#### Scenario: WWII countries unchanged
- **WHEN** the registry lists countries for era `wwii`
- **THEN** the set MUST be `UK` and `ThirdReich` and MUST NOT include
  `Georgia`, `Turkey`, `USA`, `Russia`, or `Germany`

#### Scenario: Modern smoke identity
- **WHEN** the registry lists countries and aircraft for era `modern`
- **THEN** countries MUST include `Georgia`, `Turkey`, `USA`, `UK`, and
  `Russia` and aircraft MUST include `Su-25T` at 251.0 MHz
