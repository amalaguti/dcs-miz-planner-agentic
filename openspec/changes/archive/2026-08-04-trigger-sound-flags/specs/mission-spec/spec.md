## ADDED Requirements

### Requirement: Sound actions reference curated assets only
When a Mission Spec includes a trigger `sound` action, it MUST identify audio by a
curated `asset_id` from the product sound-asset registry. The Spec MUST NOT carry raw
audio paths or binary sound data.

#### Scenario: asset_id field only
- **WHEN** a Spec declares `type: sound` with `asset_id` and no path fields
- **THEN** loading MUST succeed when the rest of the Spec is valid
