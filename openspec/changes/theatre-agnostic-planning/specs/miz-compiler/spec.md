## ADDED Requirements

### Requirement: Intercept enemy spawn is TheChannel-only
The compiler SHALL place intercept enemies using the packaged TheChannel
Hawkinge/Dover recipe only when Spec theatre is `TheChannel`. It MUST NOT
write those Channel map coordinates onto another theatre’s terrain. For any
other theatre, compilation MUST NOT produce a `.miz` (shared validation
failure or equivalent).

#### Scenario: Channel intercept still uses Hawkinge recipe
- **WHEN** the checked-in Manston intercept example Spec is compiled
- **THEN** enemy placement MUST still use the existing Hawkinge anchor plus
  Dover-approach offset (golden `x=30989.935547`, `y=-35402.577148`)

#### Scenario: Normandy intercept does not compile
- **WHEN** a Mission Spec requests theatre `Normandy` and `mission_type:
  intercept`
- **THEN** compilation MUST NOT write a `.miz`

### Requirement: Join-up outbound bearing stays airfield-relative
Wingman join-up outbound SHALL remain an airfield-relative heading default
(120°) on any bound theatre that compiles a player flight with join-up. It
MUST NOT be treated as Channel-only intercept spawn geometry.

#### Scenario: Normandy free_flight join-up still compiles
- **WHEN** a Normandy NeedsOarPoint free-flight Spec includes a wingman
  join-up
- **THEN** the compiler MUST still be allowed to emit Follow / outbound
  using the generic airfield-relative bearing
