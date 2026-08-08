## Why

`#15g` gave targets motion and land Disperse Under Fire, but convoys, AAA, and
ships still cannot express ROE, Alarm State, On Road, or other ME WP options the
pilot expects. R12 ME smoke showed options differ by domain **and** unit class
(soft truck ≠ Flak ≠ U-boat), so the planner needs a curated Spec shelf—not a
dump of every ME row.

## What Changes

- Optional per-target **AI / move knobs** on GA + recon `targets[]` (allowlisted
  ids only), filtered by land vs sea and soft vs AAA heuristics from R12.
- Compiler emits PyDCS `Opt*` on WP0 and optional `PointAction` (On/Off Road,
  Rank/Cone/Vee…) for land route legs; sea gets ROE + Alarm (+ optional engage
  air / interception range). Keep `#15g` disperse behaviour.
- Named presets optional (`convoy_transit`, `aaa_alert`, `ship_under_way`, …)
  that expand to allowlisted fields.
- Validation rejects unknown ids and class/domain mismatches (e.g. disperse on
  ships; interception range on soft trucks if we choose to forbid).
- Planning options + agent/schema notes; light brief language when presets/ai set.
- Examples: convoy with transit preset / On Road or Alarm Green; AAA alert;
  U-boat with sea ROE/Alarm. ME accept.

## Capabilities

### New Capabilities

- *(none — extends target placement / motion)*

### Modified Capabilities

- `mission-spec`: optional `targets[].ai` / presets + move_formation fields.
- `mission-validation`: allowlist + domain/class rules.
- `miz-compiler`: emit Opt* + PointAction for targets.
- `golden-fixtures`: convoy / AAA / U-boat AI option asserts.
- `mission-options` / `nl-agent` / `agent-tools` / `squadron-voice` (light):
  discoverability and brief cues.

## Impact

- `models.py`, `validation.py`, `target_motion.py` / compiler placement,
  `planning_options.yaml`, prompts/schema/voice, examples, tests, BACKLOG `#15h`.
- Builds on R12 (`research/ai-options-domain.md`); broader unit matrix is **R12b**.

## Non-goals

- Air/helicopter Option shelves for player or AI flights (separate later).
- Dumping full ME lists (Spit ECM lesson — UI ≠ capability).
- PyDCS-missing Opt* wrappers for AAA alt / formation interval / ARM (defer
  unless thin raw emit is cheap and tested).
- Lua AI; Mist/MOOSE; inventing DCS option ids.
- Completing R12b (helo/armor/more ships) before ship.

## Acceptance

ME on Channel: convoy WP shows chosen Alarm/ROE/Action; Flak shows alert-style
options when set; U-boat shows ROE/Alarm (and optional engage/intercept);
unchanged Specs behave as today.
