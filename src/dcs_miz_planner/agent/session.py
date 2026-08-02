"""Interactive multi-turn plan chat / REPL session."""

from __future__ import annotations

import itertools
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TextIO

import yaml

from ..compiler import PyDCSCompiler
from ..install.models import TheatreInventory
from ..memory import OUTCOME_COMPILE_FAILED, OUTCOME_SUCCESS, OUTCOME_VALIDATION_FAILED
from ..models import MissionSpec
from ..tools.surface import list_mission_options, research_guidance
from ..validation import validate_mission_spec
from .llm import LLMClient, default_tools
from .planner import (
    diagnose_mission_spec_parse,
    load_prefs,
    record_plan,
    write_spec_yaml,
)
from .prompts import compose_system_prompt, host_spec_repair_nudge
from .realism import channel_date_realism_warnings
from .turn import complete_with_tools
from .verbose import DEFAULT_VERBOSE, vlog
from .voice import build_commander_brief, normalize_voice, resolve_voice

_THINKING_LINES = (
    "Commander thinking...",
    "Commander thinking... (pipes another cup of tea)",
    "Commander thinking... checking the board...",
    "Commander thinking... don't scramble yet...",
)
_thinking_cycle = itertools.cycle(_THINKING_LINES)

HELP_TEXT = """\
Slash commands:
  /help              Show this help
  /quit /exit        End the session
  /show              Show draft / proposed Mission Spec YAML
  /accept            Validate and write Spec YAML (then brief)
  /compile           Accept (if needed) and compile to .miz
  /briefing          Commander brief for the current draft Spec
  /research [query]  Live web research when possible (falls back to fixtures)
  /catalog           Show local agent catalog summary
  /verbose [on|off]  Toggle debug / tool-call tracing (default: on)
  /voice <id>        Set voice for this session (raf|usaaf|neutral)
  /prefs             Show stored user preferences
  /clear             Clear chat history and draft (keep voice/prefs)
Other lines go to the squadron commander (LLM).
"""


@dataclass
class SlashResult:
    output: str
    exit_session: bool = False


