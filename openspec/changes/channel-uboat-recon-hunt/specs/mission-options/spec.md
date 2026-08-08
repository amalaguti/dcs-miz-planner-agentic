## ADDED Requirements

### Requirement: U-boat hunt planning inspiration
Planning options SHALL expose an advisory `mission_inspiration` entry for surfaced Channel
U-boat locate/hunt that points agents at recon and/or ground_attack sea_craft patterns
(not a new mission type). Channel place guidance for mid-Channel shipping MUST allow
`recon` as well as `ground_attack` where listed.

#### Scenario: Inspiration lists U-boat hunt
- **WHEN** mission_inspiration options are listed after catalog sync
- **THEN** a surfaced U-boat locate/hunt inspiration id MUST appear as advisory

#### Scenario: Mid-Channel place mentions recon
- **WHEN** channel_place options for mid-Channel shipping are listed
- **THEN** related mission types MUST include recon (and ground_attack)
