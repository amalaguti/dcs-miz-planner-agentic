## ADDED Requirements

### Requirement: Path domain mismatch remains validated
Validate SHALL continue to reject land path waypoints whose map samples are not
land (and sea path samples not sea) with motion_domain_mismatch (or an equally
specific path-point domain code). Host invent clamp MUST NOT weaken this check
for CLI validate.

#### Scenario: Off-domain land path point fails validate
- **WHEN** a land soft-vehicle target has a path point over Channel water
- **THEN** validate MUST fail with a motion domain mismatch referencing the
  path sample
