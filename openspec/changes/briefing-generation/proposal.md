## Why

Compiled Channel missions open in DCS with empty Sortie / Description / Task
dictionary strings. Pilots already get a squadron-commander brief in the CLI after
planning; that immersion never reaches the Mission Editor or Instant Action brief
panel. M4 mission types are done — this is the natural M5 immersion slice.

## What Changes

- On every successful compile, write non-empty briefing text into the `.miz` `l10n`
  dictionary via PyDCS (`sortie`, `descriptionText`, coalition task texts).
- Derive that text from the same Spec-driven commander brief used by CLI/`PlanResult`
  (voice register when enabled), split into DCS briefing fields — **not** free-form
  LLM output written into the mission package.
- Optional compile-time voice override (CLI/API); default follows squadron-voice
  resolution (`raf` when unset).
- Refresh golden fixtures and contract asserts so non-empty briefing strings are
  part of compile regression.
- Acceptance: open a compiled example in DCS ME / Instant Action and confirm Sortie,
  Description, and Task text appear.

## Non-goals

- TTS / voice-over audio, kneeboard images, or in-mission radio triggers (M6).
- Putting briefing prose into Mission Spec fields or enums.
- Letting the LLM emit raw dictionary Lua or bypass validate/compile.
- Per-language localisation beyond the mission’s default dictionary language.
- Changing mission placement, tasks, payloads, or new mission types.

## Capabilities

### New Capabilities
- `mission-briefing`: Spec → DCS briefing field mapping (sortie, description, blue/red
  tasks) written at compile time from commander-voice brief content.

### Modified Capabilities
- `miz-compiler`: Successful compiles MUST populate briefing `l10n` strings (not leave
  them empty).
- `squadron-voice`: Clarify that host/CLI briefs remain; `mission-briefing` reuses the
  same brief builder for `.miz` `l10n` (prior “MUST NOT write l10n” constraint lifts for
  that compile path only).
- `golden-fixtures`: Fixtures/contracts MUST expect non-empty briefing dictionary text
  after refresh.

## Impact

- `compiler/pydcs_compiler.py` — call PyDCS `set_sortie_text` /
  `set_description_text` / `set_description_*task_text` after placement.
- `agent/voice.py` — helpers to split commander brief into DCS fields (plain text).
- CLI `compile` (and agent `compile_mission`) — optional `--voice` / voice arg.
- Golden fixtures for all Manston examples; tests asserting dictionary content.
- README / ARCHITECTURE / BACKLOG / LESSONS as needed.
