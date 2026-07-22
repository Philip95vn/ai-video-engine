# CodingStandard.md

# AI Video Engine - Coding Standard

## 0. Purpose

This document defines the coding standard for **AI Video Engine**.

It is written for:

- human contributors
- ChatGPT
- Codex in VS Code
- GitHub Copilot
- Cursor
- Claude Code
- future maintainers

The goal is not to make code complicated.

The goal is to keep the project understandable, testable, and maintainable as it grows.

AI Video Engine is not a collection of random scripts.

It is a modular engine.

This coding standard protects that architecture.

This document should be read together with:

```text
AGENTS.md
PROJECT_RULES.md
docs/Architecture.md
docs/Pipeline.md
docs/JSONSchema.md
docs/AIDesign.md
docs/RendererDesign.md
docs/AssetGuide.md
docs/DecisionLog.md
```

---

## 1. Core coding principle

Prefer code that is:

- explicit
- boring
- readable
- testable
- modular
- local-first
- predictable
- easy to debug
- easy for AI agents to modify safely

Avoid code that is:

- clever
- hidden
- tightly coupled
- hardcoded
- unvalidated
- dependent on chat memory
- dependent on one machine
- dependent on cloud services by default

---

## 2. Python version

Use:

```text
Python 3.11+
```

Recommended:

```text
Python 3.11
```

Avoid relying on very new Python versions for AI packages until ecosystem compatibility is stable.

Reason:

- Faster Whisper
- PyTorch ecosystem
- sentence-transformers
- WhisperX
- pyannote.audio
- MoviePy
- common AI packages

are more likely to work reliably on Python 3.11.

---

## 3. Project type

AI Video Engine should be developed as a Python package-style project.

Core code belongs under:

```text
src/
```

Avoid putting production logic in:

```text
scripts/
examples/
notebooks/
```

Those folders can call core logic but should not contain the core engine.

---

## 4. Recommended repository structure

```text
ai-video-engine/
│
├── README.md
├── AGENTS.md
├── PROJECT_RULES.md
├── ROADMAP.md
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .gitignore
│
├── docs/
│
├── src/
│   ├── audio/
│   ├── speech/
│   ├── timeline/
│   ├── director/
│   ├── embedding/
│   ├── renderer/
│   ├── exporter/
│   ├── assets/
│   ├── common/
│   └── config/
│
├── prompts/
├── assets/
├── tests/
├── examples/
├── scripts/
├── output/
└── temp/
```

---

## 5. Module ownership

Each module must have a clear responsibility.

| Module | Responsibility |
|---|---|
| `src/audio/` | audio extraction and conversion |
| `src/speech/` | speech-to-text |
| `src/timeline/` | transcript normalization and timeline validation |
| `src/director/` | LLM-based visual direction |
| `src/embedding/` | semantic asset search |
| `src/renderer/` | deterministic visual rendering |
| `src/exporter/` | final MP4 export and audio merge |
| `src/assets/` | asset registry helpers |
| `src/common/` | shared utilities only |
| `src/config/` | configuration loading |

Do not mix responsibilities.

---

## 6. The most important boundary

Renderer code must not call AI.

This is forbidden:

```python
# Bad
from src.director import VisualDirector

def render_scene(scene):
    effect = VisualDirector().choose_effect(scene.text)
```

This is correct:

```python
# Good
def render_scene(scene):
    effect = scene.keywords[0].effect
```

Renderer consumes validated JSON.

Renderer does not make semantic AI decisions.

---

## 7. Script vs engine code

### 7.1 Scripts

Scripts are allowed under:

```text
scripts/
```

Scripts may:

- test a module
- run a pipeline stage
- generate sample output
- debug local setup
- validate assets

Scripts should be thin wrappers.

### 7.2 Engine code

Engine code belongs under:

```text
src/
```

Engine code should be importable, testable, and reusable.

Bad:

```python
# scripts/transcribe.py
# 300 lines of production transcription logic
```

Good:

```python
# scripts/transcribe.py
from src.speech.faster_whisper_engine import FasterWhisperEngine
```

---

## 8. Naming conventions

### 8.1 Files and folders

Use lowercase snake_case.

Good:

```text
audio_extractor.py
timeline_analyzer.py
visual_director.py
icon_selector.py
render_engine.py
```

Bad:

```text
AudioExtractor.py
finalCode.py
new_test2.py
main_old.py
```

### 8.2 Classes

Use PascalCase.

```python
class AudioExtractor:
    ...
```

### 8.3 Functions

Use snake_case.

```python
def extract_audio(...):
    ...
```

### 8.4 Variables

Use snake_case.

```python
output_path = Path("output/final.mp4")
```

### 8.5 Constants

Use UPPER_SNAKE_CASE.

```python
DEFAULT_FPS = 30
```

### 8.6 IDs

Use stable string IDs.

```text
scene_0001
seg_0001
icon_alarm_001
```

---

## 9. Import rules

### 9.1 Standard import order

Use this order:

```python
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel

from src.common.errors import MissingFFmpegError
```

Order:

1. future imports
2. standard library
3. third-party libraries
4. local project imports

### 9.2 Avoid wildcard imports

Bad:

```python
from module import *
```

Good:

```python
from module import Timeline
```

### 9.3 Avoid circular imports

If circular imports appear, module boundaries are probably wrong.

### 9.4 Renderer import rule

Renderer may import:

```text
timeline schema models
asset registry
config
common utilities
```

Renderer may not import:

```text
director
speech
embedding model clients
LLM clients
prompt loader
```

---

## 10. Type hints

Use type hints for public functions.

Good:

```python
def extract_audio(input_video: Path, output_audio: Path) -> AudioExtractionResult:
    ...
```

Avoid untyped public APIs.

Bad:

```python
def extract_audio(input_video, output_audio):
    ...
```

Internal small helpers may be less strict, but clarity is preferred.

---

## 11. `pathlib.Path`

Use `pathlib.Path` for file paths.

Good:

```python
from pathlib import Path

input_path = Path("input/video.mp4")
output_path = Path("temp/audio.wav")
```

Bad:

```python
input_path = "input/" + filename
```

Reasons:

- Windows support
- Mac support
- path joining
- path validation
- clearer code

