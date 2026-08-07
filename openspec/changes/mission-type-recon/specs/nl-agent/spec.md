## ADDED Requirements

### Requirement: NL agent may invent recon Specs
The NL invent / planning path SHALL treat `recon` as a supported mission type and MUST NOT
emit `player.payload` or `attack_ground` for recon Specs.

#### Scenario: Recon invent shape
- **WHEN** the agent plans a Channel locate/observe sortie
- **THEN** it MAY emit `mission_type: recon` with a `recon` block and `recon_area`
  objective and MUST omit payload
