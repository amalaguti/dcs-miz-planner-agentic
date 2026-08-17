## ADDED Requirements

### Requirement: Spec schema tool accepts Nevada escort
`get_mission_spec_schema` SHALL accept theatre `Nevada` with mission type
`escort`. The derived example MUST follow the Nellis north-range escort
envelope (not Manston, not Incirlik, not Batumi, not Needs Oar Point) and
notes MUST NOT concatenate Channel template bundles that cite Manston 120/55.
When mission type is `ground_attack` or `recon` on Nevada, the tool MUST NOT
return a Channel combat skeleton.

#### Scenario: Nevada escort schema uses Nellis
- **WHEN** a caller requests the escort Spec schema with theatre `Nevada`
- **THEN** the example MUST use `Nellis`, theatre `Nevada`, Su-25T, USA
  package, Russia bounce, and escort geometry 350° / 40 km (not Manston 120° /
  55 km, not Incirlik 180/40, not Batumi 270/40)