---

## 12. Relative paths

Use repository-relative paths in JSON.

Good:

```json
{
  "icon_path": "assets/icons/alarm_001.png"
}
```

Bad:

```json
{
  "icon_path": "C:\\Users\\PC\\Desktop\\alarm.png"
}
```

Absolute paths may exist at runtime but should not be committed in JSON examples.

---

## 13. Subprocess rules

Use argument lists.

Good:

```python
subprocess.run(
    [
        "ffmpeg",
        "-y",
        "-i",
        str(input_video),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        str(output_audio),
    ],
    check=True,
)
```

Bad:

```python
subprocess.run(f"ffmpeg -i {input_video} {output_audio}", shell=True)
```

Avoid `shell=True` unless there is a documented reason.

---

## 14. FFmpeg command construction

FFmpeg command construction should be testable.

Good:

```python
def build_extract_audio_command(input_video: Path, output_audio: Path) -> list[str]:
    return [
        "ffmpeg",
        "-y",
        "-i",
        str(input_video),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        str(output_audio),
    ]
```

This can be unit tested without running FFmpeg.

---

## 15. External dependency checks

Before using external tools, check availability.

Example:

```python
def check_ffmpeg_available() -> bool:
    result = shutil.which("ffmpeg")
    return result is not None
```

If missing, raise clear error.

Bad:

```text
FileNotFoundError
```

Good:

```text
FFmpeg was not found. Install with: winget install Gyan.FFmpeg
Then restart VS Code.
```

---

## 16. Error handling philosophy

Errors should be explicit and helpful.

Do not hide errors.

Do not silently skip important failures.

Do not return `None` for serious failures.

Use exceptions for fatal errors.

Use warnings for recoverable issues.

---

## 17. Custom errors

Define domain-specific errors.

Suggested:

```python
class AIVideoEngineError(Exception):
    """Base error for AI Video Engine."""

class MissingFFmpegError(AIVideoEngineError):
    """Raised when FFmpeg is not available."""

class InvalidTranscriptError(AIVideoEngineError):
    """Raised when transcript JSON is invalid."""

class InvalidTimelineError(AIVideoEngineError):
    """Raised when timeline JSON is invalid."""

class InvalidDirectorOutputError(AIVideoEngineError):
    """Raised when LLM output is invalid."""

class MissingAssetError(AIVideoEngineError):
    """Raised when an asset cannot be found."""

class UnknownEffectError(AIVideoEngineError):
    """Raised when a timeline requests an unknown effect."""

class RenderError(AIVideoEngineError):
    """Raised when rendering fails."""

class ExportError(AIVideoEngineError):
    """Raised when final export fails."""
```

These can live in:

```text
src/common/errors.py
```

---

## 18. Exception messages

Exception messages should be actionable.

Bad:

```python
raise ValueError("bad path")
```

Good:

```python
raise InputFileError(
    f"Input video not found: {input_video}. "
    "Place a video in input/ or pass --input."
)
```

---

## 19. Do not swallow exceptions

Bad:

```python
try:
    run_pipeline()
except Exception:
    pass
```

Good:

```python
try:
    run_pipeline()
except AIVideoEngineError as exc:
    logger.error(str(exc))
    raise
```

---

## 20. Broad exception handling

Avoid broad `except Exception`.

If used, add context and re-raise.

```python
try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as exc:
    raise AudioExtractionError(
        f"FFmpeg failed while extracting audio from {input_video}"
    ) from exc
```

---

## 21. Logging standard

Use logging for pipeline progress.

Initial project may use `rich` for user-friendly terminal output.

Logs should show:

- stage name
- input path
- output path
- model name
- scene count
- duration
- warnings
- errors

Logs should not expose secrets.

---

## 22. Logging style

Good:

```text
[audio] extracting audio: input/video.mp4
[audio] wrote: temp/audio.wav
[speech] model=medium language=vi
[speech] wrote: output/transcript.json
```

Bad:

```text
done
ok
processing...
```

---

## 23. JSON writing

Use UTF-8.

Use indentation.

Preserve Vietnamese characters.

Good:

```python
path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
```

Bad:

```python
path.write_text(str(data))
```

---

## 24. JSON reading

Use explicit encoding.

```python
data = json.loads(path.read_text(encoding="utf-8"))
```

Validate after reading.

---

## 25. Data validation

Validate data at module boundaries.

Use Pydantic or explicit validation functions.

Important validation targets:

```text
transcript.json
timeline.normalized.json
timeline.director.json
timeline.visual.json
icon_db.json
template config
render_report.json
```

---

## 26. Pydantic usage

Pydantic is recommended for schema validation.

Example:

```python
from pydantic import BaseModel, Field, model_validator

class TranscriptSegment(BaseModel):
    id: str
    start: float = Field(ge=0)
    end: float
    duration: float
    text: str

    @model_validator(mode="after")
    def validate_timing(self):
        if self.end <= self.start:
            raise ValueError("end must be greater than start")
        if abs(self.duration - (self.end - self.start)) > 0.05:
            raise ValueError("duration must match end - start")
        return self
```

---

## 27. Dataclasses vs Pydantic

Use Pydantic for:

- JSON input/output models
- schema validation
- data crossing module boundaries

Use dataclasses for:

- internal runtime state
- simple result objects
- renderer temporary state

Example:

```python
@dataclass
class RenderContext:
    width: int
    height: int
    fps: float
```

---

## 28. Dictionaries

Avoid passing raw dictionaries across module boundaries when schema matters.

Bad:

```python
def render(timeline: dict):
    ...
```

Better:

```python
def render(timeline: VisualTimeline):
    ...
```

Raw dictionaries are acceptable for:

- temporary JSON loading before validation
- generic metadata
- config before parsing

---

## 29. Function design

Functions should do one thing.

Good:

```python
def extract_audio(...):
    ...

def transcribe_audio(...):
    ...

def write_transcript_json(...):
    ...
```

Bad:

```python
def process_video_and_make_everything(...):
    ...
```

---

## 30. Function length

Prefer short functions.

A function over 80-120 lines should be reviewed.

Large functions often indicate missing modules.

---

## 31. Class design

Classes should represent meaningful services or data.

Good:

