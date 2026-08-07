## ADDED Requirements

### Requirement: Optional curated section orders
The Mission Spec SHALL allow an optional `player.flight.orders` list of curated
order identifiers. When omitted or empty, the compiler MUST NOT emit the
section-order F10 pack from this feature. When present, each id MUST be from the
Channel curated order set (`rejoin`, `engage`, `orbit`, `rtb`, `break` in v1).
`orders` MUST require `player.flight` to be set.

#### Scenario: Orders on wingman flight accepted
- **WHEN** a Spec sets `player.flight` with `role: wingman` and
  `orders: [rejoin, rtb]`
- **THEN** structural load MUST succeed

#### Scenario: Omit orders means none
- **WHEN** a Spec has `player.flight` but omits `orders`
- **THEN** the Spec MUST remain valid without section-order F10 emit from this feature
