## Why

M8 shipped extra homes, P-51D, artillery, scenery, and sortie-size prompts, but
invent still keys `get_mission_spec_schema` on theatre only. Channel examples
are Manston 135/25, so a Hawkinge pair copies that station despite notes.
The agent must *use* the M8 cards, not grow more YAML.

## What Changes

- `get_mission_spec_schema` / `build_spec_schema` accept optional `airfield`.
  Hawkinge loads packaged Hawkinge examples; other extra homes rewrite the
  theatre default from `*_home` place-card meta.
- Host repair infers airfield from rejected JSON so a Hawkinge draft is not
  repaired with Manston JSON.
- Invent/chat host-clamps extra-home Specs that cloned Manston (135/25, 125/76,
  120/55) or NeedsOarPoint (180/63, 180/133) stations onto the home card.
  CLI validate does not clamp. Named places (French coast, harbour) are not
  rewritten.
- One-shot host nudges when the ask implies Mustang/P-51, artillery, scenery,
  failures, F10 orders, or wingman discipline. Bare “pair from Hawkinge”
  stays size 2 + home geometry only.
- Eval catalog: pair-as-lead expects Hawkinge geometry not 135/25; new
  mustang/artillery/scenery/orders/discipline scenarios.

## Non-goals

- New aircraft, units, or Spec mission types.
- Kola Stage B–C, modern-map depth, GermanyCW.
- Changing Manston as Channel invent default.
- Expanding Channel land-path clamp to other maps.
- ME Instant Action (human do-soon; not a merge gate).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: schema by airfield; extra-home geometry clamp; M8 knob nudges.
- `agent-tools`: `get_mission_spec_schema` accepts optional `airfield`.

## Impact

Agent schema/prompts, invent/chat host clamps, tools surface, eval catalog,
hermetic tests. Channel goldens stay green. Acceptance: pytest + live eval
scenarios; ME Instant Action is not required.
