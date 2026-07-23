"""Tests for the Sprint 1 transcription script."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from ai_video_engine.common.errors import InputFileError
from ai_video_engine.speech.schema import (
    Transcript,
    TranscriptSegment,
)
from scripts import transcribe as transcribe_script


def test_parser_uses_sprint_defaults() -> None:
    args = transcribe_script.build_parser().parse_args(
        ["input/video.mp4"]
    )

    assert args.input_path == Path("input/video.mp4")
    assert args.model == "medium"
    assert args.language == "vi"
    assert args.audio_path == Path("temp/audio.wav")
    assert args.transcript_path == Path("output/transcript.json")


def test_run_transcription_orchestrates_pipeline(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = Path("input/video.mp4")
    audio_path = tmp_path / "audio.wav"
    transcript_path = tmp_path / "transcript.json"

    transcript = Transcript(
        metadata={"language": "vi"},
        segments=[
            TranscriptSegment(
                id="seg_0001",
                start=0.0,
                end=1.0,
                duration=1.0,
                text="Xin chào.",
            )
        ],
    )

    calls: dict[str, Any] = {}

    def fake_extract_audio(
        *,
        input_media: Path,
        output_audio: Path,
    ) -> SimpleNamespace:
        calls["extract"] = (input_media, output_audio)
        return SimpleNamespace(output_path=output_audio)

    class FakeTranscriber:
        def __init__(self, model_name: str) -> None:
            calls["model_name"] = model_name

        def transcribe(
            self,
            transcribed_audio_path: Path,
            *,
            language: str,
            source_input: Path,
        ) -> Transcript:
            calls["transcribe"] = (
                transcribed_audio_path,
                language,
                source_input,
            )
            return transcript

    def fake_write_json(path: Path, data: Any) -> None:
        calls["write_json"] = (path, data)

    monkeypatch.setattr(
        transcribe_script,
        "extract_audio",
        fake_extract_audio,
    )
    monkeypatch.setattr(
        transcribe_script,
        "FasterWhisperTranscriber",
        FakeTranscriber,
    )
    monkeypatch.setattr(
        transcribe_script,
        "write_json",
        fake_write_json,
    )

    result = transcribe_script.run_transcription(
        input_path,
        audio_path=audio_path,
        transcript_path=transcript_path,
        model_name="small",
        language="vi",
    )

    assert result == transcript_path
    assert calls["extract"] == (input_path, audio_path)
    assert calls["model_name"] == "small"
    assert calls["transcribe"] == (
        audio_path,
        "vi",
        input_path,
    )
    assert calls["write_json"] == (
        transcript_path,
        transcript.model_dump(mode="json"),
    )


def test_run_transcription_warns_when_no_speech_detected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    audio_path = tmp_path / "audio.wav"
    transcript_path = tmp_path / "transcript.json"

    monkeypatch.setattr(
        transcribe_script,
        "extract_audio",
        lambda **kwargs: SimpleNamespace(
            output_path=kwargs["output_audio"]
        ),
    )

    class EmptyTranscriber:
        def __init__(self, model_name: str) -> None:
            self.model_name = model_name

        def transcribe(
            self,
            audio_path: Path,
            *,
            language: str,
            source_input: Path,
        ) -> Transcript:
            return Transcript(segments=[])

    monkeypatch.setattr(
        transcribe_script,
        "FasterWhisperTranscriber",
        EmptyTranscriber,
    )
    monkeypatch.setattr(
        transcribe_script,
        "write_json",
        lambda path, data: None,
    )

    transcribe_script.run_transcription(
        Path("input/video.mp4"),
        audio_path=audio_path,
        transcript_path=transcript_path,
        model_name="small",
        language="vi",
    )

    output = capsys.readouterr().out

    assert "[speech] warning: no speech segments detected" in output


def test_main_forwards_command_line_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_run_transcription(
        input_path: Path,
        *,
        audio_path: Path,
        transcript_path: Path,
        model_name: str,
        language: str,
    ) -> Path:
        captured.update(
            {
                "input_path": input_path,
                "audio_path": audio_path,
                "transcript_path": transcript_path,
                "model_name": model_name,
                "language": language,
            }
        )
        return transcript_path

    monkeypatch.setattr(
        transcribe_script,
        "run_transcription",
        fake_run_transcription,
    )

    exit_code = transcribe_script.main(
        [
            "input/video.mp4",
            "--model",
            "small",
            "--language",
            "en",
            "--audio",
            "temp/custom.wav",
            "--output",
            "output/custom.json",
        ]
    )

    assert exit_code == 0
    assert captured == {
        "input_path": Path("input/video.mp4"),
        "audio_path": Path("temp/custom.wav"),
        "transcript_path": Path("output/custom.json"),
        "model_name": "small",
        "language": "en",
    }


def test_main_handles_engine_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fail_transcription(*args: Any, **kwargs: Any) -> Path:
        raise InputFileError("Input media not found")

    monkeypatch.setattr(
        transcribe_script,
        "run_transcription",
        fail_transcription,
    )

    exit_code = transcribe_script.main(["missing.mp4"])
    error_output = capsys.readouterr().err

    assert exit_code == 1
    assert "[error] Input media not found" in error_output


def test_main_handles_output_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fail_transcription(*args: Any, **kwargs: Any) -> Path:
        raise OSError("disk is full")

    monkeypatch.setattr(
        transcribe_script,
        "run_transcription",
        fail_transcription,
    )

    exit_code = transcribe_script.main(["input/video.mp4"])
    error_output = capsys.readouterr().err

    assert exit_code == 1
    assert "[error] Could not write output: disk is full" in error_output