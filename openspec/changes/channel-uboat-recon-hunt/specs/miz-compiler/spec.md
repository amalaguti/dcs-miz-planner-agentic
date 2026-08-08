## ADDED Requirements

### Requirement: Compile places U-boat ship groups on sea AOI/strike
For validated recon or ground_attack Specs that list `Uboat_VIIC` targets on sea-domain
geometry, the compiler MUST place PyDCS ship groups of that type near the AOI/strike
point (existing sea placement path). Free-form Lua MUST NOT be required.

#### Scenario: Recon U-boat contacts compile as ships
- **WHEN** a recon Spec with mid-Channel `Uboat_VIIC` contacts is compiled
- **THEN** the `.miz` MUST contain `Uboat_VIIC` ship unit(s) near the AOI

#### Scenario: GA U-boat targets compile as ships
- **WHEN** a ground_attack Spec with mid-Channel `Uboat_VIIC` targets is compiled
- **THEN** the `.miz` MUST contain `Uboat_VIIC` ship unit(s) near the strike point
