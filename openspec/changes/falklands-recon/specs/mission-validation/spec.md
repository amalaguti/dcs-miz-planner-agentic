## ADDED Requirements

### Requirement: Falklands recon Specs validate
Shared validation SHALL accept a well-formed Falklands recon Spec
(theatre `Falklands`, airfield `MountPleasant`, nested recon + land observe
targets) when inventory agrees.

#### Scenario: Mount Pleasant East Falkland recon validates
- **WHEN** `examples/mount_pleasant_east_falkland_recon.yaml` is validated
  against an inventory that includes offerable Falklands
- **THEN** validation MUST succeed
