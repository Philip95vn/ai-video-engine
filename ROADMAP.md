# ROADMAP.md

# AI Video Engine - Roadmap

## 0. Purpose

This roadmap defines the development plan for **AI Video Engine**.

It explains:

- what will be built
- in what order
- why that order matters
- what each sprint delivers
- what is out of scope
- how progress is measured
- how the project evolves from prototype to V1

This roadmap should be read together with:

```text
AGENTS.md
PROJECT_RULES.md
docs/Architecture.md
docs/Pipeline.md
docs/JSONSchema.md
docs/AIDesign.md
docs/RendererDesign.md
docs/DecisionLog.md
```

---

## 1. Product direction

AI Video Engine is a local-first video automation engine.

The first product target:

```text
Existing video with original voice
        ↓
Speech-to-text
        ↓
Timeline JSON
        ↓
AI visual direction
        ↓
Icon selection
        ↓
Deterministic rendering
        ↓
Final vertical short-form video
```

The first visual style:

- vertical 9:16
- large full-screen text
- dark background
- highlighted keywords
- simple icons
- dialogue-aware scenes
- original voice preserved

---

## 2. Roadmap philosophy

The project will be built through vertical slices.

Each sprint should create one working layer of the pipeline.

Do not build everything at once.

Do not build advanced visuals before the data pipeline works.

Do not add complex AI before simple deterministic stages are stable.

The roadmap prioritizes:

1. working pipeline
2. inspectable JSON
3. deterministic renderer
4. local-first workflow
5. repeatable output
6. then visual polish
7. then scale and automation

---


## 3. Current status

Current stage:

```text
Sprint 1 - Speech To Text
```

Sprint 1 status:

```text
completed
```

Completed output:

```text
temp/audio.wav
output/transcript.json
```

Validated:

- FFmpeg audio extraction works on Windows.
- Faster Whisper works on CPU with `int8`.
- Vietnamese UTF-8 text is preserved.
- Segment timestamps and IDs are generated.
- All 32 automated tests pass.
- Manual test with a real video passed.

Next engineering sprint:

```text
Sprint 2 - Timeline Analyzer
```

---


## 4. High-level roadmap

```text
Sprint 0A  - Bootstrap
Sprint 0B  - Knowledge Base
Sprint 1   - Speech To Text
Sprint 2   - Timeline Analyzer
Sprint 3   - Visual Director
Sprint 4   - Icon Selector
Sprint 5   - Basic Renderer
Sprint 6   - Exporter
Sprint 7   - Speaker Support
Sprint 8   - Template System
Sprint 9   - Animation Engine
Sprint 10  - Video Engine V1
Sprint 11  - Batch Processing
Sprint 12  - Quality Review Tools
Sprint 13  - Optional Diarization
Sprint 14  - Word-Level Timing
Sprint 15  - UI Prototype
Sprint 16  - Recruitment Video Workflow
Sprint 17  - Text-to-Video/TTS Workflow
Sprint 18  - Asset Pack System
Sprint 19  - Performance Optimization
Sprint 20  - V1 Release Hardening
```

---

## 5. Milestone overview

| Milestone | Goal | Main output |
|---|---|---|
| M0 | Project foundation | repository, docs, rules |
| M1 | Transcription pipeline | `transcript.json` |
| M2 | Timeline pipeline | `timeline.normalized.json` |
| M3 | AI visual direction | `timeline.director.json` |
| M4 | Asset selection | `timeline.visual.json` |
| M5 | Rendering | `silent_video.mp4` |
| M6 | Final export | `final.mp4` |
| M7 | V1 engine | end-to-end local pipeline |
| M8 | Scale | batch processing |
| M9 | Productization | UI/API/templates |

---

## 6. Version roadmap

### v0.1.0 - Project foundation

Includes:

- repository
- project structure
- docs
- rules
- roadmap
- initial CI

### v0.2.0 - Speech-to-text

Includes:

- FFmpeg audio extraction
- Faster Whisper transcription
- transcript JSON output

### v0.3.0 - Timeline analyzer

Includes:

- transcript validation
- scene normalization
- scene IDs
- timing validation

### v0.4.0 - Visual Director

Includes:

- prompt loader
- Ollama client
- Qwen 2.5 3B integration
- JSON output validation

### v0.5.0 - Icon selector

Includes:

- icon DB
- embedding search
- icon assignment

### v0.6.0 - Basic renderer

Includes:

- 9:16 canvas
- large text
- keyword highlight
- simple animation
- silent video

### v0.7.0 - Exporter

Includes:

- audio/video merge
- final MP4
- render report

### v0.8.0 - Template system

Includes:

- template config
- style tokens
- safe zones

### v0.9.0 - Beta engine

Includes:

- full end-to-end build
- basic docs
- tests
- sample project

### v1.0.0 - First stable release

Includes:

