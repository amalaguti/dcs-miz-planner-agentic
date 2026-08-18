## ADDED Requirements

### Requirement: Spec schema tool accepts Nevada ground_attack
`get_mission_spec_schema` SHALL accept theatre `Nevada` with mission type
`ground_attack`. The derived example MUST follow the Nellis Creech inland
envelope (not Manston, not Batumi, not Aleppo 121/200, not north-range CAP
350/40) and notes MUST NOT concatenate Channel template bundles that cite
french-coast 125/76. When mission type is `recon` on Nevada, the tool MUST NOT
return a Channel combat skeleton.

#### Scenario: Nevada ground_attack schema uses Nellis
- **WHEN** a caller requests the ground_attack Spec schema with theatre `Nevada`
- **THEN** the example MUST use `Nellis`, theatre `Nevada`, Su-25T, payload
  `su25t_2x_fab250`, Russia-country trucks, and strike geometry 303° / 85 km
  (not CAP 350/40, not Aleppo 121/200, not Kutaisi 43/110, not Manston 125/76)

#### Scenario: Nevada recon schema still has no Manston skeleton
- **WHEN** a caller requests a recon schema with theatre `Nevada`
- **THEN** the result MUST NOT present a Manston combat example as the
  template to copy

## MODIFIED Requirements

### Requirement: list_strike_targets theatre filter
`list_strike_targets(theatre="Nevada")` SHALL return the packaged modern land
trucks (`Ural-375`, `GAZ-66`, `ZIL-135`). Stored `theatre_id` MAY remain
`Caucasus`. Channel lists MUST still exclude those ids. Syria dual-offer MUST
stay. Falklands lists MUST stay empty.

#### Scenario: Nevada strike list includes modern trucks
- **WHEN** a caller lists strike targets with theatre `Nevada`
- **THEN** the result MUST include `Ural-375` and MUST NOT include Channel
  WWII `Blitz`

### Requirement: Spec schema tool accepts Nevada escort
`get_mission_spec_schema` SHALL accept theatre `Nevada` with mission type
`escort`. When mission type is `recon` on Nevada, the tool MUST NOT return a
Channel combat skeleton. Ground_attack on Nevada MUST use the inland Creech
example, not the escort envelope.

#### Scenario: Nevada escort schema uses Nellis
- **WHEN** a caller requests the escort Spec schema with theatre `Nevada`
- **THEN** the example MUST use `Nellis`, theatre `Nevada`, Su-25T, USA
