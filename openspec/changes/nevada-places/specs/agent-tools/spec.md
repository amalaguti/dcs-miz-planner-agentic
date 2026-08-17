## ADDED Requirements

### Requirement: Spec schema tool accepts Nevada CAP
`get_mission_spec_schema` SHALL accept theatre `Nevada` with mission type
`cap`. The derived example MUST follow the Nellis north-range CAP envelope
(not Manston 135/25, not Cherbourg 180/63, not Batumi 270/40, not Incirlik
180/40).

#### Scenario: Nevada CAP schema uses Nellis
- **WHEN** a caller requests the CAP Spec schema with theatre `Nevada`
- **THEN** the example MUST use `Nellis`, theatre `Nevada`, Su-25T, USA, and
  CAP 350° / 40 km (not Incirlik 180° / 40 km)