- reliable local pipeline
- stable JSON schema
- working CLI
- basic templates
- docs
- tests
- release notes

---

## 7. Sprint 0A - Bootstrap

### Status

```text
Completed
```

### Goal

Create project repository and initial skeleton.

### Scope

- Create GitHub repository.
- Connect local project to GitHub.
- Create initial folder structure.
- Add initial bootstrap files.
- Make first commit.
- Push to GitHub.

### Deliverables

```text
README.md
PROJECT_RULES.md
ROADMAP.md
CHANGELOG.md
pyproject.toml
requirements.txt
src/
docs/
assets/
prompts/
tests/
```

### Done criteria

- Git initialized.
- Remote origin configured.
- Initial commit pushed.
- Project opens in VS Code.
- Repository exists on GitHub.

### Commit

Suggested commit:

```text
chore: bootstrap AI Video Engine project
```

---

## 8. Sprint 0B - Knowledge Base

### Status

```text
Completed
```

### Goal

Convert project decisions and architecture into repository documentation.

This sprint makes the repository self-explanatory.

### Why this sprint exists

The conversation became long.

Future work may happen in:

- new ChatGPT conversation
- Codex in VS Code
- GitHub
- other AI coding tools

The repository must contain enough context to continue without chat history.

### Scope

Create substantial documentation:

```text
AGENTS.md
PROJECT_RULES.md
README.md
docs/Architecture.md
docs/Pipeline.md
docs/JSONSchema.md
docs/RendererDesign.md
docs/AIDesign.md
docs/PromptGuide.md
docs/AssetGuide.md
docs/CodingStandard.md
docs/DecisionLog.md
ROADMAP.md
docs/ProjectVision.md
docs/Sprint0.md
docs/Sprint1.md
docs/Glossary.md
```

### Non-scope

Do not implement major code in this sprint.

Do not start full STT module yet.

Do not add renderer.

Do not add complex dependencies.

### Deliverables

- Full project knowledge base.
- Clear rules for AI agents.
- Clear roadmap.
- Clear architecture.
- Clear JSON contracts.
- Clear coding standard.

### Done criteria

- Docs are not empty placeholders.
- AGENTS.md explains project to AI agents.
- PROJECT_RULES.md defines mandatory rules.
- DecisionLog records accepted decisions.
- Roadmap defines sprint order.
- User can start new chat with repository link.
- Codex can read docs and continue.

### Suggested commit

```text
docs: complete Sprint 0B project knowledge base
```

---

## 9. Sprint 1 - Speech To Text

### Status

```text
completed
```

### Goal

Convert an input video/audio file into timestamped transcript JSON.

### One-line goal

```text
input/video.mp4 → output/transcript.json
```

### Pipeline stages

```text
Validate Input
        ↓
Extract Audio
        ↓
Speech To Text
        ↓
Transcript JSON
```

### Scope

Build:

- FFmpeg availability check
- audio extraction command builder
- audio extraction function
- Faster Whisper transcription
- transcript schema
- transcript JSON writer
- transcript validator
- minimal script or CLI command
- clear Windows-friendly errors

### Non-scope

Do not build:

- Visual Director
- renderer
- icon selector
- diarization
- word-level timing
- UI
- final export

### Input

```text
input/video.mp4
```

or:

```text
input/audio.wav
```

### Output

```text
temp/audio.wav
output/transcript.json
```

