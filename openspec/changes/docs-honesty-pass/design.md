## Context

`list_installed_campaigns` returns campaign name, `.miz` filenames, `.cmp` short text when present, and `Doc/*.pdf` **filenames** only (`install/campaigns.py`). Prompts, tool descriptions, and README still say “briefing themes” / “Doc briefings,” and README Status lead still claims combat/trigger keys are reserved. Adversarial findings D1/D2; backlog `#31`.

## Goals / Non-Goals

**Goals:**

- Make README Status match shipped M4–M6 reality.
- Make every agent/user-facing campaign Doc claim match filename-only indexing.
- Keep OpenSpec `agent-tools` / `nl-agent` requirements honest so future `#40` is an explicit upgrade, not a silent fix.

**Non-Goals:**

- PDF extract (`#40`), `SPEC_SHAPE_REMINDER` empty-triggers fix (`#30c`), validation hardening (`#32`).
- Changing campaign indexer return shape (already filenames).
- Expanding MVP scope labels into new product work.

## Decisions

1. **Wording-only product change**
   Prefer string/doc edits over new APIs. Indexer already honest; copy was not.
   *Alternative:* ship `#40` first — rejected; honesty is cheaper and unblocks accurate `#30c` guidance.

2. **Allowed Doc phrasing**
   Use “Doc PDF filenames / titles” (or “Doc listing”). Forbid “themes,” “briefing text,” “prefer Doc briefings” as if content were read. Titles may be inferred from filenames only.
   *Alternative:* stop mentioning Doc entirely — rejected; filenames still useful inspiration signals.

3. **`SPEC_SHAPE_REMINDER` out of this change**
   Empty-triggers reminder stays for `#30c` even though it is also dishonest — splitting keeps `#31` reviewable as a docs/trust pass. Touch `spec_schema.py` only for Doc/campaign phrasing near the common notes if present.

4. **README Status rewrite pattern**
   Lead paragraph: what *is* true (Spec schema, combat types, native triggers, catalog, creative memory). Keep detailed accepted-in-game bullets. Drop “reserved for later” for combat/triggers. Brief “intentional limits” line (Channel MVP; campaign `.miz` not imported; stub/offline for hermetic tests) is OK.

5. **Tests**
   Update prompt/tool string assertions that lock “theme”/“briefing” wording. Campaign fixture tests already assert filenames — leave behaviour as-is.

## Risks / Trade-offs

- [Agents invent themes from filenames] → Acceptable; prompts say map onto packaged behaviours only.
- [Under-claiming Doc until `#40`] → Preferred over overclaim; `#40` or wontfix closes the gap.
- [Leaving empty-triggers reminder] → Document in tasks/LESSONS cross-link to `#30c` so honesty pass is not mistaken for complete prompt cleanup.

## Migration Plan

Single branch `docs-honesty-pass`; no data migration. Rollback = revert commit. No ME re-acceptance required.

## Open Questions

- None blocking; `#40` vs permanent filename-only remains a later challenge item.
