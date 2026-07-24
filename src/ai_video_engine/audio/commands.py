"""FFmpeg command builders for audio extraction."""

from __future__ import annotations

from pathlib import Path


def build_extract_audio_command(
    input_media: Path,
    output_audio: Path,
    sample_rate: int = 16000,
    channels: int = 1,
) -> list[str]:
    """Build an FFmpeg command that extracts audio for speech-to-text."""
    return [
        "ffmpeg",
        "-y",
        "-i",
        str(input_media),
        "-vn",
        "-ac",
        str(channels),
        "-ar",
        str(sample_rate),
        str(output_audio),
    ]