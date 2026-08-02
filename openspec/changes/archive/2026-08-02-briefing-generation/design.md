## Context

`build_commander_brief` already produces Situation / Tactics / Procedures / Watch-outs
for every mission type (CLI `/briefing`, `PlanResult.brief`). Compiled `.miz` files still
leave PyDCS default empty `l10n/DEFAULT/dictionary` strings for Sortie, Description, and
Blue/Red Task. PyDCS exposes `set_sortie_text`, `set_description_text`,
`set_description_bluetask_text`, and `set_description_redtask_text`. M4 types are done;
this change wires the brief into those fields at compile time.

Constraint: AI plans; software compiles — no LLM-authored dictionary Lua.

## Goals / Non-Goals

**Goals:**

- Every successful Channel compile writes non-empty sortie + description + player-coalition
  task text into `l10n`.
- Reuse `build_commander_brief` + voice ids (`raf` / `usaaf` / `neutral`); strip markdown
  for ME display.
- Optional `voice` on compile (CLI/API); default `raf` when unset (CLI may resolve prefs
  before calling).
- Tests assert dictionary content; golden harness includes the dictionary member.
- In-game accept: briefing panel shows the text.

**Non-Goals:**

- TTS, kneeboards, triggers, multi-language packs.
- Spec fields that hold briefing prose.
- LLM writing into the `.miz`.

## Decisions

1. **Deterministic Spec → brief → l10n (not LLM → l10n)**
   - Reuse host `build_commander_brief`. Alternatives: LLM post-compile rewrite (rejected —
     non-deterministic goldens, violates compile purity); Spec-only `description` paste
     (rejected — weak immersion, ignores voice).

2. **Field mapping**
   - **Sortie** → `spec.name` (short ME list title).
   - **Description** → Spec `description` (if non-empty) plus Situation and Watch-outs
     sections (plain text, no `##` headers).
   - **Player-coalition task** → Tactics + Procedures (+ closing line).
   - **Opposing-coalition task** → empty string in v1 (avoid inventing enemy doctrine).
   - Helper `build_mission_briefing_texts(spec, voice) ->` structured strings in
     `agent/voice.py` (or a thin `briefing.py` next to it); compiler stays the only PyDCS
     importer and only calls setters.

3. **Voice on compile**
   - `CompilerInterface.compile(..., *, voice: str | None = None)`.
   - `None` → `DEFAULT_VOICE` (`raf`). Normalize via existing `normalize_voice`.
   - CLI `dcs-miz compile --voice`; `compile_mission(..., voice=)` for tools/agent.
   - Prefs resolution stays at CLI/agent host layer (compiler does not open SQLite).

4. **Golden / regression**
   - Pin golden compiles to `voice="raf"`.
   - Extend fixture helpers to extract/compare `l10n/DEFAULT/dictionary` and require that
     zip member.
   - Contract needles: mission name in sortie; distinctive brief fragments per example
     (e.g. Manston / free flight / intercept wording).

5. **No Spec schema change**
   - Existing `name` / `description` suffice. Briefing is compile output, not a new Spec
     block.

## Risks / Trade-offs

- [Markdown looks ugly in ME] → Strip `#` headers; use blank-line section labels or none.
- [Long briefs overflow ME UI] → Keep current brief length; trim later if needed.
- [Voice diverges CLI vs .miz] → Same builder; document that compile voice defaults to raf
  unless `--voice` / tool arg matches the plan voice.
- [All goldens refresh] → Expected; one refresh pass after implement.
- [Empty red task looks unfinished] → Accept for v1; optional later stub.

## Migration Plan

1. Add briefing text builder + unit tests (no PyDCS).
2. Wire compiler setters; optional voice on interface/CLI/tools.
3. Refresh all Manston goldens with dictionary member; extend contracts.
4. Docs + BACKLOG; in-game accept one example (free flight or escort).

## Open Questions

- None blocking — opposing task stays empty unless acceptance wants a one-liner.
