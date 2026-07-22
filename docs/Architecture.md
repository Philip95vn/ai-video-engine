# Architecture.md

# AI Video Engine - Architecture

## 0. Purpose

This document defines the technical architecture of **AI Video Engine**.

It explains:

- system boundaries
- module responsibilities
- data flow
- JSON contracts
- AI boundaries
- renderer boundaries
- storage conventions
- extension points
- future scaling path

This document should be read together with:

```text
AGENTS.md
PROJECT_RULES.md
docs/Pipeline.md
docs/JSONSchema.md
docs/AIDesign.md
docs/RendererDesign.md
docs/DecisionLog.md
```

The purpose of this architecture is to keep the project maintainable as it grows from a prototype into a reusable engine.

---

## 1. Architectural summary

AI Video Engine is a local-first modular video automation engine.

It converts input media into a new short-form video using a deterministic renderer controlled by structured JSON.

The main architectural idea is:

```text
AI produces structured instructions.
Renderer consumes structured instructions.
```

The renderer does not ask AI what to do.

The AI does not render pixels.

The JSON timeline is the contract.

---

## 2. Primary architecture diagram

```text
┌──────────────────────────┐
│      Input Media         │
│  video.mp4 / audio.wav   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│      Audio Extractor     │
│       src/audio/         │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Speech To Text       │
│       src/speech/        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Transcript JSON      │
│ output/transcript.json   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│    Timeline Analyzer     │
│      src/timeline/       │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  Normalized Timeline     │
│ timeline.normalized.json │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   Visual Director AI     │
│      src/director/       │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│      Icon Selector       │
│     src/embedding/       │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  Visual Timeline JSON    │
│ timeline.visual.json     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       Renderer           │
│      src/renderer/       │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Silent Video         │
│ output/silent_video.mp4  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       Exporter           │
│      src/exporter/       │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       Final MP4          │
│    output/final.mp4      │
└──────────────────────────┘
```

---

## 3. Core architectural principles

### 3.1 AI and renderer separation

The AI layer is responsible for interpretation.

The renderer layer is responsible for execution.

AI output is declarative.

Renderer behavior is deterministic.

This separation allows:

- reproducibility
- testability
- template reuse
- local rendering
- lower cost
- future model replacement
- easier debugging

### 3.2 JSON-first design

The system is built around structured intermediate files.

The most important files are:

```text
output/transcript.json
output/timeline.normalized.json
output/timeline.visual.json
output/render_report.json
```

These files make the pipeline inspectable.

They also allow manual editing and debugging.

### 3.3 Local-first execution

The default system must run locally.

External cloud APIs may be supported later, but they must be optional.

Local-first architecture protects:

- privacy
- cost
- repeatability
- batch rendering
- offline workflows

### 3.4 Modular replacement

Each major component should be replaceable.

Examples:

- Faster Whisper can be replaced by WhisperX.
- Qwen can be replaced by another LLM.
- MoviePy renderer can be replaced by FFmpeg/OpenCV renderer.
- local icon embedding can be replaced by vector database.
- CLI can be replaced or extended by GUI/API.

### 3.5 Deterministic rendering

The renderer should produce predictable output.

If randomness is used, it must be seeded.

Rendering must not depend on live LLM calls.

---

## 4. Architectural layers

The system has six major layers.

```text
Interface Layer
Application Layer
AI Layer
Timeline Layer
Rendering Layer
Infrastructure Layer
```

---

## 5. Interface layer

The interface layer exposes the engine to users.

Initial interfaces:

```text
CLI
scripts
Python module calls
```

Future interfaces:

```text
desktop app
web app
API server
VS Code integration
batch processing UI
```

The interface layer should not contain core business logic.

It should call the application layer.

---

## 6. Application layer

The application layer coordinates pipeline stages.

It answers questions like:

- Which stage runs next?
- Which files are input and output?
- Which config should be used?
- Should cached output be reused?
- Should errors stop the pipeline?

Potential future module:

```text
src/app/
```

or:

```text
src/pipeline/
```

Early versions may use scripts, but the long-term architecture should separate orchestration from module logic.

---

## 7. AI layer

The AI layer includes:

```text
src/speech/
src/director/
src/embedding/
```

These modules use models.

They do not render video.

### AI layer responsibilities

- speech recognition
- dialogue understanding
- keyword extraction
- emotion classification
- icon query generation
- semantic asset matching

