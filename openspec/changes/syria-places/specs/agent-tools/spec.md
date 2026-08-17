## ADDED Requirements

### Requirement: Spec schema tool accepts Syria CAP
`get_mission_spec_schema` SHALL accept theatre `Syria` with mission type
`cap`. The derived example MUST follow the Incirlik Iskenderun CAP envelope
(not Manston 135/25, not Cherbourg 180/63, not Batumi 270/40).

#### Scenario: Syria CAP schema uses Incirlik
- **WHEN** a caller requests the CAP Spec schema with theatre `Syria`
- **THEN** the example MUST use `Incirlik`, theatre `Syria`, Su-25T, and
  CAP 180° / 40 km (not Batumi 270° / 40 km)
