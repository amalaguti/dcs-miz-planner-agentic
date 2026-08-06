## ADDED Requirements

### Requirement: Agent tool reweathers mission files
The agent tool surface SHALL expose a mutating tool to re-weather an existing
`.miz` (optional Spec path, weather pattern id, optional seed) that invokes the
same library API as the CLI. The tool MUST report overwrite path and whether
Spec recompile or miz patch was used.

#### Scenario: Tool reweather with pattern
- **WHEN** the agent tool is called with a `.miz` path and `broken_channel`
- **THEN** the result MUST be ok on success and include the overwritten path