### Transcript JSON example

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
      "start": 0.25,
      "end": 2.16,
      "duration": 1.91,
      "text": "Ê! Sao hôm nay đến trễ?"
    }
  ]
}
```

### Modules

```text
src/audio/
src/speech/
src/common/
src/config/
```

### Suggested files

```text
src/common/errors.py
src/common/json_io.py
src/audio/commands.py
src/audio/extractor.py
src/speech/schema.py
src/speech/faster_whisper_engine.py
scripts/transcribe.py
tests/test_audio_commands.py
tests/test_transcript_schema.py
```

### Dependencies

Required:

```text
ffmpeg
faster-whisper
pydantic
```

### Acceptance criteria

- Works on Windows.
- Works on CPU.
- Extracts audio with FFmpeg.
- Runs Faster Whisper.
- Produces valid UTF-8 JSON.
- Preserves Vietnamese text.
- Every segment has `id`, `start`, `end`, `duration`, `text`.
- Missing FFmpeg error is clear.
- Missing input file error is clear.
- Output folder is created automatically.

### Suggested commit sequence

```text
feat: add audio extraction command builder
feat: add faster whisper transcription module
test: add transcript schema validation tests
docs: document Sprint 1 speech-to-text workflow
```

---

## 10. Sprint 2 - Timeline Analyzer

### Goal

Convert raw transcript into normalized renderable scenes.

### One-line goal

```text
output/transcript.json → output/timeline.normalized.json
```

### Why this sprint matters

STT output is not ready for rendering.

Segments may be:

- too long
- too short
- poorly punctuated
- not scene-friendly
- missing speaker information

Timeline Analyzer prepares transcript for Visual Director.

### Scope

Build:

- transcript loader
- transcript validator
- scene ID generator
- text cleanup
- segment merge logic
- long segment split logic
- normalized timeline schema
- timing validation
- speaker placeholder structure
- normalized timeline writer

### Non-scope

Do not use LLM.

Do not select keywords.

Do not render.

Do not select icons.

### Input

```text
output/transcript.json
```

### Output

```text
output/timeline.normalized.json
```

### Example

```json
{
  "schema_version": "0.1.0",
  "scenes": [
    {
      "id": "scene_0001",
      "source_segment_ids": ["seg_0001"],
      "start": 0.25,
      "end": 2.16,
      "duration": 1.91,
      "speaker": {
        "id": "SPEAKER_00",
        "source": "unknown"
      },
      "text": "Ê! Sao hôm nay đến trễ?"
    }
  ]
}
```

### Modules

```text
src/timeline/
src/common/
```

### Suggested files

```text
src/timeline/schema.py
src/timeline/ids.py
src/timeline/analyzer.py
src/timeline/validation.py
tests/test_timeline_analyzer.py
```

### Acceptance criteria

- Reads transcript JSON.
- Validates transcript.
- Creates scene IDs.
- Preserves timing.
- Computes duration.
- Handles short segments.
- Handles long segments.
- Produces valid normalized timeline JSON.
- Does not call AI.

### Suggested commits

```text
feat: add normalized timeline schema
feat: add deterministic timeline analyzer
test: add timeline validation tests
docs: document timeline analyzer sprint
```

---

## 11. Sprint 3 - Visual Director

### Goal

Use local LLM to enrich normalized timeline with visual direction.

### One-line goal

```text
timeline.normalized.json → timeline.director.json
```

### Scope

Build:

- prompt loader
- prompt renderer
- Ollama client
- Visual Director service
- JSON parser
- JSON repair flow
- director output schema
- director output validator
- debug output support

### Non-scope

Do not render.

Do not select final icon file.

Do not modify original audio.

Do not implement diarization.

### Input

```text
output/timeline.normalized.json
```

### Output

```text
output/timeline.director.json
```

### Visual Director adds

- display lines
- emotion
- layout
- keywords
- effects
- icon_query
- optional animation suggestions

### Example output scene

```json
{
  "id": "scene_0001",
  "start": 0.25,
  "end": 2.16,
  "duration": 1.91,
  "text": "Ê! Sao hôm nay đến trễ?",
  "lines": ["Ê!", "SAO HÔM NAY", "ĐẾN TRỄ?"],
  "emotion": "surprised",
  "layout": {
    "name": "center_stack"
  },
  "keywords": [
    {
      "text": "ĐẾN TRỄ",
      "importance": 0.95,
      "effect": "pop",
      "style": "keyword_primary"
    }
  ],
  "assets": {
    "icon_query": "trễ giờ"
  }
}
```

### Modules

```text
src/director/
prompts/
src/common/
```

### Suggested files

```text
prompts/visual_director.md
prompts/json_repair.md
src/director/ollama_client.py
src/director/prompt_loader.py
src/director/prompt_renderer.py
src/director/json_parser.py
src/director/visual_director.py
tests/test_prompt_loader.py
tests/test_director_parser.py
```

### Dependencies

```text
requests
pydantic
```

### Acceptance criteria

- Loads prompt from file.
- Calls Ollama.
- Uses Qwen 2.5 3B by config.
- Produces JSON only.
- Validates output.
- Preserves scene IDs.
- Preserves timing.
- Preserves original text.
- Uses allowed emotions/effects/layouts.
- Returns icon_query, not icon filename.
- Can be tested with fake LLM client.

### Suggested commits

```text
feat: add prompt loader and renderer
feat: add ollama client for visual director
feat: add visual director JSON parser
test: add visual director validation tests
docs: add visual director sprint notes
```

---

## 12. Sprint 4 - Icon Selector

### Goal

Map AI-generated icon queries to real local icon assets.

### One-line goal

```text
timeline.director.json + icon_db.json → timeline.visual.json
```

### Scope

Build:

- icon DB schema
- icon DB loader
- asset registry basics
- embedding provider
- icon embedding cache
- semantic icon search
- icon score output
- visual timeline writer

### Non-scope

Do not render icons yet.

Do not build full asset pack system.

Do not use LLM for exact filename selection.

### Input

```text
output/timeline.director.json
assets/icons/icon_db.json
```

### Output

```text
output/timeline.visual.json
```

### Example

Input:

```json
{
  "icon_query": "báo thức"
}
```

Output:

```json
{
  "icon_query": "báo thức",
  "icon_id": "icon_alarm_001",
  "icon_path": "assets/icons/alarm_001.png",
  "icon_score": 0.91
}
```

### Modules

```text
src/embedding/
src/assets/
```

### Suggested files

```text
assets/icons/icon_db.json
src/assets/icon_db.py
src/embedding/icon_selector.py
src/embedding/embedder.py
tests/test_icon_db.py
tests/test_icon_selector.py
```

### Dependencies

```text
sentence-transformers
scikit-learn
numpy
```

### Acceptance criteria

- Loads icon DB.
- Validates icon DB.
- Embeds icon metadata.
- Searches by icon_query.
- Adds icon_id/icon_path/icon_score.
- Handles missing icon DB clearly.
- Handles low confidence clearly.
- Writes valid visual timeline.

### Suggested commits

```text
feat: add icon database schema
feat: add embedding-based icon selector
test: add icon selector tests
docs: document icon selector workflow
```

---

## 13. Sprint 5 - Basic Renderer

### Goal

Render visual timeline into silent vertical video.

### One-line goal

```text
timeline.visual.json → silent_video.mp4
```

### Scope

Build:

- visual timeline loader
- renderer validation
- default template
- canvas creation
- safe zone support
- text rendering
- keyword highlighting
- speaker label rendering
- at least one animation effect
- silent video export

### Non-scope

Do not merge audio yet.

Do not implement advanced transitions.

Do not implement full plugin system.

Do not implement avatars unless easy.

Do not implement SFX.

### Input

```text
output/timeline.visual.json
```

### Output

```text
output/silent_video.mp4
```

### First visual style

```text
dark background
large white text
yellow keyword
black stroke
speaker label
simple pop effect
```

### Modules

```text
src/renderer/
```

### Suggested files

```text
src/renderer/engine.py
src/renderer/context.py
src/renderer/template.py
src/renderer/text.py
src/renderer/layout.py
src/renderer/effects/pop.py
src/renderer/validation.py
tests/test_renderer_validation.py
tests/test_renderer_smoke.py
```

### Dependencies

```text
Pillow
moviepy
numpy
```

### Acceptance criteria

- Reads `timeline.visual.json`.
- Validates unknown effects/layouts.
- Renders 1080x1920 video.
- Renders Vietnamese text.
- Highlights keywords.
- Applies at least `pop` effect.
- Writes `output/silent_video.mp4`.
- Does not call AI.
- Does not merge audio.

### Suggested commits

```text
feat: add visual timeline renderer validation
feat: add basic center stack text renderer
feat: add pop keyword effect
test: add renderer smoke test
docs: document basic renderer implementation
```

---

## 14. Sprint 6 - Exporter

### Goal

Merge rendered silent video with original audio.

### One-line goal

```text
silent_video.mp4 + audio.wav → final.mp4
```

### Scope

Build:

- silent video validation
- audio validation
- FFmpeg merge command
- final MP4 export
- duration check
- render report

### Non-scope

Do not change renderer visuals.

Do not add BGM/SFX yet.

Do not add TTS yet.

### Input

```text
output/silent_video.mp4
temp/audio.wav
```

### Output

```text
output/final.mp4
output/render_report.json
```

### Modules

```text
src/exporter/
```

### Suggested files

```text
src/exporter/commands.py
src/exporter/exporter.py
src/exporter/report.py
tests/test_exporter_commands.py
```

### Acceptance criteria

- Merges silent video and original audio.
- Writes MP4.
- Preserves original voice.
- Writes render report.
- Validates output exists.
- Reports duration mismatch.

### Suggested commits

```text
feat: add audio video merge command
feat: add final mp4 exporter
feat: add render report writer
test: add exporter command tests
```

---

## 15. Sprint 7 - Speaker Support

### Goal

Improve speaker identity handling for dialogue videos.

### Scope

Build:

- speaker mapping config
- speaker labels
- speaker styles
- alternating speaker fallback
- manual speaker override
- speaker color in template
- optional speaker report

### Non-scope

Full diarization is not required yet.

### Input

```text
timeline.normalized.json
speaker config
```

### Output

```text
timeline with speaker labels/styles
```

### Example config

```yaml
speakers:
  SPEAKER_00:
    label: Nam
    style: speaker_a
  SPEAKER_01:
    label: Nữ
    style: speaker_b
