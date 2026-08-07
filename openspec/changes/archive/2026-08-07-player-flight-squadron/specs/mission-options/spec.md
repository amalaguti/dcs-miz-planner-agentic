## ADDED Requirements

### Requirement: Player flight planning options
The Channel planning-options catalog SHALL expose player flight knobs the agent can ask
about: flight size (2–4 / solo by omission) and role (`lead` / `wingman`), with short
pilot-facing descriptions. Catalog sync MUST include these options for list/ask tools.

#### Scenario: Options list includes flight role
- **WHEN** a client lists mission planning options after this change
- **THEN** the catalog MUST include player flight size and role entries