### AI layer restrictions

AI layer must not:

- generate final video
- directly create rendered frames
- bypass JSON schema
- silently modify timing
- invent unavailable final assets without verification

---

## 8. Timeline layer

The timeline layer is the structural heart of the system.

It includes:

```text
src/timeline/
```

It transforms raw transcript into renderable scenes.

It ensures:

- valid timing
- valid scene IDs
- readable scene sizes
- normalized text
- schema compatibility
- deterministic structure

The timeline layer is not an LLM layer.

It should work the same way every time.

---

## 9. Rendering layer

The rendering layer includes:

```text
src/renderer/
src/exporter/
```

It converts timeline JSON into media files.

Renderer creates silent video.

Exporter merges audio and writes final output.

Rendering layer must not call AI.

---

## 10. Infrastructure layer

Infrastructure includes:

```text
src/common/
src/config/
assets/
prompts/
temp/
output/
```

It provides:

- config loading
- path handling
- logging
- validation helpers
- asset lookup
- prompt loading
- cache management

---

## 11. Module map

```text
src/
├── audio/
│   └── audio extraction and conversion
│
├── speech/
│   └── speech-to-text
│
├── timeline/
│   └── transcript normalization and scene creation
│
├── director/
│   └── LLM-based visual direction
│
├── embedding/
│   └── asset semantic search
│
├── renderer/
│   └── visual rendering and animation
│
├── exporter/
│   └── final video/audio packaging
│
├── assets/
│   └── asset registry helpers
│
├── common/
│   └── shared utilities
│
└── config/
    └── configuration loading
```

---

## 12. `src/audio` architecture

### 12.1 Purpose

The audio module prepares audio for downstream processing.

It handles FFmpeg-based audio extraction and conversion.

### 12.2 Responsibilities

- validate input media exists
- extract audio from video
- convert audio to WAV
- normalize sample rate
- convert to mono if required
- preserve original audio path
- provide metadata about extracted audio

### 12.3 Non-responsibilities

The audio module must not:

- transcribe audio
- detect speakers
- select keywords
- render anything
- call LLMs

### 12.4 Expected input

```text
input/video.mp4
```

or:

```text
input/audio.wav
```

### 12.5 Expected output

```text
temp/audio.wav
```

### 12.6 Typical FFmpeg command

```bash
ffmpeg -y -i input/video.mp4 -vn -ac 1 -ar 16000 temp/audio.wav
```

### 12.7 Suggested functions

```python
extract_audio(input_video: Path, output_audio: Path, sample_rate: int = 16000) -> AudioExtractionResult
check_ffmpeg_available() -> bool
probe_media(input_path: Path) -> MediaInfo
```

### 12.8 Suggested data object

```python
@dataclass
class AudioExtractionResult:
    input_path: Path
    output_path: Path
    duration: float | None
    sample_rate: int
    channels: int
```

---

## 13. `src/speech` architecture

### 13.1 Purpose

The speech module converts audio into timestamped text.

### 13.2 First implementation

Use Faster Whisper.

### 13.3 Responsibilities

- load STT model
- transcribe audio
- preserve timestamps
- export transcript JSON
- support Vietnamese
- support model configuration

### 13.4 Non-responsibilities

The speech module must not:

- choose visual effects
- split text for rendering
- choose icons
- render text
- call Visual Director

### 13.5 Input

```text
temp/audio.wav
```

### 13.6 Output

```text
output/transcript.json
```

### 13.7 Transcript segment

```json
{
  "id": "seg_0001",
  "start": 0.25,
  "end": 2.16,
  "text": "Ê! Sao hôm nay đến trễ?"
}
```

### 13.8 Suggested classes

```python
class SpeechToTextEngine:
    def transcribe(self, audio_path: Path) -> Transcript:
        ...
```

```python
@dataclass
class TranscriptSegment:
    id: str
    start: float
    end: float
    text: str
```

```python
@dataclass
class Transcript:
    language: str
    duration: float | None
    segments: list[TranscriptSegment]
```

### 13.9 Configuration

```yaml
speech:
  provider: faster_whisper
  model: medium
  language: vi
  device: cpu
  compute_type: int8
  vad_filter: true
```

---

## 14. `src/timeline` architecture

### 14.1 Purpose

The timeline module transforms raw transcript into scene-based timeline data.

### 14.2 Responsibilities

