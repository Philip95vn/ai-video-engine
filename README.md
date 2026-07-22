# AI Video Engine

> Local-first AI video automation engine for generating short-form videos from voice, dialogue, transcript, and structured timeline JSON.

---

## Table of Contents

1. Project Status
2. What This Project Does
3. What This Project Does Not Do
4. Core Philosophy
5. High-Level Pipeline
6. First Target Use Case
7. Main Features
8. Current Roadmap
9. Repository Structure
10. Architecture Overview
11. AI Responsibilities
12. Renderer Responsibilities
13. Timeline JSON Contract
14. Default Output Format
15. Local Development Setup
16. Windows Setup
17. Mac Setup
18. Required External Tools
19. Python Environment
20. Installing Dependencies
21. Ollama Setup
22. Faster Whisper Setup
23. FFmpeg Setup
24. Basic Usage Goal
25. Development Workflow
26. Git Workflow
27. Sprint Workflow
28. Documentation Workflow
29. Coding Standards
30. Testing Strategy
31. Asset System
32. Prompt System
33. Template System
34. Security and Privacy
35. Contribution Rules
36. Future Vision
37. Glossary

---

## 1. Project Status

AI Video Engine is currently in early development.

Current stage:

```text
Sprint 0B - Documentation and Knowledge Base
```

The project skeleton exists.

The next engineering sprint is:

```text
Sprint 1 - Speech To Text
```

Sprint 1 goal:

```text
input video/audio → transcript.json with timestamps
```

---

## 2. What This Project Does

AI Video Engine turns existing video/audio/dialogue into structured short-form video.

The core workflow starts with a video that already has voice.

The engine extracts audio, transcribes the voice, creates a timeline, asks AI to enrich the timeline, then renders a new video style using the original voice.

Example:

```text
input/video.mp4
        ↓
temp/audio.wav
        ↓
output/transcript.json
        ↓
output/timeline.normalized.json
        ↓
output/timeline.visual.json
        ↓
output/silent_video.mp4
        ↓
output/final.mp4
```

The output should look like modern short-form videos:

- Large full-screen text
- Highlighted keywords
- Speaker-aware dialogue
- Icons
- Animated text
- Bold layouts
- Original voice preserved

---

## 3. What This Project Does Not Do

AI Video Engine is not a video diffusion model.

It does not try to replace:

- Sora
- Veo
- Runway
- Pika
- Premiere Pro
- CapCut editor
- Final Cut Pro

It does not generate realistic video from text.

It does not use AI to render final pixels.

It does not require a GPU by default.

It is a deterministic rendering engine controlled by structured JSON.

---

## 4. Core Philosophy

The project separates intelligence from rendering.

AI is the director.

Python renderer is the editor.

JSON is the contract.

```text
AI decides what should happen.
Renderer decides how to draw it.
```

AI responsibilities:

- Analyze dialogue
- Detect keywords
- Detect emotion
- Suggest layout
- Suggest icon query
- Suggest animation
- Produce structured JSON

Renderer responsibilities:

- Load timeline JSON
- Draw text
- Draw icons
- Draw backgrounds
- Animate elements
- Export silent video
- Merge original audio
- Export final MP4

The renderer must be deterministic.

---

## 5. High-Level Pipeline

```text
Input Video / Audio
        │
        ▼
Audio Extractor
        │
        ▼
Speech To Text
        │
        ▼
Transcript JSON
        │
        ▼
Speaker Mapping / Diarization
        │
        ▼
Timeline Analyzer
        │
        ▼
Visual Director AI
        │
        ▼
Icon Selector
        │
        ▼
Visual Timeline JSON
        │
        ▼
Renderer
        │
        ▼
Silent Video
        │
        ▼
Exporter
        │
        ▼
Final MP4
```

---

## 6. First Target Use Case

The first use case is:

```text
Existing video with voice
→ Speech-to-text
→ Speaker-aware transcript
→ AI-enriched visual timeline
→ Full-screen animated text video
→ Original audio preserved
```

Example input:

