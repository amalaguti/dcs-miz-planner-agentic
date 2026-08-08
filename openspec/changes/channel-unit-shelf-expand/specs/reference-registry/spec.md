## ADDED Requirements

### Requirement: Channel soft AAA sea shelf expand
Packaged Channel registry SHALL include the promoted soft, AAA, and sea craft
ids from the first shelf-expand batch (Sd_Kfz_2, Horch_901_typ_40_kfz_21,
Willys_MB, flak30/37/38, Flakscheinwerfer_37, KDO_Mod40, bofors40, Dry-cargo
ship-2, HarborTug, Higgins_boat), each with domain land or sea as appropriate.

#### Scenario: New soft land unit resolvable
- **WHEN** the registry is queried for Sd_Kfz_2
- **THEN** it MUST return a land-domain strike unit

#### Scenario: New sea harbour unit resolvable
- **WHEN** the registry is queried for HarborTug
- **THEN** it MUST return a sea-domain strike unit
