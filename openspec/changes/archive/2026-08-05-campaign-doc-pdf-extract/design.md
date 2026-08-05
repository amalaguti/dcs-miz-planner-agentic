## Context

Campaign Docs are local PDFs that rarely change. Re-parsing on every agent turn is waste.

## Goals / Non-Goals

**Goals:** Opt-in excerpts; SQLite cache by path+mtime_ns+size; caps; hermetic tests.

**Non-Goals:** OCR; default-on extract; Spec import from campaigns.

## Decisions

1. **`include_doc_text=False` by default** — listing stays filename-only and fast.
2. **Cache in inventory DB** (`campaign_doc_cache` table via `DocTextCache`).
3. **`pypdf`** for extract; skip files over 2 MiB; max 8 pages; excerpt ≤ 2000 chars;
   max 4 docs enriched per campaign.
4. **Tool returns** `docs` as list of `{filename, excerpt?}` when extract on; filenames
   strings remain OK when extract off (or unify to objects always — prefer objects with
   optional excerpt for stable shape: always `{filename, excerpt: null|str}`).

## Risks / Trade-offs

- [Breaking docs shape] → Prefer always `[{filename, excerpt}]` with excerpt null when
  not requested — cleaner for agent; update tests once.
- [Corrupt PDF] → Soft-fail that file; others continue.
