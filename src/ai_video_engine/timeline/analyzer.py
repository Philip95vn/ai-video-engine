"""Deterministic transcript-to-timeline analyzer."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path

from ai_video_engine.common.json_io import read_json, write_json
from ai_video_engine.speech.schema import Transcript, TranscriptSegment
from ai_video_engine.timeline.schema import (
    NormalizedTimeline,
    TimelineScene,
    TimelineSpeaker,
    make_scene_id,
)


@dataclass(frozen=True)
class TimelineAnalyzerConfig:
    """Configuration for deterministic timeline normalization."""

    min_scene_duration: float = 1.0
    max_scene_duration: float = 5.0
    max_scene_chars: int = 80


@dataclass(frozen=True)
class SceneCandidate:
    """Internal scene candidate before final scene IDs are assigned."""

    source_segment_ids: list[str]
    start: float
    end: float
    text: str

    @property
    def duration(self) -> float:
        """Return rounded candidate duration."""
        return round(self.end - self.start, 2)


def clean_text(text: str) -> str:
    """Normalize whitespace while preserving Vietnamese characters."""
    return re.sub(r"\s+", " ", text).strip()


def load_transcript(path: Path) -> Transcript:
    """Load and validate a transcript JSON file."""
    return Transcript.model_validate(read_json(path))


def write_normalized_timeline(path: Path, timeline: NormalizedTimeline) -> None:
    """Write normalized timeline as UTF-8 JSON."""
    write_json(path, timeline.model_dump(mode="json"))


def analyze_transcript_file(
    input_path: Path,
    output_path: Path,
    config: TimelineAnalyzerConfig | None = None,
) -> NormalizedTimeline:
    """Load transcript, analyze it, and write normalized timeline JSON."""
    transcript = load_transcript(input_path)
    timeline = analyze_transcript(transcript, config=config)
    write_normalized_timeline(output_path, timeline)
    return timeline


def analyze_transcript(
    transcript: Transcript,
    config: TimelineAnalyzerConfig | None = None,
) -> NormalizedTimeline:
    """Convert transcript segments into normalized renderable scenes."""
    config = config or TimelineAnalyzerConfig()

    candidates: list[SceneCandidate] = []

    for segment in transcript.segments:
        candidates.extend(_segment_to_candidates(segment, config))

    merged = _merge_short_candidates(candidates, config)

    scenes = [
        TimelineScene(
            id=make_scene_id(index),
            source_segment_ids=candidate.source_segment_ids,
            start=candidate.start,
            end=candidate.end,
            duration=candidate.duration,
            speaker=TimelineSpeaker(),
            text=candidate.text,
        )
        for index, candidate in enumerate(merged, start=1)
    ]

    return NormalizedTimeline(
        metadata={
            "source": "timeline_analyzer",
            "source_schema_version": transcript.schema_version,
        },
        scenes=scenes,
    )


def _segment_to_candidates(
    segment: TranscriptSegment,
    config: TimelineAnalyzerConfig,
) -> list[SceneCandidate]:
    """Convert one transcript segment into one or more scene candidates."""
    text = clean_text(segment.text)

    split_count = max(
        1,
        math.ceil(segment.duration / config.max_scene_duration),
        math.ceil(len(text) / config.max_scene_chars),
    )

    if split_count == 1:
        return [
            SceneCandidate(
                source_segment_ids=[segment.id],
                start=segment.start,
                end=segment.end,
                text=text,
            )
        ]

    text_parts = _split_text_into_parts(text, split_count)
    time_parts = _split_time_range(segment.start, segment.end, split_count)

    return [
        SceneCandidate(
            source_segment_ids=[segment.id],
            start=start,
            end=end,
            text=text_part,
        )
        for text_part, (start, end) in zip(text_parts, time_parts)
    ]


def _merge_short_candidates(
    candidates: list[SceneCandidate],
    config: TimelineAnalyzerConfig,
) -> list[SceneCandidate]:
    """Merge very short adjacent candidates when safe."""
    if not candidates:
        return []

    merged: list[SceneCandidate] = []
    buffer = candidates[0]

    for candidate in candidates[1:]:
        combined_duration = round(candidate.end - buffer.start, 2)

        should_merge = (
            buffer.duration < config.min_scene_duration
            and combined_duration <= config.max_scene_duration
        )

        if should_merge:
            buffer = _merge_candidates(buffer, candidate)
            continue

        merged.append(buffer)
        buffer = candidate

    merged.append(buffer)

    return merged


def _merge_candidates(
    first: SceneCandidate,
    second: SceneCandidate,
) -> SceneCandidate:
    """Merge two adjacent scene candidates."""
    return SceneCandidate(
        source_segment_ids=[*first.source_segment_ids, *second.source_segment_ids],
        start=first.start,
        end=second.end,
        text=clean_text(f"{first.text} {second.text}"),
    )


def _split_text_into_parts(text: str, count: int) -> list[str]:
    """Split text into deterministic word chunks."""
    words = text.split()

    if not words:
        return [text] * count

    chunk_size = math.ceil(len(words) / count)
    parts = [
        " ".join(words[index : index + chunk_size])
        for index in range(0, len(words), chunk_size)
    ]

    while len(parts) < count:
        parts.append(parts[-1])

    return parts[:count]


def _split_time_range(start: float, end: float, count: int) -> list[tuple[float, float]]:
    """Split a time range into rounded non-overlapping parts."""
    duration = end - start
    part_duration = duration / count
    ranges: list[tuple[float, float]] = []

    for index in range(count):
        part_start = round(start + part_duration * index, 2)
        part_end = round(start + part_duration * (index + 1), 2)

        if index == count - 1:
            part_end = end

        ranges.append((part_start, part_end))

    return ranges
