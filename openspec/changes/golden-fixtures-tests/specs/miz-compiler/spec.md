## ADDED Requirements

### Requirement: Manston compile covered by golden fixtures
The free-flight Manston acceptance compile path SHALL be covered by the repository’s
golden-fixture regression suite. Structural contracts previously asserted only in ad-hoc
compile tests (Channel theatre, Manston cold Spitfire placement, start time, VHF frequency,
required zip members) MUST remain enforced through that suite.

#### Scenario: Manston structural contracts still enforced
- **WHEN** the test suite runs after a compiler change that breaks Manston free-flight
  structure (for example wrong frequency or missing `theatre` member)
- **THEN** the golden-fixture (or equivalent Manston structural) tests MUST fail before the
  change is considered acceptable
