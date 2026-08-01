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
)
from ..models import MissionSpec
from ..validation import validate_mission_spec
from .llm import LLMClient, LLMResponse, default_tools
from .prompts import compose_system_prompt
from .realism import channel_date_realism_warnings
from .tool_bridge import dispatch_tool
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


def _extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    fence = _JSON_FENCE.search(text)
    if fence:
        text = fence.group(1).strip()
    return json.loads(text)


def _assistant_message(resp: LLMResponse) -> dict[str, Any]:
    msg: dict[str, Any] = {"role": "assistant", "content": resp.content}
    if resp.tool_calls:
        msg["tool_calls"] = [
            {
                "id": tc.id,
                "type": "function",
                "function": {"name": tc.name, "arguments": tc.arguments},
            }
            for tc in resp.tool_calls
        ]
    return msg


def _write_spec_yaml(spec: MissionSpec, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = spec.model_dump(mode="json")
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def _record_plan(
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


def _load_prefs(db_path: Path | str | None) -> dict[str, Any]:
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
) -> PlanResult:
    """Run the tool-using planner and write a validated Mission Spec YAML."""
    out = Path(output_path)
    prefs = _load_prefs(db_path)
    resolved_voice = resolve_voice(cli_voice=voice, prefs=prefs)
    system_prompt = compose_system_prompt(resolved_voice)
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    tools = default_tools()
    repair_used = False
    last_parse_error: str | None = None

    for _ in range(max_turns):
        resp = llm.complete(messages, tools=tools)
        messages.append(_assistant_message(resp))

        if resp.tool_calls:
            for tc in resp.tool_calls:
                result = dispatch_tool(tc.name, tc.arguments, db_path=db_path)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": json.dumps(result),
                    }
                )
            continue

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
            raw = _extract_json_object(resp.content)
            spec = MissionSpec.model_validate(raw)
        except (json.JSONDecodeError, ValueError) as exc:
            last_parse_error = str(exc)
            messages.append(
                {
                    "role": "user",
                    "content": (
                        f"Could not parse Mission Spec JSON: {exc}. Reply with corrected JSON only."
                    ),
                }
            )
            continue

        vresult = validate_mission_spec(spec, inventory=inventory)
        if vresult.ok:
            _write_spec_yaml(spec, out)
            compiled: Path | None = None
            if compile_output:
                dest = Path(miz_path) if miz_path else out.with_suffix(".miz")
                try:
                    compiled = PyDCSCompiler(inventory=inventory).compile(spec, dest)
                except ValueError as exc:
                    gid = _record_plan(
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
            gid = _record_plan(
                db_path=db_path,
                prompt=prompt,
                outcome=OUTCOME_SUCCESS,
                spec=spec,
                spec_path=out,
                miz_path=compiled,
                detail={
                    "aircraft": spec.player.aircraft,
                    "airfield": spec.player.airfield,
                    "voice": resolved_voice,
                },
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
            gid = _record_plan(
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
                "content": (
                    "Validation failed:\n"
                    + json.dumps(list(errors), indent=2)
                    + "\nReply with corrected Mission Spec JSON only."
                ),
            }
        )

    gid = _record_plan(
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
