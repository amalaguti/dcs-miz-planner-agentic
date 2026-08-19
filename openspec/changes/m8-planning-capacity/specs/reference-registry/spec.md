## MODIFIED Requirements

### Requirement: WWII countries in era package
The packaged registry SHALL list exact PyDCS country class names `UK`,
`ThirdReich`, and `USA` from era YAML (`data/era/wwii/countries.yaml`). `Germany` MUST
NOT be a known country id. `usaaf` MUST NOT be a known country (`usaaf` is voice only).

#### Scenario: UK, ThirdReich, and USA known
- **WHEN** the registry lists countries for era `wwii`
- **THEN** the set MUST include `UK`, `ThirdReich`, and `USA` and MUST NOT include
  `Germany` as a known id

## ADDED Requirements

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
