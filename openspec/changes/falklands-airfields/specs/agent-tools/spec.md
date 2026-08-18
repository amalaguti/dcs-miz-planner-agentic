## ADDED Requirements

### Requirement: Spec schema tool still uses MountPleasant for Falklands
`get_mission_spec_schema` SHALL continue to use the Mount Pleasant
free-flight envelope when theatre is `Falklands`. Extra-AF keys MUST be
findable via catalog lookup; they MUST NOT replace the invent home example.
Port Stanley MUST be findable and MUST NOT become the schema home.

#### Scenario: Falklands free_flight schema still uses MountPleasant
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Falklands`
- **THEN** the example MUST use `MountPleasant`, `Su-25T`, and `UK`
