## 1. Agent skeleton and stub

- [x] 1.1 Add `src/dcs_miz_planner/agent/` (prompts, tool bridge, LLM protocol, stub LLM)
- [x] 1.2 Implement planner loop: tools + structured Mission Spec; validate; one repair attempt
- [x] 1.3 Stub path produces Manston free-flight Spec that validates/compiles in tests
- [x] 1.4 Add `openai` dependency (or optional group) and OpenAI-compatible live adapter behind env config

## 2. CLI and wiring

- [x] 2.1 CLI `dcs-miz plan "<prompt>"` with `--stub`, output path, optional `--compile`
- [x] 2.2 Clear error when live mode lacks API key
- [x] 2.3 Tests: stub plan → YAML; tool bridge call; missing-key live failure; Ruff clean

## 3. Docs and acceptance

- [x] 3.1 Update ARCHITECTURE / README / BACKLOG (env vars, stub vs live)
- [x] 3.2 Acceptance: stub offline; live Manston prompt → Spec → compile → open `.miz` in DCS when key available
