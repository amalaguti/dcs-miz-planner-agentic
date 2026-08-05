## Context

M6 added rich native Spec behaviours. Envelope knobs are catalogued; behaviour vocab is
mostly schema footnotes. Users want creative-but-assertive missions and already point at
inspiration: stock audits (R5), user missions/campaigns (R1–R2), ME docs (R9), and the
existing `research_guidance` live web path (DuckDuckGo Instant Answer + HTML).

Live research today is generic tactics/history. It is not steered toward **how others
built DCS missions** (User Files filters, GitHub mission repos, forum/ME writeups). The
local install also already holds rich Spitfire campaigns under `Mods/campaigns` (e.g.
Beware! Beware!, Fight or Die, Epsom, The Big Show on a typical Channel install)—today
unused by the agent. Install root discovery already exists for theatres; campaign
indexing is the missing local inspiration channel.

## Goals / Non-Goals

**Goals:**

- Packaged `mission_behaviour` + `mission_inspiration` cards.
- Live `research_guidance` enrichment for mission-design / DCS-file / repo style queries.
- Local read-only index of installed campaigns/missions under the discovered DCS root
  (`Mods/campaigns`, primarily).
- Prompt loop: vague ask → cards + optional live notes and/or local campaign list → 1–2
  supported Spec behaviours.
- Document promote path for deeper R1/R2 / campaign `.miz` audits (later).

**Non-Goals:**

- Full unzip/parse of every campaign `.miz` into Spec in this change; auto-Spec from
  community or campaign binaries.
- Guaranteed scrape quality from digitalcombatsimulator.com (best-effort).

## Decisions

1. **Two packaged families** (unchanged intent): `mission_behaviour` (supported recipes)
   and `mission_inspiration` (advisory ideas → behaviour ids). YAML → catalog →
   `list_mission_options`.

2. **Live web is the third inspiration channel**, implemented by extending
   `research_guidance` rather than a separate downloader:
   - When the query (or an explicit focus) is about inventing/designing a mission,
     `enrich_live_query` (or equivalent) MUST bias the fetch string toward mission-design
     discovery—e.g. include terms / site hints such as DCS User Files Spitfire/Channel
     mission, “DCS World mission”, GitHub miz/mission, mission editor triggers—while
     keeping theatre/aircraft/mission_type context.
   - Results remain structured notes `{title, snippet, source}`; agent maps ideas onto
     `mission_behaviour` cards. Notes MUST NOT be treated as Spec field authority.
   - Soft-fail to fixtures when live empty/errors (existing contract).
   - Injectable `web_fetch` stays for hermetic tests.

3. **Optional `focus` (or query convention)** — Prefer a small explicit knob on
   `research_guidance` such as `focus: "mission_design" | "tactics"` (default tactics /
   current behaviour) so chat/plan can request mission-pattern search without overloading
   every brief. If a new parameter is awkward for the tool bridge, a documented query
   prefix / prompt instruction that always adds mission-design bias when inventing is
   acceptable for v1—design choice at apply time, prefer explicit `focus` if cheap.

4. **v1 behaviour + inspiration card sets** as previously scoped (gates, mark/smoke,
   narrative, radio/late-act, sound, group_life_less; 3–5 stock/R5-style inspiration
   cards).

5. **Assertive prompts:** list options → read inspiration + behaviour → optionally
   `research_guidance` (mission-design) and/or local campaign index when inventing →
   emit 1–2 supported behaviours; no Lua; respect hand-trigger / narrative conflicts.

6. **Local install campaign index (fourth inspiration channel):**
   - Reuse existing DCS World root discovery (`install/discover.py`).
   - Scan `Mods/campaigns/<CampaignName>/` for:
     - `*.cmp` — campaign **playlist** (Lua table: stage order, mission `.miz` filenames,
       optional campaign description / required units). Not the mission content itself.
     - `*.miz` names — mission list for that campaign.
     - `Doc/` — **primary narrative inspiration**: per-mission briefing PDFs, campaign
       intro, Form F, maps, checklists (observed on all Channel Spitfire campaigns:
       Beware!, Fight or Die, Epsom, The Big Show). List Doc filenames in the index;
       optionally expose a read helper that extracts text from a chosen Doc PDF when the
       agent wants a specific sortie brief (v1: list always; text extract if a light
       dependency is already available / cheap—otherwise filename + path is enough and
       human/agent can open the PDF offline).
   - Prefer `.cmp` + Doc listing over opening multi‑10MB `.miz` zips in v1.
   - Agent tool e.g. `list_installed_campaigns` → `{campaign, missions[], docs[],
     description?, path}` read-only. Hermetic tests use a tiny fake campaigns tree
     (no `S:\` in CI) that includes a sample `Doc/*.pdf` (or stub).
   - Agent maps Doc/campaign themes onto packaged behaviour cards; does not import
     `.miz` as Spec and does not treat Doc text as Spec field authority.

7. **R1/R2 remain the deep path:** human-audit `.miz` under `research/`, promote into
   `mission_inspiration` cards. Local index is listing/discovery (+ optional Doc text);
   Doc briefings are the local analog of R2 narrative patterns.

8. **No compiler / Spec predicate changes.**

## Risks / Trade-offs

- [Risk] DCS site / DDG blocks or returns noise → Mitigation: soft-fail fixtures;
  packaged inspiration cards remain primary offline creativity.
- [Risk] Live notes suggest Mist/MOOSE/Lua → Mitigation: prompts forbid LLM Lua; only
  emit packaged Spec types; validate catches junk.
- [Risk] Copyright / redistributing missions → Mitigation: web snippets/URLs only; local
  index returns paths on the user’s machine, no binaries in git.
- [Risk] Large `.miz` parse cost → Mitigation: v1 filename + `.cmp` + Doc list only.
- [Risk] Doc PDFs are large / image-heavy → Mitigation: index filenames first; optional
  text extract only on demand for a single chosen Doc; never bulk-ingest all PDFs.
- [Risk] Options + research noise overwhelm the model → Mitigation: small card sets;
  “pick 1–2 behaviours”; CLI family filters.

## Migration Plan

- Additive YAML + research enrichment + local index tool + prompts. Rollback: revert
  those layers.

## Open Questions

- Prefer explicit `focus=` on `research_guidance` vs prompt-only query bias (lean
  explicit at apply if tool schema change is small).
- Whether Saved Games `Missions/` should be scanned in the same tool v1 (`Mods/campaigns`
  is enough for Channel Spitfire).
- Follow-up: User Files HTML parser; light `.miz` trigger peek for promote.
