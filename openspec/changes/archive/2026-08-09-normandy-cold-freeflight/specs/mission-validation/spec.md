## ADDED Requirements

### Requirement: Normandy freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Normandy` and
airfield `NeedsOarPoint` when the packaged registry supports Normandy, a terrain
binding exists, and the install inventory reports `Normandy` as available and
planner-supported.

#### Scenario: Valid Needs Oar Point freeflight passes
- **WHEN** the checked-in Normandy cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Normandy` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Bound Normandy theatre passes binding check
- **WHEN** a Spec uses theatre `Normandy` and the Normandy terrain binding exists
- **THEN** validation MUST NOT fail solely for terrain binding
