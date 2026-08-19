## ADDED Requirements

### Requirement: Agent chooses sortie size on vague asks
Invent/chat SHALL emit `player.flight` size 2 role lead when the ask is a pair,
section, Rhubarb, or vague CAP/escort with mates, and SHALL omit `player.flight`
when the ask is clearly solo. Tangmere MUST NOT emit size 4.

#### Scenario: Pair ask uses player.flight
- **WHEN** invent is asked for a Channel pair or Rhubarb
- **THEN** schema/prompt guidance MUST tell the agent to emit `player.flight` size 2
  role lead rather than a second escort package

### Requirement: Channel invent extra homes
Channel invent default SHALL remain Manston. Extra homes Hawkinge / Detling /
Biggin Hill MUST copy per-home geometry rather than Manston 135/25 or 125/76.

#### Scenario: Schema mentions Hawkinge extra home
- **WHEN** Channel free_flight Spec schema notes are loaded
- **THEN** they MUST mention Hawkinge and MUST warn not to copy Manston stations
  onto that field