```python
class AudioExtractor:
    ...

class FasterWhisperTranscriber:
    ...

class TimelineAnalyzer:
    ...

class VisualDirector:
    ...

class RendererEngine:
    ...
```

Avoid classes that are just random bags of functions.

---

## 32. Dependency injection

Pass dependencies explicitly where practical.

Good:

```python
class VisualDirector:
    def __init__(self, llm_client: LLMClient, prompt_loader: PromptLoader):
        ...
```

Bad:

```python
class VisualDirector:
    def __init__(self):
        self.client = GlobalOllamaClient()
```

This helps testing.

---

## 33. Configuration

Do not scatter constants.

Use config.

Example config:

```yaml
video:
  width: 1080
  height: 1920
  fps: 30

speech:
  model: medium
  language: vi

director:
  model: qwen2.5:3b
```

Default values can exist in code but should be centralized.

---

## 34. Config loading

Config loading should:

- read from file
- merge defaults
- validate values
- expose typed config object
- support overrides later

Suggested location:

```text
src/config/
```

---

## 35. Hardcoding policy

Avoid hardcoding:

- local paths
- model names deep inside logic
- prompt text
- asset paths
- colors in renderer
- font paths
- output paths beyond config defaults

Allowed:

- centralized defaults
- test fixtures
- examples

---

## 36. Prompt handling

Prompts live in:

```text
prompts/
```

Do not hardcode large prompts in Python.

Bad:

```python
prompt = """
You are a visual director...
"""
```

Good:

```python
prompt = prompt_loader.load("visual_director.md")
```

---

## 37. LLM output handling

Never trust LLM output directly.

Required steps:

1. receive raw text
2. parse/extract JSON
3. repair if configured
4. validate schema
5. normalize if needed
6. write output JSON

Renderer must not consume raw LLM output.

---

## 38. AI module rule

AI modules may call models.

Renderer must not.

Allowed model-calling modules:

```text
src/speech/
src/director/
src/embedding/
```

Forbidden model-calling module:

```text
src/renderer/
```

---

## 39. Renderer coding rules

Renderer code must:

- consume visual timeline JSON
- validate input
- use templates
- use asset registry
- respect safe zones
- support Vietnamese fonts
- fail on unknown effects
- fail on unknown layouts
- produce silent video

Renderer code must not:

- call LLM
- parse raw transcript for meaning
- select semantic icons
- call speech-to-text
- merge final audio

---

## 40. Exporter coding rules

Exporter code must:

- merge silent video with audio
- use FFmpeg
- validate output path
- write final MP4
- optionally write report

Exporter code must not:

- render text
- call LLM
- transcribe audio
- change visual timeline

---

## 41. Asset coding rules

Asset code must:

- load asset DBs
- validate IDs
- validate file paths
- resolve relative paths
- check file existence
- expose helpful errors

Asset code must not:

- silently download assets
- invent missing files
- hardcode absolute paths

---

## 42. Embedding coding rules

Embedding code must:

- load metadata
- build embeddings
- cache embeddings
- search queries
- return score
- handle missing DB clearly

Embedding code must not:

- draw icons
- render video
- change timeline timing

---

## 43. Timeline coding rules

Timeline code must:

- preserve timing
- create scene IDs
- normalize transcript
- validate scenes
- remain deterministic

Timeline code should not call LLM initially.

---

## 44. Speech coding rules

Speech code must:

- support Faster Whisper
- support CPU mode
- support Vietnamese
- write transcript JSON
- include timestamps

Speech code must not:

- choose visual effects
- render video

---

## 45. Audio coding rules

Audio code must:

- use FFmpeg
- prepare audio for STT
- preserve original audio path
- write temp audio
- handle missing FFmpeg clearly

Audio code must not:

- transcribe audio
- call LLM

---

## 46. CLI coding rules

CLI should be thin.

Good:

```python
def main():
    args = parse_args()
    result = transcribe_command(args)
```

Bad:

```python
def main():
    # 500 lines of pipeline logic
```

Core logic belongs in modules.

---

## 47. Tests folder

Tests should live under:

```text
tests/
```

Suggested structure:

```text
tests/
├── unit/
├── integration/
├── fixtures/
└── smoke/
```

Early project may keep it simpler.

---

## 48. Test naming

Use descriptive names.

Good:

```text
test_audio_extractor.py
test_transcript_schema.py
test_timeline_analyzer.py
test_visual_director_parser.py
test_renderer_validation.py
```

Test functions:

```python
def test_transcript_segment_rejects_negative_duration():
    ...
```

---

## 49. Unit test rules

Unit tests should be:

- fast
- local
- deterministic
- small
- easy to run

Unit tests should not require:

- internet
- GPU
- large models
- large media files
- cloud APIs

---

## 50. Integration test rules

Integration tests may be slower.

They may call:

- FFmpeg
- Faster Whisper
- Ollama
- embedding models

They should be marked or separated.

---

## 51. Test fixtures

Use small fixtures.

Do not commit large videos.

Fixture examples:

```text
tests/fixtures/transcript_simple.json
tests/fixtures/timeline_visual_minimal.json
tests/fixtures/icon_db_small.json
```

For media tests, use very short generated files.

---

## 52. Fake providers

Use fake providers for AI tests.

Example:

```python
class FakeLLMClient:
    def generate(self, prompt: str) -> str:
        return '{"schema_version": "0.1.0", "scenes": []}'
```

This avoids depending on Ollama in unit tests.

---

## 53. Testing LLM parser

Test:

- raw JSON
- markdown-wrapped JSON
- invalid JSON
- missing fields
- changed scene ID
- invalid enum
- timing change
- extra scene

---

## 54. Testing renderer

Test:

- minimal timeline validates
- unknown effect fails
- unknown layout fails
- missing optional icon warns
- missing required font fails or falls back
- Vietnamese text renders in smoke test
- output file is created in smoke test

---

## 55. Testing audio

Test:

- command generation
- missing input path
- missing FFmpeg check
- output folder creation

Avoid running FFmpeg in unit tests unless marked integration.

---

## 56. Testing speech

Unit test:

- transcript JSON writing
- segment ID creation
- duration calculation
- transcript validation

Integration test:

- tiny audio to transcript

---