- clean text
- normalize punctuation
- split long segments
- merge very short segments
- create scene IDs
- compute duration
- assign initial speaker labels
- validate chronological order
- produce normalized timeline JSON

### 14.3 Non-responsibilities

The timeline module must not:

- call LLMs
- select icons
- create final animation decisions
- render video
- call FFmpeg

### 14.4 Input

```text
output/transcript.json
```

### 14.5 Output

```text
output/timeline.normalized.json
```

### 14.6 Normalized scene

```json
{
  "id": "scene_0001",
  "source_segment_ids": ["seg_0001"],
  "start": 0.25,
  "end": 2.16,
  "duration": 1.91,
  "speaker": {
    "id": "SPEAKER_00",
    "label": null,
    "source": "inferred",
    "confidence": null
  },
  "text": "Ê! Sao hôm nay đến trễ?"
}
```

### 14.7 Suggested classes

```python
class TimelineAnalyzer:
    def normalize(self, transcript: Transcript) -> Timeline:
        ...
```

```python
@dataclass
class TimelineScene:
    id: str
    start: float
    end: float
    duration: float
    text: str
```

### 14.8 Determinism

The same transcript and configuration must produce the same normalized timeline.

---

## 15. `src/director` architecture

### 15.1 Purpose

The director module uses LLMs to enrich normalized timeline with visual instructions.

### 15.2 Responsibilities

- load prompt templates
- call local LLM through Ollama
- parse JSON output
- repair JSON if needed
- validate output
- select keywords
- select emotion
- suggest layout
- suggest effect
- suggest icon query
- produce visual timeline JSON

### 15.3 Non-responsibilities

The director module must not:

- render frames
- pick exact icon file unless asset list is provided
- call FFmpeg
- mutate source media
- create final MP4

### 15.4 Input

```text
output/timeline.normalized.json
```

### 15.5 Output

```text
output/timeline.visual.json
```

### 15.6 Visual scene

```json
{
  "id": "scene_0001",
  "start": 0.25,
  "end": 2.16,
  "duration": 1.91,
  "speaker": {
    "id": "SPEAKER_00",
    "label": "Nam"
  },
  "text": "Ê! Sao hôm nay đến trễ?",
  "lines": ["Ê!", "SAO HÔM NAY", "ĐẾN TRỄ?"],
  "emotion": "surprised",
  "keywords": [
    {
      "text": "ĐẾN TRỄ",
      "importance": 0.95,
      "effect": "pop",
      "style": "keyword_primary"
    }
  ],
  "layout": {
    "name": "center_stack"
  },
  "assets": {
    "icon_query": "đồng hồ báo thức"
  }
}
```

### 15.7 LLM runtime

Initial runtime:

```text
Ollama
```

Initial model:

```text
qwen2.5:3b
```

### 15.8 Suggested classes

```python
class VisualDirector:
    def enrich(self, timeline: Timeline) -> VisualTimeline:
        ...
```

```python
class OllamaClient:
    def generate_json(self, prompt: str) -> dict:
        ...
```

---

## 16. `src/embedding` architecture

### 16.1 Purpose

The embedding module maps semantic queries to assets.

The first use is icon selection.

### 16.2 Responsibilities

- load icon metadata
- create embeddings
- cache embeddings
- search nearest icons
- return icon ID and confidence

### 16.3 Non-responsibilities

The embedding module must not:

- render icons
- change scene timing
- call LLM for every icon if embeddings are enough
- invent missing icons

### 16.4 Input

```json
{
  "icon_query": "báo thức"
}
```

### 16.5 Output

```json
{
  "icon_id": "icon_alarm_001",
  "icon_path": "assets/icons/alarm.png",
  "score": 0.86
}
```

### 16.6 Icon metadata

```json
{
  "id": "icon_alarm_001",
  "file": "assets/icons/alarm.png",
  "tags": ["báo thức", "đồng hồ", "trễ giờ", "dậy sớm"],
  "style": "flat",
  "mood": ["urgent", "funny"]
}
```

### 16.7 Suggested classes

```python
class IconSearchEngine:
    def search(self, query: str, top_k: int = 1) -> list[IconMatch]:
        ...
```

```python
@dataclass
class IconMatch:
    icon_id: str
    path: Path
    score: float
```

---

## 17. `src/renderer` architecture

### 17.1 Purpose

The renderer converts visual timeline JSON into silent video.

