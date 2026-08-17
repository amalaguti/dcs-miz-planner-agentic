## ADDED Requirements

### Requirement: Spec schema tool still uses Nellis for Nevada
`get_mission_spec_schema` SHALL continue to use the Nellis free-flight
envelope when theatre is `Nevada`. Extra-AF keys MUST be findable via catalog
lookup; they MUST NOT replace the invent home example.

#### Scenario: Nevada free_flight schema still uses Nellis
- **WHEN** a caller requests the free_flight Spec schema with theatre `Nevada`
- **THEN** the example MUST use `Nellis`, `Su-25T`, and `USA`
