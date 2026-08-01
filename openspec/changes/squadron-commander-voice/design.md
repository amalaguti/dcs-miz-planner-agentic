## Context

NL planning (`agent/planner.py` + `prompts.SYSTEM_PROMPT`) already tools, prefs, and
history. Prefs seed includes `squadron_voice`, but nothing selects or applies a persona.
The plan loop ends in machine Spec JSON; user-visible tone today is mostly CLI status.

Channel Spitfire content skews RAF; USAAF is a first-class alternate. Pilots also need
commander-style **operational** guidance (tactics, procedures, watch-outs) tied to mission
type and the planned Spec — optionally enriched from real-world / historical sources on
the web in live mode. Writing that text into `.miz` `l10n` remains a later change.

## Goals / Non-Goals

**Goals:**

- Curated **RAF** / **USAAF** / **neutral** voice packs with period jargon & slang guidance.
- Host resolves voice (CLI → pref → default `raf`) and composes the system prompt.
- After a validated Spec, produce a commander brief: summary + tactics + procedures +
  watch-outs, matched to mission type (`free_flight`, `intercept`, …) and Spec facts.
- Live mode: optional web-backed research tool for procedures, manoeuvres, pilot accounts,
  historical context; stub/CI stays offline with fixtures.
- Spec fields stay plain; research never invents DCS ids or bypasses catalog/validate.
- Tests cover packs, prompt composition, brief structure, and research stub wiring.

**Non-Goals:**

- `.miz` l10n briefings, TTS, in-mission radio/triggers.
- Expanding mission types or changing compile/validate.
- Scraping the web into a permanent registry; research is ephemeral guidance for the brief.
- Autogenerating slang dictionaries from web scrapes.

## Decisions

1. **Voice ids: `raf` | `usaaf` | `neutral`**
   - Match the backlog’s RAF/USAAF split; `neutral` disables persona overlay (base planner
     rules only) but MAY still emit a plain operational brief without commander register.
   - Aliases accepted at CLI/prefs normalize to these ids (`RAF` → `raf`, `us`/`usa` → `usaaf`).
   - Unknown values → fall back to default with a warning (do not fail the plan).

2. **Default: `raf`**
   - Channel + SpitfireLFMkIX is the v1 product centre; RAF is the natural default.
   - Override: `--voice` on `plan`, or pref `squadron_voice`.
   - Resolution order: CLI flag (if set) → pref → `raf`.

3. **Packs in `agent/voice.py`**
   - String constants / dataclasses for v1 (no new YAML loader unless packs outgrow code).
   - Each pack: role framing, tone rules, jargon hints, and rules that **Spec JSON stays
     plain** while the **brief** uses commander register + operational guidance.
   - Prompt also instructs: recommend tactics/procedures/watch-outs appropriate to mission
     type and the planned Spec; prefer researched or well-known WWII fighter practice over
     invented doctrine.

4. **Prompt composition API**
   - `compose_system_prompt(voice: str) -> str` = base planning rules + voice overlay +
     brief/ops guidance.
   - `resolve_voice(*, cli_voice, prefs, default="raf") -> str`.
   - Host reads `squadron_voice` before the loop so the first system message has the right
     voice (do not wait for the model to call `get_user_prefs`).

5. **Commander brief after successful Spec**
   - `PlanResult.brief: str | None` — structured text (markdown-friendly sections):
     **Situation / sortie**, **Tactics**, **Procedures**, **Watch-outs**.
   - **Live:** LLM authors the brief in-voice after Spec acceptance (extra turn or same
     final turn before JSON-only Spec — prefer a dedicated post-validate brief turn so Spec
     JSON stays clean). Host may pass Spec summary + optional research notes into that turn.
   - **Stub/CI:** deterministic host or stub-LLM brief seeded from mission-type templates so
     tests assert section presence without network.
   - CLI prints the brief on success. Full `.miz` narrative briefings stay for `#16`.

6. **Research tool: `research_guidance`**
   - Agent tool: query string + optional hints (`mission_type`, theatre, aircraft).
   - **Live:** web search (or compatible fetch) returning short excerpts/snippets + sources;
     LLM synthesizes into the brief; never copy raw pages into Spec fields.
   - **Stub:** returns canned notes for free_flight / intercept (Channel Spitfire-relevant).
   - Soft-fail: research errors MUST NOT fail an otherwise successful Spec plan; brief can
     proceed from model knowledge + curated prompt hints.
   - Alternative considered: prompt-only (no tool) — rejected because the user explicitly
     wants real web-backed procedures/history when available.

7. **Prefs**
   - Document allowed values for `squadron_voice` in README/CLI help.
   - Soft validation / alias normalize; do not hard-reject unknown pref keys.

## Risks / Trade-offs

- [Overacting / caricature slang] → Restrained period register; examples are guidance.
- [Slang or web prose leaking into Spec JSON] → Spec-only final object + validate; brief is
  a separate field/turn.
- [Hallucinated tactics / unsafe advice] → Prompt: label uncertainty; prefer researched
  snippets; keep advice high-level (not a substitute for real flight training).
- [Web flakiness / cost] → Soft-fail research; stub offline; optional skip flag if needed.
- [Scope creep into `#16`] → Brief is CLI/agent output only; no `l10n` write in this change.

## Migration Plan

1. Add `voice.py` + compose/resolve; extend prompt with ops-brief rules.
2. Add `research_guidance` tool + stub fixtures; wire tool bridge.
3. Planner: resolve voice, post-success brief turn, attach `PlanResult.brief`; CLI `--voice`
   + print brief.
4. Tests: packs, research stub, brief sections for free_flight/intercept; Spec still validates.
5. Docs + backlog `#11` at finish.

## Open Questions

- Mid-loop clarifying questions in voice — **yes when the model writes prose**; no forced
  interactive Q&A UI in this change.
- Sharing pack/brief shape with `briefing-generation` — **reuse voice ids and section
  headings** later when writing `l10n`.
- Exact web search backend (DuckDuckGo/Bing/Serp API/httpx scrape) — **resolve at apply**;
  keep behind a small adapter so CI never hits the network.
