## 1. Spec model and expander

- [x] 1.1 Add optional `narrative.enabled` to Mission Spec (default false; reject unknown fields)
- [x] 1.2 Implement `apply_narrative(spec, voice=...)` for CAP pack `cap_v1` (station zone, time push, on-station, unit_dead→message+win); voice-keyed message templates
- [x] 1.3 Wire expansion before validate and compile; clear errors for conflicts / non-CAP / missing cap|enemies

## 2. Example, agent, docs

- [x] 2.1 Add `examples/manston_cap_narrative.yaml` (CAP + `narrative.enabled: true`; leave `manston_cap.yaml` alone)
- [x] 2.2 Update agent schema notes / prompts for opt-in CAP narrative
- [x] 2.3 Flip BACKLOG `#23` to `building`; brief README next pointer

## 3. Tests and acceptance

- [x] 3.1 Tests: expand+validate+compile narrative CAP; conflict/non-CAP failures; assert `.miz` has trigger structure
- [x] 3.2 In-game: open compiled narrative CAP in ME Triggers + Instant Action; confirm messages / win path; note findings on tasks
  - Accepted 2026-08-03: ME **Set Rules for Triggers** shows `narrative_push`, `narrative_on_station`, `narrative_bandits_down` on `out/manston_cap_narrative.miz`.
