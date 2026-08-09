## ADDED Requirements

### Requirement: list_mission_options includes offerable Normandy
When Normandy is offerable on the local machine, `list_mission_options` MUST
list `Normandy` among offerable theatres.

#### Scenario: Offerable Normandy reflected
- **WHEN** Normandy is offerable on the local machine
- **THEN** `list_mission_options` MUST list Normandy among offerable theatres