## 57. Testing assets

Test:

- duplicate asset IDs fail
- absolute paths fail
- missing file warns/fails
- empty tags warning
- icon DB loads

---

## 58. Testing config

Test:

- default config loads
- overrides apply
- invalid config fails
- paths resolve

---

## 59. Test command

Eventually:

```bash
pytest
```

Early project can add tests gradually.

---

## 60. CI standard

Initial CI can be simple:

```text
install Python
run import check
run tests
```

Later:

```text
format check
lint
type check
unit tests
package build
```

CI should not download large models by default.

---

## 61. Formatting

Use consistent formatting.

Recommended later:

```text
black
ruff
```

Initial project may not enforce immediately, but should avoid messy formatting.

---

## 62. Line length

Prefer readable lines.

Suggested:

```text
88-100 characters
```

Markdown can be more flexible.

---

## 63. Comments

Use comments to explain why, not obvious what.

Bad:

```python
# increment i
i += 1
```

Good:

```python
# MoviePy expects RGB frames, so remove alpha before returning.
frame = np.array(image.convert("RGB"))
```

---

## 64. Docstrings

Public classes and functions should have docstrings.

Example:

```python
def extract_audio(input_video: Path, output_audio: Path) -> AudioExtractionResult:
    """Extract mono WAV audio from a video file for speech-to-text."""
```

Do not write huge docstrings when docs already exist.

---

## 65. README examples

README examples should be tested or kept simple.

Do not include commands that are known to be broken.

---

## 66. Documentation sync

When code changes behavior, update docs.

Examples:

- new JSON field
- new pipeline stage
- new prompt behavior
- new renderer effect
- new asset DB field
- new config setting

---

## 67. DecisionLog rule

Major decisions must be written to:

```text
docs/DecisionLog.md
```

Examples:

- choosing Faster Whisper
- choosing Ollama
- changing JSON schema
- changing renderer backend
- adding a cloud provider
- changing template structure

---

## 68. Git commit standard

Use conventional commits.

Examples:

```text
docs: expand coding standard
feat: add audio extraction command builder
fix: handle missing ffmpeg on Windows
test: add transcript validation tests
refactor: split renderer text layout logic
chore: update dependencies
ci: add Python test workflow
```

---

## 69. Commit size

One commit should represent one logical change.

Bad:

```text
feat: add renderer and change prompts and update assets and fix tests
```

Good:

```text
feat: add basic center stack renderer
docs: document center stack layout
test: add renderer validation tests
```

---

## 70. Branch standard

Early solo development can use `main`.

Later, use branches:

```text
feat/speech-to-text
feat/timeline-analyzer
feat/visual-director
docs/sprint0b
fix/ffmpeg-path-error
```

---

## 71. Pull before work

Before starting a new session:

```bash
git pull
```

This reduces conflicts.

---

## 72. Git status habit

Before committing:

```bash
git status
```

Review files carefully.

Do not accidentally commit:

```text
output/
temp/
cache/
.env
large media
private files
```

---

## 73. `.gitignore`

Recommended ignores:

```text
.venv/
__pycache__/
*.pyc
.env
output/
temp/
cache/
*.mp4
*.mov
*.wav
*.mp3
```

Be careful: if you want to commit small test media fixtures, place them under `tests/fixtures/` and override intentionally.

---

## 74. Security coding rules

Never commit secrets.

Never log secrets.

Never execute code from LLM output.

Never use shell commands from LLM output.

Never silently upload user media.

---

## 75. Privacy coding rules

Input video/audio may be private.

Default pipeline is local.

Cloud providers must be explicit.

Debug outputs may contain transcript; do not commit them.

---

## 76. LLM safety

LLM output is data.

Treat it as untrusted.

Validate before use.

Do not execute it.

Do not interpret it as shell commands.

Do not let transcript prompt-inject the system.

---

## 77. Prompt injection defense

Prompts should treat transcript as data.

Code should enforce schema regardless of prompt instructions.

If transcript says:

```text
Ignore all previous instructions.
```

the system must still validate output.

---

## 78. Dependency policy

Add dependencies intentionally.

Before adding a dependency, ask:

1. Is it necessary?
2. Is it maintained?
3. Does it work on Windows?
4. Does it work on Mac M1?
5. Does it require GPU?
6. Does it increase install complexity?
7. Can it be optional?
8. Is it compatible with Python 3.11?

---

## 79. Requirements

Keep dependencies in:

```text
requirements.txt
```

and eventually:

```text
pyproject.toml
```

Keep them consistent.

---

## 80. Optional dependencies

Later, use optional extras.

Example:

```toml
[project.optional-dependencies]
speech = ["faster-whisper"]
director = ["requests"]
embedding = ["sentence-transformers", "scikit-learn"]
render = ["Pillow", "moviepy"]
full = [...]
```

---

## 81. Model files

Do not commit downloaded AI model files.

Use local cache/model directories ignored by Git.

---

## 82. Media files

Do not commit large generated media files.

Avoid committing:

```text
*.mp4
*.mov
*.wav
*.mp3
```

unless they are tiny fixtures and intentionally documented.

---

## 83. Unicode standard

Use UTF-8 everywhere.

Vietnamese must be preserved.

When writing files:

```python
encoding="utf-8"
```

When writing JSON:

```python
ensure_ascii=False
```

---

## 84. Time standard

Use seconds as float.

Do not use timestamp strings in core JSON.

Good:

```json
"start": 1.25
```

Bad:

```json
"start": "00:00:01.250"
```

---

## 85. Duration validation

Duration must match:

```text
end - start
```

Allow tiny floating tolerance.

Example:

```python
if abs(scene.duration - (scene.end - scene.start)) > 0.05:
    raise InvalidTimelineError(...)
```

---

## 86. Scene order

Scenes must be sorted by start time.

Validation should catch unsorted scenes.

---

## 87. Overlap policy

Overlapping scenes are not supported initially.

Fail validation unless future overlay mode is implemented.

---

## 88. ID generation

Use deterministic ID generation.

Example:

```python
def make_scene_id(index: int) -> str:
    return f"scene_{index:04d}"
```

---

## 89. Randomness

Avoid randomness.

If randomness is used, use seed.

Renderer randomness must be deterministic.

