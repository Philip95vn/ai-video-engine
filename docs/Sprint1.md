# Sprint1.md

# AI Video Engine - Sprint 1: Speech To Text

## 0. Purpose

This document defines **Sprint 1** for AI Video Engine.

Sprint 1 is the first implementation sprint after the documentation foundation.

The goal is simple and important:

```text
input video/audio → output/transcript.json
```

Sprint 1 does not render video.

Sprint 1 does not call the Visual Director.

Sprint 1 does not select icons.

Sprint 1 does not create animations.

Sprint 1 only proves that the engine can reliably extract audio and produce timestamped transcript JSON.

This document should be read together with:

```text
AGENTS.md
PROJECT_RULES.md
README.md
ROADMAP.md
docs/Architecture.md
docs/Pipeline.md
docs/JSONSchema.md
docs/AIDesign.md
docs/CodingStandard.md
docs/DecisionLog.md
```

---

## 1. Sprint 1 summary

Sprint name:

```text
Speech To Text
```

Sprint goal:

```text
video.mp4 → transcript.json
```

Main output:

```text
output/transcript.json
```

Supporting output:

```text
temp/audio.wav
```

Primary tools:

```text
FFmpeg
Faster Whisper
Python 3.11
Pydantic
```

---

## 2. Sprint 1 one-line goal

```text
Given an input video with Vietnamese speech, extract audio and produce a valid timestamped transcript JSON.
```

---

## 3. Why Sprint 1 matters

All later stages depend on transcript data.

Without transcript JSON, the engine cannot:

- create scenes
- detect speakers
- identify keywords
- generate visual timeline
- render text
- sync video with voice
- preserve original timing

Sprint 1 is the foundation of the real pipeline.

---

## 4. Sprint 1 pipeline

```text
Input Video / Audio
        ↓
Validate Input
        ↓
Extract Audio
        ↓
temp/audio.wav
        ↓
Speech To Text
        ↓
output/transcript.json
        ↓
Validate Transcript
```

---

## 5. Sprint 1 input

Primary input:

```text
input/video.mp4
```

Supported later:

```text
input/audio.wav
input/audio.mp3
input/video.mov
```

For Sprint 1, focus on MP4 video first.

---

## 6. Sprint 1 output

Required output:

```text
output/transcript.json
```

Required intermediate output:

```text
temp/audio.wav
```

Optional debug output:

```text
output/stt_report.json
```

Debug output is optional for Sprint 1.

---

## 7. Sprint 1 transcript example

Expected transcript JSON:

```json
{
  "schema_version": "0.1.0",
  "metadata": {
    "speech_provider": "faster_whisper",
    "speech_model": "medium",
    "language": "vi",
    "source_audio": "temp/audio.wav",
    "source_input": "input/video.mp4"
  },
  "segments": [
    {
      "id": "seg_0001",
      "start": 0.25,
      "end": 2.16,
      "duration": 1.91,
      "text": "Ê! Sao hôm nay đến trễ?"
    },
    {
      "id": "seg_0002",
      "start": 2.30,
      "end": 3.40,
      "duration": 1.10,
      "text": "Tại báo thức."
    }
  ]
}
```

---

## 8. Sprint 1 scope

Sprint 1 includes:

- input validation
- FFmpeg availability check
- audio extraction command builder
- audio extraction function
- Faster Whisper transcription
- transcript data model
- transcript JSON writer
- transcript validation
- simple script or command to run stage
- basic tests
- documentation update

---

## 9. Sprint 1 non-scope

Sprint 1 does not include:

- timeline analyzer
- Visual Director LLM
- icon selector
- renderer
- exporter
- final MP4
- speaker diarization
- word-level timing
- avatars
- animations
- templates
- UI
- batch mode
- TTS

Do not expand Sprint 1 beyond transcription.

---

## 10. Sprint 1 modules

Sprint 1 uses these modules:

```text
src/audio/
src/speech/
src/common/
src/config/
tests/
scripts/
```

---

## 11. Recommended package layout decision

Before coding Sprint 1, make one important decision.

Recommended long-term package structure:

```text
src/ai_video_engine/
├── audio/
├── speech/
├── timeline/
├── director/
├── embedding/
├── renderer/
├── exporter/
├── assets/
├── common/
└── config/
```

This is better than:

```text
src/audio/
src/speech/
...
```

because it supports standard Python packaging.

Recommended Sprint 1 action:

```text
Move or create code under src/ai_video_engine/
```

Suggested ADR:

```text
ADR-0041 - Use src/ai_video_engine package layout
```

If this decision is accepted, Sprint 1 files should use the package layout.

---

## 12. Recommended Sprint 1 folder structure

Recommended after package layout decision:

```text
src/
└── ai_video_engine/
    ├── __init__.py
    │
    ├── audio/
    │   ├── __init__.py
    │   ├── commands.py
    │   ├── extractor.py
    │   └── probe.py
    │
    ├── speech/
    │   ├── __init__.py
    │   ├── schema.py
    │   ├── faster_whisper_engine.py
    │   └── transcript_writer.py
    │
    ├── common/
    │   ├── __init__.py
    │   ├── errors.py
    │   ├── json_io.py
    │   ├── paths.py
    │   └── subprocess_utils.py
    │
    └── config/
        ├── __init__.py
        └── settings.py
```

Scripts:

```text
scripts/
└── transcribe.py
```

Tests:

```text
tests/
├── test_audio_commands.py
├── test_transcript_schema.py
├── test_json_io.py
└── test_sprint1_smoke.py
```

---

## 13. Minimal Sprint 1 file list

Minimum files to create:

