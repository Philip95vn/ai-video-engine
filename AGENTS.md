# AGENTS.md

## 0. Purpose of this file

This file is the primary instruction document for all AI coding agents working on **AI Video Engine**.

It is intended for:

- ChatGPT
- Codex in VS Code
- GitHub Copilot
- Cursor
- Claude Code
- Gemini CLI
- Human contributors

Before changing code, an agent must read this file and follow it.

This file defines:

- Product vision
- Architecture principles
- Development workflow
- Coding rules
- AI rules
- Renderer rules
- JSON contract rules
- Git rules
- Testing expectations
- Documentation expectations
- Long-term design constraints

If a future chat loses context, this file is the recovery point.

---

## 1. Project name

**AI Video Engine**

---

## 2. Product vision

AI Video Engine is a local-first, modular system for generating short-form videos automatically.

The first product target is:

- Vertical 9:16 videos
- Dialogue-based content
- Large animated text
- Original voice preserved
- Automatic speech-to-text
- Speaker-aware timeline
- Keyword highlighting
- Icon selection
- Dynamic text layouts
- Deterministic video rendering

Long-term, the same engine should support:

- TikTok videos
- YouTube Shorts
- Instagram Reels
- Recruitment videos
- Training videos
- Marketing videos
- News recap videos
- Sales explainer videos
- Educational micro-lessons

The project is not just a script.

It is an engine.

---

## 3. Core philosophy

The project separates intelligence from rendering.

AI does not render video.

AI does not generate final pixels.

AI does not create video frames.

AI only analyzes content and produces structured instructions.

The renderer consumes structured instructions and produces the video.

This separation is the most important architectural decision in the project.

---

## 4. One-sentence architecture

Input video/audio is converted into transcript and timeline, then AI enriches the timeline into a visual script, and the deterministic renderer converts that JSON into a final video.

---

## 5. High-level pipeline

```text
Input Video / Audio
        ↓
Audio Extractor
        ↓
Speech To Text
        ↓
Transcript JSON
        ↓
Speaker Diarization / Speaker Mapping
        ↓
Timeline Analyzer
        ↓
Visual Director AI
        ↓
Icon Selector
        ↓
Timeline JSON
        ↓
Renderer
        ↓
Audio Merger
        ↓
Final MP4
```

---

## 6. Current main workflow

The current workflow starts from an existing video that already has voice.

The engine should:

1. Take an input video.
2. Extract the original audio.
3. Run speech-to-text.
4. Produce transcript with timestamps.
5. Detect or infer speaker roles.
6. Normalize the transcript into scenes.
7. Ask the Visual Director AI to enrich scenes.
8. Select keywords.
9. Select effects.
10. Select icons.
11. Produce a final visual timeline JSON.
12. Render video based on JSON.
13. Merge rendered video with original audio.
14. Export final MP4.

The original voice should be preserved.

---

## 7. Hard rules

These rules must not be broken.

1. AI must never render video directly.
2. AI must never generate final video frames.
3. AI must never be required for the renderer to run.
4. Renderer must never call an LLM.
5. Renderer must only consume structured JSON.
6. Timeline JSON is the contract between AI and renderer.
7. Every scene must have start and end time.
8. Every scene must have text.
9. Every scene must have a layout.
10. Every keyword must have a target text.
11. Every animation must have a known effect type.
12. Prompts must live in `prompts/`.
13. Prompt text must not be hardcoded in business logic.
14. Assets must not be hardcoded.
15. Every major architectural decision must be logged in `docs/DecisionLog.md`.
16. Every public module must have documentation.
17. Each feature should be developed through a Git issue when practical.
18. One commit should represent one logical change.
19. Do not rewrite large modules without documenting why.
20. Do not introduce cloud dependencies without approval.

---

## 8. Non-goals

The project is not trying to build a video diffusion model.

The project is not trying to replace Sora, Veo, Runway, or Pika.

The project is not trying to generate realistic video from text.

The project is not trying to edit arbitrary footage like Premiere Pro.

The project is not trying to be a general-purpose NLE.