```text
Nam: Ê! Sao hôm nay đến trễ?
Nữ: Tại báo thức!
Nam: Rồi nó ngủ tiếp?
Nữ: Ừ. Nó là máy chứ ai!
```

Expected visual style:

- Each frame has one or two sentences.
- Text is large.
- Keywords are highlighted.
- Effects emphasize punchlines.
- Icons appear when useful.
- Speaker identity is visually clear.

---

## 7. Main Features

### Planned V1 features

- Extract audio from video
- Speech-to-text with timestamps
- Vietnamese transcription
- Transcript JSON export
- Timeline normalization
- Basic speaker labels
- Visual Director LLM integration
- Keyword selection
- Emotion labels
- Icon query generation
- Embedding-based icon search
- Timeline JSON schema validation
- Basic 9:16 renderer
- Large text rendering
- Keyword highlight rendering
- Basic animation effects
- Original audio merge
- Final MP4 export

### Later features

- Speaker diarization
- Word-level timing
- Template system
- Avatar system
- Sound effects
- Background music
- Batch rendering
- GUI
- API server
- Web editor
- More output formats

---

## 8. Current Roadmap

```text
Sprint 0  - Bootstrap
Sprint 0B - Documentation and knowledge base
Sprint 1  - Speech To Text
Sprint 2  - Timeline Analyzer
Sprint 3  - Visual Director
Sprint 4  - Icon Selector
Sprint 5  - Basic Renderer
Sprint 6  - Exporter
Sprint 7  - Speaker Support
Sprint 8  - Template System
Sprint 9  - Animation Engine
Sprint 10 - AI Video Engine v1
```

---

## 9. Repository Structure

