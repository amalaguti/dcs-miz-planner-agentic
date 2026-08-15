## ADDED Requirements

### Requirement: Miz-patch reweather is TheChannel-only
The miz-zip weather patch path SHALL run only when the mission theatre is
`TheChannel`. For any other theatre it MUST fail closed (or require the Spec
sidecar recompile path) and MUST NOT build a dummy Manston/TheChannel Spec.

#### Scenario: Channel miz patch still allowed
- **WHEN** reweather patches a TheChannel `.miz` without a sibling Spec
- **THEN** the Channel weather overwrite path MUST still be available

#### Scenario: Normandy miz patch refused
- **WHEN** reweather is asked to miz-patch a Normandy `.miz` without using the
  Spec sidecar path
- **THEN** the operation MUST fail closed and MUST NOT apply Channel/Manston
  dummy Spec geometry
