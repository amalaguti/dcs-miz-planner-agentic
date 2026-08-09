## ADDED Requirements

### Requirement: Known catalog includes Normandy
After catalog sync from the packaged registry, known theatres MUST include
`Normandy` and known airfields MUST include `NeedsOarPoint`.

#### Scenario: Sync populates Normandy
- **WHEN** a catalog sync runs against the packaged registry after this change
- **THEN** the catalog MUST contain theatre `Normandy` and airfield
  `NeedsOarPoint`

### Requirement: Offerable Normandy when installed
An offerable-theatre query MUST include `Normandy` when it is known and the
install inventory reports it available and planner-supported.

#### Scenario: Offerable Normandy when installed
- **WHEN** Normandy is known and the install inventory reports it available and
  planner-supported
- **THEN** an offerable-theatre query MUST include Normandy
