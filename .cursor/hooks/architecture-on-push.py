"""Remind the agent to keep docs/ARCHITECTURE.md current before git push.

Only speaks up when the commits being pushed touch the product package, and only
if ARCHITECTURE.md itself was not already updated. Always allows the push.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

PACKAGE_PREFIX = "src/dcs_miz_planner/"
ARCHITECTURE_DOC = "docs/ARCHITECTURE.md"

REMINDER = (
    "This push changes src/dcs_miz_planner/ but not docs/ARCHITECTURE.md. "
    "If module responsibilities, package layout, or the Mission Spec -> .miz flow "
    "changed, update docs/ARCHITECTURE.md (keep the diagram honest) and include it "
    "in this push."
)


def _git(*args: str) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, timeout=10, check=False
        )
    except (OSError, subprocess.SubprocessError):
        return None


def _changed_files() -> list[str]:
    """Files in commits this push would send, best-effort.

    A tracking branch knows its upstream. A fresh feature branch does not, so fall
    back to the remote (then local) default branch. Returns [] if nothing resolves,
    which keeps the hook silent rather than nagging on bad data.
    """
    candidates = (
        "@{upstream}..HEAD",
        "origin/master..HEAD",
        "origin/main..HEAD",
        "master..HEAD",
        "main..HEAD",
    )
    for rev_range in candidates:
        result = _git("diff", "--name-only", rev_range)
        if result is None:
            return []
        if result.returncode == 0:
            return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return []


def main() -> None:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw or "{}")
    except json.JSONDecodeError:
        payload = {}

    command = str(payload.get("command") or "")
    if not re.search(r"\bgit\s+push\b", command, flags=re.IGNORECASE):
        sys.stdout.write(json.dumps({"permission": "allow"}))
        return

    changed = _changed_files()
    touches_package = any(path.startswith(PACKAGE_PREFIX) for path in changed)
    touches_doc = ARCHITECTURE_DOC in changed

    out: dict[str, str] = {"permission": "allow"}
    if touches_package and not touches_doc:
        out["agent_message"] = REMINDER

    sys.stdout.write(json.dumps(out))


if __name__ == "__main__":
    main()
