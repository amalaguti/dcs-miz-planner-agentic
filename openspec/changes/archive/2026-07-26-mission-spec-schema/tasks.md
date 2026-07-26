## 1. Model & contract

- [x] 1.1 Add required `schema_version` (`"1"`) to `MissionSpec` with clear validation on missing/unsupported values
- [x] 1.2 Configure Mission Spec models with `extra="forbid"` so unknown keys fail load
- [x] 1.3 Add optional reserved fields `enemies`, `objectives`, `triggers` (absent/empty OK; non-empty raises “not supported yet”)
- [x] 1.4 Update `examples/manston_cold_freeflight.yaml` with `schema_version: "1"` and no extension payloads

## 2. Loader / CLI errors

- [x] 2.1 Ensure YAML load surfaces Pydantic / “not supported yet” errors clearly via the CLI (no stack-trace-only UX for expected validation failures)
- [x] 2.2 Add or extend unit tests for: valid Manston spec; missing `schema_version`; unknown key; non-empty `enemies`

## 3. Compiler acceptance

- [x] 3.1 Confirm free-flight compile path ignores absent/empty extension fields (no behaviour change for Manston)
- [x] 3.2 Compile Manston example to `out/` and verify `.miz` zip members still meet compiler acceptance (mission/options/theatre/warehouses as required)
- [x] 3.3 Human acceptance: open compiled `.miz` in DCS Mission Editor / Instant Action (Channel + Spitfire installed) — accepted in-game 2026-07-26

## 4. Docs / backlog hygiene

- [x] 4.1 Update `docs/BACKLOG.md` item `mission-spec-schema` status to `building` while applying, then `done` when archived
- [x] 4.2 Keep README status accurate if schema_version becomes part of the documented example (no change needed — README shows the compile command only, not the YAML body)
