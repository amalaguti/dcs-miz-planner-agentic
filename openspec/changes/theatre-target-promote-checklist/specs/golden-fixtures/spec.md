## ADDED Requirements

### Requirement: Promote checklist covered by tests
Hermetic tests SHALL assert that the theatre/target promote checklist file
exists and contains theatre-slice and target-unit section headings (and the
non-goals against ME scrape / auto-promote).

#### Scenario: Checklist presence test green
- **WHEN** docs / process tests run in CI
- **THEN** they MUST fail if the checklist file or required sections are removed
