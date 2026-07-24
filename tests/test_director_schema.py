"""Tests for Visual Director output schema."""

from __future__ import annotations

from copy import deepcopy

import pytest
from pydantic import ValidationError

from ai_video_engine.director.schema import (
    DIRECTOR_SCHEMA_VERSION,
    DirectorScene,
    DirectorTimeline,
)


def make_scene(**overrides: object) -> dict[str, object]:
    """Build one valid Visual Director scene dictionary."""

    scene: dict[str, object] = {
        "id": "scene_0001",
        "source_segment_ids": ["seg_0001"],
        "start": 0.0,
        "end": 2.0,
        "duration": 2.0,
        "speaker": {
            "id": "SPEAKER_00",
            "source": "unknown",
        },
        "text": "Tại báo thức!",
        "lines": ["TẠI", "BÁO THỨC!"],
        "emotion": "funny",
        "layout": "punchline_center",
        "keywords": [
            {
                "text": "BÁO THỨC",
                "reason": "Punchline cần được nhấn mạnh",
            }
        ],
        "effects": [
            {
                "type": "shake",
                "target": "BÁO THỨC",
                "intensity": "medium",
            }
        ],
        "icon_query": "đồng hồ báo thức",
    }
    scene.update(overrides)
    return scene


def test_director_scene_accepts_valid_vietnamese_data() -> None:
    """Valid output preserves readable Vietnamese text."""

    scene = DirectorScene.model_validate(make_scene())

    assert scene.text == "Tại báo thức!"
    assert scene.lines == ["TẠI", "BÁO THỨC!"]
    assert (
        scene.keywords[0].reason
        == "Punchline cần được nhấn mạnh"
    )
    assert (
        scene.model_dump(mode="json")["icon_query"]
        == "đồng hồ báo thức"
    )


def test_director_timeline_uses_current_schema_version() -> None:
    """The current director schema version is accepted."""

    timeline = DirectorTimeline(
        metadata={"source": "visual_director"},
        scenes=[make_scene()],
    )

    assert timeline.schema_version == DIRECTOR_SCHEMA_VERSION


def test_director_timeline_rejects_unsupported_schema_version() -> None:
    """Unknown schema versions fail validation."""

    with pytest.raises(
        ValidationError,
        match="unsupported director schema version",
    ):
        DirectorTimeline(
            schema_version="9.9.9",
            scenes=[make_scene()],
        )


@pytest.mark.parametrize(
    ("field_name", "invalid_value", "message"),
    [
        ("emotion", "sleepy", "unsupported emotion"),
        ("layout", "floating_cards", "unsupported layout"),
    ],
)
def test_director_scene_rejects_unknown_controlled_values(
    field_name: str,
    invalid_value: str,
    message: str,
) -> None:
    """Unknown prompt-controlled values fail validation."""

    with pytest.raises(ValidationError, match=message):
        DirectorScene.model_validate(
            make_scene(**{field_name: invalid_value})
        )


def test_director_scene_rejects_unknown_effect_type() -> None:
    """Only prompt-supported effect names are accepted."""

    scene = make_scene()
    scene["effects"] = [
        {
            "type": "explode",
            "target": "BÁO THỨC",
            "intensity": "medium",
        }
    ]

    with pytest.raises(
        ValidationError,
        match="unsupported effect type",
    ):
        DirectorScene.model_validate(scene)


def test_director_scene_rejects_unknown_effect_intensity() -> None:
    """Only low, medium, and high intensities are accepted."""

    scene = make_scene()
    scene["effects"] = [
        {
            "type": "pop",
            "target": "BÁO THỨC",
            "intensity": "extreme",
        }
    ]

    with pytest.raises(
        ValidationError,
        match="unsupported effect intensity",
    ):
        DirectorScene.model_validate(scene)


def test_director_scene_rejects_blank_display_line() -> None:
    """Display lines cannot contain blank values."""

    with pytest.raises(
        ValidationError,
        match="lines must not contain blank values",
    ):
        DirectorScene.model_validate(
            make_scene(lines=["TẠI", "   "])
        )


def test_director_scene_rejects_more_than_six_display_lines() -> None:
    """A scene contains at most six display lines."""

    with pytest.raises(ValidationError):
        DirectorScene.model_validate(
            make_scene(
                lines=["1", "2", "3", "4", "5", "6", "7"]
            )
        )


def test_director_scene_rejects_duration_mismatch() -> None:
    """Duration must match end minus start."""

    with pytest.raises(
        ValidationError,
        match="duration must match",
    ):
        DirectorScene.model_validate(
            make_scene(duration=1.0)
        )


def test_director_scene_rejects_duplicate_source_segment_ids() -> None:
    """Source segment IDs must be unique within a scene."""

    with pytest.raises(
        ValidationError,
        match="source_segment_ids must be unique",
    ):
        DirectorScene.model_validate(
            make_scene(
                source_segment_ids=[
                    "seg_0001",
                    "seg_0001",
                ]
            )
        )


def test_director_scene_rejects_duplicate_keywords() -> None:
    """Keyword text must be unique within a scene."""

    scene = make_scene()
    scene["keywords"] = [
        {
            "text": "BÁO THỨC",
            "reason": "Primary keyword",
        },
        {
            "text": "báo thức",
            "reason": "Duplicate with different letter case",
        },
    ]

    with pytest.raises(
        ValidationError,
        match="keyword text must be unique",
    ):
        DirectorScene.model_validate(scene)


def test_director_scene_rejects_unexpected_fields() -> None:
    """LLM fields outside the contract are rejected."""

    with pytest.raises(
        ValidationError,
        match="Extra inputs are not permitted",
    ):
        DirectorScene.model_validate(
            make_scene(final_icon_file="alarm.png")
        )


def test_director_timeline_rejects_duplicate_scene_ids() -> None:
    """Scene IDs must be unique across the timeline."""

    first = make_scene()
    second = make_scene(
        start=2.0,
        end=4.0,
        duration=2.0,
        source_segment_ids=["seg_0002"],
    )

    with pytest.raises(
        ValidationError,
        match="scene IDs must be unique",
    ):
        DirectorTimeline(scenes=[first, second])


def test_director_timeline_rejects_overlapping_scenes() -> None:
    """Director scenes must not overlap."""

    first = make_scene()
    second = make_scene(
        id="scene_0002",
        start=1.5,
        end=3.0,
        duration=1.5,
        source_segment_ids=["seg_0002"],
    )

    with pytest.raises(
        ValidationError,
        match="scenes must not overlap",
    ):
        DirectorTimeline(scenes=[first, second])


def test_director_timeline_accepts_sorted_scenes() -> None:
    """Sorted, non-overlapping scenes are valid."""

    first = make_scene()
    second = deepcopy(first)
    second.update(
        {
            "id": "scene_0002",
            "source_segment_ids": ["seg_0002"],
            "start": 2.0,
            "end": 3.5,
            "duration": 1.5,
            "text": "Dậy muộn.",
            "lines": ["DẬY MUỘN."],
            "keywords": [],
            "effects": [],
            "icon_query": None,
        }
    )

    timeline = DirectorTimeline(scenes=[first, second])

    assert [scene.id for scene in timeline.scenes] == [
        "scene_0001",
        "scene_0002",
    ]
