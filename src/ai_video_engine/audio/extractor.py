"""Audio extraction using FFmpeg."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from ai_video_engine.audio.commands import build_extract_audio_command
from ai_video_engine.common.errors import (
    AudioExtractionError,
    InputFileError,
    MissingFFmpegError,
)


@dataclass(frozen=True)
class AudioExtractionResult:
    """Result of audio extraction."""

    input_path: Path
    output_path: Path
    sample_rate: int
    channels: int


def ensure_ffmpeg_available() -> None:
    """Raise an explicit error if FFmpeg is not available."""
    if shutil.which("ffmpeg") is None:
        raise MissingFFmpegError(
            "FFmpeg was not found. Install it with: winget install Gyan.FFmpeg "
            "then restart VS Code or your terminal."
        )


def extract_audio(
    input_media: Path,
    output_audio: Path,
    sample_rate: int = 16000,
    channels: int = 1,
) -> AudioExtractionResult:
    """Extract mono WAV audio from input media."""
    if not input_media.exists():
        raise InputFileError(f"Input media not found: {input_media}")

    ensure_ffmpeg_available()

    output_audio.parent.mkdir(parents=True, exist_ok=True)

    cmd = build_extract_audio_command(
        input_media=input_media,
        output_audio=output_audio,
        sample_rate=sample_rate,
        channels=channels,
    )

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        raise AudioExtractionError(
            f"FFmpeg failed while extracting audio from {input_media}."
        ) from exc

    if not output_audio.exists():
        raise AudioExtractionError(f"Expected audio output was not created: {output_audio}")

    return AudioExtractionResult(
        input_path=input_media,
        output_path=output_audio,
        sample_rate=sample_rate,
        channels=channels,
    )