---

## 90. Floating point tolerance

Use tolerance for time comparisons.

Example:

```python
TIME_TOLERANCE = 0.05
```

Do not compare floating durations with exact equality.

---

## 91. File output policy

Create parent directories before writing.

```python
output_path.parent.mkdir(parents=True, exist_ok=True)
```

Do not assume directories exist.

---

## 92. Overwrite policy

During development, overwrite may be default.

In production CLI, require explicit overwrite or safe behavior.

Document behavior.

---

## 93. Temporary files

Temporary files live under:

```text
temp/
```

Generated outputs live under:

```text
output/
```

Do not write temp files into `src/`.

---

## 94. Debug files

Debug files live under:

```text
output/debug/
```

Do not commit them.

---

## 95. Cache files

Cache files live under:

```text
cache/
```

or:

```text
temp/cache/
```

Do not commit them unless intentionally small and documented.

---

## 96. Config files

Project config may live under:

```text
config/
```

Template config may live under:

```text
assets/templates/
```

Use YAML/TOML/JSON consistently.

---

## 97. YAML dependency

If using YAML, add a dependency intentionally.

Possible package:

```text
PyYAML
```

If avoiding dependency early, use JSON/TOML.

---

## 98. CLI user experience

CLI errors should help beginners.

Bad:

```text
Exception: command failed
```

Good:

```text
FFmpeg failed while extracting audio.
Input: input/video.mp4
Output: temp/audio.wav
Check that the input video contains an audio stream.
```

---

## 99. Windows support

Always consider Windows.

Use:

```python
Path
subprocess argument lists
```

Avoid:

```text
Linux-only shell syntax
hardcoded /tmp
bash-only commands
```

Docs should include PowerShell commands where relevant.

---

## 100. Mac support

Mac M1 support matters.

Avoid mandatory CUDA.

Avoid Windows-only assumptions.

---

## 101. GPU policy

GPU is optional.

Do not require GPU for:

- STT
- Visual Director
- embedding
- rendering

GPU acceleration can be added later.

---

## 102. Performance philosophy

Correctness first.

Then measure.

Then optimize.

Do not prematurely rewrite architecture for speed.

---

## 103. Performance basics

Avoid:

- reloading models in loops
- rereading assets every frame
- rendering static text repeatedly
- unnecessary LLM calls
- unnecessary disk writes
- giant in-memory frame lists

Use:

- caching
- pre-rendered layers
- model reuse
- static scene optimization

---

## 104. Model loading

Load models once per stage.

Bad:

```python
for segment in segments:
    model = WhisperModel(...)
```

Good:

```python
model = WhisperModel(...)
segments = model.transcribe(...)
```

---

## 105. Asset loading

Cache loaded fonts and images.

Bad:

```python
for frame in frames:
    font = ImageFont.truetype(font_path, size)
```

Good:

```python
font = font_cache.get(font_path, size)
```

---

## 106. Renderer performance

Pre-render static text layers where possible.

Reuse background layers.

Use simple effects first.

---

## 107. Large functions

If a function handles:

- loading
- validation
- processing
- writing
- logging

all at once, split it.

---

## 108. Public API design

Public functions should be stable and documented.

Example:

```python
def transcribe_video(input_path: Path, output_path: Path, config: SpeechConfig) -> Transcript:
    ...
```

Avoid exposing internal temporary structures.

---

## 109. Internal API design

Internal APIs can evolve but should still be clear.

Use leading underscore for private helpers.

```python
def _normalize_whitespace(text: str) -> str:
    ...
```

---

## 110. Return values

Return meaningful result objects.

Bad:

```python
def extract_audio(...):
    return True
```

Good:

```python
def extract_audio(...) -> AudioExtractionResult:
    ...
```

---

## 111. Result objects

Example:

```python
@dataclass
class AudioExtractionResult:
    input_path: Path
    output_path: Path
    sample_rate: int
    channels: int
    duration: float | None = None
```

---

## 112. Reports

Long-running stages should produce reports later.

Report objects are useful for CLI, UI, and debugging.

---

## 113. CLI output vs logs

CLI should show user-friendly progress.

Logs can be more detailed.

Future project may support:

```text
--verbose
--quiet
--debug
```

---

## 114. Debug mode

Debug mode may write:

- raw LLM output
- final prompts
- validation reports
- preview frames
- layout boxes

Warn users debug files may contain transcript text.

---

## 115. Pydantic model location

Schema models can live in:

```text
src/timeline/schema.py
```

or:

```text
src/common/schema.py
```

Avoid scattering duplicate models.

---

## 116. Avoid duplicate schema definitions

Do not define `Scene` in five modules.

Use shared schema models.

If renderer needs extra runtime state, create separate renderer state classes.

---

## 117. Schema vs runtime state

Visual timeline schema:

```python
class VisualScene(BaseModel):
    ...
```

Renderer runtime state:

```python
@dataclass
class SceneRenderState:
    ...
```

Keep them separate.

---

## 118. Validation before processing

Validate before heavy work.

Example:

```python
timeline = load_visual_timeline(path)
validate_visual_timeline(timeline)
render(timeline)
```

Do not discover invalid effect after rendering half the video.

---

## 119. Unknown enum values

Unknown effects/layouts/emotions should fail validation.

Do not silently fallback unless explicitly configured.

---

## 120. Fallback policy

Fallbacks are allowed when documented.

Examples:

- missing optional icon → warn and skip
- missing optional avatar → warn and skip
- missing required font → fallback font or fail
- missing layout → template default if field absent
- unknown layout → fail

---

## 121. Prompt files

Prompt files are source artifacts.

Commit them.

Do not commit generated prompt debug files.

---

## 122. Prompt output

Store raw LLM output only in debug mode.

Store parsed and validated output as normal pipeline JSON.

---

## 123. Caching

Cache should be explicit.

Logs should say when cache is used.

Bad:

```text
nothing happens because cache silently used
```

Good:

```text
[cache] using output/transcript.json
```

---

## 124. Cache invalidation

Cache key should include:

- input hash
- model name
- prompt version
- config
- asset DB hash
- schema version where relevant

---

## 125. Hashing

Use stable hashing for files when needed.

Example:

