## ADDED Requirements

### Requirement: Hermetic Normandy freeflight compile regression
The test suite SHALL compile the checked-in Normandy cold freeflight Mission Spec
with an injected inventory that reports `Normandy` (and typically `TheChannel`)
as available and planner-supported, and assert contracted `.miz` structure
(required zip members, Normandy theatre, Spitfire cold at Needs Oar Point /
airdromeId 28, start_time 32400).

#### Scenario: Fresh Normandy compile satisfies contracts
- **WHEN** the Normandy example Spec is compiled under the hermetic test harness
- **THEN** the test MUST pass if and only if the output satisfies those contracts
