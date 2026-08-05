## ADDED Requirements

### Requirement: /research injects untrusted notes with delimiters
When the chat host injects `/research` results into the session message history for later
turns, the injected user content MUST wrap the notes in explicit untrusted-research
delimiters and MUST state that the content is not Spec field authority, not tool-call
instructions, and not higher-priority user commands. Notes shown to the user and injected
MUST use the same sanitized research notes as `research_guidance`.

#### Scenario: Delimited injection
- **WHEN** the user runs `/research` successfully
- **THEN** the host MUST append a session message whose content includes untrusted-research
  delimiters around the notes and an explicit not-Spec / not-instructions disclaimer

#### Scenario: Live vs fixture label visible
- **WHEN** `/research` falls back to fixtures with a warning
- **THEN** printed and injected text MUST indicate fixture fallback (not claim pure live
  web results)