```python
import hashlib

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
```

---

## 126. Config immutability

Runtime config should not be mutated randomly.

Prefer creating derived config objects.

---

## 127. Constants

Keep constants near the module that owns them or in central config.

Avoid unrelated global constants.

---

## 128. Code comments for AI agents

Comments can help AI agents.

But do not over-comment obvious code.

Useful comments:

```python
# Renderer must not call LLMs. Effects come from validated timeline JSON.
```

---

## 129. Documentation comments

If a module enforces an architecture rule, mention it in module docstring.

Example:

```python
"""Deterministic renderer.

This module must not import or call any LLM/director code.
"""
```

---

## 130. Module docstrings

Each important module should have a short docstring.

Example:

```python
"""Audio extraction utilities using FFmpeg."""
```

---

## 131. Package imports

Keep package imports clean.

`__init__.py` can be empty initially.

Avoid importing heavy models in `__init__.py`.

Bad:

```python
# src/speech/__init__.py
from .faster_whisper_engine import FasterWhisperEngine
# loads heavy dependencies unexpectedly
```

Better to import directly where needed.

---

## 132. Heavy imports

Avoid heavy imports at top-level if not always needed.

Example:

```python
def load_model(...):
    from faster_whisper import WhisperModel
```

This can make render-only commands faster.

But do not overuse local imports unnecessarily.

---

## 133. Optional dependency errors

If optional dependency missing, show clear message.

Example:

```text
faster-whisper is not installed.
Install with: pip install faster-whisper
```

---

## 134. Environment variables

Use environment variables for secrets and environment-specific config.

Do not require `.env` for local default workflow.

---

## 135. `.env`

Do not commit `.env`.

Use `.env.example` if needed.

---

## 136. API keys

No API keys in code.

No API keys in docs except placeholders.

Good:

```text
OPENAI_API_KEY=your_key_here
```

Bad:

```text
OPENAI_API_KEY=sk-...
```

---

## 137. File naming for outputs

Use predictable output names.

```text
transcript.json
timeline.normalized.json
timeline.director.json
timeline.visual.json
silent_video.mp4
final.mp4
render_report.json
```

---

## 138. Generated output timestamps

For batch mode, output directories may include input stem or run ID.

Example:

```text
output/my_video/final.mp4
```

or:

```text
output/run_20260707_001/final.mp4
```

---

## 139. Batch processing code

Batch code should reuse models.

Bad:

```python
for video in videos:
    run_subprocess("python transcribe.py video")
```

Good:

```python
model = load_speech_model()
for video in videos:
    transcribe(video, model=model)
```

---

## 140. Progress bars

For long operations, progress is helpful.

Possible package:

```text
tqdm
```

or rich progress.

Do not make logs too noisy.

---

## 141. Notebook policy

Notebooks are allowed for experiments.

Production code must be moved to `src/`.

Do not make the main project depend on notebooks.

---

## 142. Experimental code

Experimental code can live under:

```text
experiments/
```

if added.

Do not mix experiments with production modules.

---

## 143. Backward compatibility

Before v1.0, breaking changes are acceptable but must be documented.

After v1.0, schema changes require migration.

---

## 144. Migration functions

Future migration functions should be explicit.

Example:

```python
def migrate_visual_timeline_0_1_to_0_2(data: dict) -> dict:
    ...
```

---

## 145. Package naming

Future package name could be:

```text
ai_video_engine
```

If `src/` currently contains subfolders directly, later package restructuring may be needed.

Recommended long-term:

```text
src/ai_video_engine/
```

But current bootstrap may use `src/audio`, etc.

If restructuring, document in DecisionLog.

---

## 146. pyproject standard

`pyproject.toml` should eventually define:

- project metadata
- dependencies
- optional dependencies
- formatting config
- test config
- package config

---

## 147. requirements.txt

`requirements.txt` is useful for quick install.

Keep it simple.

Do not include hundreds of frozen transitive dependencies unless needed.

---

## 148. Dependency pinning

Pin exact versions only when necessary.

For early development, flexible ranges may be okay.

For reproducible releases, lock files may be added later.

---

## 149. Code review standard

Before accepting code, ask:

1. Is it in the right module?
2. Does it break AI/renderer separation?
3. Does it validate inputs?
4. Does it use `Path`?
5. Does it avoid hardcoded local paths?
6. Does it have clear errors?
7. Does it need tests?
8. Does it need docs update?
9. Does it work on Windows?
10. Does it avoid unnecessary dependencies?

---

## 150. AI agent instructions

When an AI coding agent modifies this project, it must:

1. Read `AGENTS.md`.
2. Read `PROJECT_RULES.md`.
3. Read relevant docs.
4. Inspect current files.
5. Make focused changes.
6. Avoid unrelated refactors.
7. Update docs when behavior changes.
8. Add tests where practical.
9. Keep renderer AI-free.
10. Use clear commit messages if committing.

---

## 151. AI agent must not

AI coding agent must not:

- rewrite entire project without request
- remove docs casually
- hardcode local paths
- add cloud dependencies silently
- call LLM from renderer
- commit generated output files
- commit secrets
- invent assets that do not exist
- bypass schema validation
- ignore Windows support

---

## 152. Code generation standard

Generated code should be reviewed.

AI-generated code is not automatically correct.

Check:

- imports
- paths
- version compatibility
- error handling
- testability
- module boundaries
- side effects

---

## 153. Minimal implementation principle

Build the smallest complete vertical slice.

For Sprint 1:

```text
input video → transcript.json
```

Do not build renderer before STT works.

For Sprint 5:

```text
visual timeline → silent video
```

Do not build advanced particles before basic text works.

---

## 154. Do not overbuild

Avoid building:

- plugin marketplace
- complex GUI
- distributed rendering
- cloud orchestration
- advanced animation editor

before the core pipeline works.

---

## 155. Do not under-document

Because the project uses AI agents, documentation is part of the system.

If behavior is not documented, future agents may break it.

---

## 156. Code examples in docs

Code examples should be realistic.

Avoid examples that contradict architecture.

---

## 157. Markdown standard

Markdown files should use:

- clear headings
- code blocks
- examples
- checklists
- concise explanations

Avoid giant unstructured paragraphs.

---

