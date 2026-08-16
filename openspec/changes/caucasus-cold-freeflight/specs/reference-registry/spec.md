## ADDED Requirements

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

### Requirement: Modern era countries and aircraft are era-keyed
The packaged registry SHALL load countries and aircraft from each
`data/era/<era>/` package (`wwii` and `modern`). Era `modern` SHALL include
PyDCS country `Georgia` and aircraft `Su-25T` with group radio 251.0 MHz.
It MUST NOT add those ids to the WWII era package. Known-country and
known-aircraft queries used for validation SHALL be filterable by era so
Channel/Normandy remain `UK` / `ThirdReich` and WWII aircraft only.
`Germany` MUST NOT be a known country in any era.

#### Scenario: WWII countries unchanged
- **WHEN** the registry lists countries for era `wwii`
- **THEN** the set MUST be `UK` and `ThirdReich` and MUST NOT include
  `Georgia` or `Germany`

#### Scenario: Modern smoke identity
- **WHEN** the registry lists countries and aircraft for era `modern`
- **THEN** countries MUST include `Georgia` and aircraft MUST include
  `Su-25T` at 251.0 MHz
