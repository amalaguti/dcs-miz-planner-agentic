## Context

`research_guidance` / chat `/research` already soft-fail to offline fixtures. Live mode
calls DuckDuckGo Instant Answer (`api.duckduckgo.com`) with a short timeout. Instant Answer
often returns empty JSON for multi-word aviation/history queries, so `gather_research_notes`
hits “no snippets” and returns fixtures with a warning that is easy to miss. Chat still
prints fixture titles/snippets that look like a successful live lookup. `theatre` /
`aircraft` are currently discarded and never enrich the query.

Stakeholders: interactive chat pilots and the NL agent brief path. Constraints: no paid
search keys; CI stays mocked/offline; research never becomes Spec/DCS-id authority; prefer
stdlib over new heavy deps.

## Goals / Non-Goals

**Goals:**

- When live is requested and the network works, return at least one query-relevant
  web-sourced note for typical Channel/Spitfire-style queries.
- When live is requested and fails or is empty, make the soft-fail unmistakable (structured
  warning + chat copy that labels fixtures as offline fallback).
- Use mission context (`mission_type` / `theatre` / `aircraft`) to enrich the fetch query.
- Pytest: injectable fetch covers success, empty, and exception without real network.

**Non-Goals:**

- Guaranteed coverage for every possible query or provider SLA.
- Paid APIs, API keys for research, or browser automation.
- Changing Spec/compile, voice packs, or default verbose behaviour.
- Treating web content as registry/Spec truth.

## Decisions

1. **Provider cascade (stdlib only)**
   - **First:** keep DuckDuckGo Instant Answer (cheap structured JSON).
   - **If empty:** fetch DuckDuckGo HTML results (`html.duckduckgo.com/html/?q=…`) and parse
     the first few result titles + snippets with `html.parser` (or equivalent stdlib).
   - **Alternatives considered:** Wikipedia-only (narrow); paid SerpAPI (keys/cost); keep
     Instant Answer alone (proven insufficient). Cascade preserves Instant Answer when it
     hits and adds a broader free path when it does not.

2. **Query enrichment**
   Append non-empty `mission_type`, `theatre`, and `aircraft` (and light WWII/Channel
   grounding tokens when helpful) to the live fetch string. Do not invent DCS ids beyond
   values already on the Spec/tool args.

3. **Timeouts**
   Raise default live timeout into a modest range (~8s total budget or per-step) so HTML
   fetch is usable on slow links; keep injectable for tests. Soft-fail on timeout.

4. **Failure UX contract**
   - Tool: always set `warning` when live was requested and live notes are empty or an
     exception occurred; include a short reason (empty Instant Answer + empty HTML, timeout,
     HTTP error).
   - Notes on soft-fail: still return fixtures (offline usefulness) but chat `/research`
     MUST label the block as live-unavailable / offline fixtures (not as unmarked
     “Research for: …”).
   - On live success: prefer live notes; MAY keep at most one fixture for Channel grounding;
     sources MUST remain distinguishable (`fixture:…` vs URL / `duckduckgo:…`).

5. **No new product dependencies**
   Stay on `urllib` + stdlib HTML parsing. If HTML layout breaks later, soft-fail with a clear
   warning and fixtures — same contract.

6. **Testing**
   Prefer injecting `web_fetch` / per-stage fakes over live network in pytest. One optional
   manual acceptance note for networked `/research Manston spitfire` (not CI-gated).

## Risks / Trade-offs

- **[Risk] DDG HTML markup changes** → Mitigation: defensive parse; empty → soft-fail warning;
  fixtures remain. Document pitfall in LESSONS if needed.
- **[Risk] Rate limits / bot blocks** → Mitigation: polite User-Agent; short result count;
  soft-fail; do not retry aggressively.
- **[Risk] Irrelevant snippets** → Mitigation: query enrichment; cap notes; research remains
  advisory only in prompts/help text.
- **[Trade-off] HTML scrape vs Instant Answer purity** → Accept scrape fragility for usable
  live results without paid APIs.

## Migration Plan

- Behavioural change only; no DB/schema migration.
- Roll forward with pytest green; README note that live research uses DDG Instant Answer then
  HTML fallback; mark BACKLOG `#10d` building→done on acceptance.
- Rollback: revert change branch; fixtures/offline path unchanged in spirit.

## Open Questions

- None blocking: HTML cascade vs Wikipedia secondary is decided (HTML). Revisit only if
  DDG HTML is consistently blocked in acceptance testing — then consider Wikimedia as a
  second free backend in a follow-up.
