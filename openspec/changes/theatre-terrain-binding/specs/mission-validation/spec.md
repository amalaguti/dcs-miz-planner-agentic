## ADDED Requirements

### Requirement: Registry theatres must have terrain bindings
Validation MUST fail when the Spec theatre is present in the packaged registry but has no
compiler terrain binding, with a stable code (e.g. `theatre_terrain_unbound`). This prevents
aspirational theatre ids from validating green before the compiler can place them.

#### Scenario: Bound Channel theatre passes binding check
- **WHEN** a Spec uses theatre `TheChannel` and the Channel binding exists
- **THEN** validation MUST NOT fail solely for terrain binding

#### Scenario: Unbound registry theatre fails
- **WHEN** validation sees a registry theatre id that is missing from the terrain binding map
- **THEN** validation MUST fail with `theatre_terrain_unbound` (or equivalent)
