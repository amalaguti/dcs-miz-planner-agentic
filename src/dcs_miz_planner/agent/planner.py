"""NL → Mission Spec planner loop."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ..compiler import PyDCSCompiler
from ..install.models import TheatreInventory
from ..memory import (
    OUTCOME_COMPILE_FAILED,
    OUTCOME_FAILED,
    OUTCOME_SUCCESS,
    OUTCOME_VALIDATION_FAILED,
    UserMemoryService,
    detail_with_inferred_creative,
    format_creative_bias_fragment,
    load_creative_bias,
)
from ..models import MissionSpec
from ..validation import validate_mission_spec
from .immersion import host_harbour_unit_nudge, host_immersion_repair_nudge
from .llm import LLMClient, default_tools
from .path_clamp import try_clamp_land_paths_if_needed
from .prompts import compose_system_prompt, host_spec_repair_nudge
from .realism import channel_date_realism_warnings
from .turn import complete_with_tools
from .verbose import DEFAULT_VERBOSE, vlog
from .voice import build_commander_brief, resolve_voice

_JSON_FENCE = re.compile(r"```(?:json)?\s*([\s\S]*?)```", re.IGNORECASE)


@dataclass(frozen=True)
class PlanResult:
    ok: bool
    spec_path: Path | None = None
    miz_path: Path | None = None
    error: str | None = None
    validation_errors: tuple[dict[str, Any], ...] = ()
    spec: MissionSpec | None = None
    warnings: tuple[str, ...] = ()
    generation_id: int | None = None
    voice: str | None = None
    system_prompt: str | None = None
    brief: str | None = None


def extract_json_object(text: str) -> dict[str, Any]:
    """Parse a JSON object from text (whole string, fenced block, or first {...})."""
    text = text.strip()
    fence = _JSON_FENCE.search(text)
    if fence:
        text = fence.group(1).strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            raise
        data = json.loads(text[start : end + 1])
    if not isinstance(data, dict):
        raise TypeError("Mission Spec JSON must be an object")
    return data


def try_parse_mission_spec(text: str | None) -> MissionSpec | None:
    """Best-effort Spec parse from assistant text; None if not Spec JSON."""
    spec, _err = diagnose_mission_spec_parse(text)
    return spec


def diagnose_mission_spec_parse(text: str | None) -> tuple[MissionSpec | None, str | None]:
    """
    Try to parse a Mission Spec from assistant text.

    Returns ``(spec, None)`` on success, ``(None, None)`` if no JSON object looks present,
    or ``(None, error)`` if JSON was found but invalid as a Mission Spec.
    """
    if not text or not text.strip():
        return None, None
    stripped = text.strip()
    looks_like_json = (
        stripped.startswith("{")
        or "```" in stripped
        or ("{" in stripped and "}" in stripped and "schema_version" in stripped)
        or ("{" in stripped and "}" in stripped and "mission_type" in stripped)
    )
    if not looks_like_json:
        return None, None
    try:
        raw = extract_json_object(text)
        return MissionSpec.model_validate(raw), None
    except (json.JSONDecodeError, ValueError) as exc:
        return None, str(exc)


def write_spec_yaml(spec: MissionSpec, path: Path) -> None:
    from ..weather_invent import ensure_weather_seed

    path.parent.mkdir(parents=True, exist_ok=True)
    # Persist invent seed when omitted so sidecar compiles reproduce.
    if spec.weather_opts is None:
        spec = ensure_weather_seed(spec, draw=True)
    data = spec.model_dump(mode="json")
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def record_plan(
    *,
    db_path: Path | str | None,
    prompt: str,
    outcome: str,
    spec: MissionSpec | None = None,
    spec_path: Path | None = None,
    miz_path: Path | None = None,
    detail: dict[str, Any] | None = None,
) -> int | None:
    try:
        return UserMemoryService(db_path=db_path).record_generation(
            outcome=outcome,
            prompt=prompt,
            mission_type=spec.mission_type.value if spec is not None else None,
            theatre=spec.theatre if spec is not None else None,
            spec_path=str(spec_path) if spec_path is not None else None,
            miz_path=str(miz_path) if miz_path is not None else None,
            detail=detail,
        )
    except OSError:
        return None


def load_prefs(db_path: Path | str | None) -> dict[str, Any]:
    try:
        return UserMemoryService(db_path=db_path).get_prefs()
    except OSError:
        return {}


def plan_mission(
    prompt: str,
    output_path: str | Path,
    *,
    llm: LLMClient,
    compile_output: bool = False,
    miz_path: str | Path | None = None,
    inventory: TheatreInventory | None = None,
    db_path: Path | str | None = None,
    voice: str | None = None,
    max_turns: int = 8,
    verbose: bool = DEFAULT_VERBOSE,
) -> PlanResult:
    """Run the tool-using planner and write a validated Mission Spec YAML."""
    out = Path(output_path)
    prefs = load_prefs(db_path)
    resolved_voice = resolve_voice(cli_voice=voice, prefs=prefs)
    bias = load_creative_bias(db_path=db_path)
    system_prompt = compose_system_prompt(
        resolved_voice,
        mode="oneshot",
        creative_bias_fragment=format_creative_bias_fragment(bias),
    )
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    tools = default_tools()
    repair_used = False
    immersion_repair_used = False
    last_parse_error: str | None = None
    outer_rounds = max(1, max_turns)
    vlog(verbose, f"[verbose] plan_mission start voice={resolved_voice}")

    for _ in range(outer_rounds):
        resp = complete_with_tools(
            llm,
            messages,
            tools=tools,
            db_path=db_path,
            max_rounds=max_turns,
            verbose=verbose,
        )

        if not resp.content or not resp.content.strip():
            last_parse_error = "Model returned empty content without tool calls"
            messages.append(
                {
                    "role": "user",
                    "content": "Respond with Mission Spec JSON only, or call a tool.",
                }
            )
            continue

        try:
            raw = extract_json_object(resp.content)
            spec = MissionSpec.model_validate(raw)
        except (json.JSONDecodeError, ValueError, TypeError) as exc:
            last_parse_error = str(exc)
            messages.append(
                {
                    "role": "user",
                    "content": host_spec_repair_nudge(str(exc), rejected_text=resp.content),
                }
            )
            continue

        vresult = validate_mission_spec(spec, inventory=inventory)
        if not vresult.ok:
            clamped = try_clamp_land_paths_if_needed(spec, list(vresult.errors))
            if clamped is not None:
                v2 = validate_mission_spec(clamped, inventory=inventory)
                if v2.ok:
                    spec = clamped
                    vresult = v2
                    vlog(verbose, "[verbose] host clamped land path onto strike deltas")
        elif (clamped := try_clamp_land_paths_if_needed(spec)) is not None:
            v2 = validate_mission_spec(clamped, inventory=inventory)
            if v2.ok:
                spec = clamped
                vresult = v2
                vlog(verbose, "[verbose] host clamped divergent land path onto strike deltas")
        if vresult.ok:
            if not immersion_repair_used:
                harbour_nudge = host_harbour_unit_nudge(prompt, spec)
                if harbour_nudge:
                    immersion_repair_used = True
                    messages.append({"role": "user", "content": harbour_nudge})
                    continue
                nudge = host_immersion_repair_nudge(prompt, spec)
                if nudge:
                    immersion_repair_used = True
                    messages.append({"role": "user", "content": nudge})
                    continue
            write_spec_yaml(spec, out)
            compiled: Path | None = None
            if compile_output:
                dest = Path(miz_path) if miz_path else out.with_suffix(".miz")
                try:
                    compiled = PyDCSCompiler(inventory=inventory).compile(spec, dest)
                except ValueError as exc:
                    gid = record_plan(
                        db_path=db_path,
                        prompt=prompt,
                        outcome=OUTCOME_COMPILE_FAILED,
                        spec=spec,
                        spec_path=out,
                        detail={"error": str(exc)},
                    )
                    return PlanResult(
                        ok=False,
                        spec_path=out,
                        error=str(exc),
                        spec=spec,
                        generation_id=gid,
                        voice=resolved_voice,
                        system_prompt=system_prompt,
                    )
            brief = build_commander_brief(spec, resolved_voice)
            gid = record_plan(
                db_path=db_path,
                prompt=prompt,
                outcome=OUTCOME_SUCCESS,
                spec=spec,
                spec_path=out,
                miz_path=compiled,
                detail=detail_with_inferred_creative(
                    {
                        "aircraft": spec.player.aircraft,
                        "airfield": spec.player.airfield,
                        "voice": resolved_voice,
                    },
                    spec,
                ),
            )
            return PlanResult(
                ok=True,
                spec_path=out,
                miz_path=compiled,
                spec=spec,
                warnings=channel_date_realism_warnings(spec),
                generation_id=gid,
                voice=resolved_voice,
                system_prompt=system_prompt,
                brief=brief,
            )

        errors = tuple(
            {
                "code": e.code,
                "path": e.path,
                "message": e.message,
                "hint": e.hint,
            }
            for e in vresult.errors
        )
        if repair_used:
            gid = record_plan(
                db_path=db_path,
                prompt=prompt,
                outcome=OUTCOME_VALIDATION_FAILED,
                spec=spec,
                detail={"errors": list(errors)},
            )
            return PlanResult(
                ok=False,
                error="Mission Spec failed validation after repair attempt",
                validation_errors=errors,
                spec=spec,
                generation_id=gid,
                voice=resolved_voice,
                system_prompt=system_prompt,
            )
        repair_used = True
        messages.append(
            {
                "role": "user",
                "content": host_spec_repair_nudge(
                    "Validation failed:\n" + json.dumps(list(errors), indent=2),
                    mission_type=spec.mission_type.value,
                ),
            }
        )

    gid = record_plan(
        db_path=db_path,
        prompt=prompt,
        outcome=OUTCOME_FAILED,
        detail={"error": last_parse_error or f"Planner exceeded max_turns={max_turns}"},
    )
    return PlanResult(
        ok=False,
        error=last_parse_error or f"Planner exceeded max_turns={max_turns}",
        generation_id=gid,
        voice=resolved_voice,
        system_prompt=system_prompt,
    )
