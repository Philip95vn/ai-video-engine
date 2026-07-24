"""Pydantic models for speech transcript data."""

from __future__ import annotations

from math import isclose
from typing import Any, Self

from pydantic import BaseModel, Field, field_validator, model_validator


TIME_TOLERANCE = 0.05
TRANSCRIPT_SCHEMA_VERSION = "0.1.0"


def make_segment_id(index: int) -> str:
    """Create a deterministic, one-based segment ID."""
    if index < 1:
        raise ValueError("segment index must be at least 1")

    return f"seg_{index:04d}"


class TranscriptSegment(BaseModel):
    """One timestamped speech-to-text segment."""

    id: str = Field(min_length=1)
    start: float = Field(ge=0)
    end: float = Field(gt=0)
    duration: float = Field(gt=0)
    text: str = Field(min_length=1)

    @field_validator("id", "text")
    @classmethod
    def validate_non_blank(cls, value: str) -> str:
        """Reject blank IDs and text while removing surrounding whitespace."""
        value = value.strip()

        if not value:
            raise ValueError("must not be blank")

        return value

    @model_validator(mode="after")
    def validate_timing(self) -> Self:
        """Validate segment timing and calculated duration."""
        if self.end <= self.start:
            raise ValueError("end must be greater than start")

        expected_duration = self.end - self.start

        if not isclose(
            self.duration,
            expected_duration,
            rel_tol=0.0,
            abs_tol=TIME_TOLERANCE,
        ):
            raise ValueError(
                "duration must match end - start within "
                f"{TIME_TOLERANCE} seconds"
            )

        return self


class Transcript(BaseModel):
    """Validated speech-to-text transcript."""

    schema_version: str = TRANSCRIPT_SCHEMA_VERSION
    metadata: dict[str, Any] = Field(default_factory=dict)
    segments: list[TranscriptSegment]

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: str) -> str:
        """Reject an empty schema version."""
        value = value.strip()

        if not value:
            raise ValueError("schema_version must not be blank")

        return value

    @model_validator(mode="after")
    def validate_segments(self) -> Self:
        """Validate segment IDs and chronological ordering."""
        segment_ids = [segment.id for segment in self.segments]

        if len(segment_ids) != len(set(segment_ids)):
            raise ValueError("segment IDs must be unique")

        if any(
            current.start > following.start
            for current, following in zip(
                self.segments,
                self.segments[1:],
            )
        ):
            raise ValueError("segments must be sorted by start time")

        return self