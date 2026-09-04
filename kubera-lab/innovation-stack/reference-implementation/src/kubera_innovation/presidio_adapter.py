"""Optional Microsoft Presidio adapter for the KUBERA PrivacyGate.

The adapter imports Presidio lazily, so the core reference runtime stays
provider-neutral and dependency-free unless this integration is explicitly used.
"""
from __future__ import annotations

from typing import Any, Iterable


class PresidioUnavailableError(RuntimeError):
    """Raised when Presidio is requested but its Python packages are unavailable."""


class PresidioTextRedactor:
    """Implement the KUBERA TextRedactor protocol with Presidio.

    ``analyzer`` and ``anonymizer`` are injectable to keep tests dependency-free.
    When neither is supplied, the adapter lazily imports ``presidio_analyzer`` and
    ``presidio_anonymizer`` and constructs their default engines.
    """

    def __init__(
        self,
        *,
        language: str = "en",
        entities: Iterable[str] | None = None,
        analyzer: Any | None = None,
        anonymizer: Any | None = None,
    ) -> None:
        if not language.strip():
            raise ValueError("language must not be empty")
        if (analyzer is None) != (anonymizer is None):
            raise ValueError("analyzer and anonymizer must be supplied together")

        if analyzer is None:
            try:
                from presidio_analyzer import AnalyzerEngine
                from presidio_anonymizer import AnonymizerEngine
            except ImportError as exc:
                raise PresidioUnavailableError(
                    "Presidio integration requires presidio-analyzer and presidio-anonymizer"
                ) from exc
            analyzer = AnalyzerEngine()
            anonymizer = AnonymizerEngine()

        self.language = language
        self.entities = tuple(entities) if entities is not None else None
        self._analyzer = analyzer
        self._anonymizer = anonymizer

    def redact(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        analyze_kwargs: dict[str, Any] = {"text": text, "language": self.language}
        if self.entities is not None:
            analyze_kwargs["entities"] = list(self.entities)
        analyzer_results = self._analyzer.analyze(**analyze_kwargs)
        result = self._anonymizer.anonymize(text=text, analyzer_results=analyzer_results)
        redacted = getattr(result, "text", None)
        if not isinstance(redacted, str):
            raise RuntimeError("Presidio anonymizer returned an invalid result")
        return redacted
