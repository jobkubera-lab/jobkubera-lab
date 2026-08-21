"""Model-agnostic visual-system contract for KUBERA integrations.

This module does not vendor or execute Diagram Design. It provides a validated
intent payload that can be handed to a compatible renderer/skill.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional

SUPPORTED_DIAGRAM_TYPES = frozenset({
    "architecture", "it-current-state", "flowchart", "sequence", "state-machine", "er-data-model",
    "timeline", "swimlane", "quadrant", "radar-spider", "polar-chart", "loop-flywheel", "nested", "tree",
    "org-chart", "layer-stack", "venn", "pyramid-funnel", "treemap", "bar", "line", "gantt", "scatter",
    "high-level", "process", "medallion", "data-flow", "dp-integration", "dp-security-matrix", "sankey",
    "fishbone", "wardley-map", "kanban", "user-journey", "deployment", "dependency-graph", "uml-class",
    "story-map", "database-schema",
})

SUPPORTED_OUTPUT_FORMATS = frozenset({"html", "svg", "png"})
SUPPORTED_THEMES = frozenset({"light", "dark", "full-editorial"})
SUPPORTED_DETAIL_LEVELS = frozenset({"low", "medium", "high"})
SUPPORTED_SOURCE_FORMATS = frozenset({"mermaid", "drawio"})


@dataclass(frozen=True)
class DiagramIntent:
    """Validated intent passed from KUBERA logic to a visual renderer."""

    diagram_type: str
    title: str
    purpose: str
    audience: str = "general"
    detail: str = "medium"
    output_format: str = "html"
    theme: str = "light"
    brand_source: Optional[str] = None
    source_format: Optional[str] = None
    motion: bool = False

    def __post_init__(self) -> None:
        if self.diagram_type not in SUPPORTED_DIAGRAM_TYPES:
            raise ValueError(f"Unsupported diagram_type: {self.diagram_type}")
        if not self.title.strip():
            raise ValueError("title must not be empty")
        if not self.purpose.strip():
            raise ValueError("purpose must not be empty")
        if self.detail not in SUPPORTED_DETAIL_LEVELS:
            raise ValueError(f"Unsupported detail: {self.detail}")
        if self.output_format not in SUPPORTED_OUTPUT_FORMATS:
            raise ValueError(f"Unsupported output_format: {self.output_format}")
        if self.theme not in SUPPORTED_THEMES:
            raise ValueError(f"Unsupported theme: {self.theme}")
        if self.source_format is not None and self.source_format not in SUPPORTED_SOURCE_FORMATS:
            raise ValueError(f"Unsupported source_format: {self.source_format}")

    def to_payload(self) -> dict:
        payload = asdict(self)
        payload["contract_version"] = "1.0"
        payload["accessibility"] = {
            "static_default": True,
            "motion_optional": True,
            "contrast_check_required": True,
        }
        return payload

    def to_renderer_instruction(self) -> str:
        brand = f" Match brand tokens from {self.brand_source}." if self.brand_source else ""
        source = f" Redraw source format: {self.source_format}." if self.source_format else ""
        motion = (
            " Motion may be used when it improves an ordered explanation."
            if self.motion
            else " Keep output static."
        )
        return (
            f"Create a {self.diagram_type} diagram titled '{self.title}' for {self.audience}. "
            f"Purpose: {self.purpose}. Detail: {self.detail}. "
            f"Output: self-contained {self.output_format}; theme: {self.theme}.{brand}{source}{motion} "
            "Use semantic emphasis sparingly, preserve readability, and verify contrast."
        )
