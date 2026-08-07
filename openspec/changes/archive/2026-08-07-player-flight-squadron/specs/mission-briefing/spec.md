## ADDED Requirements

### Requirement: Brief mentions player flight when present
When `player.flight` is present, generated briefing / squadron-voice text SHALL mention
the section size and whether the human flies as lead or wingman, in voice-appropriate
language. Solo Specs (no `player.flight`) MUST keep existing brief behaviour.

#### Scenario: Four-ship lead brief
- **WHEN** briefing a Spec with `player.flight.size: 4` and `role: lead`
- **THEN** Sortie/Description or Task text MUST indicate a four-ship section led by the
  player (wording may vary by voice)