@dataclass
class PlanSession:
    """In-process multi-turn planning chat."""

    llm: LLMClient
    output_path: Path
    db_path: Path | str | None = None
    voice: str | None = None
    inventory: TheatreInventory | None = None
    compile_on_accept: bool = False
    miz_path: Path | None = None
    verbose: bool = DEFAULT_VERBOSE
    messages: list[dict[str, Any]] = field(default_factory=list)
    draft_spec: MissionSpec | None = None
    proposed_spec: MissionSpec | None = None
    last_spec_error: str | None = None
    system_prompt: str = ""
    resolved_voice: str = ""
    last_generation_id: int | None = None
    _started: bool = False

    def start(self) -> str:
        prefs = load_prefs(self.db_path)
        self.resolved_voice = resolve_voice(cli_voice=self.voice, prefs=prefs)
        self.system_prompt = compose_system_prompt(self.resolved_voice, mode="chat")
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self._started = True
        verb = "on" if self.verbose else "off"
        return (
            f"Interactive plan chat (voice={self.resolved_voice}, verbose={verb}). "
            f"Type /help for commands. Spec out: {self.output_path}"
        )

    def handle_line(self, line: str) -> SlashResult:
        if not self._started:
            banner = self.start()
            # fall through to process line after start
            if not line.strip():
                return SlashResult(output=banner)
            nested = self.handle_line(line)
            return SlashResult(
                output=f"{banner}\n\n{nested.output}",
                exit_session=nested.exit_session,
            )

        text = line.rstrip("\n")
        stripped = text.strip()
        if not stripped:
            return SlashResult(output="")

        if stripped.startswith("/"):
            return self._slash(stripped)

        return self._chat_turn(stripped)

    def _chat_turn(self, user_text: str) -> SlashResult:
        self.messages.append({"role": "user", "content": user_text})
        print(next(_thinking_cycle), file=sys.stderr, flush=True)
        try:
            resp = complete_with_tools(
                self.llm,
                self.messages,
                tools=default_tools(),
                db_path=self.db_path,
                verbose=self.verbose,
            )
        except Exception as exc:  # noqa: BLE001 — keep REPL alive; show error
            vlog(True, f"[verbose] turn failed: {exc}")
            return SlashResult(output=f"[Host] LLM/tool error: {exc}")
        content = (resp.content or "").strip() or "(no reply)"
        parsed, parse_err = diagnose_mission_spec_parse(resp.content)
        if parsed is not None:
            self.proposed_spec = parsed
            self.draft_spec = parsed
            self.last_spec_error = None
            vlog(self.verbose, "[verbose] draft Spec captured from assistant JSON")
            content += (
                "\n\n[Host] Draft Spec captured. Type /accept to validate and write YAML, "
                "or keep refining."
            )
        elif parse_err is not None:
            self.last_spec_error = parse_err
            vlog(self.verbose, f"[verbose] Spec JSON rejected: {parse_err}")
            content += (
                "\n\n[Host] Spec JSON was present but invalid — draft NOT captured.\n"
                f"  {parse_err}\n"
                "The commander has been nudged with the correct Spec shape — "
                "send any follow-up (e.g. 'fix the Spec') or wait for a corrected JSON, "
                "then /accept."
            )
            # Nudge the model with the full shape so the next turn can repair.
            self.messages.append({"role": "user", "content": host_spec_repair_nudge(parse_err)})
        return SlashResult(output=content)

    def _slash(self, cmd_line: str) -> SlashResult:
        parts = cmd_line.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd in ("/quit", "/exit"):
            return SlashResult(output="Session ended.", exit_session=True)
        if cmd == "/help":
            return SlashResult(output=HELP_TEXT.strip())
        if cmd == "/clear":
            self.messages = [{"role": "system", "content": self.system_prompt}]
            self.draft_spec = None
            self.proposed_spec = None
            self.last_spec_error = None
            return SlashResult(output="Cleared conversation and draft.")
        if cmd == "/voice":
            if not arg:
                return SlashResult(output=f"Current voice: {self.resolved_voice}")
            normalized = normalize_voice(arg)
            if normalized is None:
                return SlashResult(output="Unknown voice. Use raf, usaaf, or neutral.")
            self.voice = normalized
            self.resolved_voice = normalized
            self.system_prompt = compose_system_prompt(normalized, mode="chat")
            # Replace system message
            if self.messages and self.messages[0].get("role") == "system":
                self.messages[0] = {"role": "system", "content": self.system_prompt}
            else:
                self.messages.insert(0, {"role": "system", "content": self.system_prompt})
            return SlashResult(output=f"Voice set to {normalized}.")
        if cmd == "/verbose":
            key = arg.strip().lower()
            if not key:
                state = "on" if self.verbose else "off"
                return SlashResult(output=f"verbose is {state} (use /verbose on|off)")
            if key in ("on", "1", "true", "yes"):
                self.verbose = True
                return SlashResult(output="verbose on — tool calls and debug on stderr")
            if key in ("off", "0", "false", "no", "quiet"):
                self.verbose = False
                return SlashResult(output="verbose off")
            return SlashResult(output="Usage: /verbose on|off")
        if cmd == "/prefs":
            prefs = load_prefs(self.db_path)
            if not prefs:
                return SlashResult(output="No prefs set.")
            lines = [f"{k}={v!r}" for k, v in sorted(prefs.items())]
            return SlashResult(output="Prefs:\n" + "\n".join(lines))
        if cmd == "/show":
            return SlashResult(output=self._show_spec())
        if cmd == "/briefing":
            return SlashResult(output=self._briefing())
        if cmd == "/research":
            return SlashResult(output=self._research(arg))
        if cmd == "/catalog":
            return SlashResult(output=self._catalog())
        if cmd == "/accept":
            return SlashResult(output=self._accept(compile_after=False))
        if cmd == "/compile":
            return SlashResult(output=self._accept(compile_after=True))
        return SlashResult(output=f"Unknown command {cmd}.\n{HELP_TEXT.strip()}")

    def _show_spec(self) -> str:
        spec = self.draft_spec or self.proposed_spec
        if spec is None:
            hint = "No draft Spec yet. Chat with the commander, then /accept when ready."
            if self.last_spec_error:
                hint += f"\nLast Spec JSON error: {self.last_spec_error}"
            return hint
        return yaml.safe_dump(spec.model_dump(mode="json"), sort_keys=False, allow_unicode=True)

    def _briefing(self) -> str:
        spec = self.draft_spec or self.proposed_spec
        if spec is None:
            hint = "No draft Spec yet — propose a mission first, then /briefing."
            if self.last_spec_error:
                hint += f"\nLast Spec JSON error: {self.last_spec_error}"
            return hint
        return build_commander_brief(spec, self.resolved_voice)

    def _research(self, query: str) -> str:
        q = query.strip()
        mission_type = None
        theatre = None
        aircraft = None
        spec = self.draft_spec or self.proposed_spec
        if spec is not None:
            mission_type = spec.mission_type.value
            theatre = spec.theatre
            aircraft = spec.player.aircraft
            if not q:
                q = f"{mission_type} {theatre} {aircraft} tactics procedures history"
        if not q:
            q = "Channel Spitfire WWII mission planning tactics weather history"
        print("Commander researching... (live web when available)", file=sys.stderr, flush=True)
        vlog(self.verbose, f"[verbose] /research live=True query={q!r}")
        # Chat /research prefers live fetch; soft-fails to fixtures with a warning.
        result = research_guidance(
            q,
            mission_type=mission_type,
            theatre=theatre,
            aircraft=aircraft,
            live=True,
            db_path=self.db_path,
        )
        notes = result.get("notes") or []
        lines = [f"Research for: {q}"]
        if result.get("warning"):
            lines.append(f"Warning: {result['warning']}")
        for note in notes:
            title = note.get("title") or "note"
            snippet = note.get("snippet") or ""
            source = note.get("source") or ""
            src = f" [{source}]" if source else ""
            lines.append(f"- {title}{src}: {snippet}")
        if not notes:
            lines.append("(no notes)")
        summary = "\n".join(lines)
        # Inject into session for later turns
        self.messages.append(
            {
                "role": "user",
                "content": f"[Host /research]\n{summary}\nUse this as context only; not Spec authority.",
            }
        )
        self.messages.append(
            {
                "role": "assistant",
                "content": "Research noted. I'll factor it into the brief and plan — not as Spec ids.",
            }
        )
        return summary

    def _catalog(self) -> str:
        result = list_mission_options(db_path=self.db_path)
        if not result.get("ok"):
            return f"Catalog unavailable: {result.get('error') or result}"
        lines: list[str] = ["Local planning catalog:"]
        mtypes = result.get("mission_types") or []
        lines.append(f"  mission_types: {', '.join(mtypes)}")
        offerable = result.get("offerable_theatres") or []
        if offerable:
            ids = [t.get("theatre_id") for t in offerable if isinstance(t, dict)]
            lines.append(f"  offerable_theatres: {', '.join(str(i) for i in ids)}")
        options = result.get("options") or []
        by_family: dict[str, list[str]] = {}
        for opt in options:
            if not isinstance(opt, dict):
                continue
            fam = str(opt.get("family") or "?")
            oid = str(opt.get("id") or "?")
            support = str(opt.get("support") or "?")
            by_family.setdefault(fam, []).append(f"{oid} ({support})")
        for fam in sorted(by_family):
            lines.append(f"  {fam}:")
            for item in by_family[fam][:12]:
                lines.append(f"    - {item}")
            if len(by_family[fam]) > 12:
                lines.append(f"    … +{len(by_family[fam]) - 12} more")
        aircraft = result.get("aircraft") or []
        if aircraft:
            shown = ", ".join(str(a) for a in aircraft[:16])
            extra = f" … +{len(aircraft) - 16} more" if len(aircraft) > 16 else ""
            lines.append(f"  aircraft: {shown}{extra}")
        return "\n".join(lines)

    def _accept(self, *, compile_after: bool) -> str:
        spec = self.proposed_spec or self.draft_spec
        if spec is None:
            msg = "Nothing to accept — no draft Spec yet."
            if self.last_spec_error:
                msg += (
                    f"\nLast Spec JSON error: {self.last_spec_error}\n"
                    "Send a follow-up so the commander can emit corrected Spec JSON "
                    "(shape was already nudged), then /accept again."
                )
            return msg
        do_compile = compile_after or self.compile_on_accept
        vresult = validate_mission_spec(spec, inventory=self.inventory)
        if not vresult.ok:
            errors = [
                {
                    "code": e.code,
                    "path": e.path,
                    "message": e.message,
                    "hint": e.hint,
                }
                for e in vresult.errors
            ]
            record_plan(
                db_path=self.db_path,
                prompt="[chat /accept]",
                outcome=OUTCOME_VALIDATION_FAILED,
                spec=spec,
                detail={"errors": errors},
            )
            err_lines = [f"  [{e['code']}] {e['path']}: {e['message']}" for e in errors]
            return "Validation failed:\n" + "\n".join(err_lines)

        write_spec_yaml(spec, self.output_path)
        self.draft_spec = spec
        compiled: Path | None = None
        lines = [f"Wrote Spec {self.output_path}"]
        if do_compile:
            dest = self.miz_path or self.output_path.with_suffix(".miz")
            try:
                compiled = PyDCSCompiler(inventory=self.inventory).compile(spec, dest)
                lines.append(f"Wrote {compiled}")
            except ValueError as exc:
                record_plan(
                    db_path=self.db_path,
                    prompt="[chat /compile]",
                    outcome=OUTCOME_COMPILE_FAILED,
                    spec=spec,
                    spec_path=self.output_path,
                    detail={"error": str(exc)},
                )
                return f"Wrote Spec {self.output_path}\nCompile failed: {exc}"

        brief = build_commander_brief(spec, self.resolved_voice)
        gid = record_plan(
            db_path=self.db_path,
            prompt="[chat /accept]",
            outcome=OUTCOME_SUCCESS,
            spec=spec,
            spec_path=self.output_path,
            miz_path=compiled,
            detail={"voice": self.resolved_voice, "source": "chat"},
        )
        self.last_generation_id = gid
        for w in channel_date_realism_warnings(spec):
            lines.append(f"Warning: {w}")
        lines.append("")
        lines.append(brief)
        return "\n".join(lines)


def run_chat_repl(
    session: PlanSession,
    *,
    input_fn: Callable[[str], str] | None = None,
    stdin: TextIO | None = None,
    stdout: TextIO | None = None,
) -> int:
    """Run interactive loop until quit/EOF. Returns process exit code."""
    import sys

    out = stdout or sys.stdout
    read = input_fn
    if read is None:

        def _default_input(prompt: str) -> str:
            return input(prompt)

        read = _default_input
        del stdin  # use builtin input

    print(session.start(), file=out)
    while True:
        try:
            line = read("pilot> ")
        except EOFError:
            print("\nEOF — session ended.", file=out)
            return 0
        except KeyboardInterrupt:
            print("\nInterrupted — session ended.", file=out)
            return 0
        result = session.handle_line(line)
        if result.output:
            print(result.output, file=out)
        if result.exit_session:
            return 0