The first goal is automated short-form motion-text videos.

---

## 9. Target user experience

A user should eventually be able to run:

```bash
python -m ai_video_engine input/video.mp4
```

and receive:

```text
output/final.mp4
output/transcript.json
output/timeline.json
output/render_report.json
```

The default output should be a 9:16 video.

---

## 10. Default video format

Default format:

- Width: 1080
- Height: 1920
- Aspect ratio: 9:16
- FPS: 30
- Codec: H.264
- Audio codec: AAC
- Container: MP4

These defaults may be overridden by templates.

---

## 11. Main modules

The project should be organized around modules.

Each module should have one main responsibility.

Recommended module structure:

```text
src/
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

---

## 12. `src/audio`

Responsible for audio extraction and audio preparation.

Typical responsibilities:

- Extract audio from video.
- Convert audio to WAV.
- Normalize sample rate.
- Convert stereo to mono when needed.
- Prepare input for speech-to-text.
- Preserve original audio for final merge.

This module should use FFmpeg.

It should not call Whisper.

It should not call LLMs.

---

## 13. `src/speech`

Responsible for speech-to-text.

Typical responsibilities:

- Load speech-to-text model.
- Transcribe audio.
- Produce timestamped transcript.
- Support Vietnamese.
- Export transcript JSON.
- Optionally support word timestamps later.

Initial recommended tool:

- Faster Whisper

Possible later tools:

- WhisperX
- pyannote.audio
- cloud STT APIs

This module should not choose visual effects.

This module should not select icons.

---

## 14. `src/timeline`

Responsible for normalizing transcript into scenes.

Typical responsibilities:

- Clean transcript text.
- Merge short segments.
- Split long segments.
- Enforce max scene duration.
- Preserve start and end times.
- Create scene IDs.
- Create speaker turns.
- Ensure each scene is renderable.

This module is deterministic.

It should not require an LLM.

---

## 15. `src/director`

Responsible for AI-based visual direction.

Typical responsibilities:

- Analyze scene text.
- Pick important keywords.
- Pick emotion.
- Pick text layout style.
- Pick animation style.
- Pick icon query.
- Pick speaker mood.
- Produce enriched scene JSON.

This is where LLMs are allowed.

The director returns structured JSON only.

It does not render.

It does not draw.

It does not invoke FFmpeg.

---

## 16. `src/embedding`

Responsible for semantic search over assets.

Typical responsibilities:

- Build icon embeddings.
- Search icon database.
- Match icon query to available icon.
- Cache vectors.
- Return asset IDs or file paths.

Recommended first model:

- `paraphrase-multilingual-MiniLM-L12-v2`

Possible later models:

- BGE-M3
- multilingual-e5-small
- local vector database

This module should be replaceable.

---

## 17. `src/renderer`

Responsible for visual rendering.

Typical responsibilities:

- Load Timeline JSON.
- Draw background.
- Draw text.
- Draw highlighted keywords.
- Draw icons.
- Draw avatars.
- Apply animation.
- Generate video frames or clips.
- Export silent video.

Renderer must be deterministic.

Given the same input JSON and same assets, it should produce the same result.

Renderer must not call any LLM.

---

## 18. `src/exporter`

Responsible for final output.

Typical responsibilities:

- Merge rendered silent video with original audio.
- Export MP4.
- Write render report.
- Validate output duration.
- Validate audio/video sync.

This module should use FFmpeg.

---

## 19. `src/common`

Common utilities.

Typical responsibilities:

- File paths
- Logging
- JSON helpers
- Time helpers
- Validation helpers
- Error classes

Do not place business logic here.

---

## 20. `src/config`

Configuration loading.

Typical responsibilities:

- Load YAML/TOML/JSON config.
- Provide typed config objects.
- Resolve project paths.
- Resolve template defaults.

---

## 21. Asset structure

Assets should live under:

```text
assets/
├── icons/
├── avatars/
├── backgrounds/
├── fonts/
├── sfx/
└── templates/
```

No asset should be referenced by random absolute paths.

Assets should be selected by IDs or relative paths.

---

## 22. Prompt structure

Prompts should live under:

```text
prompts/
├── visual_director.md
├── timeline_analyzer.md
├── keyword_extractor.md
├── emotion_classifier.md
├── icon_query.md
└── json_repair.md
```

Prompt versions should be documented.

Prompt changes can affect output quality and must be treated as product changes.

---

## 23. Documentation structure

Documentation should live under:

```text
docs/
├── ProjectVision.md
├── Architecture.md
├── Pipeline.md
├── JSONSchema.md
├── RendererDesign.md
├── AIDesign.md
├── PromptGuide.md
├── AssetGuide.md
├── CodingStandard.md
├── DecisionLog.md
├── Sprint0.md
├── Sprint1.md
└── Glossary.md
```

Documentation should be kept in sync with code.

---

## 24. JSON is the main contract

The Timeline JSON is the most important interface in the project.

All modules should either:

- produce JSON,
- validate JSON,
- enrich JSON,
- consume JSON,
- or export results derived from JSON.

The renderer should never guess intent from raw transcript if that intent should already be in JSON.

---

## 25. Timeline JSON minimum fields

Each scene should eventually contain:

```json
{
  "id": "scene_0001",
  "start": 0.25,
  "end": 2.16,
  "duration": 1.91,
  "speaker": "speaker_00",
  "text": "Ê! Sao hôm nay đến trễ?",
  "lines": ["Ê!", "SAO HÔM NAY", "ĐẾN TRỄ?"],
  "keywords": [],
  "layout": {},
  "animations": [],
  "assets": {},
  "audio": {}
}
```

---

## 26. Scene timing rules

Every scene must have:

- `start`
- `end`
- `duration`

`duration` should equal `end - start`.

Scene duration should not be negative.

Scene duration should not be zero.

Default minimum duration should be configurable.

Default maximum duration should be configurable.

---

## 27. Text rules

Text should be readable on mobile.

Each frame should normally contain one or two sentences only.

Large text is preferred.

Too much text per frame should be avoided.

The renderer should support line breaks.

The director may suggest line breaks.

The timeline analyzer may enforce line length limits.

---

## 28. Keyword rules

Keywords are not subtitles.

Keywords are emphasis targets.

A keyword should usually be:

- funny
- surprising
- emotional
- important
- punchline-related
- contrastive
- visually meaningful

A keyword must map to text appearing in the scene, unless explicitly marked as conceptual.

---

## 29. Animation rules

Animation should emphasize meaning.

Examples:

- `pop` for surprise
- `shake` for anger or chaos
- `bounce` for humor
- `glow` for important concepts
- `slide` for conversational flow
- `typewriter` for suspense
- `zoom` for punchline

Animation names must be from a known registry.

The renderer should fail clearly if an unknown animation is requested.

---

## 30. Icon rules

Icons are selected in two stages.

Stage 1: AI produces `icon_query`.

Stage 2: embedding/icon selector maps query to actual available icon.

AI should not be expected to know every icon filename.

The icon selector should use asset metadata.

---

## 31. Speaker rules

Speaker labels may begin as:

- `SPEAKER_00`
- `SPEAKER_01`

Later they may be mapped to:

- `Nam`
- `Nữ`
- `Host`
- `Guest`
- `Character A`
- `Character B`

Speaker mapping should be editable.

The engine must not assume gender from voice unless the user explicitly configures it.

---

## 32. Speech-to-text rules

Speech-to-text should preserve timestamps.

Vietnamese support is required.

The first implementation should use Faster Whisper.

The model should be configurable.

Possible model choices:

- `small`
- `medium`
- `large-v3`

The default should balance speed and quality.

---

## 33. Diarization rules

Speaker diarization is optional in early versions.

If diarization is unavailable, use alternating speaker inference only as a fallback.

Fallback speaker inference must be marked as low confidence.

Later diarization may use WhisperX and pyannote.audio.

---

## 34. Renderer determinism

Given:

- same timeline JSON
- same assets
- same fonts
- same renderer version
- same config

the renderer should produce consistent output.

Random effects must use a seed.

---

## 35. Templates

Templates define style.

Examples:

- `tiktok_dark_comic`
- `neon_dialogue`
- `minimal_black`
- `recruitment_pitch`
- `news_bold`
- `education_clean`

Templates may define:

- font
- colors
- text positions
- animation defaults
- icon behavior
- avatar behavior
- background behavior
- safe zones

---

## 36. Safe zones

Vertical video must respect mobile UI overlays.

Text should avoid:

- very top edge
- very bottom edge
- right-side TikTok buttons
- caption overlap zones

Safe zones should be configurable.

---

## 37. Original audio policy

When input video has original voice, preserve the original audio by default.

Do not replace voice with TTS unless user requests it.

The output should merge rendered visual video with original audio.

---

## 38. TTS policy

TTS is optional.

TTS may be used for generated scripts.

For current workflow, original voice is primary.

When TTS is used, voice metadata should be stored in JSON.

---

## 39. Error handling rules

Errors should be explicit.

Do not silently skip failed stages.

Bad JSON should fail validation.

Missing assets should produce clear warnings or errors.

Unknown effects should fail before render.

Invalid timestamps should fail before render.

---

## 40. Logging rules

Use structured logging where practical.

Logs should show:

- input file
- output file
- model name
- duration
- scene count
- warnings
- errors

Logs should not leak secrets.

---

## 41. Configuration rules

Do not scatter constants across modules.

Use config files for:

- video width
- video height
- fps
- default template
- model names
- output paths
- max scene duration
- font defaults

---

## 42. Caching rules

AI and embedding operations can be expensive.

Cache where appropriate:

- STT output
- LLM output
- icon embeddings
- asset database
- rendered intermediate clips

Cache invalidation should be simple and documented.

---

## 43. Testing strategy

Tests should cover:

- audio extraction command creation
- transcript parsing
- timeline validation
- JSON schema validation
- director output parsing
- icon selection
- renderer smoke test
- exporter command generation

Do not require large models in unit tests.

Model-dependent tests should be optional integration tests.

---

## 44. Unit test rules

Unit tests should be fast.

Unit tests should not require internet.

Unit tests should not require GPU.

Unit tests should not require large media files.

Use small fixtures.

---

## 45. Integration test rules

Integration tests may use small audio/video samples.

They may be slower.

They should be clearly separated from unit tests.

---

## 46. Git workflow

Recommended workflow:

```text
git pull
create issue
create branch
design
code
test
commit
push
merge
```

For a solo project, direct commits to `main` are acceptable during early development.

Later, use branches and pull requests.

---

## 47. Commit message rules

Use conventional commits:

- `feat:`
- `fix:`
- `docs:`
- `refactor:`
- `test:`
- `chore:`
- `perf:`
- `ci:`

Examples:

```text
docs: expand project rules for renderer architecture
feat: add faster whisper transcript exporter
fix: validate scene duration before render
test: add timeline schema tests
```

---

## 48. Versioning

Use semantic versioning when releases begin.

Example:

- `v0.1.0` project skeleton
- `v0.2.0` speech-to-text
- `v0.3.0` timeline analyzer
- `v0.4.0` visual director
- `v0.5.0` basic renderer
- `v1.0.0` first complete engine

---

## 49. Branch naming

Recommended branch names:

```text
feat/speech-to-text
feat/timeline-analyzer
feat/visual-director
feat/basic-renderer
docs/project-rules
fix/json-validation
```

---

## 50. Python version

Use Python 3.11+.

Avoid relying on Python 3.14 for now because many AI packages may not fully support it.

---

## 51. Dependency policy

Prefer stable packages.

Avoid unnecessary dependencies.

Dependencies must be added intentionally.

Large AI dependencies should be optional when possible.

---

## 52. Current recommended dependencies

Core:

- faster-whisper
- requests
- sentence-transformers
- scikit-learn
- numpy
- Pillow
- moviepy
- pydub
- rich
- orjson
- pydantic

Optional:

- whisperx
- pyannote.audio
- opencv-python
- faiss-cpu
- edge-tts

---

## 53. Windows support

Windows support is required.

FFmpeg must be installed and available in PATH.

PowerShell commands should be documented when needed.

Avoid Linux-only assumptions.

---

## 54. Mac support

Mac M1 support is important.

The engine should run without a discrete GPU.

Avoid mandatory CUDA dependencies.

---

## 55. GPU policy

GPU should be optional.

The project should work on CPU.

GPU acceleration may be added later for performance.

---

## 56. LLM policy

The local LLM should initially run through Ollama.

Recommended first LLM:

- Qwen 2.5 3B Instruct

Other possible LLMs:

- Phi-3 Mini
- Gemma 4B
- Llama 3.2 3B

LLM output must be validated.

---

## 57. LLM output rules

LLM must return JSON.

No markdown.

No explanations.

No comments inside JSON.

No trailing commas.

If the LLM output is invalid, use a repair step or fail clearly.

---

## 58. Prompt output schema

Prompts should specify exact output fields.

Prompts should include allowed enum values.

Prompts should include examples.

Prompts should include constraints.

Prompts should include language-specific notes for Vietnamese.

---

## 59. Vietnamese support

Vietnamese is a first-class language.

The engine should handle:

- Vietnamese accents
- Vietnamese punctuation
- Vietnamese dialogue
- Vietnamese short-form humor
- Vietnamese slang where possible

---

## 60. Dialogue content

The first content style is humorous dialogue between two people.

Each visual scene should normally represent one speaker turn or one short phrase.

Do not create dense subtitles.

The whole frame should be designed around large text.

---

## 61. Subtitle policy

The system is not a simple subtitle generator.

It creates full-screen kinetic text scenes.

Text should be large, expressive, and layout-driven.

---

## 62. Visual style

Initial visual style:

- dark background
- bold text
- high contrast
- highlighted keywords
- simple icons
- playful motion
- speaker identity colors

Example:

- Speaker A blue
- Speaker B pink
- Keyword yellow
- Background near-black

These are defaults, not hard rules.

---

## 63. Renderer plugin model

Effects should be plugin-like.

Renderer should support adding new effects without rewriting the engine.

Example effect plugins:

- pop
- bounce
- shake
- glow
- slide
- typewriter
- zoom
- fade
- pulse

---

## 64. Effect registry

Effects should be registered in one place.

Renderer should check if requested effect exists.

Unknown effects should fail validation.

---

## 65. Layout registry

Layouts should be registered in one place.

Example layouts:

- center_stack
- left_avatar_right_text
- top_question_bottom_answer
- comic_panel
- punchline_center
- split_speaker

---

## 66. Asset metadata

Assets should have metadata.

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

## 67. Icon selection strategy

Do not ask the LLM to pick exact icon filenames from memory.

Ask the LLM for an `icon_query`.

Then use embedding search to map query to icon metadata.

---

## 68. Validation strategy

Validation should happen at stage boundaries.

Examples:

- validate transcript JSON
- validate normalized timeline
- validate visual director output
- validate final render timeline
- validate output media

---

## 69. Schema strategy

Use Pydantic or JSON Schema.

Pydantic is acceptable for Python-first validation.

JSON Schema is useful for documentation and external tools.

Both may coexist.

---

## 70. CLI strategy

The project should eventually expose a CLI.

Example commands:

```bash
ai-video extract-audio input.mp4
ai-video transcribe input.mp4
ai-video direct transcript.json
ai-video render timeline.json
ai-video build input.mp4
```

---

## 71. Report files

Each run should eventually produce reports:

```text
output/transcript.json
output/timeline.normalized.json
output/timeline.visual.json
output/render_report.json
output/final.mp4
```

---

## 72. File naming

Use predictable names.

Examples:

```text
input/video.mp4
temp/audio.wav
output/transcript.json
output/timeline.json
output/silent_video.mp4
output/final.mp4
```

---

## 73. Security rules

Do not commit secrets.

Do not commit API keys.

Use `.env` for local secrets.

Add `.env` to `.gitignore`.

Do not log secrets.

---

## 74. Privacy rules

Input videos may contain personal voice or private content.

Avoid uploading media to external services unless explicitly requested.

Prefer local processing.

---

## 75. Cloud service policy

Cloud services are allowed only when intentionally configured.

Default should be local.

Examples of optional cloud services:

- OpenAI API
- ElevenLabs
- Azure TTS
- cloud storage

---

## 76. Model download policy

Large models should not be committed to Git.

Use `models/` for local storage if needed.

Add model binary patterns to `.gitignore` if necessary.

---

## 77. Media file policy

Do not commit large media files.

Use small examples only.

Large examples should be stored outside Git or via Git LFS if needed.

---

## 78. README expectations

README should include:

- what the project does
- current status
- quick start
- pipeline diagram
- supported platforms
- example commands
- roadmap
- development workflow

---

## 79. DecisionLog expectations

DecisionLog should record:

- date
- decision
- context
- alternatives considered
- reason
- impact
- follow-up

---

## 80. Sprint documentation

Each sprint should have:

- goal
- scope
- non-scope
- deliverables
- test plan
- completion checklist

---

## 81. Sprint 0

Sprint 0 is project bootstrap.

It includes:

- GitHub repository
- project structure
- documentation skeleton
- AGENTS.md
- rules
- roadmap
- CI skeleton

---

## 82. Sprint 0B

Sprint 0B is knowledge-base completion.

It includes:

- expanded README
- expanded AGENTS.md
- expanded rules
- architecture docs
- pipeline docs
- schema docs
- design docs

---

## 83. Sprint 1

Sprint 1 is Speech To Text.

It includes:

- audio extraction
- Faster Whisper integration
- transcript JSON export
- basic tests
- documentation update

---

## 84. Sprint 2

Sprint 2 is Timeline Analyzer.

It includes:

- clean transcript
- merge segments
- split long segments
- normalize scenes
- validate timing

---

## 85. Sprint 3

Sprint 3 is Visual Director.

It includes:

- LLM integration through Ollama
- prompt loading
- keyword selection
- emotion selection
- effect selection
- icon query suggestion

---

## 86. Sprint 4

Sprint 4 is Icon Selector.

It includes:

- icon metadata
- embedding model
- semantic search
- cache
- icon assignment

---

## 87. Sprint 5

Sprint 5 is Basic Renderer.

It includes:

- 1080x1920 output
- background
- large text
- keyword highlight
- simple animations
- silent video export

---

## 88. Sprint 6

Sprint 6 is Final Export.

It includes:

- merge original audio
- export MP4
- validate duration
- render report

---

## 89. Sprint 7

Sprint 7 is Speaker Support.

It includes:

- speaker color
- speaker avatar
- speaker label
- speaker mapping UI/config

---

## 90. Sprint 8

Sprint 8 is Template System.

It includes:

- template config
- multiple visual styles
- template inheritance
- safe zones

---

## 91. Coding style

Prefer clarity over cleverness.

Use readable names.

Avoid over-abstracting too early.

Keep functions short.

Keep modules focused.

---

## 92. Type hints

Use type hints for public functions.

Use dataclasses or Pydantic models where useful.

Avoid untyped dictionaries across module boundaries when schema matters.

---

## 93. Exceptions

Use custom exceptions for predictable domain errors.

Examples:

- `InvalidTimelineError`
- `MissingAssetError`
- `UnknownEffectError`
- `SpeechToTextError`
- `RenderError`

---

## 94. Path handling

Use `pathlib.Path`.

Avoid string path concatenation.

Support Windows paths.

Support spaces in file paths.

---

## 95. FFmpeg handling

Call FFmpeg through subprocess.

Validate FFmpeg exists before running.

Show clear error if FFmpeg is missing.

Do not assume FFmpeg path.

---

## 96. Model configuration

Model names should be configurable.

Do not hardcode `medium` or `qwen2.5:3b` deep inside logic.

Defaults may live in config.

---

## 97. Environment variables

Use environment variables for secrets and optional services.

Use `.env` locally.

Do not require `.env` for the core local workflow.

---

## 98. CI policy

CI should start simple.

Initial CI:

- install Python
- run import checks
- run unit tests

Later CI:

- format check
- lint
- type check
- package build

---

## 99. Formatting

Use Black or Ruff formatting later.

Do not mix formatting styles.

Keep documentation line lengths readable.

---

## 100. Linting

Linting should be introduced gradually.

Do not block early exploration with too many lint rules.

---

## 101. Human review

Before major changes, ask:

- Does this preserve AI/renderer separation?
- Does this keep JSON contract stable?
- Does this add unnecessary coupling?
- Does this make future templates easier?
- Does this make testing harder?

---

## 102. Agent behavior

When an AI agent works on this project, it should:

1. Read `AGENTS.md`.
2. Read related docs.
3. Inspect current code.
4. Make minimal focused changes.
5. Update docs if behavior changes.
6. Add tests when practical.
7. Use conventional commits.
8. Avoid unrelated refactors.

---

## 103. Agent must not

An agent must not:

- rewrite the entire project without request
- remove documentation casually
- introduce cloud dependencies silently
- hardcode local paths
- hardcode API keys
- bypass schema validation
- make renderer depend on LLM
- invent assets that do not exist
- commit large media files
- ignore Windows support

---

## 104. Prompt engineering principles

Prompts should be:

- explicit
- schema-driven
- short enough to maintain
- versioned
- tested with examples
- designed for JSON output

Prompts should include:

- role
- task
- input
- output schema
- constraints
- allowed values
- examples
- failure behavior

---

## 105. JSON repair

LLM output may be invalid.

A JSON repair step is allowed.

But the system must not blindly accept repaired output.

Validate after repair.

---

## 106. Confidence fields

Where useful, AI outputs may include confidence.

Example:

```json
{
  "speaker_confidence": 0.72,
  "keyword_confidence": 0.88
}
```

Low confidence should be handled gracefully.

---

## 107. Manual override

The system should allow manual correction.

Examples:

- edit transcript
- edit speaker mapping
- edit keywords
- edit icon choice
- edit animation
- edit timing

JSON should remain human-readable.

---

## 108. User editing

Eventually, the user should be able to modify timeline JSON manually.

The schema should be understandable.

Avoid deeply nested unnecessary structures.

---

## 109. Rendering strategy

Initial renderer can use Python libraries.

Possible tools:

- Pillow
- MoviePy
- FFmpeg
- OpenCV later

Start simple.

Optimize later.

---

## 110. Animation strategy

Start with simple animations.

Implement stable basics first:

- pop
- fade
- slide
- shake
- bounce

Avoid complex particle systems early.

---

## 111. Text rendering strategy

Text quality matters.

Use proper fonts.

Support Vietnamese accents.

Use stroke or shadow for readability.

Use high contrast.

Avoid tiny text.

---

## 112. Font policy

Fonts must come from assets or known system fonts.

Do not distribute licensed fonts without permission.

Do not assume the same fonts exist on every machine.

---

## 113. Color policy

Templates should define colors.

Renderer should not hardcode all colors.

Default dark style is acceptable for early version.

---

## 114. Background policy

Backgrounds may be:

- solid color
- gradient
- image
- animated pattern

Initial version may use solid dark background.

---

## 115. Avatar policy

Avatar support is optional early.

When added, avatar selection should be based on speaker and emotion.

Avatar files should be asset-managed.

---

## 116. SFX policy

SFX support is optional.

When added, SFX should align with animations.

Do not overuse SFX.

---

## 117. BGM policy

Background music is optional.

If used, volume ducking may be needed.

Never overpower original voice.

---

## 118. Audio sync policy

Audio sync is critical.

Rendered video duration should match original audio duration.

Final export should validate duration mismatch.

---

## 119. Scene boundaries

Scene boundaries should follow speech timing.

Avoid visual scene changes that feel late or early.

When in doubt, preserve STT timestamps.

---

## 120. Word-level timing

Word-level timing is optional initially.

Later it can support per-word animation.

Possible tools:

- WhisperX
- alignment models

---

## 121. Speaker diarization strategy

Initial version may not include full diarization.

For two-person dialogues, fallback can alternate speakers if configured.

But this must be marked as inferred.

---

## 122. Model strategy

The project uses multiple small specialized models rather than one large model.

Recommended roles:

- Faster Whisper for STT
- Qwen 2.5 3B for visual direction
- multilingual embedding model for icon search

---

## 123. Local-first rationale

Local-first is preferred because:

- lower cost
- privacy
- repeatability
- offline workflow
- easier batch processing

Cloud models may improve quality but should be optional.

---

## 124. Batch processing

Long-term, the engine should support batch generation.

Example:

```bash
ai-video build input_folder/ --template tiktok_dark
```

Batch mode should reuse cached models.

---

## 125. Project status labels

Use status terms consistently:

- experimental
- draft
- stable
- deprecated

Docs should mark unstable modules clearly.

---

## 126. Backward compatibility

Before v1.0, breaking changes are acceptable.

After v1.0, schema changes should be versioned.

---

## 127. Schema versioning

Timeline JSON should include schema version.

Example:

```json
{
  "schema_version": "0.1.0",
  "scenes": []
}
```

---

## 128. Render report

Render report should include:

- input file
- output file
- template
- scene count
- duration
- warnings
- errors
- renderer version

---

## 129. Debug mode

Debug mode should allow:

- show scene boxes
- show safe zones
- show timestamps
- show asset IDs
- export frame previews

---

## 130. Preview mode

Preview mode should render faster and lower quality.

Example:

- 540x960
- lower FPS
- shorter test range

---

## 131. Production render

Production render should use full resolution.

Example:

- 1080x1920
- 30 FPS
- H.264
- AAC

---

## 132. Configuration files

Possible config files:

```text
config/default.yaml
config/templates/tiktok_dark.yaml
config/models.yaml
```

Keep config human-readable.

---

## 133. CLI error messages

CLI should be friendly.

Bad:

```text
Exception: FileNotFound
```

Good:

```text
Input video not found: input/video.mp4
Please check the path and try again.
```

---

## 134. Documentation update trigger

Update docs when:

- pipeline changes
- schema changes
- module responsibility changes
- default model changes
- prompt behavior changes
- renderer behavior changes
- asset conventions change

---

## 135. Review checklist

Before committing, check:

- Does it run?
- Is it documented?
- Is it focused?
- Does it break JSON contract?
- Does renderer remain deterministic?
- Are there hardcoded local paths?
- Are large files avoided?
- Are tests added where practical?

---

## 136. Future UI

A GUI may be built later.

Possible forms:

- Streamlit
- desktop app
- web app
- VS Code extension

Do not design core engine around UI assumptions.

---

## 137. API future

An API may be built later.

Core engine should be importable as Python modules.

Avoid mixing CLI code with core logic.

---

## 138. Package strategy

The project may become an installable Python package.

Use `pyproject.toml`.

Keep source code package-friendly.

---

## 139. Current repository source of truth

The GitHub repository is the source of truth.

Chat history is not the source of truth.

Important decisions must be written into repository files.

---

## 140. How to continue in a new chat

When continuing in a new chat, say:

```text
Continue AI Video Engine. Read AGENTS.md and docs before coding.
Current sprint: Sprint 1 - Speech To Text.
```

Then provide the GitHub repository link.

---

## 141. How Codex should work

Codex should:

- open repository
- read AGENTS.md
- read docs
- inspect target module
- make small changes
- update tests
- update docs
- commit with clear message if requested

---

## 142. No hidden context dependency

The project must be understandable without this conversation.

Every important idea from the conversation should eventually be encoded in docs.

---

## 143. Final principle

When in doubt, prefer:

- explicit JSON over implicit behavior
- deterministic rendering over AI guessing
- small modules over giant scripts
- local processing over cloud dependency
- documentation over memory
- stable pipeline over flashy demo
