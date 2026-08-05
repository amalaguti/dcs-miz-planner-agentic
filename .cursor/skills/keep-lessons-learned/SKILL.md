---
name: keep-lessons-learned
description: Maintain and consult docs/LESSONS_LEARNED.md so known PyDCS/DCS/compiler pitfalls are not repeated. Use when starting compiler or PyDCS work, debugging DCS/.miz/payload/weather/airfield issues, finishing an OpenSpec apply slice, or after fixing a non-obvious bug or wrong assumption.
---

# Keep Lessons Learned

Canonical file: `docs/LESSONS_LEARNED.md` (repo root)

## When to read

**Before** working on any of:

- PyDCS, `.miz` compile/save, payloads, weather, parking/start types
- DCS type ids, theatres, `airdromeId`, Channel airfields
- Compiler interface or Mission Spec ↔ backend mapping

Skim matching entries first; do not rediscover known KeyErrors / enum mistakes.

## When to write

Append (or update) an entry when **any** of these happen:

- A non-obvious bug is fixed (especially third-party / PyDCS / DCS install interaction)
- An assumption about DCS ids or `.miz` layout was wrong
- A workaround is added that future agents must preserve
- Acceptance testing reveals a tweak that should not be forgotten

Do **not** log routine typos, lint noise, or OpenSpec checkbox edits.

## Entry rules

- Newest entries near the **top** of the lesson list
- Use the existing format: title, date, symptom → cause → fix, code touchpoint
- Keep entries short and actionable
- This file is agent memory, not the product contract — durable requirements stay in OpenSpec specs

## Related

- README stays brief (`keep-readme-updated`); do not dump lessons into README — link if needed
- Research samples stay in gitignored `research/`; promote durable facts here or into the registry/specs
- Live agent creativity regressions: skill `eval-agent-creativity` (vague-ask suite → LESSONS /
  OpenSpec). Append agent-behaviour pitfalls found there when they are durable.
