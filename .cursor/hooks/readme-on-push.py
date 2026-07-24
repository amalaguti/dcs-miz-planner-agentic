"""Remind the agent to keep README.md current before git push.

Always allows the push; does not rewrite or block the command.
"""

from __future__ import annotations

import json
import re
import sys


def main() -> None:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw or "{}")
    except json.JSONDecodeError:
        payload = {}

    command = str(payload.get("command") or "")
    if re.search(r"\bgit\s+push\b", command, flags=re.IGNORECASE):
        out = {
            "permission": "allow",
            "agent_message": (
                "Before pushing: if this session changed project status, MVP scope, "
                "stack, or setup, update README.md (keep it brief) using the "
                "keep-readme-updated skill, then include that change in what you push."
            ),
        }
    else:
        out = {"permission": "allow"}

    sys.stdout.write(json.dumps(out))


if __name__ == "__main__":
    main()