### 17.2 Responsibilities

- validate visual timeline
- load template
- load assets
- prepare canvas
- render backgrounds
- render text
- render keywords
- render icons
- render avatars
- apply animations
- write silent video

### 17.3 Non-responsibilities

The renderer must not:

- call LLMs
- transcribe audio
- merge final audio
- choose semantic keywords
- search icons semantically
- modify source transcript

### 17.4 Input

```text
output/timeline.visual.json
```

### 17.5 Output

```text
output/silent_video.mp4
```

### 17.6 Renderer submodules

Recommended structure:

```text
src/renderer/
├── engine.py
├── canvas.py
├── text.py
├── keyword.py
├── icon.py
├── avatar.py
├── background.py
├── layout.py
├── template.py
├── effects/
│   ├── pop.py
│   ├── shake.py
│   ├── bounce.py
│   ├── glow.py
│   └── slide.py
└── registry.py
```

### 17.7 Effect registry

Effects should be registered.

Unknown effects must fail validation.

Example:

```python
EFFECT_REGISTRY = {
    "pop": PopEffect,
    "shake": ShakeEffect,
    "bounce": BounceEffect,
    "glow": GlowEffect,
    "slide": SlideEffect,
}
```

### 17.8 Layout registry

Layouts should be registered.

Example:

```python
LAYOUT_REGISTRY = {
    "center_stack": CenterStackLayout,
    "comic_panel": ComicPanelLayout,
    "split_speaker": SplitSpeakerLayout,
}
```

---

## 18. `src/exporter` architecture

### 18.1 Purpose

The exporter creates the final video file.

### 18.2 Responsibilities

- merge silent video with original audio
- encode final MP4
- validate duration
- create render report
- write final output path

### 18.3 Non-responsibilities

The exporter must not:

- render visual elements
- call LLMs
- transcribe audio
- change visual timeline

### 18.4 Input

```text
output/silent_video.mp4
temp/audio.wav
```

### 18.5 Output

```text
output/final.mp4
output/render_report.json
```

### 18.6 Typical FFmpeg command

```bash
ffmpeg -y -i output/silent_video.mp4 -i temp/audio.wav -c:v copy -c:a aac -shortest output/final.mp4
```

---

## 19. `src/common` architecture

### 19.1 Purpose

Common utilities used across modules.

### 19.2 Allowed utilities

- path helpers
- JSON helpers
- logging helpers
- time helpers
- error classes
- validation utilities

### 19.3 Not allowed

Do not place core business logic in common.

If a function belongs to a domain module, keep it there.

---

## 20. `src/config` architecture

### 20.1 Purpose

Load and validate configuration.

### 20.2 Config sources

Possible config files:

```text
config/default.yaml
config/models.yaml
config/templates/*.yaml
```

### 20.3 Suggested config areas

```yaml
video:
  width: 1080
  height: 1920
  fps: 30

speech:
  provider: faster_whisper
  model: medium
  language: vi

director:
  provider: ollama
  model: qwen2.5:3b

renderer:
  template: tiktok_dark_comic

paths:
  input: input
  temp: temp
  output: output
```

---

## 21. Data contracts

Data contracts define how modules communicate.

The project should avoid passing unstructured dictionaries between modules without validation.

Recommended contracts:

```text
MediaInfo
AudioExtractionResult
Transcript
TranscriptSegment
Timeline
TimelineScene
VisualTimeline
VisualScene
Keyword
Animation
AssetReference
RenderReport
```

---

## 22. Transcript contract

Transcript is raw STT output.

It should not contain visual decisions.

Example:

```json
{
  "schema_version": "0.1.0",
  "language": "vi",
  "segments": [
    {
      "id": "seg_0001",
      "start": 0.25,
      "end": 2.16,
      "text": "Ê! Sao hôm nay đến trễ?"
    }
  ]
}
```

---

## 23. Normalized timeline contract

Normalized timeline is render-preparation but not visual direction.

Example:

```json
{
  "schema_version": "0.1.0",
  "source": {
    "transcript": "output/transcript.json"
  },
  "scenes": [
    {
      "id": "scene_0001",
      "source_segment_ids": ["seg_0001"],
      "start": 0.25,
      "end": 2.16,
      "duration": 1.91,
      "speaker": {
        "id": "SPEAKER_00",
        "label": null,
        "source": "unknown"
      },
      "text": "Ê! Sao hôm nay đến trễ?"
    }
  ]
}
```

