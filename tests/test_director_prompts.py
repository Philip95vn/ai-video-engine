import pytest

from ai_video_engine.director.prompts import (
    ALLOWED_EFFECTS,
    ALLOWED_EMOTIONS,
    ALLOWED_LAYOUTS,
    DEFAULT_VISUAL_DIRECTOR_PROMPT,
    PromptTemplateError,
    format_allowed_values,
    load_prompt,
    render_prompt,
    render_visual_director_prompt,
)
from ai_video_engine.timeline.schema import NormalizedTimeline, TimelineScene


def make_timeline() -> NormalizedTimeline:
    return NormalizedTimeline(
        metadata={"source": "unit_test"},
        scenes=[
            TimelineScene(
                id="scene_0001",
                source_segment_ids=["seg_0001"],
                start=0.0,
                end=2.0,
                duration=2.0,
                text="Xin chào Việt Nam.",
            )
        ],
    )


def test_load_prompt_reads_utf8_text(tmp_path):
    prompt_path = tmp_path / "prompt.md"
    prompt_path.write_text("Xin chào $name", encoding="utf-8")

    prompt = load_prompt(prompt_path)

    assert prompt.path == prompt_path
    assert prompt.text == "Xin chào $name"


def test_load_prompt_rejects_missing_file(tmp_path):
    with pytest.raises(PromptTemplateError):
        load_prompt(tmp_path / "missing.md")


def test_render_prompt_substitutes_required_variables(tmp_path):
    prompt_path = tmp_path / "prompt.md"
    prompt_path.write_text("Hello $name", encoding="utf-8")
    prompt = load_prompt(prompt_path)

    rendered = render_prompt(prompt, {"name": "Philip"})

    assert rendered == "Hello Philip"


def test_render_prompt_rejects_missing_variable(tmp_path):
    prompt_path = tmp_path / "prompt.md"
    prompt_path.write_text("Hello $name", encoding="utf-8")
    prompt = load_prompt(prompt_path)

    with pytest.raises(PromptTemplateError):
        render_prompt(prompt, {})


def test_format_allowed_values_uses_bullets():
    assert format_allowed_values(["pop", "shake"]) == "- pop\n- shake"


def test_format_allowed_values_rejects_empty_values():
    with pytest.raises(PromptTemplateError):
        format_allowed_values([])


def test_render_visual_director_prompt_uses_default_prompt_file():
    timeline = make_timeline()

    rendered = render_visual_director_prompt(timeline)

    assert DEFAULT_VISUAL_DIRECTOR_PROMPT.exists()
    assert "Return JSON only." in rendered
    assert "scene_0001" in rendered
    assert "Xin chào Việt Nam." in rendered
    assert "- neutral" in rendered
    assert "- center_stack" in rendered
    assert "- pop" in rendered
    assert "$timeline_json" not in rendered
    assert "$allowed_emotions" not in rendered
    assert "$allowed_layouts" not in rendered
    assert "$allowed_effects" not in rendered


def test_prompt_allowed_values_are_not_empty():
    assert ALLOWED_EMOTIONS
    assert ALLOWED_LAYOUTS
    assert ALLOWED_EFFECTS
