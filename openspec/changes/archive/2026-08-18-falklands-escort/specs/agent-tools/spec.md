## MODIFIED Requirements

### Requirement: Spec schema tool accepts Falklands
`get_mission_spec_schema` SHALL accept theatre `Falklands`. When mission type
is `free_flight`, the derived example MUST follow the Mount Pleasant envelope
(not Manston, NeedsOarPoint, Batumi, Incirlik, or Nellis) and notes MUST NOT
concatenate Channel/prior-map template bundles. When mission type is `cap`,
the derived example MUST follow the Mount Pleasant South Atlantic CAP envelope
(150° / 40 km / 4000 m). When mission type is `intercept`, the derived example
MUST follow the Mount Pleasant dawn intercept envelope. When mission type is
`escort`, the derived example MUST follow the Mount Pleasant South Atlantic
escort envelope (150° / 40 km; UK package; Argentina bounce; not Channel
escort 120/55, not Nellis 350/40). When mission type is `ground_attack` or
`recon`, the tool MUST NOT return a prior-map combat skeleton.

#### Scenario: Falklands free_flight schema uses MountPleasant
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Falklands`
- **THEN** the example MUST use `MountPleasant`, `Su-25T`, and `UK`

#### Scenario: Extra Falklands airfields do not replace MountPleasant schema
- **WHEN** a caller requests the free_flight Spec schema with theatre
  `Falklands`
- **THEN** the example MUST still use `MountPleasant` (not `RioGallegos` or
  `PortStanley`); extra curated keys MUST remain findable via catalog lookup

#### Scenario: Falklands CAP schema uses MountPleasant
- **WHEN** a caller requests the CAP Spec schema with theatre `Falklands`
- **THEN** the example MUST use `MountPleasant`, theatre `Falklands`,
  Su-25T, UK, Argentina opposition, and CAP 150° / 40 km (not Nellis 350° /
  40 km)

#### Scenario: Falklands intercept schema uses MountPleasant
- **WHEN** a caller requests the intercept Spec schema with theatre
  `Falklands`
- **THEN** the example MUST use `MountPleasant`, theatre `Falklands`,
  Su-25T, UK, and country-Argentina opposition

#### Scenario: Falklands escort schema uses MountPleasant
- **WHEN** a caller requests the escort Spec schema with theatre `Falklands`
- **THEN** the example MUST use `MountPleasant`, theatre `Falklands`,
  Su-25T, UK package, Argentina bounce, and escort 150° / 40 km (MUST NOT
  present Manston 120/55 as the template to copy)
