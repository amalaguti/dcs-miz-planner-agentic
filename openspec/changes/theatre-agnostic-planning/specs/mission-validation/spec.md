## ADDED Requirements

### Requirement: Domain checks are theatre-keyed
Validation SHALL NOT run TheChannel UK–FR airport-chord domain classification
for a Spec whose theatre is not `TheChannel`. When a non-Channel Spec includes
strike, recon, or target-path geometry that requires land/sea domain checks,
validation MUST fail with a stable code `domain_unsupported_theatre` (or
equivalent). Airfield-relative map points MUST resolve `airdromeId` with the
Spec theatre.

#### Scenario: Normandy strike domain fails closed
- **WHEN** a Mission Spec sets theatre `Normandy` and includes land/sea strike
  or recon geometry that requires domain classification
- **THEN** validation MUST fail with `domain_unsupported_theatre` and MUST NOT
  classify points using Channel UK/FR airdrome ids

#### Scenario: Channel strike domain still classified
- **WHEN** a TheChannel ground-attack Spec is validated
- **THEN** validation MUST still apply the Channel land/sea domain rules

### Requirement: Intercept spawn is Channel-only
Validation SHALL reject `mission_type: intercept` when Spec theatre is not
`TheChannel`, with stable code `intercept_unsupported_theatre` (or equivalent).

#### Scenario: Normandy intercept fails validation
- **WHEN** a Mission Spec sets theatre `Normandy` and `mission_type: intercept`
- **THEN** validation MUST fail with `intercept_unsupported_theatre`
