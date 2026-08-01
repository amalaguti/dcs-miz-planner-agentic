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
from ..models import MissionSpec
from ..validation import validate_mission_spec
from .llm import LLMClient, LLMResponse, default_tools
from .prompts import SYSTEM_PROMPT
from .tool_bridge import dispatch_tool

_JSON_FENCE = re.compile(r"```(?:json)?\s*([\s\S]*?)```", re.IGNORECASE)


@dataclass(frozen=True)
class PlanResult:
    ok: bool
    spec_path: Path | None = None
    miz_path: Path | None = None
    error: str | None = None
    validation_errors: tuple[dict[str, Any], ...] = ()
    spec: MissionSpec | None = None


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


def plan_mission(
    prompt: str,
    output_path: str | Path,
    *,
    llm: LLMClient,
    compile_output: bool = False,
    miz_path: str | Path | None = None,
    inventory: TheatreInventory | None = None,
    max_turns: int = 8,
) -> PlanResult:
    """Run the tool-using planner and write a validated Mission Spec YAML."""
    out = Path(output_path)
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
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
                result = dispatch_tool(tc.name, tc.arguments)
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
                compiled = PyDCSCompiler(inventory=inventory).compile(spec, dest)
            return PlanResult(
                ok=True,
                spec_path=out,
                miz_path=compiled,
                spec=spec,
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
            return PlanResult(
                ok=False,
                error="Mission Spec failed validation after repair attempt",
                validation_errors=errors,
                spec=spec,
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

    return PlanResult(
        ok=False,
        error=last_parse_error or f"Planner exceeded max_turns={max_turns}",
    )
