## ADDED Requirements

### Requirement: Invent uses Channel place geometry
The invent path SHALL instruct the agent to copy `channel_place` geometry recipes
for GA/recon strike/AOI when placing targets, keep land path waypoints on land
near the strike, and place sea targets on water geometry. Validation repair
nudges for `motion_domain_mismatch` or `strike_domain_mismatch` MUST mention
Channel place recipes (or equivalent concrete bearing/distance guidance).

#### Scenario: Prompts or schema mention place geometry
- **WHEN** invent prompts or GA/recon Spec schema notes are loaded
- **THEN** they MUST mention using channel_place bearing/distance recipes and
  land-vs-sea path/strike coherence

#### Scenario: Domain mismatch repair mentions geometry
- **WHEN** host_spec_repair_nudge is built for a validation payload containing
  motion_domain_mismatch or strike_domain_mismatch
- **THEN** the nudge text MUST include Channel place geometry guidance
