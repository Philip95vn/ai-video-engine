from ai_video_engine.common.json_io import read_json, write_json


def test_write_json_preserves_vietnamese(tmp_path):
    path = tmp_path / "test.json"
    data = {"text": "ĐẾN TRỄ? BÁO THỨC!"}

    write_json(path, data)

    raw = path.read_text(encoding="utf-8")
    assert "ĐẾN TRỄ" in raw
    assert "BÁO THỨC" in raw

    loaded = read_json(path)
    assert loaded["text"] == data["text"]