## ADDED Requirements

### Requirement: NL agent may set target motion
The invent path SHALL be allowed to emit `motion: patrol` or `motion: path` on
`targets[]` for GA and recon when place/class heuristics fit, and MUST prefer
omit/static for harbour and AAA. Paths MUST stay short (≤6 points). The agent
MUST NOT invent rail-mesh trains or ASW motion.

#### Scenario: Agent emits patrol for mid-Channel U-boat
- **WHEN** the pilot asks for a mid-Channel U-boat under way
- **THEN** the agent MAY emit recon or GA with `Uboat_VIIC` and `motion: patrol`
