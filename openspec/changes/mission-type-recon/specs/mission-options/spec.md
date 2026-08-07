## ADDED Requirements

### Requirement: Recon planning option supported
Planning options SHALL list `mission_type` id `recon` with `support: supported` and a
pilot-facing description of locate/observe without strike payload.

#### Scenario: list_mission_options includes recon
- **WHEN** mission-type planning options are listed
- **THEN** `recon` MUST appear as supported
