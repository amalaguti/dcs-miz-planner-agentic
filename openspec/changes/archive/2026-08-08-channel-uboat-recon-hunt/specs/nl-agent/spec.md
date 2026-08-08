## ADDED Requirements

### Requirement: NL agent may plan surfaced U-boat sorties
The NL invent path SHALL be allowed to emit `recon` or `ground_attack` Specs using
registry `Uboat_VIIC` on mid-Channel water geometry, and MUST NOT invent ASW mission
types, depth-charge payloads, or submerged-detection fields.

#### Scenario: Agent emits recon or GA for U-boat ask
- **WHEN** the pilot asks for a Channel U-boat locate or hunt
- **THEN** the agent MAY emit recon (locate) and/or ground_attack (hunt) Specs with
  `Uboat_VIIC` and MUST omit unsupported ASW fields
