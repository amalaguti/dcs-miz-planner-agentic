## Why

The planner still speaks like a generic assistant. Pilots expect a squadron commander —
period jargon, calm authority, the right RAF or USAAF flavour, and real operational
guidance (tactics, procedures, what to watch for) grounded in the mission type and plan.
Prefs already store `squadron_voice`; ship the persona and commander brief now so live
planning (and later `.miz` briefings) share one voice contract.

## What Changes

- Add configurable squadron-commander persona packs (**RAF**, **USAAF**, plus a **neutral**
  off-switch) with period-appropriate jargon and slang guidance.
- Compose the NL agent system prompt from base planning rules + the selected voice pack.
- Resolve voice from CLI override → stored `squadron_voice` pref → Channel-sensible default
  (`raf`).
- After a successful validated Spec, produce a **commander brief** covering sortie summary,
  **tactics** for the mission type/plan, **procedure** recommendations, and **watch-outs**
  for successful execution — in the selected voice.
- Live planning MAY **research** flight procedures, combat manoeuvres, pilot accounts, and
  historical context (web-backed tool when available); stub/CI uses canned notes offline.
- Keep Mission Spec JSON/YAML fields plain and machine-oriented; voice and brief apply to
  agent guidance and CLI output — not to Spec keys. Research MUST NOT invent DCS ids or
  override catalog/validate.

## Non-goals

- Writing briefing text into `.miz` `l10n` dictionaries (`briefing-generation`).
- TTS / VO audio, radio scripts, or in-mission trigger messages (`mission-events-narrative`).
- New mission types, theatres, or compiler behaviour.
- Training an ML style model; packs are curated prompt text.
- Changing the rule that the LLM never authors DCS Lua.
- Treating web pages as a second Spec/registry source of truth.

## Capabilities

### New Capabilities
- `squadron-voice`: Selectable commander persona packs (RAF/USAAF/neutral), prompt
  composition, jargon guidance, and operational commander briefs (tactics / procedures /
  watch-outs), with optional research for live guidance.

### Modified Capabilities
- `nl-agent`: Planning loop MUST apply the selected squadron voice to the system prompt
  and MUST surface a commander brief after a successful plan; live mode MAY expose a
  research tool for tactics/procedures/history.
- `user-memory`: Document allowed `squadron_voice` preference values and default resolution.

## Impact

- `agent/voice.py` + `prompts.py`: packs, resolve/compose, brief section guidance.
- Optional research tool on the agent tool surface (live web; stub fixtures).
- `agent/planner.py` / CLI `plan`: resolve voice, compose prompt, print commander brief.
- Prefs seed key `squadron_voice` already exists — wire selection and docs/tests.
- Acceptance: stub/live plan with `--voice raf|usaaf` yields commander-toned prompt + brief
  with tactics/procedures/watch-outs; Spec still validates. Opening a compiled `.miz` in DCS
  is unchanged (voice/brief are agent-side).
