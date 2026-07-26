"""Block agent mutations while on master/main; allow branch creation/switch away.

Used for preToolUse (file edits) and beforeShellExecution (risky git).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

PROTECTED = frozenset({"master", "main"})

# Tools that mutate the workspace (Cursor agent tool names).
MUTATING_TOOLS = frozenset(
    {
        "Write",
        "StrReplace",
        "Delete",
        "EditNotebook",
        "CallDynamicTool",  # may include Write/Delete via cursor namespace
    }
)

SAFE_SHELL_ON_PROTECTED = re.compile(
    r"""(?ix)
    ^\s*(
        git\s+(status|diff|log|show|fetch|remote|rev-parse|branch\b(?!\s+-[dD])|stash\s+list)
      | git\s+(checkout|switch)(\s+-b|\s+-c)?\s+\S+
      | git\s+branch\s+\S+
      | python\s+\.cursor/hooks/
      | npx\s+openspec\s+(list|status|instructions|show|view|doctor)
    )
    """,
)

DENY_SHELL_ON_PROTECTED = re.compile(
    r"""(?ix)
    \b(
        git\s+commit
      | git\s+merge
      | git\s+rebase
      | git\s+cherry-pick
      | git\s+am\b
      | git\s+push
      | git\s+add\b
      | git\s+reset\b
      | git\s+stash\s+(push|pop|apply)
    )\b
    """,
)

MSG = (
    "Refusing work on protected branch (master/main). "
    "Checkout a feature branch first. For OpenSpec propose/apply, use: "
    "git checkout -b <openspec-change-name> (branch name = change name), "
    "then retry. See skill openspec-git-branch."
)


def current_branch() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if r.returncode != 0:
            return ""
        return (r.stdout or "").strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def on_protected() -> bool:
    return current_branch() in PROTECTED


def allow() -> dict:
    return {"permission": "allow"}


def deny(agent_message: str | None = None) -> dict:
    return {
        "permission": "deny",
        "agent_message": agent_message or MSG,
        "user_message": "Blocked: agent cannot change files on master/main.",
    }


def handle_pre_tool(payload: dict) -> dict:
    if not on_protected():
        return allow()

    tool = payload.get("tool_name") or payload.get("toolName") or payload.get("tool") or ""
    tool = str(tool)

    # Match bare tool names and MCP-style names.
    base = tool.split(":")[-1] if tool else ""
    if tool in MUTATING_TOOLS or base in MUTATING_TOOLS:
        # Allow Delete only if somehow needed? No — deny all mutating.
        return deny()

    return allow()


def handle_shell(payload: dict) -> dict:
    if not on_protected():
        return allow()

    command = str(payload.get("command") or "")

    # Always allow creating/switching off the protected branch.
    if re.search(r"(?i)\bgit\s+(checkout|switch)\b", command):
        return allow()

    if DENY_SHELL_ON_PROTECTED.search(command):
        return deny()

    if SAFE_SHELL_ON_PROTECTED.search(command):
        return allow()

    # Fail closed for other shell on protected branches (avoids echo>file etc.).
    return deny(MSG + " Shell on master/main is limited to read-only git and checkout/switch.")


def main() -> None:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw or "{}")
    except json.JSONDecodeError:
        payload = {}

    # Heuristic: shell hooks include "command"; tool hooks include tool name fields.
    if (
        "command" in payload
        and (
            payload.get("tool_name") is None
            and payload.get("toolName") is None
            and "tool_input" not in payload
        )
        or payload.get("command")
        and not (payload.get("tool_name") or payload.get("toolName") or payload.get("tool"))
    ):
        out = handle_shell(payload)
    else:
        # Prefer tool handling when tool fields present; else if command, shell.
        if payload.get("tool_name") or payload.get("toolName") or payload.get("tool"):
            out = handle_pre_tool(payload)
        elif "command" in payload:
            out = handle_shell(payload)
        else:
            # Unknown event shape — fail open to avoid breaking Cursor.
            out = allow()

    sys.stdout.write(json.dumps(out))


if __name__ == "__main__":
    main()