```

### Acceptance criteria

- User can map speaker IDs.
- Renderer shows speaker label.
- Speaker styles come from template.
- No gender inference unless configured.

---

## 16. Sprint 8 - Template System

### Goal

Make visual style configurable through templates.

### Scope

Build:

- template loader
- default template
- color tokens
- font tokens
- safe zones
- speaker styles
- keyword styles
- default layout/effect

### Non-scope

Do not build full template marketplace.

### Output

```text
assets/templates/tiktok_dark_comic.yaml
```

### Acceptance criteria

- Renderer uses template.
- No hardcoded colors deep in renderer.
- Template controls safe zone.
- Template controls font and keyword style.
- Template can be changed without code changes.

---

## 17. Sprint 9 - Animation Engine

### Goal

Expand animation system.

### Scope

Build:

- effect registry
- layout registry
- effect base interface
- pop
- bounce
- shake
- glow
- slide
- fade
- pulse
- effect validation
- animation timing

### Non-scope

Do not build complex particles yet.

### Acceptance criteria

- Effects are registered.
- Unknown effect fails validation.
- Multiple effects work.
- Effects are deterministic.
- Effects use scene-local timing.

---

## 18. Sprint 10 - AI Video Engine V1

### Goal

Deliver first complete end-to-end engine.

### Scope

V1 should support:

```text
input/video.mp4
      ↓