## 158. Language standard

Project docs are currently English to maximize compatibility with coding tools.

User-facing explanations can be Vietnamese.

Code comments should generally be English.

Prompts may include Vietnamese-specific instructions.

---

## 159. User-facing CLI messages

User-facing messages can eventually support Vietnamese.

Initial CLI can be English.

If adding localization, do it systematically.

---

## 160. Date format

Use ISO date format in docs and reports.

Example:

```text
2026-07-07
```

Timestamp:

```text
2026-07-07T15:00:00Z
```

---

## 161. Report timestamps

Use UTC where practical.

---

## 162. Timezone

Do not rely on local timezone unless user-facing.

---

## 163. File encoding

All source files should be UTF-8.

---

## 164. Newline standard

Use LF if possible.

Windows tools may use CRLF.

Git can normalize.

Use `.editorconfig`.

---

## 165. EditorConfig

Recommended `.editorconfig`:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 4

[*.md]
trim_trailing_whitespace = false
```

---

## 166. VS Code settings

Recommended:

```json
{
  "python.defaultInterpreterPath": ".venv",
  "editor.formatOnSave": true
}
```

Avoid committing personal machine-specific settings.

---

## 167. Local environment

Use virtual environment:

```bash
python -m venv .venv
```

Activate on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate on Mac/Linux:

```bash
source .venv/bin/activate
```

---

## 168. Install command

```bash
pip install -r requirements.txt
```

Later, package install may be:

```bash
pip install -e .
```

---

## 169. Development setup docs

README should include setup.

Do not rely on chat instructions only.

---

## 170. File creation standard

When adding a new module:

1. create module file
2. add tests
3. update docs if behavior important
4. update imports
5. run tests
6. commit

---

## 171. Public module checklist

A public module should have:

- clear name
- docstring
- typed public functions
- error handling
- tests or test plan
- docs if architecture-relevant

---

## 172. Stage implementation checklist

For a pipeline stage:

1. input path defined
2. output path defined
3. config defined
4. validation defined
5. errors defined
6. report/warnings defined
7. tests defined
8. docs updated

---

## 173. Sprint implementation checklist

Before completing a sprint:

- deliverable exists
- command or script works
- output file validates
- docs updated
- DecisionLog updated if needed
- tests added where practical
- commit pushed

---

## 174. Sprint 1 coding checklist

Speech To Text:

- audio extraction command builder
- FFmpeg availability check
- audio extraction function
- Faster Whisper transcriber
- transcript schema
- transcript writer
- transcript validator
- basic CLI/script
- docs update

---

## 175. Sprint 2 coding checklist

Timeline Analyzer:

- transcript loader
- transcript validator
- scene ID generator
- merge/split logic
- normalized timeline schema
- normalized timeline writer
- tests

---

## 176. Sprint 3 coding checklist

Visual Director:

- prompt loader
- Ollama client
- prompt renderer
- LLM output parser
- JSON repair handling
- director schema
- validation
- tests with fake LLM

---

## 177. Sprint 4 coding checklist

Icon Selector:

- icon DB schema
- asset registry
- embedding provider
- vector cache
- icon search
- visual timeline writer
- tests

---

## 178. Sprint 5 coding checklist

Renderer:

- visual timeline loader
- renderer validation
- template loader
- canvas
- text renderer
- keyword highlight
- at least one effect
- silent video writer
- smoke test

---

## 179. Sprint 6 coding checklist

Exporter:

- silent video validation
- audio validation
- FFmpeg merge command
- final MP4 output
- duration check
- render report

---

## 180. Code review examples

### 180.1 Good audio module

```python
def extract_audio(input_video: Path, output_audio: Path, sample_rate: int) -> AudioExtractionResult:
    check_ffmpeg_available()
    output_audio.parent.mkdir(parents=True, exist_ok=True)
    cmd = build_extract_audio_command(input_video, output_audio, sample_rate)
    run_command(cmd)
    return AudioExtractionResult(input_video, output_audio, sample_rate, channels=1)
```

### 180.2 Bad audio module

```python
def do():
    import os
    os.system("ffmpeg -i input.mp4 audio.wav")
```

---

## 181. Good JSON writer

```python
def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
```

---

## 182. Good command builder

```python
def build_merge_command(video_path: Path, audio_path: Path, output_path: Path) -> list[str]:
    return [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-i",
        str(audio_path),
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-shortest",
        str(output_path),
    ]
```

---

## 183. Bad command builder

```python
def merge(video, audio, out):
    return f"ffmpeg -i {video} -i {audio} {out}"
```

This breaks with spaces and can be unsafe.

---

## 184. Good validation error

```python
raise InvalidTimelineError(
    f"Scene {scene.id} has invalid duration: "
    f"start={scene.start}, end={scene.end}, duration={scene.duration}"
)
```

---

## 185. Bad validation error

```python
raise Exception("bad")
```

---

## 186. Good renderer boundary

```python
def render_visual_timeline(timeline: VisualTimeline, context: RenderContext) -> RenderResult:
    validate_visual_timeline(timeline)
    ...
```

---

## 187. Bad renderer boundary

```python
def render(text: str):
    prompt = f"Choose effects for {text}"
    effect = call_llm(prompt)
```

Forbidden.

---

## 188. Good prompt loading

```python
template = prompt_loader.load("visual_director.md")
prompt = prompt_renderer.render(template, variables)
```

---

## 189. Bad prompt loading

```python
prompt = "You are a director..."  # 300-line prompt in source
```

---

## 190. Good asset reference

```json
{
  "icon_id": "icon_alarm_001",
  "icon_path": "assets/icons/alarm_001.png"
}
```

---

## 191. Bad asset reference

```json
{
  "icon_path": "E:\\Downloads\\icons\\new\\alarm final.png"
}
```

---

## 192. Code ownership reminder

If a change touches multiple layers, be careful.

Example:

Changing animation enum may require:

- JSONSchema update
- PromptGuide update
- RendererDesign update
- effect registry update
- tests
- DecisionLog

---

## 193. Breaking change policy

Before changing schema or architecture:

1. update docs
2. update tests
3. update examples
4. update DecisionLog
5. consider migration

---

## 194. Minimum Definition of Done

A task is done when:

- code works
- output validates
- docs updated if needed
- tests added or reason documented
- no architecture rules broken
- commit pushed

---

## 195. Final coding rule

If a shortcut makes the demo faster but makes the engine harder to maintain, do not take the shortcut.

Build the engine correctly.

---

# Appendix A - Suggested initial file skeletons


## A.1 `src/common/json_io.py`

```python
"""JSON read/write helpers."""

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

