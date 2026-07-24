"""Pydantic models for normalized timeline data."""

from __future__ import annotations

from math import isclose
from typing import Any, Self

from pydantic import BaseModel, Field, field_validator, model_validator

TIME_TOLERANCE = 0.05
TIMELINE_SCHEMA_VERSION = "0.1.0"
DEFAULT_SPEAKER_ID = "SPEAKER_00"
DEFAULT_SPEAKER_SOURCE = "unknown"


def make_scene_id(index: int) -> str:
    """Create a deterministic, one-based scene ID."""
    if index < 1:
        raise ValueError("scene index must be at least 1")
    return f"scene_{index:04d}"


class TimelineSpeaker(BaseModel):
    """Speaker placeholder for a normalized timeline scene."""

    id: str = DEFAULT_SPEAKER_ID
    source: str = DEFAULT_SPEAKER_SOURCE

    @field_validator("id", "source")
    @classmethod
    def validate_non_blank(cls, value: str) -> str:
        """Reject blank speaker fields while removing surrounding whitespace."""
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class TimelineScene(BaseModel):
    """One renderable normalized scene."""

    id: str = Field(min_length=1)
    source_segment_ids: list[str] = Field(min_length=1)
    start: float = Field(ge=0)
    end: float = Field(gt=0)
    duration: float = Field(gt=0)
    speaker: TimelineSpeaker = Field(default_factory=TimelineSpeaker)
    text: str = Field(min_length=1)

    @field_validator("id", "text")
    @classmethod
    def validate_non_blank(cls, value: str) -> str:
        """Reject blank IDs and text while removing surrounding whitespace."""
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value

    @field_validator("source_segment_ids")
    @classmethod
    def validate_source_segment_ids(cls, values: list[str]) -> list[str]:
        """Reject blank or duplicated source segment IDs."""
        cleaned = [value.strip() for value in values]

        if any(not value for value in cleaned):
            raise ValueError("source_segment_ids must not contain blank values")

        if len(cleaned) != len(set(cleaned)):
            raise ValueError("source_segment_ids must be unique within a scene")

        return cleaned

    @model_validator(mode="after")
    def validate_timing(self) -> Self:
        """Validate scene timing and calculated duration."""
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


class NormalizedTimeline(BaseModel):
    """Validated normalized timeline."""

    schema_version: str = TIMELINE_SCHEMA_VERSION
    metadata: dict[str, Any] = Field(default_factory=dict)
    scenes: list[TimelineScene]

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: str) -> str:
        """Reject an empty schema version."""
        value = value.strip()
        if not value:
            raise ValueError("schema_version must not be blank")
        return value

    @model_validator(mode="after")
    def validate_scenes(self) -> Self:
        """Validate scene IDs and chronological ordering."""
        scene_ids = [scene.id for scene in self.scenes]

        if len(scene_ids) != len(set(scene_ids)):
            raise ValueError("scene IDs must be unique")

        for current, following in zip(self.scenes, self.scenes[1:]):
            if current.start > following.start:
                raise ValueError("scenes must be sorted by start time")

            if current.end > following.start + TIME_TOLERANCE:
                raise ValueError("scenes must not overlap")

        return self
