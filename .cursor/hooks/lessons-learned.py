"""Remind the agent to consult / update lessons + dcs-dev skills.

sessionStart: inject context to skim topic files / skills for compiler/DCS work.
beforeShellExecution (git push): soft reminder to append new lessons before push.
Always allows the action; never blocks.
"""

from __future__ import annotations

import json
import re
import sys

SESSION_CONTEXT = (
    "Project memory: before PyDCS / compiler / .miz / DCS-id work, skim the "
    "matching docs/lessons/<topic>.md or dcs-dev-* skill (index: "
    "docs/LESSONS_LEARNED.md; workflow: keep-lessons-learned). After a "
    "non-obvious bug or wrong DCS/PyDCS assumption: append to the topic file, "
    "add an index row, and update the matching dcs-dev-* skill if procedure "
    "changed."
)

PUSH_REMINDER = (
    "Before pushing: if this session fixed a non-obvious PyDCS/DCS/compiler "
    "bug or wrong assumption, update docs/lessons/<topic>.md + "
    "docs/LESSONS_LEARNED.md index (+ dcs-dev-* skill if needed) via "
    "keep-lessons-learned, and include those updates in what you push."
)


def main() -> None:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw or "{}")
    except json.JSONDecodeError:
        payload = {}

    # sessionStart: no "command"; often has session-related fields.
    command = payload.get("command")
    if command is None and not (
        payload.get("tool_name") or payload.get("toolName") or payload.get("tool")
    ):
        # Heuristic: treat as sessionStart / context inject.
        out = {"additional_context": SESSION_CONTEXT}
        sys.stdout.write(json.dumps(out))
        return

    command_s = str(command or "")
    if re.search(r"\bgit\s+push\b", command_s, flags=re.IGNORECASE):
        out = {"permission": "allow", "agent_message": PUSH_REMINDER}
    else:
        out = {"permission": "allow"}

    sys.stdout.write(json.dumps(out))


if __name__ == "__main__":
    main()
