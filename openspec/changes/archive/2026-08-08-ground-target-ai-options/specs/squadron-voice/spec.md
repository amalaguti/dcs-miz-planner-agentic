## ADDED Requirements

### Requirement: Brief may note alert or transit posture
When a Spec sets non-default target AI presets (e.g. AAA alert or convoy
transit), squadron-commander voice SHOULD briefly reflect posture (alert guns /
column under way) without inventing ASW or air-only tactics.

#### Scenario: AAA alert brief cue
- **WHEN** a commander brief is generated for a Spec with aaa_alert-style targets
- **THEN** the text MAY mention alert or ready guns without claiming unsupported systems
