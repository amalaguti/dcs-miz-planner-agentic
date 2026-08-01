"""Structured tool results for agent-facing callables."""

from __future__ import annotations

from typing import Any


def ok_result(**payload: Any) -> dict[str, Any]:
    return {"ok": True, **payload}


def err_result(error: str, *, code: str | None = None, **payload: Any) -> dict[str, Any]:
    out: dict[str, Any] = {"ok": False, "error": error}
    if code is not None:
        out["code"] = code
    out.update(payload)
    return out
