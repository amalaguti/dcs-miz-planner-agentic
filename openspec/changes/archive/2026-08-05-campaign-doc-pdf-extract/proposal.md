## Why

`#31` honesty: Doc entries are filenames only, so the agent cannot use real campaign
briefing themes. User wants optional PDF text extract for inspiration, with caching so
rarely changing campaign Docs are not re-parsed on every tool call (adversarial D2 / `#40`).

## What Changes

- Opt-in `include_doc_text` on `list_installed_campaigns` (default false = filenames only).
- When enabled, extract short text excerpts from local `Doc/*.pdf` with size/page/char caps.
- Persist excerpts in SQLite (same inventory DB area) keyed by absolute path + mtime + size;
  cache hits MUST NOT re-read the PDF.
- Soft-fail per file on unreadable PDFs; never import `.miz` as Spec.
- Update agent-tools / prompts; hermetic tests with real tiny PDFs + cache-hit proof.

## Non-goals

- OCR for scanned PDFs; full-document return; network PDF fetch.
- Default-on extract on every campaign list (opt-in keeps listing cheap).
- Closing as wontfix.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `agent-tools`: Opt-in Doc PDF excerpt extract with mtime/size cache.
- `golden-fixtures` (or agent-tools only): hermetic campaign Doc extract coverage if
  already required there — prefer agent-tools + existing campaign tests.

## Impact

- `pypdf` dependency; `install/doc_extract.py` (+ cache); campaigns/tool/bridge/prompts;
  docs/BACKLOG `#40`.
