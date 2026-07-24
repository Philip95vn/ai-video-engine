import pytest
from pydantic import ValidationError

from ai_video_engine.timeline.schema import (
    NormalizedTimeline,
    TimelineScene,
    TimelineSpeaker,
    make_scene_id,
)


def test_make_scene_id_uses_one_based_index():
    assert make_scene_id(1) == "scene_0001"
    assert make_scene_id(12) == "scene_0012"


def test_make_scene_id_rejects_zero():
    with pytest.raises(ValueError):
        make_scene_id(0)


def test_timeline_speaker_defaults():
    speaker = TimelineSpeaker()

    assert speaker.id == "SPEAKER_00"
    assert speaker.source == "unknown"


def test_timeline_scene_accepts_valid_data():
    scene = TimelineScene(
        id="scene_0001",
        source_segment_ids=["seg_0001"],
        start=0.0,
        end=2.5,
        duration=2.5,
        text="Xin chao.",
    )

    assert scene.id == "scene_0001"
    assert scene.speaker.id == "SPEAKER_00"


def test_timeline_scene_rejects_duration_mismatch():
    with pytest.raises(ValidationError):
        TimelineScene(
            id="scene_0001",
            source_segment_ids=["seg_0001"],
            start=0.0,
            end=2.5,
            duration=1.0,
            text="Xin chao.",
        )


def test_timeline_scene_rejects_duplicate_source_segments():
    with pytest.raises(ValidationError):
        TimelineScene(
            id="scene_0001",
            source_segment_ids=["seg_0001", "seg_0001"],
            start=0.0,
            end=2.5,
            duration=2.5,
            text="Xin chao.",
        )


def test_normalized_timeline_accepts_valid_scenes():
    timeline = NormalizedTimeline(
        metadata={"source": "unit_test"},
        scenes=[
            TimelineScene(
                id="scene_0001",
                source_segment_ids=["seg_0001"],
                start=0.0,
                end=2.0,
                duration=2.0,
                text="Scene one.",
            ),
            TimelineScene(
                id="scene_0002",
                source_segment_ids=["seg_0002"],
                start=2.0,
                end=4.0,
                duration=2.0,
                text="Scene two.",
            ),
        ],
    )

    assert timeline.schema_version == "0.1.0"
    assert len(timeline.scenes) == 2


def test_normalized_timeline_rejects_duplicate_scene_ids():
    with pytest.raises(ValidationError):
        NormalizedTimeline(
            scenes=[
                TimelineScene(
                    id="scene_0001",
                    source_segment_ids=["seg_0001"],
                    start=0.0,
                    end=2.0,
                    duration=2.0,
                    text="Scene one.",
                ),
                TimelineScene(
                    id="scene_0001",
                    source_segment_ids=["seg_0002"],
                    start=2.0,
                    end=4.0,
                    duration=2.0,
                    text="Scene two.",
                ),
            ],
        )


def test_normalized_timeline_rejects_overlapping_scenes():
    with pytest.raises(ValidationError):
        NormalizedTimeline(
            scenes=[
                TimelineScene(
                    id="scene_0001",
                    source_segment_ids=["seg_0001"],
                    start=0.0,
                    end=2.5,
                    duration=2.5,
                    text="Scene one.",
                ),
                TimelineScene(
                    id="scene_0002",
                    source_segment_ids=["seg_0002"],
                    start=2.0,
                    end=4.0,
                    duration=2.0,
                    text="Scene two.",
                ),
            ],
        )