output/final.mp4
```

with:

- STT
- timeline analyzer
- visual director
- icon selector
- renderer
- exporter
- default template
- documentation
- basic tests

### Acceptance criteria

- One command or script can run full pipeline.
- Output video has original audio.
- Output is vertical 9:16.
- Text is readable.
- Keywords highlighted.
- JSON files inspectable.
- Renderer does not call AI.
- Documentation explains setup and usage.

### Suggested version

```text
v1.0.0-alpha
```

---

## 19. Sprint 11 - Batch Processing

### Goal

Process many videos/scripts efficiently.

### Scope

Build:

- batch input folder
- per-video output folder
- batch report
- model reuse
- cache reuse
- progress logging

### Example

```bash
ai-video build input_folder/
```

### Output

```text
output/video_001/final.mp4
output/video_002/final.mp4
output/batch_report.json
```

### Acceptance criteria

- Multiple videos process sequentially.
- Models are not reloaded unnecessarily.
- Failures are reported per input.
- Batch report exists.

---

## 20. Sprint 12 - Quality Review Tools

### Goal

Add tools to review and debug video quality.

### Scope

Build:

- timeline validation report
- prompt debug output
- render debug frames
- safe zone preview
- icon match report
- low-confidence report

### Acceptance criteria

- User can inspect why a scene looks wrong.
- Debug outputs are optional.
- Debug files are ignored by Git.

---

## 21. Sprint 13 - Optional Diarization

### Goal

Add better speaker separation.

### Scope

Evaluate and optionally implement:

- WhisperX
- pyannote.audio
- diarization provider abstraction
- speaker segment merging
- confidence score
- fallback behavior

### Non-scope

Diarization should not become mandatory.

### Acceptance criteria

- Diarization can be enabled by config.
- Basic pipeline works without diarization.
- Speaker output includes source/confidence.

---

## 22. Sprint 14 - Word-Level Timing

### Goal

Enable per-word animation.

### Scope

Build:

- word timing schema
- alignment provider
- keyword timing resolution
- per-word highlight
- karaoke-style highlight
- word-level animation target

### Acceptance criteria

- Words have start/end.
- Keyword animation can sync more accurately.
- Renderer can highlight word or phrase by timing.

---

## 23. Sprint 15 - UI Prototype

### Goal

Make workflow easier for non-technical users.

### Possible UI choices

- Streamlit
- simple web app
- desktop app
- VS Code workflow

### Scope

Prototype should allow:

- choose input video
- run STT
- view transcript
- edit timeline JSON
- render preview
- export final video

### Non-scope

Do not let UI logic replace core engine.

Core engine remains separate.

---

## 24. Sprint 16 - Recruitment Video Workflow

### Goal

Use engine for recruitment content.

### Why

The user is a recruiter.

Possible workflows:

```text
job description → script → video
```

```text
CV → candidate intro → video
```

### Scope

Build:

- recruitment template
- script generator prompt
- recruitment visual style
- job benefits icons
- call-to-action layout

### Acceptance criteria

- Can generate recruitment short video from structured input.
- Uses existing engine pipeline.
- Does not fork renderer.

---

## 25. Sprint 17 - Text-to-Video / TTS Workflow

### Goal

Support videos starting from dialogue text instead of existing voice.

### Pipeline

```text
dialogue.txt
      ↓
script parser
      ↓
Visual Director
      ↓
TTS
      ↓
timeline with generated audio
      ↓
renderer
      ↓
