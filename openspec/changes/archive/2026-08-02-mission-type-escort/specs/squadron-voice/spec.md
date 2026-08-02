## ADDED Requirements

### Requirement: Escort commander brief notes
When squadron-commander voice is enabled and the planned Spec is escort, the commander brief
SHALL include escort-specific tactics, procedures, and watch-outs (stay with the package,
engagement posture, bounce awareness). Briefs MUST remain host/CLI output only — not Spec
fields or `.miz` `l10n`.

#### Scenario: Escort brief branch
- **WHEN** `build_commander_brief` is invoked for a valid escort Spec with voice enabled
- **THEN** the brief MUST include escort-oriented tactics/procedures/watch-outs