---

## 24. Visual timeline contract

Visual timeline is the renderer input.

Example:

```json
{
  "schema_version": "0.1.0",
  "template": "tiktok_dark_comic",
  "video": {
    "width": 1080,
    "height": 1920,
    "fps": 30
  },
  "scenes": [
    {
      "id": "scene_0001",
      "start": 0.25,
      "end": 2.16,
      "duration": 1.91,
      "speaker": {
        "id": "SPEAKER_00",
        "label": "Nam"
      },
      "text": "Ê! Sao hôm nay đến trễ?",
      "lines": ["Ê!", "SAO HÔM NAY", "ĐẾN TRỄ?"],
      "emotion": "surprised",
      "layout": {
        "name": "center_stack"
      },
      "keywords": [
        {
          "text": "ĐẾN TRỄ",
          "effect": "pop",
          "style": "primary"
        }
      ],
      "assets": {
        "icon_query": "báo thức",
        "icon_id": "icon_alarm_001"
      },
      "animations": [
        {
          "target": "ĐẾN TRỄ",
          "type": "pop",
          "start_offset": 1.1,
          "duration": 0.35
        }
      ]
    }
  ]
}
```

---

## 25. Render report contract

Render report documents the result.

Example:

```json
{
  "schema_version": "0.1.0",
  "input": "input/video.mp4",
  "output": "output/final.mp4",
  "duration": 28.4,
  "scene_count": 14,
  "template": "tiktok_dark_comic",
  "warnings": [],
  "errors": []
}
```

---

## 26. Validation architecture

Validation should happen at every stage boundary.

```text
transcript JSON
        ↓ validate
normalized timeline
        ↓ validate
visual timeline
        ↓ validate
render state
        ↓ validate
final report
```

Validation prevents bad data from reaching later modules.

---

## 27. Error architecture

The project should use explicit errors.

Suggested errors:

```python
class AIVideoEngineError(Exception): ...
class MissingFFmpegError(AIVideoEngineError): ...
class InvalidTranscriptError(AIVideoEngineError): ...
class InvalidTimelineError(AIVideoEngineError): ...
class InvalidDirectorOutputError(AIVideoEngineError): ...
class MissingAssetError(AIVideoEngineError): ...
class UnknownEffectError(AIVideoEngineError): ...
class RenderError(AIVideoEngineError): ...
class ExportError(AIVideoEngineError): ...
```

Error messages should be actionable.

---

## 28. Logging architecture

Logging should show pipeline progress.

Example:

```text
[audio] extracting audio from input/video.mp4
[speech] loading faster-whisper model medium
[speech] transcribed 18 segments
[timeline] normalized 18 segments into 14 scenes
[director] enriched 14 scenes
[embedding] matched 12 icons
[renderer] rendered 14 scenes
[exporter] wrote output/final.mp4
```

Use concise logs by default.

Verbose debug logs should be optional.

---

## 29. Cache architecture

Caching is important for AI and media tasks.

Potential cache targets:

```text
temp/audio.wav
output/transcript.json
output/timeline.normalized.json
output/timeline.visual.json
cache/icon_embeddings.json
cache/llm_responses/
```

Cache should be optional and clear.

Do not hide stale cache issues.

---

## 30. Prompt architecture

Prompts should be external files.

Example:

```text
prompts/visual_director.md
prompts/json_repair.md
prompts/icon_query.md
```

The code should load prompts from files.

Prompt variables should be injected safely.

Example variables:

```text
{{timeline_json}}
{{allowed_effects}}
{{allowed_layouts}}
{{language}}
{{template_name}}
```

---

## 31. LLM client architecture

The first LLM client is Ollama.

Suggested abstraction:

```python
class LLMClient:
    def generate(self, prompt: str) -> str:
        ...
```

```python
class OllamaClient(LLMClient):
    def generate(self, prompt: str) -> str:
        ...
```

This allows replacing Ollama later.

---

## 32. Director output parser

LLM output may be invalid.

The parser should:

1. receive raw LLM text
2. strip wrappers if needed
3. parse JSON
4. optionally repair JSON
5. validate against schema
6. return typed object

Do not pass raw LLM output to renderer.

---

## 33. Speaker architecture

Speaker data evolves through stages.

### Stage 1

Unknown or inferred speakers:

