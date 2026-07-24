import json

from ai_video_engine.common.json_io import write_json
from ai_video_engine.speech.schema import Transcript, TranscriptSegment
from ai_video_engine.timeline.analyzer import (
    TimelineAnalyzerConfig,
    analyze_transcript,
    analyze_transcript_file,
    clean_text,
)


def make_segment(
    segment_id: str,
    start: float,
    end: float,
    text: str,
) -> TranscriptSegment:
    return TranscriptSegment(
        id=segment_id,
        start=start,
        end=end,
        duration=round(end - start, 2),
        text=text,
    )


def test_clean_text_normalizes_whitespace_and_preserves_vietnamese():
    assert clean_text(" Xin   chào   Việt Nam ") == "Xin chào Việt Nam"


def test_analyze_transcript_creates_scene_from_segment():
    transcript = Transcript(
        segments=[
            make_segment("seg_0001", 0.0, 2.0, "Xin chào."),
        ],
    )

    timeline = analyze_transcript(transcript)

    assert len(timeline.scenes) == 1
    assert timeline.scenes[0].id == "scene_0001"
    assert timeline.scenes[0].source_segment_ids == ["seg_0001"]
    assert timeline.scenes[0].start == 0.0
    assert timeline.scenes[0].end == 2.0
    assert timeline.scenes[0].duration == 2.0
    assert timeline.scenes[0].speaker.id == "SPEAKER_00"
    assert timeline.scenes[0].text == "Xin chào."


def test_analyze_transcript_merges_short_adjacent_segments():
    transcript = Transcript(
        segments=[
            make_segment("seg_0001", 0.0, 0.5, "Xin"),
            make_segment("seg_0002", 0.5, 2.0, "chào."),
        ],
    )

    timeline = analyze_transcript(transcript)

    assert len(timeline.scenes) == 1
    assert timeline.scenes[0].source_segment_ids == ["seg_0001", "seg_0002"]
    assert timeline.scenes[0].start == 0.0
    assert timeline.scenes[0].end == 2.0
    assert timeline.scenes[0].text == "Xin chào."


def test_analyze_transcript_splits_long_segment_by_duration():
    transcript = Transcript(
        segments=[
            make_segment(
                "seg_0001",
                0.0,
                8.0,
                "Một hai ba bốn năm sáu bảy tám.",
            ),
        ],
    )

    timeline = analyze_transcript(transcript)

    assert len(timeline.scenes) == 2
    assert timeline.scenes[0].id == "scene_0001"
    assert timeline.scenes[1].id == "scene_0002"
    assert timeline.scenes[0].start == 0.0
    assert timeline.scenes[0].end == 4.0
    assert timeline.scenes[1].start == 4.0
    assert timeline.scenes[1].end == 8.0
    assert timeline.scenes[0].source_segment_ids == ["seg_0001"]
    assert timeline.scenes[1].source_segment_ids == ["seg_0001"]


def test_analyze_transcript_splits_long_segment_by_text_length():
    transcript = Transcript(
        segments=[
            make_segment(
                "seg_0001",
                0.0,
                4.0,
                " ".join(["từ"] * 20),
            ),
        ],
    )

    config = TimelineAnalyzerConfig(max_scene_chars=20)
    timeline = analyze_transcript(transcript, config=config)

    assert len(timeline.scenes) > 1
    assert timeline.scenes[0].start == 0.0
    assert timeline.scenes[-1].end == 4.0


def test_analyze_transcript_file_writes_normalized_timeline_json(tmp_path):
    input_path = tmp_path / "transcript.json"
    output_path = tmp_path / "timeline.normalized.json"

    write_json(
        input_path,
        {
            "schema_version": "0.1.0",
            "metadata": {"source_input": "input/video.mp4"},
            "segments": [
                {
                    "id": "seg_0001",
                    "start": 0.0,
                    "end": 2.0,
                    "duration": 2.0,
                    "text": "Xin chào Việt Nam.",
                }
            ],
        },
    )

    timeline = analyze_transcript_file(input_path, output_path)

    assert output_path.exists()
    assert len(timeline.scenes) == 1

    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert data["schema_version"] == "0.1.0"
    assert data["scenes"][0]["text"] == "Xin chào Việt Nam."
