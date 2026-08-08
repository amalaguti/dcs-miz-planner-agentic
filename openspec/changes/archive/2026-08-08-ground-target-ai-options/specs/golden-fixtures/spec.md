## ADDED Requirements

### Requirement: Examples cover convoy AAA and sea AI options
The repository SHALL include or update checked-in examples that demonstrate
(1) soft-vehicle convoy with transit-style AI / move_formation, (2) AAA or
flak with alert-style AI where practical, and (3) U-boat or sea craft with
roe/alarm. Compile asserts MUST verify option and/or PointAction evidence in
the `.miz`.

#### Scenario: Convoy AI example green
- **WHEN** the convoy AI example is validated and compiled in CI
- **THEN** tests MUST pass and assert AI/move evidence in the `.miz`

#### Scenario: Sea AI example green
- **WHEN** the sea AI example is validated and compiled in CI
- **THEN** tests MUST pass and assert ROE/Alarm (or documented) evidence in the `.miz`
