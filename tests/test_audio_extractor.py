from pathlib import Path
import subprocess

import pytest

from ai_video_engine.audio import extractor
from ai_video_engine.audio.extractor import extract_audio
from ai_video_engine.common.errors import (
    AudioExtractionError,
    InputFileError,
    MissingFFmpegError,
)


def test_extract_audio_rejects_missing_input(tmp_path):
    with pytest.raises(InputFileError):
        extract_audio(
            input_media=tmp_path / "missing.mp4",
            output_audio=tmp_path / "audio.wav",
        )


def test_extract_audio_rejects_missing_ffmpeg(tmp_path, monkeypatch):
    input_media = tmp_path / "video.mp4"
    input_media.write_bytes(b"fake video")

    monkeypatch.setattr(extractor.shutil, "which", lambda name: None)

    with pytest.raises(MissingFFmpegError):
        extract_audio(
            input_media=input_media,
            output_audio=tmp_path / "audio.wav",
        )


def test_extract_audio_success(tmp_path, monkeypatch):
    input_media = tmp_path / "video.mp4"
    output_audio = tmp_path / "audio.wav"
    input_media.write_bytes(b"fake video")

    monkeypatch.setattr(extractor.shutil, "which", lambda name: "ffmpeg")

    def fake_run(cmd, check, capture_output, text):
        output_audio.write_bytes(b"fake audio")
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(extractor.subprocess, "run", fake_run)

    result = extract_audio(
        input_media=input_media,
        output_audio=output_audio,
    )

    assert result.input_path == input_media
    assert result.output_path == output_audio
    assert result.sample_rate == 16000
    assert result.channels == 1
    assert output_audio.exists()


def test_extract_audio_raises_when_ffmpeg_fails(tmp_path, monkeypatch):
    input_media = tmp_path / "video.mp4"
    input_media.write_bytes(b"fake video")

    monkeypatch.setattr(extractor.shutil, "which", lambda name: "ffmpeg")

    def fake_run(cmd, check, capture_output, text):
        raise subprocess.CalledProcessError(returncode=1, cmd=cmd)

    monkeypatch.setattr(extractor.subprocess, "run", fake_run)

    with pytest.raises(AudioExtractionError):
        extract_audio(
            input_media=input_media,
            output_audio=tmp_path / "audio.wav",
        )