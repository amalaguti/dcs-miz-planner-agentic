## ADDED Requirements

### Requirement: Infer Syria from curated airfield keys
When rejected Spec JSON names a curated Syria airfield and omits a usable
theatre field, theatre inference MUST return `Syria` (not Caucasus when
the key is `Palmyra`).

#### Scenario: Palmyra infers Syria
- **WHEN** rejected JSON contains `"airfield": "Palmyra"` without theatre
- **THEN** `infer_theatre` MUST return `Syria`
