## MODIFIED Requirements

### Requirement: Invent uses Channel place geometry
The invent path SHALL instruct the agent to copy `channel_place` geometry
recipes for GA/recon strike/AOI when placing targets. Validation repair
nudges for `motion_domain_mismatch` or `strike_domain_mismatch` MUST use
the inferred theatre: TheChannel (or unspecified) SHALL mention Channel
place recipes (french-coast ~125°/76 km). Caucasus SHALL mention
`kutaisi_inland_strike` 43°/110 km (MUST NOT mention french_coast 125/76 as
the template to copy). Normandy SHALL mention `maupertus_inland_strike`
180°/133 km (MUST NOT mention french_coast 125/76 as the template to copy).

#### Scenario: Domain mismatch repair mentions geometry
- **WHEN** host_spec_repair_nudge is built for a validation payload containing
  motion_domain_mismatch or strike_domain_mismatch and theatre is TheChannel
  or unspecified
- **THEN** the nudge text MUST include Channel place geometry guidance

#### Scenario: Caucasus domain mismatch repair uses Kutaisi
- **WHEN** host_spec_repair_nudge is built for strike_domain_mismatch or
  motion_domain_mismatch with theatre Caucasus (or airfield Batumi)
- **THEN** the nudge MUST mention kutaisi_inland_strike or 43° / 110 km and
  MUST NOT present french_coast_strike_belt 125/76 as the geometry to copy

#### Scenario: Normandy domain mismatch repair uses Maupertus
- **WHEN** host_spec_repair_nudge is built for strike_domain_mismatch or
  motion_domain_mismatch with theatre Normandy
- **THEN** the nudge MUST mention maupertus_inland_strike or 180° / 133 km
  and MUST NOT present french_coast_strike_belt 125/76 as the geometry to copy
