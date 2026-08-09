## ADDED Requirements

### Requirement: Normandy freeflight Mission Spec representable
The Mission Spec SHALL accept a free-flight shape with theatre `Normandy`,
player `SpitfireLFMkIX`, airfield `NeedsOarPoint`, cold parking, start time
09:00, and weather `sunny_clear`.

#### Scenario: Needs Oar Point cold freeflight example is representable
- **WHEN** an author provides that Normandy freeflight Mission Spec with
  `schema_version` `"1"`
- **THEN** the Mission Spec SHALL be accepted as structurally valid for
  compilation

### Requirement: Checked-in Normandy example Mission Spec
The repository SHALL include a checked-in example Mission Spec for Needs Oar
Point cold freeflight on Normandy.

#### Scenario: Normandy example file present
- **WHEN** a developer clones the repository
- **THEN** an example Mission Spec for Normandy Needs Oar Point cold freeflight
  MUST be present, include `schema_version` `"1"`, and be usable as compile input
