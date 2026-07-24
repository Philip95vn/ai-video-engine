import json

from ai_video_engine.common.json_io import write_json
from scripts.analyze_timeline import DEFAULT_TIMELINE_PATH, build_parser, main


def test_build_parser_uses_default_output_path():
    args = build_parser().parse_args(["output/transcript.json"])

    assert args.input_path.name == "transcript.json"
    assert args.timeline_path == DEFAULT_TIMELINE_PATH


def test_analyze_timeline_script_writes_output(tmp_path):
    input_path = tmp_path / "transcript.json"
    output_path = tmp_path / "timeline.normalized.json"

    write_json(
        input_path,
        {
            "schema_version": "0.1.0",
            "segments": [
                {
                    "id": "seg_0001",
                    "start": 0.0,
                    "end": 2.0,
                    "duration": 2.0,
                    "text": "Xin chào Việt Nam.",
                }
            ],
        },
    )

    exit_code = main([str(input_path), "--output", str(output_path)])

    assert exit_code == 0
    assert output_path.exists()

    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert data["schema_version"] == "0.1.0"
    assert data["scenes"][0]["id"] == "scene_0001"
    assert data["scenes"][0]["text"] == "Xin chào Việt Nam."


def test_analyze_timeline_script_returns_error_for_missing_input(tmp_path):
    output_path = tmp_path / "timeline.normalized.json"

    exit_code = main(
        [
            str(tmp_path / "missing.json"),
            "--output",
            str(output_path),
        ]
    )

    assert exit_code == 1
    assert not output_path.exists()
