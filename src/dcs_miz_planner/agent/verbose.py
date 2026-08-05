"""Agent debug / verbose logging (stderr). Default off; opt in with --verbose / /verbose on."""

from __future__ import annotations

import json
import sys
from typing import Any

# Quiet by default (adversarial C3 / backlog #10b). Opt in via CLI or /verbose on.
DEFAULT_VERBOSE = False


def vlog(verbose: bool, message: str) -> None:
    """Print a verbose line to stderr when enabled."""
    if verbose:
        print(message, file=sys.stderr, flush=True)


def vlog_json(verbose: bool, label: str, payload: Any, *, max_len: int = 1200) -> None:
    """Print a labelled JSON-ish payload, truncated for readability."""
    if not verbose:
        return
    try:
        text = json.dumps(payload, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        text = repr(payload)
    if len(text) > max_len:
        text = text[: max_len - 3] + "..."
    print(f"{label} {text}", file=sys.stderr, flush=True)
