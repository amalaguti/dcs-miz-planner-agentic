## ADDED Requirements

### Requirement: Ground-attack strike domain matches target units
For ground-attack Mission Specs, validation MUST resolve the strike map point from the
player airfield and `strike` bearing/distance using the same Channel terrain math as
compile, classify that point as land or sea, and require every `targets[]` unit’s
registry domain (`land` or `sea`) to match. Mismatches MUST fail with a clear
strike-domain error (e.g. land vehicles over water, or ships over land).

#### Scenario: Shipped Manston ground-attack example passes
- **WHEN** the checked-in Manston ground-attack Spec is validated
- **THEN** strike-domain checks MUST succeed

#### Scenario: Land unit over water fails
- **WHEN** a ground-attack Spec places a land-domain target at a mid-Channel strike point
- **THEN** validation MUST fail with a strike-domain mismatch error
