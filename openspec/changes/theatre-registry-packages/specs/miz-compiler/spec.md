## ADDED Requirements

### Requirement: Player airdrome resolved for Spec theatre
The compiler SHALL resolve the player airfield → `airdromeId` using the Spec
theatre’s packaged airfield map. It MUST NOT apply another theatre’s airdrome
id (for example Channel `Manston=5` on Normandy terrain).

#### Scenario: NeedsOarPoint compile uses Normandy map
- **WHEN** the checked-in Needs Oar Point cold free-flight Mission Spec is
  compiled
- **THEN** the compiler MUST obtain `NeedsOarPoint`’s `airdromeId` from the
  Normandy theatre package and the resulting `.miz` MUST place the player cold
  at airdromeId 28

#### Scenario: Wrong-theatre airfield does not compile
- **WHEN** a Mission Spec requests theatre `Normandy` and airfield `Manston`
- **THEN** compilation MUST NOT write a `.miz` (shared validation failure or
  equivalent registry error)

## MODIFIED Requirements

### Requirement: Compiler resolves facts via Channel registry
The free-flight compiler SHALL resolve theatre support, player airfield →
`airdromeId` (for the Spec theatre), known aircraft checks, and group radio
frequency through the packaged registry API rather than private ad-hoc
constants inaccessible to other components.

#### Scenario: Manston compile still uses registry Manston=5
- **WHEN** the checked-in Manston free-flight Mission Spec is compiled
- **THEN** the compiler MUST obtain Manston’s `airdromeId` from the packaged
  registry for theatre `TheChannel` and the resulting `.miz` MUST still place
  the player cold at Manston (`airdromeId` 5) with Spitfire group frequency
  124.0 MHz and remain openable in DCS Mission Editor / Instant Action
