## ADDED Requirements

### Requirement: Compiler emits Opt* and PointAction for target AI
For each target with non-empty resolved AI / move_formation (after preset
expand), the compiler MUST attach native PyDCS option tasks on the placed
ship or vehicle group (prefer first waypoint) and MUST set land waypoint
`PointAction` when `move_formation` is set (including all motion route points).
Emit MUST use allowlisted Opt* only (e.g. `OptROE`, `OptAlarmState`,
`OptEngageAirWeapons`, `OptRestrictTargets`, `OptInterceptionRange` where
class allows). Free-form Lua MUST NOT be required. Targets that omit AI MUST
retain `#15g` motion/disperse behaviour only.

#### Scenario: Convoy Alarm and Off/On Road compile
- **WHEN** a soft-vehicle path Spec with alarm and move_formation is compiled
- **THEN** the `.miz` MUST include the corresponding option wiring and Action
  string for the vehicle route

#### Scenario: U-boat ROE and Alarm compile
- **WHEN** a sea Spec with U-boat ai roe/alarm is compiled
- **THEN** the `.miz` MUST include those options on the ship group route

#### Scenario: Static omit unchanged
- **WHEN** a Spec target omits ai and move_formation
- **THEN** compile MUST NOT add new AI option tasks beyond existing motion/disperse rules
