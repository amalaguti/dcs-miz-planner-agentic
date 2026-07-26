## ADDED Requirements

### Requirement: Compiler resolves facts via Channel registry
The free-flight compiler SHALL resolve theatre support, player airfield → `airdromeId`, known aircraft checks, and group radio frequency through the Channel reference registry API rather than private ad-hoc constants inaccessible to other components.

#### Scenario: Manston compile still uses registry Manston=5
- **WHEN** the checked-in Manston free-flight Mission Spec is compiled
- **THEN** the compiler MUST obtain Manston’s `airdromeId` from the Channel registry and the resulting `.miz` MUST still place the player cold at Manston (`airdromeId` 5) with Spitfire group frequency 124.0 MHz and remain openable in DCS Mission Editor / Instant Action
