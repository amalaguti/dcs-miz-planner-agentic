## 1. Live retrieval cascade

- [x] 1.1 Enrich live query with `mission_type` / `theatre` / `aircraft` (stop discarding context)
- [x] 1.2 Keep DuckDuckGo Instant Answer as first attempt; increase usable timeout budget
- [x] 1.3 Add stdlib HTML results fallback (`html.duckduckgo.com`) when Instant Answer is empty
- [x] 1.4 Merge policy: live notes preferred; at most one fixture on success; fixtures + clear warning on empty/error

## 2. Chat / tool UX

- [x] 2.1 Ensure `research_guidance` always sets a live-unavailable `warning` on empty/error when live was requested
- [x] 2.2 Update `/research` output to label offline fixture fallback when a live warning is present
- [x] 2.3 Keep session injection advisory-only (not Spec authority)

## 3. Tests

- [x] 3.1 Pytest: live success via injectable fetch → non-fixture sources, no unavailable warning
- [x] 3.2 Pytest: live empty → fixtures + warning
- [x] 3.3 Pytest: live exception → fixtures + failure warning
- [x] 3.4 Pytest: `/research` output includes warning/offline label when live soft-fails

## 4. Docs / backlog

- [x] 4.1 Update README research/`/research` notes for Instant Answer + HTML fallback and clearer soft-fail
- [x] 4.2 Mark BACKLOG `#10d` `fix-chat-research-live` building→done when accepted; LESSONS only if a non-obvious provider pitfall is found
- [x] 4.3 Manual smoke (optional): networked `/research Manston spitfire` returns live-sourced notes or a clear live-failure message