Recommended structure:

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
│   ├── ProjectVision.md
│   ├── Architecture.md
│   ├── Pipeline.md
│   ├── JSONSchema.md
│   ├── RendererDesign.md
│   ├── AIDesign.md
│   ├── PromptGuide.md
│   ├── AssetGuide.md
│   ├── CodingStandard.md
│   ├── DecisionLog.md
│   ├── Sprint0.md
│   ├── Sprint1.md
│   └── Glossary.md
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
│   ├── visual_director.md
│   ├── timeline_analyzer.md
│   ├── keyword_extractor.md
│   ├── emotion_classifier.md
│   └── json_repair.md
│
├── assets/
│   ├── icons/
│   ├── avatars/
│   ├── backgrounds/
│   ├── fonts/
│   ├── sfx/
│   └── templates/
│
├── examples/
├── tests/
├── scripts/
├── output/
└── temp/
```

---

## 10. Architecture Overview

The project is designed as a modular engine.

Each module has one responsibility.

### Audio module

Location:

```text
src/audio/
```

Responsibilities:

- Extract audio from video
- Convert audio format
- Prepare audio for STT
- Preserve original audio

### Speech module

Location:

```text
src/speech/
```

Responsibilities:

- Load STT model
- Transcribe audio
- Export transcript JSON

### Timeline module

Location:

```text
src/timeline/
```

Responsibilities:

- Clean transcript
- Merge short segments
- Split long segments
- Normalize timing
- Validate scene structure

### Director module

Location:

```text
src/director/
```

Responsibilities:

- Call local LLM
- Generate visual direction
- Select keywords
- Select emotions
- Suggest animations
- Suggest icon queries

### Embedding module

Location:

```text
src/embedding/
```

Responsibilities:

- Build icon database
- Embed asset metadata
- Match icon query to available icons

### Renderer module

Location:

```text
src/renderer/
```

Responsibilities:

- Render text
- Render keywords
- Render icons
- Render avatars
- Render backgrounds
- Apply animations
- Export silent video

### Exporter module

Location:

```text
src/exporter/
```

Responsibilities:

- Merge silent video with original audio
- Export final MP4
- Write render report

---

## 11. AI Responsibilities

AI is allowed to do:

- Transcript interpretation
- Keyword detection
- Punchline detection
- Emotion labeling
- Layout suggestion
- Animation suggestion
- Icon query generation
- Speaker mood suggestion
- JSON enrichment

AI is not allowed to do:

- Render video
- Generate final frames
- Modify original media directly
- Execute code
- Bypass renderer
- Invent unavailable assets as final references

AI output must be validated before use.

---

## 12. Renderer Responsibilities

Renderer is responsible for turning validated timeline JSON into video.

Renderer can:

- Load assets
- Draw text
- Draw keyword highlights
- Draw icons
- Draw avatars
- Apply effects
- Create video clips
- Export silent video

Renderer cannot:

- Call LLM
- Parse natural language intent
- Guess missing timeline semantics
- Download assets silently
- Change scene timing without explicit instruction

---

## 13. Timeline JSON Contract

The Timeline JSON is the central contract.

Everything important must be represented in JSON.

Example simplified scene:

```json
{
  "id": "scene_0001",
  "start": 0.25,
  "end": 2.16,
  "duration": 1.91,
  "speaker": {
    "id": "SPEAKER_00",
    "label": "Nam",
    "confidence": 0.72
  },
  "text": "Ê! Sao hôm nay đến trễ?",
  "lines": ["Ê!", "SAO HÔM NAY", "ĐẾN TRỄ?"],
  "keywords": [
    {
      "text": "ĐẾN TRỄ",
      "importance": 0.95,
      "effect": "pop",
      "style": "highlight_yellow"
    }
  ],
  "layout": {
    "name": "center_stack"
  },
  "assets": {
    "icon_query": "đồng hồ báo thức",
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
```

---

## 14. Default Output Format

Default render settings:

```yaml
video:
  width: 1080
  height: 1920
  fps: 30
  codec: h264
  audio_codec: aac
  format: mp4
```

Default paths:

```text
input/
temp/
output/
```

Default output files:

```text
output/transcript.json
output/timeline.normalized.json
output/timeline.visual.json
output/silent_video.mp4
output/final.mp4
output/render_report.json
```

---

## 15. Local Development Setup

General steps:

```bash
git clone <repository-url>
cd ai-video-engine
python -m venv .venv
```

Activate environment.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
.venv\Scripts\activate.bat
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 16. Windows Setup

### Check Python

```powershell
python --version
```

Recommended:

```text
Python 3.11+
```

### Check Git

```powershell
git --version
```

### Check FFmpeg

```powershell
ffmpeg -version
```

If FFmpeg is missing, install via winget:

```powershell
winget install Gyan.FFmpeg
```

After installation, close and reopen VS Code or terminal.

### Check Ollama

```powershell
ollama --version
```

Pull model:

```powershell
ollama pull qwen2.5:3b
```

---

## 17. Mac Setup

Install Homebrew if needed.

Install FFmpeg:

```bash
brew install ffmpeg
```

Install Ollama:

```bash
brew install ollama
```

Pull model:

```bash
ollama pull qwen2.5:3b
```

Create venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 18. Required External Tools

### Required

- Python 3.11+
- Git
- FFmpeg

### Required for AI Director

- Ollama
- Qwen 2.5 3B or compatible local model

### Required for Speech-To-Text

- Faster Whisper

### Optional later

- WhisperX
- pyannote.audio
- OpenCV
- FAISS
- Edge TTS
- Streamlit
- FastAPI

---

## 19. Python Environment

Recommended:

```text
Python 3.11
```

Avoid using very new Python versions for AI packages until compatibility is stable.

Use virtual environment:

```bash
python -m venv .venv
```

Do not install project packages globally.

---

## 20. Installing Dependencies

Initial requirements:

```text
faster-whisper
requests
sentence-transformers
scikit-learn
numpy
Pillow
moviepy
pydub
rich
orjson
pydantic
edge-tts
```

Install:

```bash
pip install -r requirements.txt
```

---

## 21. Ollama Setup

Ollama is used to run local LLMs.

Initial recommended model:

```text
qwen2.5:3b
```

Pull model:

```bash
ollama pull qwen2.5:3b
```

Test:

```bash
ollama run qwen2.5:3b
```

Example prompt:

```text
Return valid JSON only.
Analyze this dialogue and select keywords.
```

---

## 22. Faster Whisper Setup

Faster Whisper is used for speech-to-text.

Initial model recommendation:

```text
medium
```

For weaker machines:

```text
small
```

For higher accuracy:

```text
large-v3
```

The STT module should allow configuration.

Example future config:

```yaml
speech:
  provider: faster_whisper
  model: medium
  device: cpu
  compute_type: int8
  language: vi
```

---

## 23. FFmpeg Setup

FFmpeg is used for:

- Extracting audio
- Converting audio
- Merging audio and video
- Exporting final MP4

Example audio extraction command:

```bash
ffmpeg -y -i input/video.mp4 -vn -ac 1 -ar 16000 temp/audio.wav
```

Example merge command:

```bash
ffmpeg -y -i output/silent_video.mp4 -i temp/audio.wav -c:v copy -c:a aac -shortest output/final.mp4
```

---

## 24. Basic Usage Goal

Final target usage:

```bash
ai-video build input/video.mp4
```

Expected output:

```text
output/final.mp4
```

Intermediate output:

```text
output/transcript.json
output/timeline.normalized.json
output/timeline.visual.json
output/render_report.json
```

Before CLI exists, development may use Python module commands or scripts.

---

## 25. Development Workflow

Use this flow:

```text
Issue
→ Design
→ Code
→ Test
→ Docs
→ Commit
→ Push
```

Do not jump directly into coding large features.

Each sprint should produce a working vertical slice.

---

## 26. Git Workflow

Daily workflow:

```bash
git pull
git status
git add .
git commit -m "type: message"
git push
```

Commit message examples:

```text
docs: expand architecture documentation
feat: add audio extraction module
test: add timeline validation tests
fix: handle missing ffmpeg path
```

Use conventional commits:

- `feat:`
- `fix:`
- `docs:`
- `refactor:`
- `test:`
- `chore:`
- `ci:`
- `perf:`

---

## 27. Sprint Workflow

### Sprint 0

Bootstrap repository.

### Sprint 0B

Complete project documentation.

### Sprint 1

Speech-to-text.

Goal:

```text
video.mp4 → transcript.json
```

### Sprint 2

Timeline analyzer.

Goal:

```text
transcript.json → timeline.normalized.json
```

### Sprint 3

Visual Director.

Goal:

```text
timeline.normalized.json → timeline.visual.json
```

### Sprint 4

Icon Selector.

Goal:

```text
icon_query → icon asset
```

### Sprint 5

Renderer.

Goal:

```text
timeline.visual.json → silent_video.mp4
```

### Sprint 6

Exporter.

Goal:

```text
silent_video.mp4 + original audio → final.mp4
```

---

## 28. Documentation Workflow

Important files:

```text
AGENTS.md
PROJECT_RULES.md
docs/Architecture.md
docs/Pipeline.md
docs/JSONSchema.md
docs/DecisionLog.md
```

Every architecture change should update docs.

Every major decision should update DecisionLog.

Every schema change should update JSONSchema.

Every prompt change should update PromptGuide.

---

## 29. Coding Standards

Use:

- Python 3.11+
- Type hints
- `pathlib.Path`
- Clear module boundaries
- Small functions
- Explicit errors
- JSON validation

Avoid:

- hardcoded machine paths
- hidden global state
- renderer calling LLM
- giant scripts
- unvalidated LLM output
- committing generated media

---

## 30. Testing Strategy

Unit tests should be:

- small
- fast
- local
- deterministic

Unit tests should not require:

- internet
- GPU
- large media files
- large AI models

Integration tests may be slower and model-dependent.

Test targets:

- audio extraction command generation
- transcript parsing
- timeline validation
- LLM JSON parsing
- icon selection
- renderer smoke test
- exporter command generation

---

## 31. Asset System

Assets live under:

```text
assets/
├── icons/
├── avatars/
├── backgrounds/
├── fonts/
├── sfx/
└── templates/
```

Assets should be referenced by ID or relative path.

Icon metadata should include tags.

Example:

```json
{
  "id": "icon_alarm_001",
  "file": "assets/icons/alarm.png",
  "tags": ["báo thức", "đồng hồ", "trễ giờ"],
  "style": "flat",
  "mood": ["funny", "urgent"]
}
```

---

## 32. Prompt System

Prompts live under:

```text
prompts/
```

Example prompt files:

```text
prompts/visual_director.md
prompts/keyword_extractor.md
prompts/emotion_classifier.md
prompts/icon_query.md
prompts/json_repair.md
```

Prompts must request valid JSON only.

Prompts should include:

- role
- task
- input
- output schema
- constraints
- examples
- allowed enum values

---

## 33. Template System

Templates define visual style.

A template may define:

- resolution
- FPS
- background
- fonts
- colors
- safe zones
- default layouts
- default animations
- keyword style
- speaker style
- icon style
- avatar style

Example template names:

```text
tiktok_dark_comic
neon_dialogue
minimal_black
recruitment_clean
education_bold
```

---

## 34. Security and Privacy

Input media may contain private voice or personal content.

Default behavior should be local.

Do not upload media to cloud services unless explicitly configured.

Never commit:

- API keys
- private video
- private audio
- `.env`
- large model files
- credentials

---

## 35. Contribution Rules

Before contributing:

1. Read `AGENTS.md`.
2. Read `PROJECT_RULES.md`.
3. Check current sprint.
4. Keep changes focused.
5. Update docs when needed.
6. Add tests when practical.
7. Use meaningful commit messages.

---

## 36. Future Vision

Long-term, AI Video Engine should become a reusable automation system.

Possible future workflows:

### Dialogue to video

```text
dialogue.txt
→ visual timeline
→ voice
→ video
```

### Existing video to redesigned video

```text
video.mp4
→ transcript
→ visual timeline
→ new stylized video
```

### Recruitment video

```text
job description
→ script
→ video
```

### Candidate intro video

```text
CV
→ script
→ voice
→ video
```

### News recap video

```text
article
→ summary
→ script
→ video
```

### Batch content factory

```text
folder of scripts/videos
→ batch render
→ final videos
```

---

## 37. Glossary

### AI Director

The LLM-powered module that enriches timeline JSON.

### Timeline JSON

The structured file that describes scenes, timing, text, animations, and assets.

### Scene

A timed unit of video content.

### Keyword

Text that should be emphasized visually.

### Renderer

The deterministic module that turns timeline JSON into video.

### Exporter

The module that merges video and audio and writes final output.

### Template

A reusable visual style definition.

### Asset

Any external visual/audio resource used by renderer.

### STT

Speech-to-text.

### Diarization

Speaker separation and speaker labeling.

---

## 38. Quick Start After Sprint 1

Expected future command:

```bash
python -m ai_video_engine transcribe input/video.mp4
```

Expected output:

```text
output/transcript.json
```

Expected transcript item:

```json
{
  "id": "seg_0001",
  "start": 0.25,
  "end": 2.16,
  "text": "Ê! Sao hôm nay đến trễ?"
}
```

---

## 39. Quick Start After Sprint 6

Expected future command:

```bash
python -m ai_video_engine build input/video.mp4
```

Expected output:

```text
output/final.mp4
```

---

## 40. How To Continue In A New Chat

Use this message:

```text
Continue AI Video Engine.
Read AGENTS.md and PROJECT_RULES.md before coding.
Current sprint: Sprint 1 - Speech To Text.
Repository: <GitHub URL>
```

The repository should contain enough context for any AI coding agent to continue.

---

## 41. Current Recommended Next Step

Complete Sprint 0B documentation.

Then begin Sprint 1:

```text
Speech To Text
```

Sprint 1 deliverable:

```text
input video/audio → output/transcript.json
```

---

## 42. Maintainer Notes

This project should be developed carefully.

Avoid short-term hacks that damage long-term architecture.

The most important invariant:

```text
AI produces JSON.
Renderer consumes JSON.
```

Everything else can evolve.
