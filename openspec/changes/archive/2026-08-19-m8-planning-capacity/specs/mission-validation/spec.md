## MODIFIED Requirements

### Requirement: Channel accepts USA
Shared validation SHALL accept player country `USA` on a WWII theatre
(TheChannel / Normandy) when the rest of the Spec is well-formed. It MUST still
reject modern-only countries on Channel.

#### Scenario: Channel accepts USA
- **WHEN** a TheChannel Mission Spec sets player country `USA`
- **THEN** validation MUST succeed when the rest of the Spec is well-formed

## ADDED Requirements

### Requirement: Unknown scenery types fail validation
Shared validation SHALL reject `scenery[].type` values absent from the packaged
WWII statics registry with a stable `unknown_static` error.

#### Scenario: Unknown hangar id fails
- **WHEN** a Spec lists scenery type `NotARealHangar`
- **THEN** validation MUST fail with code `unknown_static`
