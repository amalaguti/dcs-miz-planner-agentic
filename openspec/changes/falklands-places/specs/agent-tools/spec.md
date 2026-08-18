## MODIFIED Requirements

### Requirement: Spec schema tool accepts Falklands
`get_mission_spec_schema` SHALL accept theatre `Falklands`. When mission type
is `free_flight`, the derived example MUST follow the Mount Pleasant envelope
(not Manston, NeedsOarPoint, Batumi, Incirlik, or Nellis) and notes MUST NOT
concatenate Channel/prior-map template bundles. When mission type is `cap`,
the derived example MUST follow the Mount Pleasant South Atlantic CAP envelope
(150° / 40 km / 4000 m; not Manston 135/25, not Cherbourg 180/63, not
Incirlik 180/40, not Batumi 270/40, not Nellis 350/40). When mission type is
`intercept`, `ground_attack`, `escort`, or `recon`, the tool MUST NOT return
a prior-map combat skeleton.

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

#### Scenario: Falklands intercept schema has no Manston skeleton
- **WHEN** a caller requests an intercept schema with theatre `Falklands`
- **THEN** the result MUST NOT present a Manston, NeedsOarPoint, Batumi,
  Incirlik, or Nellis example as the template to copy
