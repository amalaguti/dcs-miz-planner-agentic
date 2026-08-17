## ADDED Requirements

### Requirement: Infer Nevada from curated airfield keys
When rejected Spec JSON names a curated Nevada airfield and omits a usable
theatre field, theatre inference MUST return `Nevada` (not Falklands when
the key is `GroomLake`). Invent MUST remain free_flight-only at Nellis.

#### Scenario: GroomLake infers Nevada
- **WHEN** rejected JSON contains `"airfield": "GroomLake"` without theatre
- **THEN** `infer_theatre` MUST return `Nevada`
