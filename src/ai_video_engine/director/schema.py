"""Pydantic models for Visual Director output."""

from __future__ import annotations

from math import isclose
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ai_video_engine.director.prompts import (
    ALLOWED_EFFECTS,
    ALLOWED_EMOTIONS,
    ALLOWED_LAYOUTS,
)
from ai_video_engine.timeline.schema import (
    DEFAULT_SPEAKER_ID,
    DEFAULT_SPEAKER_SOURCE,
    TIME_TOLERANCE,
)

DIRECTOR_SCHEMA_VERSION = "0.1.0"
ALLOWED_EFFECT_INTENSITIES: tuple[str, ...] = ("low", "medium", "high")


class DirectorModel(BaseModel):
    """Strict base model for LLM-produced Visual Director data."""

    model_config = ConfigDict(extra="forbid")


class DirectorSpeaker(DirectorModel):
    """Speaker information preserved from the normalized timeline."""

    id: str = DEFAULT_SPEAKER_ID
    source: str = DEFAULT_SPEAKER_SOURCE

    @field_validator("id", "source")
    @classmethod
    def validate_non_blank(cls, value: str) -> str:
        """Reject blank speaker values."""

        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class DirectorKeyword(DirectorModel):
    """Keyword selected for visual emphasis."""

    text: str = Field(min_length=1)
    reason: str = Field(min_length=1)

    @field_validator("text", "reason")
    @classmethod
    def validate_non_blank(cls, value: str) -> str:
        """Reject blank keyword fields."""

        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class DirectorEffect(DirectorModel):
    """Visual effect requested by the Visual Director."""

    type: str
    target: str = Field(min_length=1)
    intensity: str = "medium"

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str) -> str:
        """Accept only supported effect names."""

        value = value.strip()
        if value not in ALLOWED_EFFECTS:
            allowed = ", ".join(ALLOWED_EFFECTS)
            raise ValueError(
                f"unsupported effect type: {value}; allowed: {allowed}"
            )
        return value

    @field_validator("target")
    @classmethod
    def validate_target(cls, value: str) -> str:
        """Reject blank effect targets."""

        value = value.strip()
        if not value:
            raise ValueError("target must not be blank")
        return value

    @field_validator("intensity")
    @classmethod
    def validate_intensity(cls, value: str) -> str:
        """Accept only supported effect intensities."""

        value = value.strip()
        if value not in ALLOWED_EFFECT_INTENSITIES:
            allowed = ", ".join(ALLOWED_EFFECT_INTENSITIES)
            raise ValueError(
                f"unsupported effect intensity: {value}; allowed: {allowed}"
            )
        return value


class DirectorScene(DirectorModel):
    """One AI-enriched scene in the Visual Director timeline."""

    id: str = Field(min_length=1)
    source_segment_ids: list[str] = Field(min_length=1)
    start: float = Field(ge=0)
    end: float = Field(gt=0)
    duration: float = Field(gt=0)
    speaker: DirectorSpeaker = Field(default_factory=DirectorSpeaker)
    text: str = Field(min_length=1)
    lines: list[str] = Field(min_length=1, max_length=6)
    emotion: str
    layout: str
    keywords: list[DirectorKeyword] = Field(default_factory=list)
    effects: list[DirectorEffect] = Field(default_factory=list)
    icon_query: str | None = None

    @field_validator("id", "text")
    @classmethod
    def validate_non_blank(cls, value: str) -> str:
        """Reject blank scene IDs and source text."""

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
            raise ValueError(
                "source_segment_ids must not contain blank values"
            )
        if len(cleaned) != len(set(cleaned)):
            raise ValueError(
                "source_segment_ids must be unique within a scene"
            )
        return cleaned

    @field_validator("lines")
    @classmethod
    def validate_lines(cls, values: list[str]) -> list[str]:
        """Reject blank display lines."""

        cleaned = [value.strip() for value in values]
        if any(not value for value in cleaned):
            raise ValueError("lines must not contain blank values")
        return cleaned

    @field_validator("emotion")
    @classmethod
    def validate_emotion(cls, value: str) -> str:
        """Accept only emotions supported by the prompt contract."""

        value = value.strip()
        if value not in ALLOWED_EMOTIONS:
            allowed = ", ".join(ALLOWED_EMOTIONS)
            raise ValueError(
                f"unsupported emotion: {value}; allowed: {allowed}"
            )
        return value

    @field_validator("layout")
    @classmethod
    def validate_layout(cls, value: str) -> str:
        """Accept only layouts supported by the prompt contract."""

        value = value.strip()
        if value not in ALLOWED_LAYOUTS:
            allowed = ", ".join(ALLOWED_LAYOUTS)
            raise ValueError(
                f"unsupported layout: {value}; allowed: {allowed}"
            )
        return value

    @field_validator("icon_query")
    @classmethod
    def validate_icon_query(cls, value: str | None) -> str | None:
        """Allow null or a non-blank icon search phrase."""

        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("icon_query must not be blank")
        return value

    @field_validator("keywords")
    @classmethod
    def validate_unique_keywords(
        cls,
        values: list[DirectorKeyword],
    ) -> list[DirectorKeyword]:
        """Reject duplicate keyword text within one scene."""

        normalized = [keyword.text.casefold() for keyword in values]
        if len(normalized) != len(set(normalized)):
            raise ValueError(
                "keyword text must be unique within a scene"
            )
        return values

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


class DirectorTimeline(DirectorModel):
    """Validated Visual Director output timeline."""

    schema_version: str = DIRECTOR_SCHEMA_VERSION
    metadata: dict[str, Any] = Field(default_factory=dict)
    scenes: list[DirectorScene]

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: str) -> str:
        """Reject unsupported Visual Director schema versions."""

        value = value.strip()
        if value != DIRECTOR_SCHEMA_VERSION:
            raise ValueError(
                "unsupported director schema version: "
                f"{value}; expected: {DIRECTOR_SCHEMA_VERSION}"
            )
        return value

    @model_validator(mode="after")
    def validate_scenes(self) -> Self:
        """Validate scene IDs and chronological ordering."""

        scene_ids = [scene.id for scene in self.scenes]
        if len(scene_ids) != len(set(scene_ids)):
            raise ValueError("scene IDs must be unique")

        for current, following in zip(
            self.scenes,
            self.scenes[1:],
        ):
            if current.start > following.start:
                raise ValueError(
                    "scenes must be sorted by start time"
                )
            if current.end > following.start + TIME_TOLERANCE:
                raise ValueError("scenes must not overlap")

        return self
