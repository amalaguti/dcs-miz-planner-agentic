"""Shared LLM turn runner: complete until a final assistant reply (tools in between)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .llm import LLMClient, LLMResponse, default_tools
from .tool_bridge import dispatch_tool
from .verbose import DEFAULT_VERBOSE, vlog, vlog_json


def assistant_message(resp: LLMResponse) -> dict[str, Any]:
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


def complete_with_tools(
    llm: LLMClient,
    messages: list[dict[str, Any]],
    *,
    tools: list[dict[str, Any]] | None = None,
    db_path: Path | str | None = None,
    max_rounds: int = 8,
    verbose: bool = DEFAULT_VERBOSE,
) -> LLMResponse:
    """
    Run LLM + tool dispatch until a response with no tool calls.

    Appends assistant and tool messages onto ``messages`` in place.
    """
    tool_defs = tools if tools is not None else default_tools()
    last: LLMResponse | None = None
    for round_i in range(max_rounds):
        vlog(verbose, f"[verbose] LLM round {round_i + 1}/{max_rounds}…")
        try:
            resp = llm.complete(messages, tools=tool_defs)
        except Exception as exc:
            vlog(verbose, f"[verbose] LLM error: {exc}")
            raise
        last = resp
        messages.append(assistant_message(resp))
        if not resp.tool_calls:
            if verbose and resp.content:
                preview = resp.content.strip().replace("\n", " ")
                if len(preview) > 160:
                    preview = preview[:157] + "..."
                vlog(verbose, f"[verbose] assistant text: {preview}")
            return resp
        for tc in resp.tool_calls:
            vlog(verbose, f"[verbose] tool → {tc.name}({tc.arguments})")
            try:
                result = dispatch_tool(tc.name, tc.arguments, db_path=db_path)
            except Exception as exc:  # noqa: BLE001
                vlog(verbose, f"[verbose] tool error {tc.name}: {exc}")
                result = {"ok": False, "error": str(exc), "code": "tool_dispatch_error"}
            vlog_json(verbose, f"[verbose] tool ← {tc.name}", result)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result),
                }
            )
    vlog(verbose, f"[verbose] hit max_rounds={max_rounds} without final text")
    return last or LLMResponse(content=None)
