## 1. Guidance + place notes

- [x] 1.1 Enrich french_coast / coastal_harbour descriptions for short path
      deltas and harbour→sea-only units
- [x] 1.2 Prompts + Spec schema: 2–3 path points from deltas; harbour →
      list_strike_targets(domain=sea)
- [x] 1.3 Enrich host_spec_repair_nudge with pasteable inland path YAML; harbour
      sea-unit nudge when relevant

## 2. Host land path clamp

- [x] 2.1 Implement narrow invent/chat clamp: land path domain fail → rewrite
      path from strike + path_point_deltas; re-validate once
- [x] 2.2 Ensure CLI `dcs-miz validate` does not auto-clamp

## 3. Tests + backlog + accept

- [x] 3.1 Hermetic tests: path deltas, harbour sea guidance, repair path
      example, clamp behaviour
- [x] 3.2 BACKLOG `#8g` building→done when accepted; next = `#8e` shelf expand
- [x] 3.3 Ruff + full pytest green
- [x] 3.4 Accept: hermetic green; live invent convoy + harbour prefer pass
      (CLI/API; ME not required) — live suite 2026-08-08 PASS 6/6 after
      harbour 120/68 + divergent path clamp
