## ADDED Requirements

### Requirement: Infer Caucasus from curated airfield keys
When rejected Spec JSON names a curated Caucasus airfield and omits a usable
theatre field, theatre inference MUST return `Caucasus` (not Normandy when
the key is `Mozdok`).

#### Scenario: Mozdok infers Caucasus
- **WHEN** rejected JSON contains `"airfield": "Mozdok"` without theatre
- **THEN** `infer_theatre` MUST return `Caucasus`