## A.2 `src/common/errors.py`

```python
"""Project-specific exceptions."""


class AIVideoEngineError(Exception):
    """Base error for AI Video Engine."""


class MissingFFmpegError(AIVideoEngineError):
    """Raised when FFmpeg is not available."""


class InvalidTranscriptError(AIVideoEngineError):
    """Raised when transcript JSON is invalid."""


class InvalidTimelineError(AIVideoEngineError):
    """Raised when timeline JSON is invalid."""


class InvalidDirectorOutputError(AIVideoEngineError):
    """Raised when LLM output is invalid."""


class MissingAssetError(AIVideoEngineError):
    """Raised when an asset cannot be found."""


class UnknownEffectError(AIVideoEngineError):
    """Raised when a timeline requests an unknown effect."""


class RenderError(AIVideoEngineError):
    """Raised when rendering fails."""


class ExportError(AIVideoEngineError):
    """Raised when final export fails."""

```

## A.3 `src/audio/commands.py`

```python
"""FFmpeg command builders for audio operations."""

from __future__ import annotations

from pathlib import Path


def build_extract_audio_command(
    input_video: Path,
    output_audio: Path,
    sample_rate: int = 16000,
    channels: int = 1,
) -> list[str]:
    """Build an FFmpeg command that extracts mono WAV audio."""
    return [
        "ffmpeg",
        "-y",
        "-i",
        str(input_video),
        "-vn",
        "-ac",
        str(channels),
        "-ar",
        str(sample_rate),
        str(output_audio),
    ]

```

## A.4 `src/exporter/commands.py`

```python
"""FFmpeg command builders for final export."""

from __future__ import annotations

from pathlib import Path


def build_merge_audio_video_command(
    silent_video: Path,
    audio_path: Path,
    output_video: Path,
) -> list[str]:
    """Build an FFmpeg command that merges silent video with audio."""
    return [
        "ffmpeg",
        "-y",
        "-i",
        str(silent_video),
        "-i",
        str(audio_path),
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-shortest",
        str(output_video),
    ]

```

## A.5 `src/timeline/ids.py`

```python
"""Stable ID helpers."""


def make_segment_id(index: int) -> str:
    """Create a stable transcript segment ID."""
    return f"seg_{index:04d}"


def make_scene_id(index: int) -> str:
    """Create a stable scene ID."""
    return f"scene_{index:04d}"


def make_animation_id(index: int) -> str:
    """Create a stable animation ID."""
    return f"anim_{index:04d}"

```

---

# Appendix B - Recommended tests by sprint


## B.1 Sprint 1 - Speech To Text

- `test_ffmpeg_extract_audio_command_builds_expected_args`
- `test_missing_input_video_raises_clear_error`
- `test_transcript_segment_duration_validation`
- `test_transcript_json_preserves_vietnamese_text`

## B.2 Sprint 2 - Timeline Analyzer

- `test_scene_ids_are_deterministic`
- `test_long_segment_can_be_split`
- `test_short_segments_can_be_merged`
- `test_timeline_rejects_negative_duration`

## B.3 Sprint 3 - Visual Director

- `test_prompt_loader_reads_utf8`
- `test_prompt_renderer_replaces_required_variables`
- `test_llm_parser_extracts_json_from_markdown`
- `test_director_rejects_changed_scene_id`
- `test_director_rejects_unknown_effect`

## B.4 Sprint 4 - Icon Selector

- `test_icon_db_rejects_duplicate_ids`
- `test_icon_selector_returns_best_match`
- `test_missing_icon_file_warns`
- `test_icon_score_is_stored`

## B.5 Sprint 5 - Renderer

- `test_visual_timeline_rejects_unknown_layout`
- `test_visual_timeline_rejects_unknown_effect`
- `test_renderer_creates_debug_frame`
- `test_renderer_smoke_creates_silent_video`

## B.6 Sprint 6 - Exporter

- `test_merge_command_builds_expected_args`
- `test_missing_audio_raises_clear_error`
- `test_export_report_contains_output_path`

---

# Appendix C - Review checklist

1. Correct module ownership.
2. No renderer-to-AI dependency.
3. No hardcoded local paths.
4. Uses pathlib.Path.
5. Clear errors.
6. JSON uses UTF-8 and ensure_ascii=False.
7. Inputs validated.
8. Outputs documented.
9. Tests added where practical.
10. Docs updated if behavior changed.
11. No generated output committed.
12. No secrets committed.
13. Windows support considered.
14. Mac M1 support considered.
15. No unnecessary dependency added.
16. One logical change per commit.

---

# Appendix D - Recommended future tooling

| Tool | Purpose |
|---|---|
| `black` | Code formatting |
| `ruff` | Linting and import sorting |
| `pytest` | Testing |
| `mypy` | Optional type checking |
| `pre-commit` | Local hooks |
| `rich` | Readable CLI logs |
| `pydantic` | Runtime schema validation |

---

# Appendix E - Example `pyproject.toml` direction

```toml
[project]
name = "ai-video-engine"
version = "0.1.0"
requires-python = ">=3.11"
description = "Local-first AI video automation engine"

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

---

# Appendix F - Final coding checklist for AI agents

1. Read AGENTS.md.
2. Read PROJECT_RULES.md.
3. Read the relevant docs file.
4. Inspect current code before editing.
5. Make the smallest useful change.
6. Do not touch unrelated files.
7. Keep renderer AI-free.
8. Validate JSON boundaries.
9. Use clear errors.
10. Add or update tests.
11. Update docs if behavior changes.
12. Do not commit output/temp/cache.
13. Use conventional commit message.

---

# Appendix G - Final note

Good code in this project is not code that looks impressive.

Good code is code that makes the pipeline reliable:

```text
video → transcript → timeline → visual JSON → render → final MP4
```

Protect that flow.