```json
{
  "id": "SPEAKER_00",
  "label": null,
  "source": "unknown"
}
```

### Stage 2

User-mapped speakers:

```json
{
  "id": "SPEAKER_00",
  "label": "Nam",
  "source": "manual"
}
```

### Stage 3

Diarized speakers:

```json
{
  "id": "SPEAKER_00",
  "label": "Nam",
  "source": "diarization",
  "confidence": 0.91
}
```

---

## 34. Diarization architecture

Diarization is optional in early versions.

Possible future tools:

```text
WhisperX
pyannote.audio
```

Diarization should not block Sprint 1.

The architecture should allow speaker labels to be added later.

---

## 35. Template architecture

Templates define style.

Template example:

```yaml
name: tiktok_dark_comic
version: 0.1.0

video:
  width: 1080
  height: 1920
  fps: 30

colors:
  background: "#080A12"
  text_primary: "#FFFFFF"
  keyword_primary: "#FFD400"
  speaker_a: "#3291FF"
  speaker_b: "#FF5A8C"

font:
  family: "Inter"
  weight: "bold"

safe_zone:
  top: 120
  bottom: 220
  left: 80
  right: 140

defaults:
  layout: center_stack
  keyword_effect: pop
```

The renderer should use templates instead of hardcoded style.

---

## 36. Effect plugin architecture

Effects should be isolated.

Example:

```python
class Effect:
    name: str

    def apply(self, element, time: float, params: dict):
        ...
```

Example effects:

```text
pop
bounce
shake
glow
slide
fade
pulse
typewriter
```

The renderer should use an effect registry.

---

## 37. Layout plugin architecture

Layouts should be isolated.

Example:

```python
class Layout:
    name: str

    def compute(self, scene, canvas, template) -> LayoutResult:
        ...
```

Example layouts:

```text
center_stack
comic_panel
split_speaker
punchline_center
avatar_left_text_right
question_answer
```

---

## 38. Asset registry architecture

Assets should be registered.

Possible structure:

```text
assets/manifest.json
assets/icons/icon_db.json
assets/avatars/avatar_db.json
```

Icon registry example:

```json
[
  {
    "id": "icon_alarm_001",
    "file": "icons/alarm.png",
    "tags": ["báo thức", "đồng hồ", "trễ giờ"]
  }
]
```

---

## 39. Export architecture

The exporter should be separate from renderer.

This allows:

- preview renders
- silent renders
- re-export with different audio
- different codecs
- future upload pipelines

Exporter can use FFmpeg.

---

## 40. CLI architecture

Future CLI structure:

```text
ai-video extract-audio input/video.mp4
ai-video transcribe input/video.mp4
ai-video normalize output/transcript.json
ai-video direct output/timeline.normalized.json
ai-video render output/timeline.visual.json
ai-video export output/silent_video.mp4 temp/audio.wav
ai-video build input/video.mp4
```

CLI should be thin.

Core logic should remain importable.

---

## 41. Configuration architecture

Configuration should support:

- defaults
- user overrides
- template-specific settings
- model settings
- path settings

Possible loading order:

```text
built-in defaults
→ config/default.yaml
→ template config
→ user config
→ CLI flags
```

Later values override earlier values.

---

## 42. Development architecture

Early development can proceed as vertical slices.

Each sprint should deliver one working stage.

Recommended order:

```text
Speech To Text
Timeline Analyzer
Visual Director
Icon Selector
Renderer
Exporter
Template System
```

Avoid implementing everything at once.

---

## 43. Testing architecture

Testing layers:

```text
unit tests
integration tests
smoke tests
golden file tests
manual review outputs
```

### Unit tests

Fast and local.

### Integration tests

May use small media files.

### Smoke tests

Ensure end-to-end path runs.

### Golden file tests

Compare expected JSON output.

### Manual review

Important for visual quality.

---

## 44. Schema validation architecture

Schema validation can use Pydantic.

Example models:

```python
class TranscriptSegment(BaseModel):
    id: str
    start: float
    end: float
    text: str
```

```python
class Scene(BaseModel):
    id: str
    start: float
    end: float
    duration: float
    text: str
```

Validation rules should check:

- positive duration
- sorted scenes
- required fields
- known effects
- known layouts
- valid asset references

---

## 45. Future API architecture

The engine may expose an API later.

Possible architecture:

```text
FastAPI app
        ↓
Application service
        ↓
Core modules
        ↓
Output files
```

