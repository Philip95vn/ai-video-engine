"""Command-line entry point for Sprint 2 timeline analysis."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from ai_video_engine.common.errors import AIVideoEngineError
from ai_video_engine.timeline.analyzer import (
    TimelineAnalyzerConfig,
    analyze_transcript_file,
)

DEFAULT_TIMELINE_PATH = Path("output/timeline.normalized.json")


def build_parser() -> argparse.ArgumentParser:
    """Build the Sprint 2 timeline analyzer argument parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Convert transcript JSON into a normalized renderable timeline JSON."
        )
    )

    parser.add_argument(
        "input_path",
        type=Path,
        help="Input transcript JSON path.",
    )
    parser.add_argument(
        "--output",
        dest="timeline_path",
        type=Path,
        default=DEFAULT_TIMELINE_PATH,
        help="Normalized timeline JSON path. Default: output/timeline.normalized.json.",
    )
    parser.add_argument(
        "--min-scene-duration",
        type=float,
        default=1.0,
        help="Minimum scene duration before merge. Default: 1.0.",
    )
    parser.add_argument(
        "--max-scene-duration",
        type=float,
        default=5.0,
        help="Maximum scene duration before split. Default: 5.0.",
    )
    parser.add_argument(
        "--max-scene-chars",
        type=int,
        default=80,
        help="Maximum scene text length before split. Default: 80.",
    )

    return parser


def run_analysis(
    input_path: Path,
    *,
    timeline_path: Path,
    min_scene_duration: float,
    max_scene_duration: float,
    max_scene_chars: int,
) -> Path:
    """Run transcript-to-timeline analysis and write JSON output."""
    config = TimelineAnalyzerConfig(
        min_scene_duration=min_scene_duration,
        max_scene_duration=max_scene_duration,
        max_scene_chars=max_scene_chars,
    )

    print(f"[timeline] analyzing {input_path}")

    timeline = analyze_transcript_file(
        input_path=input_path,
        output_path=timeline_path,
        config=config,
    )

    print(f"[timeline] scenes: {len(timeline.scenes)}")
    print(f"[timeline] wrote {timeline_path}")

    return timeline_path


def main(argv: Sequence[str] | None = None) -> int:
    """Run the timeline analyzer command."""
    args = build_parser().parse_args(argv)

    try:
        run_analysis(
            args.input_path,
            timeline_path=args.timeline_path,
            min_scene_duration=args.min_scene_duration,
            max_scene_duration=args.max_scene_duration,
            max_scene_chars=args.max_scene_chars,
        )
    except AIVideoEngineError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    except ValidationError as exc:
        print(f"[error] Invalid transcript or timeline data: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"[error] Could not read or write file: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
