## Why

Local QAG discovery HTML under gitignored `research/DCS *` is useful mission-design colour (era, generator types, class taxonomies, Assets Pack flags) but `research_guidance` still only serves a few canned Channel/Spitfire notes. Offline invent therefore cannot read those pages, and we must not scrape them into catalog YAML or ship the dump.

## What Changes

- Keep a thin packaged **index** of the QAG pages (paths, keywords, Spec-type mapping, skip-duplicate). The HTML stays in gitignored `research/` and is read at runtime when present.
- Rank/filter by query, Spec `mission_type`, optional theatre/era hints, and `focus=mission_design`.
- Keep QAG UI names, site templates, and `template.lua` strings as untrusted colour — never Spec/PyDCS/catalog authority.
- Skip the Cold War Anti-Ship HTML that is a copy of the WWII anti-ship page.
- When `research/` is absent (CI, installed wheel), QAG notes are empty; canned Channel fixtures remain.
- Tests + README/ARCHITECTURE/lessons so agents know this is local research, not packaged content.

## Non-goals

- No catalog YAML / strike-class / aircraft-shelf promote from QAG names (`#8e` still required).
- No new Spec `mission_type`s (Dogfight, Anti-Ship SR, SEAD SR, Bomber Escort).
- No Cold War Spec era; QAG 1947–1970 is colour only.
- No live-web or research-provider changes; no ME Instant Action gate.
- Do not copy `research/` HTML into the package or git.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `agent-tools`: offline `research_guidance` MUST include notes from indexed local QAG HTML when that dump is present (not canned Channel notes alone) and MUST keep `fixture:` sources plus the existing untrusted / not-id-authority contract. Missing dump MUST NOT fail the tool.
- `nl-agent`: invent prompts MUST treat QAG research notes as mission-design colour only (QAG labels ≠ Spec ids; no SEAD/anti-ship Spec types).

## Impact

- `tools/research.py`, `tools/qag_fixtures.py`, thin `data/qag_fixtures/qag_index.yaml`, `agent/prompts.py`, pytest; README / ARCHITECTURE / `docs/THEATRE_TARGET_PROMOTE.md` / agent-tooling lesson.
- No compiler, registry unit ids, or catalog sync changes. `research/` stays gitignored.
