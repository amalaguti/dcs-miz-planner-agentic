## ADDED Requirements

### Requirement: Free-flight compile ignores absent extension points
When compiling a free-flight Mission Spec, the compiler SHALL treat absent or empty `enemies`, `objectives`, and `triggers` as no-ops and MUST produce the same free-flight placement behaviour as before this change.

#### Scenario: Manston example without extensions
- **WHEN** the checked-in Manston free-flight Mission Spec (with `schema_version` `"1"` and no extension payloads) is compiled
- **THEN** the system MUST write a `.miz` that places the player cold at Manston on The Channel with the Spec’s time and weather, and the `.miz` MUST remain openable in the DCS Mission Editor / Instant Action

### Requirement: Non-empty extension points not compiled yet
The compiler (or loader, before compile) MUST NOT silently drop non-empty `enemies`, `objectives`, or `triggers`. Until a later change implements those capabilities, non-empty values MUST cause a clear failure.

#### Scenario: Non-empty enemies refused
- **WHEN** a Mission Spec includes a non-empty `enemies` collection
- **THEN** compilation MUST NOT produce a combat `.miz` for this change, and the user MUST receive an error that combat extensions are not supported yet
