## ADDED Requirements

### Requirement: Normandy land/sea domain is classified
Validation SHALL classify land vs sea for Spec theatre `Normandy` using a
UK–Cotentin airport chord (curated Normandy airdrome ids), not the Channel
UK–FR chord. A well-formed Normandy ground-attack Spec whose strike point is
inland of Maupertus MUST pass domain checks when targets are land units.
Other non-Channel theatres MUST still fail with `domain_unsupported_theatre`.

#### Scenario: Normandy inland strike is land
- **WHEN** a Normandy Spec places strike at 180° / 133 km from NeedsOarPoint
  with land targets
- **THEN** validation MUST succeed (MUST NOT emit `domain_unsupported_theatre`)

#### Scenario: Normandy mid-Channel CAP station is sea
- **WHEN** domain is classified at 180° / 63 km from NeedsOarPoint on
  Normandy terrain
- **THEN** the result MUST be `sea`

#### Scenario: Caucasus strike still fails closed
- **WHEN** a Caucasus Spec includes strike geometry that requires domain
  classification
- **THEN** validation MUST fail with `domain_unsupported_theatre`

### Requirement: Normandy ground_attack Specs validate
Shared validation SHALL accept a well-formed Normandy ground-attack Spec
(theatre `Normandy`, airfield `NeedsOarPoint`, strike + land targets) when
inventory agrees. It MUST still reject Normandy intercept with
`intercept_unsupported_theatre`.

#### Scenario: Needs Oar Point ground_attack validates
- **WHEN** `examples/needs_oar_point_ground_attack.yaml` is validated against
  an inventory that includes offerable Normandy
- **THEN** validation MUST succeed

## MODIFIED Requirements

### Requirement: Domain checks are theatre-keyed
Validation SHALL NOT run TheChannel UK–FR airport-chord domain classification
for a Spec whose theatre is not `TheChannel`. When Spec theatre is
`Normandy`, validation MUST run the Normandy UK–Cotentin chord instead.
When a Spec theatre is neither TheChannel nor Normandy and includes strike,
recon, or target-path geometry that requires land/sea domain checks,
validation MUST fail with a stable code `domain_unsupported_theatre` (or
equivalent). Airfield-relative map points MUST resolve `airdromeId` with the
Spec theatre.

#### Scenario: Normandy strike domain uses Normandy chord
- **WHEN** a Mission Spec sets theatre `Normandy` and includes land/sea strike
  geometry that requires domain classification
- **THEN** validation MUST classify using Normandy airport ids and MUST NOT
  classify points using Channel UK/FR airdrome ids

#### Scenario: Channel strike domain still classified
- **WHEN** a TheChannel ground-attack Spec is validated
- **THEN** validation MUST still apply the Channel land/sea domain rules

### Requirement: Normandy CAP Specs validate
Shared validation SHALL accept a well-formed Normandy CAP Spec (theatre
`Normandy`, airfield `NeedsOarPoint`, CAP geometry present) when inventory
agrees. It MUST still reject Normandy intercept with
`intercept_unsupported_theatre`. Well-formed Normandy ground-attack Specs
MUST NOT fail solely with `domain_unsupported_theatre`.

#### Scenario: Needs Oar Point CAP validates
- **WHEN** `examples/needs_oar_point_cap.yaml` is validated against an
  inventory that includes offerable Normandy
- **THEN** validation MUST succeed

#### Scenario: Normandy intercept still fails closed
- **WHEN** a Mission Spec sets theatre `Normandy` and `mission_type: intercept`
- **THEN** validation MUST fail with `intercept_unsupported_theatre`
