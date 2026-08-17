## ADDED Requirements

### Requirement: Syria land/sea domain classification
Shared validation SHALL classify strike and recon map points on theatre
`Syria` as land or sea using curated coastal vs inland airport ids (Incirlik
16, Bassel Al-Assad 21, Beirut-Rafic Hariri 6 coastal; Aleppo 27, Palmyra 28,
Damascus 7, Ramat David 30, King Hussein 19 inland). Incirlik seaward heading
MUST be 165–195°. It MUST NOT run Channel UK–FR, Normandy UK–Cotentin, or
Caucasus west-of-coast chords on Syria x,y. Nevada MUST still fail closed.

#### Scenario: Incirlik CAP station is sea
- **WHEN** a Syria Spec strike or CAP-equivalent point is 180° / 40 km from
  Incirlik
- **THEN** domain classification MUST return sea

#### Scenario: Aleppo inland strike is land
- **WHEN** a Syria Spec strike point is 121° / 200 km from Incirlik
- **THEN** domain classification MUST return land

### Requirement: Syria ground_attack Specs validate
Shared validation SHALL accept a well-formed Syria ground_attack Spec
(theatre `Syria`, airfield `Incirlik`, nested strike + land targets) when
inventory agrees. It MUST still reject Syria recon invent.

#### Scenario: Incirlik Aleppo ground_attack validates
- **WHEN** `examples/incirlik_aleppo_ground_attack.yaml` is validated against
  an inventory that includes offerable Syria
- **THEN** validation MUST succeed
