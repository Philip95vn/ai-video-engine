"""Command-line entry point for Sprint 1 speech-to-text."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from ai_video_engine.audio.extractor import extract_audio
from ai_video_engine.common.errors import AIVideoEngineError
from ai_video_engine.common.json_io import write_json
from ai_video_engine.speech.faster_whisper_engine import (
    FasterWhisperTranscriber,
)


DEFAULT_AUDIO_PATH = Path("temp/audio.wav")
DEFAULT_TRANSCRIPT_PATH = Path("output/transcript.json")


def build_parser() -> argparse.ArgumentParser:
    """Build the Sprint 1 transcription argument parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Extract audio from an input media file and create "
            "a timestamped transcript JSON."
        )
    )
    parser.add_argument(
        "input_path",
        type=Path,
        help="Input video or audio path.",
    )
    parser.add_argument(
        "--model",
        default="medium",
        help="Faster Whisper model name. Default: medium.",
    )
    parser.add_argument(
        "--language",
        default="vi",
        help="Speech language code. Default: vi.",
    )
    parser.add_argument(
        "--audio",
        dest="audio_path",
        type=Path,
        default=DEFAULT_AUDIO_PATH,
        help="Extracted WAV path. Default: temp/audio.wav.",
    )
    parser.add_argument(
        "--output",
        dest="transcript_path",
        type=Path,
        default=DEFAULT_TRANSCRIPT_PATH,
        help="Transcript JSON path. Default: output/transcript.json.",
    )
    return parser


def run_transcription(
    input_path: Path,
    *,
    audio_path: Path,
    transcript_path: Path,
    model_name: str,
    language: str,
) -> Path:
    """Run audio extraction, transcription, and JSON writing."""
    print(f"[audio] extracting audio from {input_path}")

    extraction_result = extract_audio(
        input_media=input_path,
        output_audio=audio_path,
    )

    print(f"[audio] wrote {extraction_result.output_path}")
    print(f"[speech] loading faster-whisper model: {model_name}")

    transcriber = FasterWhisperTranscriber(model_name=model_name)

    print(f"[speech] transcribing language={language}")

    transcript = transcriber.transcribe(
        extraction_result.output_path,
        language=language,
        source_input=input_path,
    )

    if not transcript.segments:
        print("[speech] warning: no speech segments detected")

    write_json(
        transcript_path,
        transcript.model_dump(mode="json"),
    )

    print(f"[speech] wrote {transcript_path}")

    return transcript_path


def main(argv: Sequence[str] | None = None) -> int:
    """Run the transcription command."""
    args = build_parser().parse_args(argv)

    try:
        run_transcription(
            args.input_path,
            audio_path=args.audio_path,
            transcript_path=args.transcript_path,
            model_name=args.model,
            language=args.language,
        )
    except AIVideoEngineError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"[error] Could not write output: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())