"""Prompt loading and rendering for Visual Director."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from string import Template

from ai_video_engine.common.errors import AIVideoEngineError
from ai_video_engine.timeline.schema import NormalizedTimeline

DEFAULT_VISUAL_DIRECTOR_PROMPT = Path("prompts/visual_director.md")

ALLOWED_EMOTIONS: tuple[str, ...] = (
    "neutral",
    "funny",
    "surprised",
    "angry",
    "sad",
    "excited",
    "confused",
)

ALLOWED_LAYOUTS: tuple[str, ...] = (
    "center_stack",
    "split_speaker",
    "punchline_center",
    "top_question_bottom_answer",
)

ALLOWED_EFFECTS: tuple[str, ...] = (
    "none",
    "pop",
    "bounce",
    "shake",
    "glow",
    "slide",
    "typewriter",
    "zoom",
    "fade",
    "pulse",
)


class PromptTemplateError(AIVideoEngineError):
    """Raised when a prompt template cannot be loaded or rendered."""


@dataclass(frozen=True)
class PromptTemplate:
    """Loaded prompt template text."""

    path: Path
    text: str


def load_prompt(path: Path) -> PromptTemplate:
    """Load a UTF-8 prompt template from disk."""
    if not path.exists():
        raise PromptTemplateError(f"Prompt template not found: {path}")

    text = path.read_text(encoding="utf-8").strip()

    if not text:
        raise PromptTemplateError(f"Prompt template is empty: {path}")

    return PromptTemplate(path=path, text=text)


def render_prompt(
    prompt_template: PromptTemplate,
    variables: Mapping[str, str],
) -> str:
    """Render a prompt using required string.Template variables."""
    try:
        rendered = Template(prompt_template.text).substitute(variables)
    except KeyError as exc:
        missing_key = exc.args[0]
        raise PromptTemplateError(f"Missing prompt variable: {missing_key}") from exc
    except ValueError as exc:
        raise PromptTemplateError(
            f"Invalid prompt template syntax: {prompt_template.path}"
        ) from exc

    rendered = rendered.strip()

    if not rendered:
        raise PromptTemplateError(
            f"Rendered prompt is empty: {prompt_template.path}"
        )

    return rendered


def render_visual_director_prompt(
    timeline: NormalizedTimeline,
    prompt_path: Path = DEFAULT_VISUAL_DIRECTOR_PROMPT,
) -> str:
    """Render the Visual Director prompt from a normalized timeline."""
    prompt_template = load_prompt(prompt_path)

    timeline_json = json.dumps(
        timeline.model_dump(mode="json"),
        ensure_ascii=False,
        indent=2,
    )

    return render_prompt(
        prompt_template,
        {
            "timeline_json": timeline_json,
            "allowed_emotions": format_allowed_values(ALLOWED_EMOTIONS),
            "allowed_layouts": format_allowed_values(ALLOWED_LAYOUTS),
            "allowed_effects": format_allowed_values(ALLOWED_EFFECTS),
        },
    )


def format_allowed_values(values: Sequence[str]) -> str:
    """Format allowed values as prompt bullet lines."""
    if not values:
        raise PromptTemplateError("Allowed values must not be empty")

    return "\n".join(f"- {value}" for value in values)
