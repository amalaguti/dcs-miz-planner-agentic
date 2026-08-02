## ADDED Requirements

### Requirement: Randomized Specs use shared validation
A Spec produced by seeded randomization MUST be subject to the same shared validation
engine as any other Mission Spec before compile. The system MUST NOT provide a compile
path that skips validation solely because the Spec was randomized.

#### Scenario: Invalid randomized output is refused
- **WHEN** a randomized Spec would fail structural or semantic validation
- **THEN** validate/compile MUST report the failure and MUST NOT write a `.miz`
