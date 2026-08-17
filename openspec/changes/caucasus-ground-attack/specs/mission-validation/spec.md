## ADDED Requirements

### Requirement: Caucasus land/sea domain is classified
Validation SHALL classify land vs sea for Spec theatre `Caucasus` using a
west-of-coast seaward sector (curated Caucasus coastal vs inland airdrome
ids), not the Channel UK–FR chord and not the Normandy UK–Cotentin chord. A
well-formed Caucasus ground-attack Spec whose strike point is inland past
Kutaisi MUST pass domain checks when targets are land units. Syria, Nevada,
and Falklands MUST still fail with `domain_unsupported_theatre`.

#### Scenario: Caucasus inland strike is land
- **WHEN** a Caucasus Spec places strike at 43° / 110 km from Batumi with
  land targets
- **THEN** validation MUST succeed (MUST NOT emit `domain_unsupported_theatre`)

#### Scenario: Caucasus Black Sea CAP station is sea
- **WHEN** domain is classified at 270° / 40 km from Batumi on Caucasus
  terrain
- **THEN** the result MUST be `sea`

#### Scenario: Syria strike still fails closed
- **WHEN** a Syria Spec includes strike geometry that requires domain
  classification
- **THEN** validation MUST fail with `domain_unsupported_theatre`

### Requirement: Caucasus ground_attack Specs validate
Shared validation SHALL accept a well-formed Caucasus ground-attack Spec
(theatre `Caucasus`, airfield `Batumi`, strike + land targets) when inventory
agrees. It MUST still reject Caucasus intercept with
`combat_unsupported_theatre` at the schema/invent layer.

#### Scenario: Batumi ground_attack validates
- **WHEN** `examples/batumi_kutaisi_ground_attack.yaml` is validated against
  an inventory that includes offerable Caucasus
- **THEN** validation MUST succeed

## MODIFIED Requirements

### Requirement: Domain checks are theatre-keyed
Validation SHALL NOT run TheChannel UK–FR airport-chord domain classification
for a Spec whose theatre is not `TheChannel`. When Spec theatre is
`Normandy`, validation MUST run the Normandy UK–Cotentin chord instead. When
Spec theatre is `Caucasus`, validation MUST run the Caucasus west-of-coast
recipe instead. When a Spec theatre is none of TheChannel, Normandy, or
Caucasus and includes strike, recon, or target-path geometry that requires
land/sea domain checks, validation MUST fail with a stable code
`domain_unsupported_theatre` (or equivalent). Airfield-relative map points
MUST resolve `airdromeId` with the Spec theatre.

#### Scenario: Normandy strike domain uses Normandy chord
- **WHEN** a Mission Spec sets theatre `Normandy` and includes land/sea strike
  geometry that requires domain classification
- **THEN** validation MUST classify using Normandy airport ids and MUST NOT
  classify points using Channel UK/FR airdrome ids

#### Scenario: Caucasus strike domain uses Caucasus recipe
- **WHEN** a Mission Spec sets theatre `Caucasus` and includes land/sea strike
  geometry that requires domain classification
- **THEN** validation MUST classify using Caucasus coastal/inland airport ids
  and MUST NOT classify points using Channel or Normandy airdrome ids

#### Scenario: Channel strike domain still classified
- **WHEN** a TheChannel ground-attack Spec is validated
- **THEN** validation MUST still apply the Channel land/sea domain rules
