## ADDED Requirements

### Requirement: Channel R13 shelf promote
Packaged Channel registry SHALL include R13-promoted land ids `flak41`,
`M45_Quadmount`, `QF_37_AA`, `Allies_Director`, `Tiger_I`, `SturmPzIV`,
`Pz_V_Panther_G`, `JagdPz_IV`, `Jagdpanther_G1`, `Coach cargo`,
`Coach cargo open`, and sea ids `LST_Mk2`, `USS_Samuel_Chase`.

#### Scenario: flak41 resolvable
- **WHEN** the registry is queried for flak41
- **THEN** it MUST return a land-domain strike unit

#### Scenario: LST_Mk2 resolvable
- **WHEN** the registry is queried for LST_Mk2
- **THEN** it MUST return a sea-domain strike unit
