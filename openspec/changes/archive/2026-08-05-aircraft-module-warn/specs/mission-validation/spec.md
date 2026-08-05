## ADDED Requirements

### Requirement: Soft-warn missing known aircraft modules
When a usable DCS install root from the theatre inventory is present on disk, validation
MUST soft-warn (MUST NOT fail solely for this reason) if the Mission Spec references a
known Channel aircraft whose expected module folder is missing under that install’s
aircraft locations (at least `Mods/aircraft` and `CoreMods/WWII Units`, using the
committed Spec-id → folder map including known hyphen aliases). Warnings MUST use a
stable code (e.g. `aircraft_module_missing`) and MUST NOT write or promote module ids
into registry YAML. When no inventory roots exist on disk, validation MUST skip this
check (no spurious warnings).

#### Scenario: Missing Spitfire folder warns
- **WHEN** a free-flight Spec uses `SpitfireLFMkIX` and the inventory points at a DCS root
  on disk that lacks the Spitfire aircraft folder
- **THEN** validation MUST still be ok for this reason alone and MUST include an
  `aircraft_module_missing` warning for the player aircraft

#### Scenario: Present folder does not warn
- **WHEN** the same Spec is validated against a root that contains the Spitfire folder
- **THEN** validation MUST NOT emit `aircraft_module_missing` for that aircraft

#### Scenario: No roots on disk skips check
- **WHEN** inventory lists no DCS roots that exist as directories
- **THEN** validation MUST NOT emit aircraft-module-missing warnings