Do not tie core engine to API framework.

---

## 46. Future UI architecture

Possible UI options:

- Streamlit prototype
- Electron desktop app
- Web app
- VS Code extension

UI should call core engine.

Core engine should not depend on UI.

---

## 47. Batch architecture

Batch rendering should reuse loaded models.

Example:

```text
load whisper once
load embedding model once
process many videos
write outputs per video
```

Batch mode should avoid repeated model loading.

---

## 48. Performance architecture

Performance priorities:

1. Avoid unnecessary model reloads.
2. Cache expensive outputs.
3. Keep renderer simple first.
4. Optimize rendering after correctness.
5. Add GPU acceleration only if useful.

Initial target:

- run on Windows CPU
- run on Mac M1 CPU
- no mandatory GPU

---

## 49. Security architecture

Security principles:

- no secrets in repo
- no untrusted code execution
- no shell string subprocess calls when avoidable
- no silent external uploads
- no committed private media

Subprocess calls should use argument lists.

---

## 50. Privacy architecture

Default media processing is local.

Voice and video should not leave the machine by default.

Cloud integrations must be explicit.

---

## 51. Failure modes

Known possible failures:

- FFmpeg not installed
- unsupported video format
- Whisper model download fails
- STT output has poor punctuation
- LLM returns invalid JSON
- icon query has no good match
- font missing Vietnamese glyphs
- renderer output duration mismatch
- audio/video sync issue

Each should have a clear error or warning path.

---

## 52. Minimal viable architecture

The simplest useful version is:

```text
input video
→ extract audio
→ transcribe
→ make simple timeline
→ render black background + big text
→ merge original audio
→ final mp4
```

This is enough for an early demo.

Do not block early progress with advanced features.

---

## 53. Production architecture direction

A more complete version adds:

- schema validation
- template system
- effect registry
- layout registry
- icon embedding
- speaker mapping
- cache
- CLI
- reports
- tests
- docs
- CI

---

## 54. Architectural decisions already made

### Decision 1

AI will not render video.

### Decision 2

Renderer will be deterministic.

### Decision 3

Timeline JSON is the central contract.

### Decision 4

First STT implementation will use Faster Whisper.

### Decision 5

First local LLM runtime will use Ollama.

### Decision 6

First director model will be Qwen 2.5 3B.

### Decision 7

First icon selection approach will use embeddings.

### Decision 8

Original voice is preserved for existing-video workflows.

### Decision 9

Default output is 1080x1920 vertical MP4.

### Decision 10

Repository documentation is the source of truth.

---

## 55. Architectural anti-patterns

Avoid these:

### Anti-pattern 1

One giant `main.py`.

### Anti-pattern 2

Renderer calling the LLM.

### Anti-pattern 3

Prompts embedded inside Python business logic.

### Anti-pattern 4

Hardcoded absolute asset paths.

### Anti-pattern 5

Timeline stored only in memory.

### Anti-pattern 6

Skipping schema validation.

### Anti-pattern 7

Using AI output directly without parsing.

### Anti-pattern 8

Changing architecture without updating docs.

### Anti-pattern 9

Committing generated MP4 files.

### Anti-pattern 10

Building a complex renderer before basic pipeline works.

---

## 56. Recommended first implementation path

### Step 1

Build audio extraction.

### Step 2

Build Faster Whisper transcription.

### Step 3

Export transcript JSON.

### Step 4

Build timeline analyzer.

### Step 5

Build basic visual director.

### Step 6

Build basic renderer.

### Step 7

Merge original audio.

### Step 8

Polish template and animation.

---

## 57. Architecture review checklist

Before merging a major change, verify:

- Does AI still only produce JSON?
- Does renderer remain deterministic?
- Does the change preserve module boundaries?
- Is the data contract documented?
- Are intermediate outputs inspectable?
- Does it run on Windows?
- Does it avoid mandatory GPU?
- Are prompts externalized?
- Are schema changes documented?
- Is the change testable?

---

## 58. How to continue architecture in future chats

Use this instruction:

```text
Continue AI Video Engine.
Read AGENTS.md, PROJECT_RULES.md, and docs/Architecture.md first.
Do not code until you understand the current sprint.
```

---

## 59. Final architecture principle

The engine should be boring, predictable, inspectable, and extensible.

The videos can be flashy.

The architecture should not be.