```text
src/ai_video_engine/common/errors.py
src/ai_video_engine/common/json_io.py
src/ai_video_engine/audio/commands.py
src/ai_video_engine/audio/extractor.py
src/ai_video_engine/speech/schema.py
src/ai_video_engine/speech/faster_whisper_engine.py
scripts/transcribe.py
tests/test_audio_commands.py
tests/test_transcript_schema.py
```

---

## 14. Sprint 1 responsibilities by file

### 14.1 `common/errors.py`

Defines project-specific exceptions.

### 14.2 `common/json_io.py`

Reads and writes UTF-8 JSON.

### 14.3 `audio/commands.py`

Builds FFmpeg commands.

### 14.4 `audio/extractor.py`

Runs FFmpeg to extract audio.

### 14.5 `speech/schema.py`

Defines Transcript and TranscriptSegment models.

### 14.6 `speech/faster_whisper_engine.py`

Runs Faster Whisper and returns Transcript.

### 14.7 `scripts/transcribe.py`

Thin wrapper for user testing.

### 14.8 `tests/test_audio_commands.py`

Tests command construction.

### 14.9 `tests/test_transcript_schema.py`

Tests transcript validation.

---

## 15. Sprint 1 dependency requirements

Required Python packages:

```text
faster-whisper
pydantic
rich
orjson
```

Optional but useful:

```text
pytest
```

External tool:

```text
FFmpeg
```

---

## 16. Sprint 1 requirements.txt check

`requirements.txt` should include at least:

```text
faster-whisper
pydantic
rich
orjson
```

If not present, add them.

Do not add WhisperX in Sprint 1.

Do not add pyannote in Sprint 1.

---

## 17. Sprint 1 environment checks

Before coding, verify:

```bash
python --version
ffmpeg -version
pip show faster-whisper
```

On Windows PowerShell:

```powershell
python --version
ffmpeg -version
pip show faster-whisper
```

Expected Python:

```text
Python 3.11+
```

---

## 18. Sprint 1 FFmpeg requirement

FFmpeg must be available in PATH.

Check:

```bash
ffmpeg -version
```

If not available on Windows:

```powershell
winget install Gyan.FFmpeg
```

Then restart VS Code.

---

## 19. Sprint 1 Faster Whisper requirement

Install:

```bash
pip install faster-whisper
```

Test import:

```bash
python -c "from faster_whisper import WhisperModel; print('ok')"
```

---

## 20. Sprint 1 virtual environment

Use virtual environment.

Create:

```bash
python -m venv .venv
```

Activate Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate Mac/Linux:

```bash
source .venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

---

## 21. Sprint 1 command goal

By the end of Sprint 1, this should work:

```bash
python scripts/transcribe.py input/video.mp4
```

Expected outputs:

```text
temp/audio.wav
output/transcript.json
```

Optional future command:

```bash
python -m ai_video_engine transcribe input/video.mp4
```

---

## 22. Sprint 1 config defaults

Recommended defaults:

```yaml
audio:
  sample_rate: 16000
  channels: 1
  output_format: wav

speech:
  provider: faster_whisper
  model: medium
  language: vi
  device: cpu
  compute_type: int8
  vad_filter: true
  beam_size: 5

paths:
  input_dir: input
  temp_dir: temp
  output_dir: output
```

For Sprint 1, config may be hardcoded centrally in one settings module if config loader is not ready.

Do not scatter defaults across many files.

---

## 23. Sprint 1 audio format

Recommended STT audio format:

```text
WAV
mono
16000 Hz
```

FFmpeg command:

```bash
ffmpeg -y -i input/video.mp4 -vn -ac 1 -ar 16000 temp/audio.wav
```

---

## 24. Sprint 1 audio extraction command builder

Create function:

```python
def build_extract_audio_command(
    input_video: Path,
    output_audio: Path,
    sample_rate: int = 16000,
    channels: int = 1,
) -> list[str]:
    ...
```

Expected output:

```python
[
    "ffmpeg",
    "-y",
    "-i",
    "input/video.mp4",
    "-vn",
    "-ac",
    "1",
    "-ar",
    "16000",
    "temp/audio.wav",
]
```

---

## 25. Sprint 1 audio extraction function

Create function:

```python
def extract_audio(
    input_video: Path,
    output_audio: Path,
    sample_rate: int = 16000,
    channels: int = 1,
) -> AudioExtractionResult:
    ...
```

Responsibilities:

- validate input exists
- validate FFmpeg available
- create output folder
- run FFmpeg
- validate output exists
- return result

---

## 26. Sprint 1 AudioExtractionResult

Suggested dataclass:

```python
@dataclass
class AudioExtractionResult:
    input_path: Path
    output_path: Path
    sample_rate: int
    channels: int
```

Optional fields:

```python
duration: float | None = None
```

Duration probing can be added later.

---

## 27. Sprint 1 transcript schema

Create Pydantic models:

```python
class TranscriptSegment(BaseModel):
    id: str
    start: float
    end: float
    duration: float
    text: str
```

```python
class Transcript(BaseModel):
    schema_version: str = "0.1.0"
    metadata: dict[str, Any] = Field(default_factory=dict)
    segments: list[TranscriptSegment]
```

---

## 28. Sprint 1 transcript segment validation

Validate:

- start >= 0
- end > start
- duration > 0
- duration ≈ end - start
- text not empty

Use tolerance:

```python
TIME_TOLERANCE = 0.05
```

---

## 29. Sprint 1 transcript validation

Validate:

- schema_version exists
- segments list exists
- segment IDs unique
- segments sorted
- no negative timestamps
- no empty text
- UTF-8 preserved

---

## 30. Sprint 1 segment ID generation

Create deterministic IDs:

```python
def make_segment_id(index: int) -> str:
    return f"seg_{index:04d}"
