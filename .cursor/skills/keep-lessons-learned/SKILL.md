---
name: keep-lessons-learned
description: >-
  Maintain docs/LESSONS_LEARNED.md (index), docs/lessons/*.md topic files, and
  matching dcs-dev-* skills so PyDCS/DCS/compiler pitfalls are not repeated. Use
  when starting compiler or PyDCS work, debugging DCS/.miz/payload/weather/
  airfield/trigger/failures issues, finishing an OpenSpec apply slice, or after
  fixing a non-obvious bug or wrong assumption.
---

# Keep Lessons Learned

## Layout

| Path | Role |
|------|------|
| [`docs/LESSONS_LEARNED.md`](../../../docs/LESSONS_LEARNED.md) | **Index** — how to use + newest-first table of links |
| [`docs/lessons/*.md`](../../../docs/lessons/) | **Full entries** by topic (newest first within file) |
| `.cursor/skills/dcs-dev-*/SKILL.md` | **Procedures** distilled from topic clusters |

Durable product contracts stay in OpenSpec specs — not here.

## When to read

**Do not** read the whole index end-to-end. Pick the topic / skill:

| Work | Topic file | Skill |
|------|------------|-------|
| Triggers, failures, ME behaviour, fog scripts | `triggers-me` | `dcs-dev-triggers-me` |
| `player.flight` / wingman / Follow | `player-flight` | `dcs-dev-player-flight` |
| Weather presets, invent, fog_dynamics | `weather` | `dcs-dev-weather` |
| Aircraft/country/airfield/radio ids | `channel-ids` | `dcs-dev-channel-ids` |
| Compiler, payloads, goldens, theatre zip | `pydcs-compile` | `dcs-dev-pydcs-compile` |
| Agent, catalog, memory, research | `agent-tooling` | `dcs-dev-agent-tooling` |
| CI, inventory cache, OpenSpec process | `ci-process` | `dcs-dev-ci-process` |

Skim matching entries first; do not rediscover known KeyErrors / enum mistakes.

## When to write (always both log + skill check)

Append when **any** of these happen:

- A non-obvious bug is fixed (especially third-party / PyDCS / DCS install)
- An assumption about DCS ids or `.miz` layout was wrong
- A workaround must be preserved
- Acceptance testing reveals a durable tweak

**Do not** log routine typos, lint noise, or OpenSpec checkbox edits.

### Write steps (required order)

1. **Topic file** — prepend a full entry at the top of the matching
   `docs/lessons/<topic>.md` (below the header/`---`), newest first.
2. **Index** — add one row at the top of the Index table in
   `docs/LESSONS_LEARNED.md` (date | linked title | topic).
3. **Skill** — if the pitfall changes a **procedure** agents must follow, update
   the matching `dcs-dev-*` skill Hard rules (keep skills short; link to the
   topic file for narrative). If a new cluster appears (3+ related entries with
   no skill), propose a new `dcs-dev-*` skill rather than bloating the index.

## Entry format (topic files)

```markdown
## Short title (YYYY-MM-DD)

- **Date:** YYYY-MM-DD
- **Symptom:** …
- **Cause:** …
- **Fix:** …
- **Code / notes:** …
```

Or a short **Lesson:** bullet when there is no bug narrative.

## Related

- README stays brief (`keep-readme-updated`) — link the index, not every lesson
- Research samples stay gitignored `research/`; promote durable facts into
  topic files / registry / OpenSpec
- Creativity regressions: `eval-agent-creativity` → append here when durable
