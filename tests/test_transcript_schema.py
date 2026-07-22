"""Tests for transcript schema models."""

import pytest
from pydantic import ValidationError

from ai_video_engine.speech.schema import (
    Transcript,
    TranscriptSegment,
    make_segment_id,
)


def build_segment(
    *,
    segment_id: str = "seg_0001",
    start: float = 0.0,
    end: float = 1.5,
    duration: float = 1.5,
    text: str = "Xin chào.",
) -> TranscriptSegment:
    """Create a valid transcript segment for tests."""
    return TranscriptSegment(
        id=segment_id,
        start=start,
        end=end,
        duration=duration,
        text=text,
    )


def test_make_segment_id_is_deterministic() -> None:
    assert make_segment_id(1) == "seg_0001"
    assert make_segment_id(12) == "seg_0012"


def test_make_segment_id_rejects_non_positive_index() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        make_segment_id(0)


def test_transcript_segment_is_valid() -> None:
    segment = build_segment(text="ĐẾN TRỄ? BÁO THỨC!")

    assert segment.id == "seg_0001"
    assert segment.duration == 1.5
    assert segment.text == "ĐẾN TRỄ? BÁO THỨC!"


def test_transcript_segment_strips_id_and_text() -> None:
    segment = build_segment(
        segment_id=" seg_0001 ",
        text=" Xin chào. ",
    )

    assert segment.id == "seg_0001"
    assert segment.text == "Xin chào."


def test_transcript_segment_rejects_negative_start() -> None:
    with pytest.raises(ValidationError):
        build_segment(
            start=-0.1,
            end=1.0,
            duration=1.1,
        )


def test_transcript_segment_rejects_invalid_end() -> None:
    with pytest.raises(
        ValidationError,
        match="end must be greater than start",
    ):
        build_segment(
            start=1.0,
            end=1.0,
            duration=0.1,
        )


def test_transcript_segment_accepts_duration_within_tolerance() -> None:
    segment = build_segment(
        end=1.0,
        duration=1.04,
    )

    assert segment.duration == 1.04


def test_transcript_segment_rejects_duration_mismatch() -> None:
    with pytest.raises(
        ValidationError,
        match="duration must match end - start",
    ):
        build_segment(
            end=1.0,
            duration=1.1,
        )


def test_transcript_segment_rejects_blank_text() -> None:
    with pytest.raises(ValidationError, match="must not be blank"):
        build_segment(text="   ")


def test_transcript_uses_defaults() -> None:
    transcript = Transcript(segments=[build_segment()])

    assert transcript.schema_version == "0.1.0"
    assert transcript.metadata == {}


def test_transcript_rejects_duplicate_ids() -> None:
    with pytest.raises(
        ValidationError,
        match="segment IDs must be unique",
    ):
        Transcript(
            segments=[
                build_segment(),
                build_segment(
                    start=1.6,
                    end=2.5,
                    duration=0.9,
                    text="Đoạn thứ hai.",
                ),
            ]
        )


def test_transcript_rejects_unsorted_segments() -> None:
    with pytest.raises(
        ValidationError,
        match="segments must be sorted by start time",
    ):
        Transcript(
            segments=[
                build_segment(
                    segment_id="seg_0001",
                    start=2.0,
                    end=3.0,
                    duration=1.0,
                ),
                build_segment(
                    segment_id="seg_0002",
                    start=0.0,
                    end=1.0,
                    duration=1.0,
                ),
            ]
        )