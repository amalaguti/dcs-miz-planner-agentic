## ADDED Requirements

### Requirement: Nevada land/sea domain classification
Shared validation SHALL classify strike and recon map points on theatre
`Nevada` as land or sea using desert-default land on the eight curated airport
ids (Nellis 4, GroomLake 2, Creech 1, TonopahTestRange 18, NorthLasVegas 15,
HendersonExecutive 8, BoulderCity 6, Mesquite 13). Near a curated airfield
MUST be land; otherwise MUST be land. It MUST NOT run Channel UK–FR, Normandy
UK–Cotentin, Caucasus west-of-coast, or Syria seaward chords on Nevada x,y.
It MUST NOT promote Echo Bay id 7. Falklands MUST still fail closed.

#### Scenario: Nellis CAP station is land
- **WHEN** a Nevada Spec strike or CAP-equivalent point is 350° / 40 km from
  Nellis
- **THEN** domain classification MUST return land

#### Scenario: Creech inland strike is land
- **WHEN** a Nevada Spec strike point is 303° / 85 km from Nellis
- **THEN** domain classification MUST return land

### Requirement: Nevada ground_attack Specs validate
Shared validation SHALL accept a well-formed Nevada ground_attack Spec
(theatre `Nevada`, airfield `Nellis`, nested strike + land targets) when
inventory agrees. It MUST still reject Nevada recon invent.

#### Scenario: Nellis Creech ground_attack validates
- **WHEN** `examples/nellis_creech_ground_attack.yaml` is validated against
  an inventory that includes offerable Nevada
- **THEN** validation MUST succeed

## MODIFIED Requirements

### Requirement: Nevada CAP Specs validate
Shared validation SHALL accept a well-formed Nevada CAP Spec
(theatre `Nevada`, airfield `Nellis`, nested cap) when inventory agrees.
It MUST still reject Nevada recon invent.

#### Scenario: Nellis north-range CAP validates
- **WHEN** `examples/nellis_north_range_cap.yaml` is validated against an
  inventory that includes offerable Nevada
- **THEN** validation MUST succeed

### Requirement: Nevada escort Specs validate
Shared validation SHALL accept a well-formed Nevada escort Spec
(theatre `Nevada`, airfield `Nellis`, nested escort + package) when
inventory agrees. It MUST still reject Nevada recon invent.

#### Scenario: Nellis north-range escort validates
- **WHEN** `examples/nellis_north_range_escort.yaml` is validated against an
  inventory that includes offerable Nevada
- **THEN** validation MUST succeed

### Requirement: Extra Nevada airfields validate
Shared validation SHALL accept a well-formed Nevada free-flight Spec whose
player airfield is a curated extra Nevada key (e.g. `GroomLake`) when
inventory agrees. Recon invent on Nevada MUST still be rejected.

#### Scenario: Groom Lake freeflight validates
- **WHEN** `examples/groom_lake_cold_freeflight.yaml` is validated against an
  inventory that includes offerable Nevada
- **THEN** validation MUST succeed
