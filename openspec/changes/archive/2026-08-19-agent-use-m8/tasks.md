## 1. Schema by home airfield

- [x] 1.1 Add optional `airfield` to `build_spec_schema` / `get_mission_spec_schema`; infer from rejected JSON (`infer_airfield`)
- [x] 1.2 Hawkinge + free_flight/cap load packaged Hawkinge examples; other extra homes rewrite theatre default from `*_home` place-card meta
- [x] 1.3 `host_spec_repair_nudge` passes inferred airfield; invent prompt calls schema with airfield when the ask names a home
- [x] 1.4 Tool bridge documents optional `airfield`

## 2. Extra-home geometry clamp

- [x] 2.1 Host clamp: extra-home Specs that cloned Manston 135/25, 125/76, 120/55 or NeedsOarPoint 180/63, 180/133 rewrite from home card (invent/chat only)
- [x] 2.2 Skip clamp for Manston/NOP default homes and named-place asks (French coast, harbour, mid-Channel)
- [x] 2.3 Wire clamp into planner.py and session.py after land-path clamp

## 3. M8 knob nudges

- [x] 3.1 One-shot host nudges for Mustang/P-51, artillery, scenery, failures, F10 orders, wingman discipline
- [x] 3.2 Bare Hawkinge pair does not stack those knobs; Channel immersion floor unchanged

## 4. Tests, eval, docs

- [x] 4.1 Hermetic tests: Hawkinge schema 76/32; Detling rewrite; Chailey not 180/63; Manston unchanged; clamp 135/25→76/32; Manston not clamped
- [x] 4.2 Eval catalog: pair-as-lead geometry; mustang-strafe, artillery-hunt, scenery-or-failures, section-orders, wingman-discipline (live 2026-08-19: Hawkinge pair 76/32 + size 2; knobs green; first section-orders fail was narrative+dynamics xor flake)
- [x] 4.3 BACKLOG M9, README Status, lessons + dcs-dev-agent-tooling; ruff + pytest
