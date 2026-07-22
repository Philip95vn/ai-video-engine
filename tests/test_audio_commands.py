from pathlib import Path

from ai_video_engine.audio.commands import build_extract_audio_command


def test_build_extract_audio_command_default_values():
    cmd = build_extract_audio_command(
        input_media=Path("input/video.mp4"),
        output_audio=Path("temp/audio.wav"),
    )

    assert cmd == [
        "ffmpeg",
        "-y",
        "-i",
        "input\\video.mp4",
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "temp\\audio.wav",
    ]


def test_build_extract_audio_command_custom_values():
    cmd = build_extract_audio_command(
        input_media=Path("input/test.mp4"),
        output_audio=Path("temp/test.wav"),
        sample_rate=44100,
        channels=2,
    )

    assert "-ar" in cmd
    assert "44100" in cmd
    assert "-ac" in cmd
    assert "2" in cmd