exporter
```

### Possible TTS providers

- Edge TTS
- OpenAI TTS
- Azure TTS
- ElevenLabs

### Non-scope

Do not replace existing-video workflow.

TTS is an additional mode.

---

## 26. Sprint 18 - Asset Pack System

### Goal

Organize reusable asset packs.

### Scope

Build:

- asset pack manifest
- asset validation
- template dependencies
- icon pack support
- font pack support
- preview tools

### Example

```text
asset_packs/dark_comic_v1/
asset_packs/recruitment_clean_v1/
```

### Acceptance criteria

- Asset packs can be validated.
- Templates can depend on asset packs.
- Missing assets are detected.

---

## 27. Sprint 19 - Performance Optimization

### Goal

Improve render speed and batch performance.

### Scope

Optimize:

- model loading
- embedding cache
- text layer caching
- image caching
- frame generation
- video encoding
- batch processing

### Possible improvements

- frame pipe to FFmpeg
- OpenCV backend
- static scene optimization
- pre-rendered layers
- preview mode

### Acceptance criteria

- Faster render time.
- No architecture break.
- Same output quality.

---

## 28. Sprint 20 - V1 Release Hardening

### Goal

Prepare stable V1 release.

### Scope

- schema cleanup
- docs review
- tests
- CI
- examples
- release notes
- sample assets
- install guide
- troubleshooting guide

### Acceptance criteria

- New user can install and run.
- Example input produces example output.
- Docs explain all required tools.
- Core tests pass.
- Release tag created.

---

## 29. Long-term roadmap

### 29.1 API server

Add FastAPI wrapper.

Possible endpoints:

```text
POST /build
POST /transcribe
POST /render
GET /jobs/{id}
```

### 29.2 Desktop app

Local app for creators.

Features:

- drag-and-drop video
- transcript editor
- style selector
- render preview
- export

### 29.3 Web editor

Browser-based timeline editing.

### 29.4 VS Code extension

Developer-focused workflow.

### 29.5 Auto upload

Future integration with platforms.

Not early priority.

### 29.6 Scheduler

Batch content generation and scheduling.

### 29.7 Template marketplace

Reusable visual styles.

Not early priority.

---

## 30. Product tracks

The engine can support multiple product tracks.

### Track A - Existing video redesign

Input:

```text
video with voice
```

Output:

```text
stylized short-form video
```

### Track B - Dialogue text to video

Input:

```text
dialogue text
```

Output:

```text
TTS + animated text video
```

### Track C - Recruitment video

Input:

```text
job description
```

Output:

```text
recruitment short video
```

### Track D - Candidate intro video

Input:

```text
CV
```

Output:

```text
candidate intro video
```

### Track E - News recap video

Input:

```text
article/news source
```

Output:

```text
summary video
```

Track A is first.

---

## 31. Current priority order

Highest priority now:

1. Complete docs.
2. Commit docs to GitHub.
3. Start Sprint 1.
4. Get transcript JSON from real video.
5. Build timeline analyzer.
6. Add Visual Director.
7. Render simple video.
8. Merge original audio.

Do not jump to UI yet.

Do not jump to advanced animations yet.

---

## 32. Out-of-scope until V1

Avoid these before V1:

- full web app
- complex desktop app
- cloud rendering
- video diffusion generation
- advanced diarization dependency
- complex particles
- auto upload to social platforms
- payment/subscription system
- plugin marketplace
- large asset marketplace
- multi-user collaboration

---

## 33. Risk register

### Risk 1 - Setup complexity

AI packages can be hard to install.

Mitigation:

- use Python 3.11
- start with simple dependencies
- avoid WhisperX early
- document Windows setup

### Risk 2 - LLM invalid JSON

Mitigation:

- strict prompts
- JSON repair
- validation
- fake tests

### Risk 3 - Poor STT output

Mitigation:

- allow manual transcript edit
- configurable model
- future WhisperX

### Risk 4 - Renderer performance

Mitigation:

- simple first renderer
- optimize later
- backend abstraction

### Risk 5 - Asset inconsistency

Mitigation:

- asset DB
- metadata
- validation
- templates

### Risk 6 - Chat context loss

Mitigation:

- docs as source of truth
- AGENTS.md
- GitHub

### Risk 7 - Overbuilding

Mitigation:

- sprint scope
- vertical slices
- clear non-scope

---

## 34. Success metrics

### Technical metrics

- STT produces valid transcript.
- Timeline JSON validates.
- LLM JSON validation pass rate.
- Renderer success rate.
- Final export success rate.
- Average render time.
- Batch success rate.

### Product metrics

- Text readability.
- Keyword relevance.
- Icon relevance.
- Audio sync.
- Visual style consistency.
- User correction count.
- Time saved per video.

### Development metrics

- tests passing
- docs updated
- small commits
- no architecture violations
- reproducible output

---

## 35. Definition of Done by level

### Task done

- code or doc change complete
- local check performed
- no unrelated changes
- commit ready

### Sprint done

- deliverable exists
- docs updated
- tests added where practical
- commit pushed
- next sprint unblocked

### Milestone done

- feature works end-to-end
- sample input/output exists
- docs explain usage
- known limitations listed

### V1 done

- full pipeline works
- install guide works
- schema stable enough
- example video works
- renderer deterministic
- local-first maintained

---

## 36. Documentation roadmap

### Required docs

```text
AGENTS.md
PROJECT_RULES.md
README.md
ROADMAP.md
CHANGELOG.md
docs/ProjectVision.md
docs/Architecture.md
docs/Pipeline.md
docs/JSONSchema.md
docs/RendererDesign.md
docs/AIDesign.md
docs/PromptGuide.md
docs/AssetGuide.md
docs/CodingStandard.md
docs/DecisionLog.md
docs/Sprint0.md
docs/Sprint1.md
docs/Glossary.md
```

### Later docs

```text
docs/Troubleshooting.md
docs/InstallWindows.md
docs/InstallMac.md
docs/CLI.md
docs/Templates.md
docs/AssetPacks.md
docs/Testing.md
docs/ReleaseProcess.md
```

---

## 37. Testing roadmap

### Sprint 1 tests

- audio command builder
- transcript schema
- JSON writing

### Sprint 2 tests

- timeline validation
- scene ID generation
- split/merge behavior

### Sprint 3 tests

- prompt loader
- LLM parser
- invalid JSON handling
- enum validation

### Sprint 4 tests

- icon DB validation
- icon search

### Sprint 5 tests

- renderer validation
- minimal render smoke

### Sprint 6 tests

- FFmpeg merge command
- report writer

### Later tests

- integration pipeline
- batch processing
- renderer visual regression
- template validation

---

## 38. CI roadmap

### Initial CI

```text
setup Python
print Python version
```

### Next CI

```text
install requirements
run unit tests
```

### Later CI

```text
ruff
black check
pytest
schema validation
docs link check
```

### Avoid in CI initially

- downloading large models
- running Whisper
- running Ollama
- rendering long videos

---

## 39. CLI roadmap

### Stage 1

Scripts:

```bash
python scripts/transcribe.py input/video.mp4
```

### Stage 2

Module commands:

```bash
python -m ai_video_engine transcribe input/video.mp4
```

### Stage 3

Installed CLI:

```bash
ai-video transcribe input/video.mp4
ai-video build input/video.mp4
```

### Future commands

```bash
ai-video assets validate
ai-video assets search-icon "báo thức"
ai-video render output/timeline.visual.json
ai-video export output/silent_video.mp4 temp/audio.wav
```

---

## 40. Package roadmap

Current:

```text
src/audio
src/speech
...
```

Possible future:

```text
src/ai_video_engine/audio
src/ai_video_engine/speech
...
```

Before significant code is added, decide package layout.

Potential next ADR:

```text
ADR-0041 - Choose Python package layout
```

---

## 41. Asset roadmap

### Phase 1

No assets required.

### Phase 2

Starter icon DB.

### Phase 3

Default font.

### Phase 4

Default template.

### Phase 5

Basic icons.

### Phase 6

Avatars.

### Phase 7

SFX.

### Phase 8

Asset packs.

---

## 42. Template roadmap

### Template 1

```text
tiktok_dark_comic
```

### Template 2

```text
minimal_black
```

### Template 3

```text
neon_dialogue
```

### Template 4

```text
recruitment_clean
```

### Template 5

```text
education_bold
```

Only Template 1 is required before V1.

---

## 43. Prompt roadmap

### Prompt 1

```text
visual_director.md
```

### Prompt 2

```text
json_repair.md
```

### Prompt 3

```text
keyword_extractor.md
```

### Prompt 4

```text
emotion_classifier.md
```

### Prompt 5

```text
icon_query.md
```

### Prompt 6

```text
speaker_mapping.md
```

Only Prompt 1 and Prompt 2 are required early.

---

## 44. Model roadmap

### Current planned models

```text
Faster Whisper
Qwen 2.5 3B through Ollama
sentence-transformers multilingual embedding
```

### Future models

```text
WhisperX
pyannote.audio
BGE-M3
cloud LLM providers
cloud STT providers
TTS providers
```

Future models must be optional.

---

## 45. Renderer roadmap

### Renderer v0

Static text.

### Renderer v1

Large text, keyword highlight.

### Renderer v2

Basic animations.

### Renderer v3

Icons.

### Renderer v4

Templates.

### Renderer v5

Avatars.

### Renderer v6

Transitions.

### Renderer v7

Performance backend.

---

## 46. Export roadmap

### Export v0

Merge silent video with original audio.

### Export v1

Render report.

### Export v2

Duration validation.

### Export v3

SFX mixing.

### Export v4

BGM ducking.

### Export v5

Multiple output formats.

---

## 47. Speaker roadmap

### Speaker v0

Unknown speakers.

### Speaker v1

Manual mapping.

### Speaker v2

Alternating fallback.

### Speaker v3

Diarization provider.

### Speaker v4

Speaker avatars.

### Speaker v5

Speaker-specific styles.

---

## 48. JSON schema roadmap

### Schema v0.1

Basic transcript, timeline, visual timeline.

### Schema v0.2

Add stronger asset references.

### Schema v0.3

Add animation target improvements.

### Schema v0.4

Add word timing.

### Schema v0.5

Add speaker diarization fields.

### Schema v1.0

Stable V1 schema.

---

## 49. Roadmap governance

This roadmap should be updated when:

- sprint scope changes
- sprint order changes
- major feature added
- major feature removed
- release target changes
- architecture decision changes

Major roadmap changes should be recorded in DecisionLog.

---

## 50. Roadmap anti-patterns

Avoid:

- jumping to UI before pipeline works
- adding many AI models before basic STT works
- adding advanced renderer before timeline schema works
- adding cloud dependencies by default
- building features without docs
- making huge commits
- ignoring tests
- ignoring Windows support
- breaking AI/renderer boundary

---

## 51. Immediate next actions

After Sprint 0B docs are added to repository:

1. Commit docs.

```bash
git add .
git commit -m "docs: complete Sprint 0B project knowledge base"
git push
```

2. Open or create GitHub issue:

```text
Sprint 1 - Speech To Text
```

3. Start Sprint 1 implementation.

4. First Sprint 1 goal:

```text
extract audio from input/video.mp4
```

5. Second Sprint 1 goal:

```text
transcribe temp/audio.wav to output/transcript.json
```

---

## 52. Current recommended next commit

```text
docs: complete Sprint 0B project knowledge base
```

This commit should include:

```text
AGENTS.md
PROJECT_RULES.md
README.md
ROADMAP.md
docs/*.md
```

---

## 53. How to continue in a new chat

Use this message:

```text
Continue AI Video Engine.
Read AGENTS.md, PROJECT_RULES.md, ROADMAP.md, and docs/ before coding.
Current sprint: Sprint 1 - Speech To Text.
Repository: <GitHub URL>
```

---

## 54. How to continue in Codex

Instruction to Codex:

```text
Read AGENTS.md first.
Then read PROJECT_RULES.md and ROADMAP.md.
Do not code until you understand the current sprint.
Current sprint is Sprint 1 - Speech To Text.
Implement the smallest useful vertical slice.
```

---

## 55. Final roadmap principle

Build the engine in the correct order.

The first impressive milestone is not a fancy animation.

The first impressive milestone is:

```text
input/video.mp4 → output/final.mp4
```

with the original voice preserved and all intermediate JSON inspectable.

Everything else becomes easier after that.

---

# Appendix A - Sprint checklist table

| Sprint | Name | Deliverable | Status |
|---|---|---|---|
| 0A | Bootstrap | `repo + skeleton` | completed |
| 0B | Knowledge Base | `docs complete` | completed |
| 1 | Speech To Text | `transcript.json` | completed |
| 2 | Timeline Analyzer | `timeline.normalized.json` | next |
| 3 | Visual Director | `timeline.director.json` | planned |
| 4 | Icon Selector | `timeline.visual.json` | planned |
| 5 | Basic Renderer | `silent_video.mp4` | planned |
| 6 | Exporter | `final.mp4` | planned |
| 7 | Speaker Support | `speaker mapping` | planned |
| 8 | Template System | `template config` | planned |
| 9 | Animation Engine | `effect registry` | planned |
| 10 | Engine V1 | `end-to-end build` | planned |

---

# Appendix B - Feature dependency graph

```text
Documentation
    ↓
Speech To Text
    ↓
Timeline Analyzer
    ↓
Visual Director
    ↓
Icon Selector
    ↓
Renderer
    ↓
Exporter
    ↓
End-to-End V1
    ↓
Templates / Batch / UI / Diarization / Word Timing
```

---

# Appendix C - Minimal V1 checklist

1. Can install dependencies.
2. Can run on Windows.
3. Can run without GPU.
4. Can extract audio.
5. Can transcribe Vietnamese audio.
6. Can write transcript.json.
7. Can normalize timeline.
8. Can call local LLM for visual direction.
9. Can validate LLM output.
10. Can select icons from local DB.
11. Can render large text video.
12. Can highlight keywords.
13. Can merge original audio.
14. Can export final.mp4.
15. Can inspect intermediate JSON.
16. Docs explain workflow.

---

# Appendix D - Release naming

Suggested release names:

```text
v0.1.0-foundation
v0.2.0-transcription
v0.3.0-timeline
v0.4.0-director
v0.5.0-icon-selector
v0.6.0-renderer
v0.7.0-exporter
v1.0.0-alpha
v1.0.0
```

---

# Appendix E - Roadmap update checklist

1. Does the sprint order still make sense?
2. Has any sprint scope changed?
3. Has any dependency changed?
4. Has any feature moved out of V1?
5. Has any feature moved into V1?
6. Do docs match the roadmap?
7. Does DecisionLog need an entry?
8. Does README need a status update?
9. Does GitHub issue list match sprint plan?

---

# Appendix F - Final note

This roadmap is intentionally practical.

The project should move from:

```text
documentation → transcript → timeline → AI direction → render → final video
```

without skipping the foundations.
