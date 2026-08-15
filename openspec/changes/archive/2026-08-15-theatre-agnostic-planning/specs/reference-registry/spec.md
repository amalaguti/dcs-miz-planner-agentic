## ADDED Requirements

### Requirement: WWII countries in era package
The packaged registry SHALL list exact PyDCS country class names `UK` and
`ThirdReich` from era YAML (`data/era/wwii/countries.yaml`). `Germany` MUST
NOT be a known country id (hint to `ThirdReich` MAY remain). The registry MUST
NOT invent country strings.

#### Scenario: UK and ThirdReich known
- **WHEN** the registry lists countries
- **THEN** the set MUST include `UK` and `ThirdReich` and MUST NOT include
  `Germany` as a known id

### Requirement: Theatre era membership is retained
The packaged registry SHALL retain each theatre package’s `era:` (today `wwii`
for TheChannel and Normandy) so catalog/allowlists can resolve era without a
second hardcoded Channel list.

#### Scenario: Normandy era is wwii
- **WHEN** a caller asks the registry for the era of theatre `Normandy`
- **THEN** it MUST return `wwii`
