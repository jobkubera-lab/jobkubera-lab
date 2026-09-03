"""Narrow local draft adapter for the KUBERA reference demo.

This is deliberately not an email, Slack, browser, payment, or publishing adapter.
It performs one reversible local side effect: writing a UTF-8 draft file under a
configured root directory. Application code should expose it only through
SovereignToolExecutor.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


class LocalDraftAdapter:
    """Write a text draft inside one configured directory.

    The adapter accepts only ``tool_name='local-draft'`` and
    ``operation='write_draft'``. The target must be a simple filename so callers
    cannot escape the configured root via path traversal.
    """

    TOOL_NAME = "local-draft"
    OPERATION = "write_draft"

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root).expanduser().resolve()
        self._root.mkdir(parents=True, exist_ok=True)

    @property
    def root(self) -> Path:
        return self._root

    def execute(
        self,
        *,
        tool_name: str,
        operation: str,
        target: str,
        arguments: Mapping[str, Any],
    ) -> dict[str, Any]:
        if tool_name != self.TOOL_NAME:
            raise ValueError("unsupported tool_name")
        if operation != self.OPERATION:
            raise ValueError("unsupported operation")

        filename = str(target).strip()
        if not filename or Path(filename).name != filename or filename in {".", ".."}:
            raise ValueError("target must be a simple filename inside the configured draft root")

        body = arguments.get("body")
        if not isinstance(body, str) or not body.strip():
            raise ValueError("body must be a non-empty string")

        destination = (self._root / filename).resolve()
        if destination.parent != self._root:
            raise ValueError("target escapes configured draft root")

        destination.write_text(body, encoding="utf-8")
        return {
            "ok": True,
            "kind": "local_draft",
            "filename": destination.name,
            "bytes": len(body.encode("utf-8")),
        }
