"""Compiler boundary.

The Mission Spec is the public contract. Concrete compilers (PyDCS today,
possibly a native serializer later) implement this interface so the backend
stays interchangeable.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ..models import MissionSpec


class CompilerInterface(ABC):
    @abstractmethod
    def compile(
        self,
        spec: MissionSpec,
        output_path: str | Path,
        *,
        voice: str | None = None,
    ) -> Path:
        """Compile a Mission Spec into a .miz file. Returns the written path.

        ``voice`` selects squadron-commander register for briefing ``l10n`` text;
        when omitted the implementation uses the default voice (``raf``).
        """
        raise NotImplementedError