```

Use 1-based indexing:

```text
seg_0001
seg_0002
seg_0003
```

---

## 31. Sprint 1 Faster Whisper engine

Suggested class:

```python
class FasterWhisperTranscriber:
    def __init__(
        self,
        model_name: str = "medium",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        ...

    def transcribe(
        self,
        audio_path: Path,
        language: str = "vi",
    ) -> Transcript:
        ...
```

---

## 32. Sprint 1 Faster Whisper call

Concept:

```python
segments, info = model.transcribe(
    str(audio_path),
    language="vi",
    vad_filter=True,
    beam_size=5,
)
```

For each segment:

```python
TranscriptSegment(
    id=make_segment_id(index),
    start=round(segment.start, 2),
    end=round(segment.end, 2),
    duration=round(segment.end - segment.start, 2),
    text=segment.text.strip(),
)
```

---

## 33. Sprint 1 transcript metadata

Recommended metadata:

```json
{
  "speech_provider": "faster_whisper",
  "speech_model": "medium",
  "language": "vi",
  "source_audio": "temp/audio.wav",
  "source_input": "input/video.mp4"
}
```

Optional:

```json
{
  "duration": 28.4,
  "device": "cpu",
  "compute_type": "int8"
}
```

---

## 34. Sprint 1 JSON writer

Use helper:

```python
def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
```

This preserves Vietnamese text.

---

## 35. Sprint 1 script behavior

`scripts/transcribe.py` should:

1. accept input path argument
2. default output paths
3. extract audio
4. transcribe audio
5. write transcript JSON
6. print output path

Example:

```bash
python scripts/transcribe.py input/video.mp4
```

Optional flags later:

```bash
--model small
--language vi
--output output/transcript.json
--audio temp/audio.wav
```

---

## 36. Sprint 1 simple script interface

Initial script can be:

```bash
python scripts/transcribe.py input/video.mp4
```

No need for complex CLI in first commit.

Use `argparse`.

---

## 37. Sprint 1 logging

Use simple logs:

```text
[audio] extracting audio from input/video.mp4
[audio] wrote temp/audio.wav
[speech] loading faster-whisper model: medium
[speech] transcribing language=vi
[speech] wrote output/transcript.json
```

---

## 38. Sprint 1 errors

Expected errors:

- input file not found
- FFmpeg not found
- FFmpeg extraction failed
- Faster Whisper not installed
- model load failed
- audio file missing
- empty transcript
- invalid transcript timing
- output path not writable

Errors should be clear.

---

## 39. Sprint 1 MissingFFmpegError

Example message:

```text
FFmpeg was not found.
Install it with:
winget install Gyan.FFmpeg
Then restart VS Code or terminal.
```

---

## 40. Sprint 1 missing input error

Example message:

```text
Input media not found: input/video.mp4
Place a video in input/ or pass a valid file path.
```

---

## 41. Sprint 1 model load error

Example message:

```text
Failed to load Faster Whisper model: medium
Try a smaller model such as: small
```

---

## 42. Sprint 1 empty transcript behavior

If no speech is detected:

Option A:

```text
write empty transcript with warning
```

Option B:

```text
fail
```

Recommended Sprint 1 behavior:

```text
write empty transcript with warning
```

But if audio extraction failed, fail.

---

## 43. Sprint 1 tests overview

Minimum tests:

```text
test_audio_commands.py
test_transcript_schema.py
test_json_io.py
```

Optional integration test:

```text
test_sprint1_integration.py
```

Integration test can be skipped if FFmpeg/model not available.

---

## 44. Sprint 1 test: audio command builder

Test:

```python
def test_build_extract_audio_command():
    cmd = build_extract_audio_command(
        Path("input/video.mp4"),
        Path("temp/audio.wav"),
    )

    assert cmd[0] == "ffmpeg"
    assert "-i" in cmd
    assert "input/video.mp4" in cmd
    assert "temp/audio.wav" in cmd
```

This does not require FFmpeg.

---

## 45. Sprint 1 test: transcript segment validation

Test valid segment:

```python
segment = TranscriptSegment(
    id="seg_0001",
    start=0.0,
    end=1.5,
    duration=1.5,
    text="Xin chào.",
)
```

Test invalid duration:

```python
with pytest.raises(ValueError):
    TranscriptSegment(
        id="seg_0001",
        start=1.0,
        end=0.5,
        duration=-0.5,
        text="bad",
    )
```

---

## 46. Sprint 1 test: Vietnamese JSON

Test that Vietnamese is not escaped.

Expected output contains:

```text
Xin chào
ĐẾN TRỄ
BÁO THỨC
```

not only Unicode escapes.

---

## 47. Sprint 1 integration test

Optional integration test:

```text
generate tiny audio
run transcriber
write transcript
```

But do not require model download in default CI.

Mark as integration.

---

## 48. Sprint 1 no-GPU rule

Sprint 1 must work with:

```python
device="cpu"
compute_type="int8"
```

Do not require CUDA.

---

## 49. Sprint 1 model choice

Default:

```text
medium
```

If machine is weak:

```text
small
```

If accuracy needed later:

```text
large-v3
```

Model name must be configurable.

---

## 50. Sprint 1 speed expectation

Speed varies by machine.

Sprint 1 should prioritize correctness over speed.

Optimization later.

---

## 51. Sprint 1 output quality expectation

STT output may not be perfect.

That is acceptable.

Sprint 1 success means:

- transcript exists
- timestamps exist
- JSON validates

Perfect punctuation is not required.

---

## 52. Sprint 1 speaker expectation

Sprint 1 does not require speaker diarization.

Transcript segments may not have speaker fields.

Speaker support comes later.

If speaker field exists, it should be optional.

---

## 53. Sprint 1 word timing expectation

Sprint 1 does not require word-level timing.

Segment-level timing is enough.

Word-level timing comes later with WhisperX or alignment.

---

## 54. Sprint 1 language expectation

Default language:

```text
vi
```

Language should be configurable.

If language is unknown, future config may allow auto-detection.

For Sprint 1, use Vietnamese by default.

---

## 55. Sprint 1 file overwrite policy

During development:

```text
overwrite temp/audio.wav
overwrite output/transcript.json
```

This is acceptable.

Later CLI may support `--no-overwrite`.

---

## 56. Sprint 1 cache policy

If transcript exists, early script may overwrite.

Later cache behavior can skip stages.

For Sprint 1, keep it simple.

---

## 57. Sprint 1 report policy

A separate STT report is optional.

Do not block Sprint 1 on report generation.

But transcript metadata should include model info.

---

## 58. Sprint 1 docs update policy

When Sprint 1 code is implemented, update:

```text
README.md
docs/Sprint1.md
docs/Pipeline.md
docs/DecisionLog.md
```

if behavior differs from this plan.

---

## 59. Sprint 1 GitHub issue template

Issue title:

```text
Sprint 1 - Speech To Text
```

Issue body:

```markdown
## Goal

Convert input video/audio into timestamped transcript JSON.

## Input

- input/video.mp4

## Output

- temp/audio.wav
- output/transcript.json

## Tasks

- [ ] Add FFmpeg audio extraction command builder
- [ ] Add audio extraction function
- [ ] Add transcript schema
- [ ] Add Faster Whisper transcriber
- [ ] Add JSON writer
- [ ] Add transcribe script
- [ ] Add basic tests
- [ ] Update docs

## Acceptance Criteria

- [ ] Works on Windows CPU
- [ ] Extracts audio with FFmpeg
- [ ] Produces valid transcript JSON
- [ ] Vietnamese text preserved
- [ ] Missing FFmpeg error is clear
- [ ] No renderer code added
```

---

## 60. Sprint 1 commit plan

Recommended commits:

### Commit 1

```text
feat: add audio extraction command builder
```

Files:

```text
src/ai_video_engine/audio/commands.py
tests/test_audio_commands.py
```

### Commit 2

```text
feat: add audio extractor
```

Files:

```text
src/ai_video_engine/audio/extractor.py
src/ai_video_engine/common/errors.py
```

### Commit 3

```text
feat: add transcript schema
```

Files:

```text
src/ai_video_engine/speech/schema.py
tests/test_transcript_schema.py
```

### Commit 4

```text
feat: add faster whisper transcriber
```

Files:

```text
src/ai_video_engine/speech/faster_whisper_engine.py
```

### Commit 5

```text
feat: add transcribe script
```

Files:

```text
scripts/transcribe.py
```

### Commit 6

```text
docs: document Sprint 1 speech-to-text implementation
```

Files:

```text
docs/Sprint1.md
README.md
```

---

## 61. Sprint 1 Definition of Done

Sprint 1 is done when:

1. User can place a video at `input/video.mp4`.
2. User can run a transcribe script.
3. `temp/audio.wav` is created.
4. `output/transcript.json` is created.
5. Transcript JSON is valid.
6. Vietnamese text is preserved.
7. Segment timestamps exist.
8. CPU mode works.
9. Missing FFmpeg error is clear.
10. No renderer code was added.
11. Basic tests exist.
12. Code is committed and pushed.

---

## 62. Sprint 1 expected manual test

Manual test:

```bash
python scripts/transcribe.py input/video.mp4
```

Expected console output:

```text
[audio] extracting audio from input/video.mp4
[audio] wrote temp/audio.wav
[speech] loading faster-whisper model: medium
[speech] transcribing...
[speech] wrote output/transcript.json
```

Expected file:

```text
output/transcript.json
```

---

## 63. Sprint 1 transcript output review

Open `output/transcript.json`.

Check:

- Vietnamese text visible
- timestamps reasonable
- segment IDs exist
- JSON formatted
- no Python object strings
- no escaped-only Vietnamese
- no empty text segments unless expected

---

## 64. Sprint 1 validation command future

Future command:

```bash
ai-video validate-transcript output/transcript.json
```

Not required now.

---

## 65. Sprint 1 troubleshooting

### 65.1 `ffmpeg` not recognized

Cause:

FFmpeg not in PATH or terminal not restarted.

Fix:

```powershell
winget install Gyan.FFmpeg
```

Restart VS Code.

Check:

```powershell
ffmpeg -version
```

### 65.2 `faster_whisper` import error

Fix:

```bash
pip install faster-whisper
```

Ensure venv is active.

### 65.3 Model too slow

Use smaller model:

```bash
--model small
```

### 65.4 Out of memory

Use:

```text
small
cpu
int8
```

### 65.5 Transcript has wrong language

Ensure:

```text
language=vi
```

### 65.6 No audio extracted

Check input video has audio stream.

Try:

```bash
ffmpeg -i input/video.mp4
```

---

## 66. Sprint 1 Windows-specific notes

Use PowerShell.

Activate venv:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation blocked:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then reopen terminal.

---

## 67. Sprint 1 Mac-specific notes

Activate venv:

```bash
source .venv/bin/activate
```

Install FFmpeg:

```bash
brew install ffmpeg
```

---

## 68. Sprint 1 package import test

After creating package structure, test:

```bash
python -c "import ai_video_engine; print('ok')"
```

This requires correct package layout.

If using `src/` layout, install editable:

```bash
pip install -e .
```

or configure `PYTHONPATH`.

For beginner simplicity, scripts may temporarily adjust path, but long-term package install is better.

---

## 69. Sprint 1 pyproject package note

If using `src/ai_video_engine`, update `pyproject.toml`.

Example:

```toml
[project]
name = "ai-video-engine"
version = "0.1.0"
requires-python = ">=3.11"

[tool.setuptools.packages.find]
where = ["src"]
```

This allows:

```bash
pip install -e .
```

---

## 70. Sprint 1 coding order

Recommended coding order:

1. decide package layout
2. add common errors
3. add JSON IO
4. add audio command builder
5. add tests for command builder
6. add audio extractor
7. add transcript schema
8. add tests for schema
9. add Faster Whisper transcriber
10. add transcribe script
11. manual test with real video
12. commit and push

---

## 71. Sprint 1 first code file: errors

Create:

```text
src/ai_video_engine/common/errors.py
```

Content:

```python
class AIVideoEngineError(Exception):
    """Base error for AI Video Engine."""


class InputFileError(AIVideoEngineError):
    """Raised when input media is invalid."""


class MissingFFmpegError(AIVideoEngineError):
    """Raised when FFmpeg is not available."""


class AudioExtractionError(AIVideoEngineError):
    """Raised when audio extraction fails."""


class SpeechToTextError(AIVideoEngineError):
    """Raised when speech-to-text fails."""


class InvalidTranscriptError(AIVideoEngineError):
    """Raised when transcript validation fails."""
```

---

## 72. Sprint 1 second code file: json_io

Create:

```text
src/ai_video_engine/common/json_io.py
```

Content:

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    """Read a UTF-8 JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    """Write UTF-8 JSON with Vietnamese text preserved."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
```

---

## 73. Sprint 1 third code file: audio commands

Create:

```text
src/ai_video_engine/audio/commands.py
```

Content:

```python
from __future__ import annotations

from pathlib import Path


def build_extract_audio_command(
    input_media: Path,
    output_audio: Path,
    sample_rate: int = 16000,
    channels: int = 1,
) -> list[str]:
    """Build an FFmpeg command that extracts mono WAV audio."""
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
```

---

## 74. Sprint 1 fourth code file: audio extractor

Create:

```text
src/ai_video_engine/audio/extractor.py
```

Responsibilities:

- validate input exists
- check FFmpeg
- create output parent
- run command
- validate output

Pseudo:

```python
def extract_audio(input_media: Path, output_audio: Path) -> AudioExtractionResult:
    if not input_media.exists():
        raise InputFileError(...)

    if shutil.which("ffmpeg") is None:
        raise MissingFFmpegError(...)

    output_audio.parent.mkdir(parents=True, exist_ok=True)

    cmd = build_extract_audio_command(input_media, output_audio)

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        raise AudioExtractionError(...) from exc

    if not output_audio.exists():
        raise AudioExtractionError(...)

    return AudioExtractionResult(...)
```

---

## 75. Sprint 1 fifth code file: transcript schema

Create:

```text
src/ai_video_engine/speech/schema.py
```

Fields:

```text
Transcript
TranscriptSegment
```

Use Pydantic.

Validation:

- end > start
- duration matches
- text non-empty
- IDs unique at Transcript level

---

## 76. Sprint 1 sixth code file: Faster Whisper engine

Create:

```text
src/ai_video_engine/speech/faster_whisper_engine.py
```

Responsibilities:

- load model
- transcribe audio
- convert segments to Transcript
- add metadata
- preserve Vietnamese
- handle errors

---

## 77. Sprint 1 seventh code file: transcribe script

Create:

```text
scripts/transcribe.py
```

Responsibilities:

- parse input argument
- call audio extractor
- call transcriber
- write JSON
- print success

---

## 78. Sprint 1 script example

Future script concept:

```python
from __future__ import annotations

import argparse
from pathlib import Path

from ai_video_engine.audio.extractor import extract_audio
from ai_video_engine.common.json_io import write_json
from ai_video_engine.speech.faster_whisper_engine import FasterWhisperTranscriber


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--model", default="medium")
    parser.add_argument("--language", default="vi")
    args = parser.parse_args()

    audio_path = Path("temp/audio.wav")
    transcript_path = Path("output/transcript.json")

    extract_audio(args.input, audio_path)

    transcriber = FasterWhisperTranscriber(model_name=args.model)
    transcript = transcriber.transcribe(audio_path, language=args.language)

    write_json(transcript_path, transcript.model_dump(mode="json"))

    print(f"Transcript written: {transcript_path}")


if __name__ == "__main__":
    main()
```

---

## 79. Sprint 1 command examples

Default:

```bash
python scripts/transcribe.py input/video.mp4
```

Small model:

```bash
python scripts/transcribe.py input/video.mp4 --model small
```

English test:

```bash
python scripts/transcribe.py input/video.mp4 --language en
```

---

## 80. Sprint 1 output example

After command:

```text
temp/audio.wav
output/transcript.json
```

---

## 81. Sprint 1 success sample

Example output:

```json
{
  "schema_version": "0.1.0",
  "metadata": {
    "speech_provider": "faster_whisper",
    "speech_model": "medium",
    "language": "vi",
    "source_audio": "temp/audio.wav"
  },
  "segments": [
    {
      "id": "seg_0001",
      "start": 0.12,
      "end": 1.75,
      "duration": 1.63,
      "text": "Ê! Sao hôm nay đến trễ?"
    }
  ]
}
```

---

## 82. Sprint 1 quality threshold

Sprint 1 is accepted even if transcript punctuation is imperfect.

It is not accepted if:

- JSON invalid
- timestamps missing
- text empty
- audio extraction fails silently
- Vietnamese encoding broken
- code only works on one local path

---

## 83. Sprint 1 must not include renderer

Do not add:

```text
src/renderer/
```

implementation yet.

Renderer docs exist, but implementation comes later.

---

## 84. Sprint 1 must not include Visual Director

Do not add:

```text
src/director/visual_director.py
```

implementation yet.

That is Sprint 3.

---

## 85. Sprint 1 must not include icon selector

Do not add embedding logic yet.

That is Sprint 4.

---

## 86. Sprint 1 must not include diarization

Do not add WhisperX or pyannote yet.

Keep Sprint 1 simple.

---

## 87. Sprint 1 must not include TTS

Do not add TTS.

Existing-video workflow preserves original audio.

---

## 88. Sprint 1 possible issue: Python import path

If script cannot import package, options:

### Option A

Install editable package:

```bash
pip install -e .
```

Recommended long-term.

### Option B

Temporarily add project root to `sys.path` in script.

Acceptable for very early testing, but not ideal.

Recommended:

```text
use pyproject + pip install -e .
```

---

## 89. Sprint 1 pyproject requirement for editable install

Example minimal `pyproject.toml`:

```toml
[project]
name = "ai-video-engine"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "faster-whisper",
  "pydantic",
  "rich",
  "orjson"
]

[tool.setuptools.packages.find]
where = ["src"]
```

If package is under `src/ai_video_engine`, this should work.

---

## 90. Sprint 1 install editable

After pyproject update:

```bash
pip install -e .
```

Then test:

```bash
python -c "import ai_video_engine; print('ok')"
```

---

## 91. Sprint 1 recommended ADR before coding

Add to DecisionLog:

```text
ADR-0041 - Use src/ai_video_engine package layout
```

Status:

```text
Accepted
```

Reason:

- standard Python package
- easier imports
- easier CLI entry point
- better Codex navigation

This can be done before or during Sprint 1.

---

## 92. Sprint 1 package layout migration

If current repo has:

```text
src/audio/
src/speech/
```

create:

```text
src/ai_video_engine/audio/
src/ai_video_engine/speech/
```

Move or recreate empty modules.

Do not delete docs.

Update imports accordingly.

---

## 93. Sprint 1 test install

After creating package:

```bash
pip install -e .
pytest
```

If pytest not installed:

```bash
pip install pytest
```

---

## 94. Sprint 1 CI update

Optional Sprint 1 CI update:

```yaml
- run: pip install -r requirements.txt
- run: pip install -e .
- run: pytest
```

But do not run model-heavy integration tests in CI.

---

## 95. Sprint 1 integration test marker

If adding integration tests:

```python
import pytest

@pytest.mark.integration
def test_transcribe_tiny_audio():
    ...
```

Default CI may skip integration tests.

---

## 96. Sprint 1 `.gitignore` check

Make sure these are ignored:

```text
temp/
output/
*.mp4
*.wav
*.mp3
```

Otherwise real media may be committed accidentally.

---

## 97. Sprint 1 sample input policy

Do not commit private input video.

For testing, place video locally:

```text
input/video.mp4
```

but keep `input/` or media files ignored.

---

## 98. Sprint 1 output policy

Do not commit:

```text
temp/audio.wav
output/transcript.json
```

unless using tiny committed fixtures under `tests/fixtures/`.

Generated outputs are local artifacts.

---

## 99. Sprint 1 security

Do not upload user audio/video anywhere.

Faster Whisper runs locally.

No API key required.

---

## 100. Sprint 1 privacy

Input videos may contain private voice.

Do not commit them.

Do not upload them.

Do not log full transcript unless debug mode or user expects it.

For early development, printing segments is acceptable, but be aware.

---

## 101. Sprint 1 performance

Avoid loading model multiple times.

Good:

```python
transcriber = FasterWhisperTranscriber(...)
transcriber.transcribe(audio_path)
```

Bad:

```python
for segment:
    load model
```

---

## 102. Sprint 1 memory

If model too heavy, use:

```text
small
```

and:

```text
compute_type=int8
```

---

## 103. Sprint 1 batch preparation

Do not build batch processing yet.

But design transcriber so model can be reused later.

---

## 104. Sprint 1 future extension: audio input

Later, if input is already audio, skip extraction or convert format.

Sprint 1 can focus on video input.

---

## 105. Sprint 1 future extension: media probe

Later, add:

```text
src/audio/probe.py
```

to get duration and streams.

Not required for first working version.

---

## 106. Sprint 1 future extension: transcript editing

Later, user can edit transcript JSON manually.

Sprint 1 should write readable JSON.

---

## 107. Sprint 1 future extension: speaker field

Later transcript segments may include speaker.

Example:

```json
"speaker": {
  "id": "SPEAKER_00",
  "source": "diarization"
}
```

Not required now.

---

## 108. Sprint 1 future extension: word timing

Later transcript segments may include:

```json
"words": []
```

Not required now.

---

## 109. Sprint 1 future extension: confidence

If model provides useful confidence, include later.

Not required now.

---

## 110. Sprint 1 interaction with Sprint 2

Sprint 2 consumes:

```text
output/transcript.json
```

Therefore Sprint 1 output must be stable enough for Timeline Analyzer.

Critical fields:

```text
id
start
end
duration
text
```

---

## 111. Sprint 1 interaction with Sprint 3

Visual Director does not consume raw transcript directly in the default pipeline.

It consumes normalized timeline from Sprint 2.

Therefore Sprint 1 should not add Visual Director fields.

---

## 112. Sprint 1 interaction with Renderer

Renderer does not consume transcript.

Renderer consumes visual timeline.

Therefore Sprint 1 should not optimize for renderer directly.

---

## 113. Sprint 1 review checklist

Before closing Sprint 1, check:

1. Does audio extraction work?
2. Does STT work?
3. Does transcript JSON validate?
4. Is Vietnamese preserved?
5. Are errors clear?
6. Is code in correct modules?
7. Are tests present?
8. Are docs updated?
9. Are generated files ignored?
10. Was commit pushed?

---

## 114. Sprint 1 user test checklist

User should run:

```bash
python scripts/transcribe.py input/video.mp4 --model small
```

Then check:

```text
temp/audio.wav exists
output/transcript.json exists
```

Open transcript.

Confirm text appears.

---

## 115. Sprint 1 expected limitations

Expected limitations:

- no speaker diarization
- no word-level timing
- punctuation may be imperfect
- STT speed depends on machine
- first model download may take time
- no visual output yet

These are acceptable.

---

## 116. Sprint 1 completion message

When Sprint 1 is completed, a good summary is:

```text
Sprint 1 completed.
The project can now extract audio from video and generate output/transcript.json using Faster Whisper.
```

Then move to Sprint 2.

---

## 117. Sprint 2 handoff

Sprint 2 starts with:

```text
output/transcript.json
```

Sprint 2 goal:

```text
output/transcript.json → output/timeline.normalized.json
```

Sprint 1 must provide clean transcript JSON for this.

---

## 118. Sprint 1 final rule

Do not make Sprint 1 bigger than it needs to be.

A successful Sprint 1 is a reliable transcript generator.

That is enough.

---

# Appendix A - Sprint 1 task board

| ID | Task | Status |
|---|---|---|
| S1-001 | Decide package layout | planned |
| S1-002 | Update pyproject for src package | planned |
| S1-003 | Create common errors | planned |
| S1-004 | Create JSON IO helpers | planned |
| S1-005 | Create FFmpeg command builder | planned |
| S1-006 | Test FFmpeg command builder | planned |
| S1-007 | Create audio extractor | planned |
| S1-008 | Create transcript schema | planned |
| S1-009 | Test transcript schema | planned |
| S1-010 | Create Faster Whisper transcriber | planned |
| S1-011 | Create transcribe script | planned |
| S1-012 | Manual test with real video | planned |
| S1-013 | Update docs | planned |
| S1-014 | Commit and push | planned |

---

# Appendix B - Sprint 1 code skeletons


## B.1 `src/ai_video_engine/common/errors.py`

```python
"""Project-specific exceptions for AI Video Engine."""


class AIVideoEngineError(Exception):
    """Base error for AI Video Engine."""


class InputFileError(AIVideoEngineError):
    """Raised when an input media file is invalid."""


class MissingFFmpegError(AIVideoEngineError):
    """Raised when FFmpeg is not available."""


class AudioExtractionError(AIVideoEngineError):
    """Raised when audio extraction fails."""


class SpeechToTextError(AIVideoEngineError):
    """Raised when speech-to-text fails."""


class InvalidTranscriptError(AIVideoEngineError):
    """Raised when transcript validation fails."""

```

## B.2 `src/ai_video_engine/common/json_io.py`

```python
"""JSON IO helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    """Read a UTF-8 JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    """Write formatted UTF-8 JSON and preserve Vietnamese characters."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

```

## B.3 `src/ai_video_engine/audio/commands.py`

```python
"""FFmpeg command builders for audio extraction."""

from __future__ import annotations

from pathlib import Path


def build_extract_audio_command(
    input_media: Path,
    output_audio: Path,
    sample_rate: int = 16000,
    channels: int = 1,
) -> list[str]:
    """Build an FFmpeg command that extracts audio for STT."""
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

```

## B.4 `src/ai_video_engine/audio/extractor.py`

```python
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

```

## B.5 `src/ai_video_engine/speech/schema.py`

```python
"""Transcript schema models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, model_validator

TIME_TOLERANCE = 0.05


class TranscriptSegment(BaseModel):
    """One timestamped speech-to-text segment."""

    id: str
    start: float = Field(ge=0)
    end: float
    duration: float
    text: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_timing(self) -> "TranscriptSegment":
        """Validate segment timing."""
        if self.end <= self.start:
            raise ValueError("Segment end must be greater than start.")

        if self.duration <= 0:
            raise ValueError("Segment duration must be positive.")

        expected = self.end - self.start
        if abs(self.duration - expected) > TIME_TOLERANCE:
            raise ValueError("Segment duration must match end - start.")

        return self


class Transcript(BaseModel):
    """Timestamped transcript."""

    schema_version: str = "0.1.0"
    metadata: dict[str, Any] = Field(default_factory=dict)
    segments: list[TranscriptSegment] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_segments(self) -> "Transcript":
        """Validate transcript segment IDs and ordering."""
        ids = [segment.id for segment in self.segments]
        if len(ids) != len(set(ids)):
            raise ValueError("Transcript segment IDs must be unique.")

        starts = [segment.start for segment in self.segments]
        if starts != sorted(starts):
            raise ValueError("Transcript segments must be sorted by start time.")

        return self

```

## B.6 `src/ai_video_engine/speech/faster_whisper_engine.py`

```python
"""Faster Whisper speech-to-text engine."""

from __future__ import annotations

from pathlib import Path

from ai_video_engine.common.errors import SpeechToTextError
from ai_video_engine.speech.schema import Transcript, TranscriptSegment


def make_segment_id(index: int) -> str:
    """Create stable transcript segment ID."""
    return f"seg_{index:04d}"


class FasterWhisperTranscriber:
    """Transcribe audio using Faster Whisper."""

    def __init__(
        self,
        model_name: str = "medium",
        device: str = "cpu",
        compute_type: str = "int8",
    ) -> None:
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self._model = None

    def _load_model(self):
        """Load Faster Whisper model lazily."""
        if self._model is None:
            try:
                from faster_whisper import WhisperModel
            except ImportError as exc:
                raise SpeechToTextError(
                    "faster-whisper is not installed. Install it with: pip install faster-whisper"
                ) from exc

            try:
                self._model = WhisperModel(
                    self.model_name,
                    device=self.device,
                    compute_type=self.compute_type,
                )
            except Exception as exc:
                raise SpeechToTextError(
                    f"Failed to load Faster Whisper model: {self.model_name}"
                ) from exc

        return self._model

    def transcribe(
        self,
        audio_path: Path,
        language: str = "vi",
        vad_filter: bool = True,
        beam_size: int = 5,
        source_input: str | None = None,
    ) -> Transcript:
        """Transcribe an audio file into Transcript."""
        if not audio_path.exists():
            raise SpeechToTextError(f"Audio file not found: {audio_path}")

        model = self._load_model()

        try:
            segments_iter, info = model.transcribe(
                str(audio_path),
                language=language,
                vad_filter=vad_filter,
                beam_size=beam_size,
            )
        except Exception as exc:
            raise SpeechToTextError(f"Failed to transcribe audio: {audio_path}") from exc

        segments: list[TranscriptSegment] = []

        for index, segment in enumerate(segments_iter, start=1):
            text = segment.text.strip()
            if not text:
                continue

            start = round(float(segment.start), 2)
            end = round(float(segment.end), 2)
            duration = round(end - start, 2)

            segments.append(
                TranscriptSegment(
                    id=make_segment_id(index),
                    start=start,
                    end=end,
                    duration=duration,
                    text=text,
                )
            )

        metadata = {
            "speech_provider": "faster_whisper",
            "speech_model": self.model_name,
            "language": language,
            "source_audio": str(audio_path),
            "device": self.device,
            "compute_type": self.compute_type,
        }

        if source_input:
            metadata["source_input"] = source_input

        return Transcript(metadata=metadata, segments=segments)

```

## B.7 `scripts/transcribe.py`

```python
"""Transcribe a video/audio file into output/transcript.json."""

from __future__ import annotations

import argparse
from pathlib import Path

from ai_video_engine.audio.extractor import extract_audio
from ai_video_engine.common.json_io import write_json
from ai_video_engine.speech.faster_whisper_engine import FasterWhisperTranscriber


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe media using Faster Whisper.")
    parser.add_argument("input", type=Path, help="Input video/audio path")
    parser.add_argument("--model", default="medium", help="Faster Whisper model name")
    parser.add_argument("--language", default="vi", help="Speech language")
    parser.add_argument("--audio-output", type=Path, default=Path("temp/audio.wav"))
    parser.add_argument("--transcript-output", type=Path, default=Path("output/transcript.json"))

    args = parser.parse_args()

    print(f"[audio] extracting audio from {args.input}")
    extract_audio(args.input, args.audio_output)
    print(f"[audio] wrote {args.audio_output}")

    print(f"[speech] loading/transcribing with model={args.model} language={args.language}")
    transcriber = FasterWhisperTranscriber(model_name=args.model)
    transcript = transcriber.transcribe(
        args.audio_output,
        language=args.language,
        source_input=str(args.input),
    )

    write_json(args.transcript_output, transcript.model_dump(mode="json"))
    print(f"[speech] wrote {args.transcript_output}")


if __name__ == "__main__":
    main()

```

---

# Appendix C - Sprint 1 test skeletons


## C.1 `tests/test_audio_commands.py`

```python
from pathlib import Path

from ai_video_engine.audio.commands import build_extract_audio_command


def test_build_extract_audio_command():
    cmd = build_extract_audio_command(
        input_media=Path("input/video.mp4"),
        output_audio=Path("temp/audio.wav"),
    )

    assert cmd[0] == "ffmpeg"
    assert "-i" in cmd
    assert "input/video.mp4" in cmd
    assert "temp/audio.wav" in cmd
    assert "-ar" in cmd
    assert "16000" in cmd

```

## C.2 `tests/test_transcript_schema.py`

```python
import pytest

from ai_video_engine.speech.schema import Transcript, TranscriptSegment


def test_transcript_segment_valid():
    segment = TranscriptSegment(
        id="seg_0001",
        start=0.0,
        end=1.5,
        duration=1.5,
        text="Xin chào.",
    )

    assert segment.id == "seg_0001"


def test_transcript_segment_rejects_invalid_timing():
    with pytest.raises(ValueError):
        TranscriptSegment(
            id="seg_0001",
            start=2.0,
            end=1.0,
            duration=-1.0,
            text="bad",
        )


def test_transcript_rejects_duplicate_ids():
    with pytest.raises(ValueError):
        Transcript(
            segments=[
                TranscriptSegment(id="seg_0001", start=0.0, end=1.0, duration=1.0, text="A"),
                TranscriptSegment(id="seg_0001", start=1.1, end=2.0, duration=0.9, text="B"),
            ]
        )

```

## C.3 `tests/test_json_io.py`

```python
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

```

---

# Appendix D - Sprint 1 manual execution checklist

1. Activate virtual environment.
2. Run `python --version`.
3. Run `ffmpeg -version`.
4. Run `python -c "from faster_whisper import WhisperModel; print('ok')"`.
5. Place test video at `input/video.mp4`.
6. Run `python scripts/transcribe.py input/video.mp4 --model small`.
7. Confirm `temp/audio.wav` exists.
8. Confirm `output/transcript.json` exists.
9. Open transcript JSON.
10. Check Vietnamese text and timestamps.

---

# Appendix E - Sprint 1 final handoff to Sprint 2

Sprint 1 hands off this file to Sprint 2:

```text
output/transcript.json
```

Sprint 2 should not depend on Faster Whisper directly.

Sprint 2 should only read transcript JSON.

This keeps pipeline stages independent.
