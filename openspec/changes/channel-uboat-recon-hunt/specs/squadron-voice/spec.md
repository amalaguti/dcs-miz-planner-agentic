## ADDED Requirements

### Requirement: Commander brief mentions surfaced U-boat discipline
When briefing a Spec whose targets/contacts include `Uboat_VIIC` (recon or ground_attack),
squadron-commander voice SHALL mention that the boat is to be observed or attacked
**while surfaced** and MUST NOT instruct depth-charge / submerged ASW procedures.

#### Scenario: U-boat brief language
- **WHEN** a commander brief is generated for a Spec with `Uboat_VIIC` targets or contacts
- **THEN** the text MUST indicate surfaced observe/attack (and MUST NOT claim depth charges)
