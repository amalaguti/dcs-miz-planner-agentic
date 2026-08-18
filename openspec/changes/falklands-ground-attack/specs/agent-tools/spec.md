## MODIFIED Requirements

### Requirement: Spec schema tool accepts Falklands
`get_mission_spec_schema` SHALL accept theatre `Falklands`. When mission type
is `free_flight`, `cap`, `intercept`, or `escort`, the derived example MUST
follow the existing Mount Pleasant envelopes. When mission type is
`ground_attack`, the derived example MUST follow the East Falkland inland
strike envelope (269° / 21 km / 2000 m; `su25t_2x_fab250`; Argentina trucks;
not CAP 150/40, not 303/85, not 121/200, not 43/110, not 125/76). When mission
type is `recon`, the tool MUST NOT return a prior-map combat skeleton.

#### Scenario: Falklands ground_attack schema uses MountPleasant
- **WHEN** a caller requests the ground_attack Spec schema with theatre
  `Falklands`
- **THEN** the example MUST use `MountPleasant`, theatre `Falklands`, Su-25T,
  UK, payload `su25t_2x_fab250`, Argentina-country trucks, and strike 269° /
  21 km (MUST NOT present Manston 125/76 or CAP 150/40 as the template)

### Requirement: list_strike_targets offers modern land trucks on Falklands
`list_strike_targets(theatre="Falklands")` SHALL return `Ural-375`, `GAZ-66`,
and `ZIL-135`. Stored `theatre_id` MAY remain `Caucasus`. Channel lists MUST
still exclude those ids. Syria/Nevada dual-offer MUST stay.

#### Scenario: Falklands strike list dual-offers Caucasus modern trucks
- **WHEN** a caller lists strike units with theatre `Falklands`
- **THEN** the result MUST include `Ural-375` and MUST NOT include Channel
  WWII `Blitz_36-6700A`
