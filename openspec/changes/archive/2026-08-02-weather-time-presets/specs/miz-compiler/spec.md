## ADDED Requirements

### Requirement: Compile applies dawn and marginal weather
The compiler SHALL map Spec weather `dawn_clear` and `marginal_vfr` to distinct PyDCS
weather configurations (visibility and/or cloud density differing from `sunny_clear`).
Precipitation fields MUST use PyDCS perception enums (not raw integers). Unsupported
weather values MUST fail before writing a `.miz`.

#### Scenario: Dawn clear compile differs from sunny
- **WHEN** the dawn example Spec is compiled
- **THEN** the `.miz` weather configuration MUST differ from the sunny-clear free-flight
  example in visibility and/or cloud settings as designed

#### Scenario: Marginal VFR compile reduces visibility
- **WHEN** the marginal VFR example Spec is compiled
- **THEN** the `.miz` MUST reflect reduced visibility versus `sunny_clear` (marginal VFR
  band) and MUST still place the player per the Spec

#### Scenario: Sunny clear still compiles
- **WHEN** the Manston cold free-flight Spec (`sunny_clear`) is compiled
- **THEN** prior clear-weather behaviour MUST remain
