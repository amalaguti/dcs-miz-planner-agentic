## ADDED Requirements

### Requirement: Validation accepts weather_opts
Shared validation MUST accept Specs with valid `weather_opts.seed` (non-negative
integer or project-defined int range) and MUST continue to reject unknown
weather pattern ids. Invent/resolution failures (e.g. empty gallery family
config) MUST surface as clear validation or compile errors.

#### Scenario: Valid seed validates
- **WHEN** a Channel Spec uses a known weather pattern and `weather_opts.seed`
  within the allowed range
- **THEN** validation MUST succeed for weather_opts
