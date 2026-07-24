"""Tests for the Faster Whisper speech-to-text engine."""

from __future__ import annotations

import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any
from unittest.mock import Mock

import pytest

from ai_video_engine.common.errors import SpeechToTextError
from ai_video_engine.speech.faster_whisper_engine import (
    FasterWhisperTranscriber,
)


class FakeModel:
    """Small fake that behaves like a Faster Whisper model."""

    def __init__(self, segments: list[Any]) -> None:
        self.segments = segments
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def transcribe(
        self,
        audio_path: str,
        **kwargs: Any,
    ) -> tuple[list[Any], object]:
        self.calls.append((audio_path, kwargs))
        return self.segments, object()


def create_audio_file(tmp_path: Path) -> Path:
    """Create a placeholder audio file for unit tests."""
    audio_path = tmp_path / "audio.wav"
    audio_path.write_bytes(b"fake audio")
    return audio_path


def test_transcriber_uses_cpu_defaults() -> None:
    transcriber = FasterWhisperTranscriber()

    assert transcriber.model_name == "medium"
    assert transcriber.device == "cpu"
    assert transcriber.compute_type == "int8"
    assert transcriber._model is None


def test_transcribe_rejects_missing_audio(tmp_path: Path) -> None:
    transcriber = FasterWhisperTranscriber()

    with pytest.raises(
        SpeechToTextError,
        match="Audio file not found",
    ):
        transcriber.transcribe(tmp_path / "missing.wav")


def test_load_model_is_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    created_models: list[tuple[str, str, str]] = []
    fake_model = object()

    def fake_whisper_model(
        model_name: str,
        *,
        device: str,
        compute_type: str,
    ) -> object:
        created_models.append((model_name, device, compute_type))
        return fake_model

    fake_module = ModuleType("faster_whisper")
    fake_module.WhisperModel = fake_whisper_model  # type: ignore[attr-defined]

    monkeypatch.setitem(sys.modules, "faster_whisper", fake_module)

    transcriber = FasterWhisperTranscriber(
        model_name="small",
        device="cpu",
        compute_type="int8",
    )

    first_result = transcriber._load_model()
    second_result = transcriber._load_model()

    assert first_result is fake_model
    assert second_result is fake_model
    assert created_models == [("small", "cpu", "int8")]


def test_load_model_wraps_constructor_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def failing_whisper_model(
        model_name: str,
        *,
        device: str,
        compute_type: str,
    ) -> object:
        raise RuntimeError("model failed")

    fake_module = ModuleType("faster_whisper")
    fake_module.WhisperModel = failing_whisper_model  # type: ignore[attr-defined]

    monkeypatch.setitem(sys.modules, "faster_whisper", fake_module)

    transcriber = FasterWhisperTranscriber(model_name="medium")

    with pytest.raises(
        SpeechToTextError,
        match="Failed to load Faster Whisper model: medium",
    ):
        transcriber._load_model()


def test_transcribe_converts_segments_and_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    audio_path = create_audio_file(tmp_path)
    source_input = Path("input/video.mp4")

    fake_model = FakeModel(
        [
            SimpleNamespace(
                start=0.0,
                end=0.5,
                text="   ",
            ),
            SimpleNamespace(
                start=0.124,
                end=1.876,
                text=" Xin chào. ",
            ),
            SimpleNamespace(
                start=2.0,
                end=3.25,
                text=" ĐẾN TRỄ? ",
            ),
        ]
    )

    transcriber = FasterWhisperTranscriber(model_name="small")
    monkeypatch.setattr(
        transcriber,
        "_load_model",
        lambda: fake_model,
    )

    transcript = transcriber.transcribe(
        audio_path,
        language="vi",
        vad_filter=False,
        beam_size=3,
        source_input=source_input,
    )

    assert [segment.id for segment in transcript.segments] == [
        "seg_0001",
        "seg_0002",
    ]

    first_segment = transcript.segments[0]

    assert first_segment.start == 0.12
    assert first_segment.end == 1.88
    assert first_segment.duration == 1.76
    assert first_segment.text == "Xin chào."

    assert transcript.metadata == {
        "speech_provider": "faster_whisper",
        "speech_model": "small",
        "language": "vi",
        "source_audio": str(audio_path),
        "device": "cpu",
        "compute_type": "int8",
        "source_input": str(source_input),
    }

    assert fake_model.calls == [
        (
            str(audio_path),
            {
                "language": "vi",
                "vad_filter": False,
                "beam_size": 3,
            },
        )
    ]


def test_transcribe_allows_empty_transcript(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    audio_path = create_audio_file(tmp_path)
    fake_model = FakeModel([])

    transcriber = FasterWhisperTranscriber()
    monkeypatch.setattr(
        transcriber,
        "_load_model",
        lambda: fake_model,
    )

    transcript = transcriber.transcribe(audio_path)

    assert transcript.segments == []


def test_transcribe_wraps_model_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    audio_path = create_audio_file(tmp_path)
    broken_model = Mock()
    broken_model.transcribe.side_effect = RuntimeError(
        "transcription failed"
    )

    transcriber = FasterWhisperTranscriber()
    monkeypatch.setattr(
        transcriber,
        "_load_model",
        lambda: broken_model,
    )

    with pytest.raises(
        SpeechToTextError,
        match="Failed to transcribe audio",
    ):
        transcriber.transcribe(audio_path)