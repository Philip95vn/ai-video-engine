# PROJECT_RULES.md

# AI Video Engine - Project Rules

## 0. Purpose

This document defines the mandatory rules for the AI Video Engine project.

These rules are stricter than normal documentation.

They are intended to protect the architecture from becoming messy as the project grows.

Every human contributor and AI coding agent must follow this document.

If there is a conflict between a quick implementation and this document, this document wins.

---

## 1. Project identity

### Rule 1.1 - The project is an engine, not a script

AI Video Engine must be treated as a reusable engine.

It must not be developed as a pile of one-off scripts.

One-off scripts are allowed only under `scripts/` or `examples/`.

Core behavior must live under `src/`.

### Rule 1.2 - The project is local-first

The default workflow must run locally.

Cloud services may be added only as optional integrations.

### Rule 1.3 - The project targets short-form video first

The first target format is vertical 9:16 video.

Default resolution:

```text
1080 x 1920
```

Default FPS:

```text
30
```

Default export:

```text
MP4 / H.264 / AAC
```

### Rule 1.4 - The project must remain template-driven

Visual styles must be controlled by templates.

The engine must not be locked to one TikTok style.

---

## 2. Absolute architecture rules

### Rule 2.1 - AI must not render video

AI must never directly render video frames.

AI must never be responsible for final pixels.

AI must never generate the final MP4.

### Rule 2.2 - AI generates instructions only

AI may generate:

- timeline JSON
- keywords
- emotion labels
- layout suggestions
- icon queries
- animation suggestions
- speaker mood
- template suggestions

AI may not generate:

- final video files
- rendered frames
- binary assets
- FFmpeg commands that bypass the renderer

### Rule 2.3 - Renderer must be deterministic

Given the same:

- timeline JSON
- config
- assets
- fonts
- template
- renderer version

the renderer should produce the same result.

### Rule 2.4 - Renderer must not call LLMs

Renderer code must never call:

- Ollama
- OpenAI API
- Gemini API
- Claude API
- any LLM endpoint
- any prompt runner

The renderer consumes JSON only.

### Rule 2.5 - JSON is the contract

All AI-to-renderer communication must happen through structured JSON.

Natural language must not be passed directly to the renderer as instruction.

### Rule 2.6 - Module boundaries must be respected

Speech modules do speech.

Timeline modules normalize timeline.

Director modules use AI.

Renderer modules render.

Exporter modules export.

Do not mix responsibilities.

---

## 3. Repository rules

### Rule 3.1 - Repository is the source of truth

Chat history is not the source of truth.

Important ideas must be written into repository files.

### Rule 3.2 - Required root files

The repository should contain:

```text
README.md
AGENTS.md
PROJECT_RULES.md
ROADMAP.md
CHANGELOG.md
LICENSE
pyproject.toml
requirements.txt
.gitignore
```

### Rule 3.3 - Required docs

The repository should contain:

```text
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
docs/Glossary.md
```

### Rule 3.4 - Do not commit generated output

Do not commit files in:

```text
output/
temp/
```

unless they are tiny fixtures intentionally placed under `examples/` or `tests/fixtures/`.

### Rule 3.5 - Do not commit large models

Do not commit model files.

Do not commit downloaded LLMs.

Do not commit Whisper model binaries.

Do not commit embedding model binaries.

### Rule 3.6 - Do not commit secrets

Do not commit:

- API keys
- tokens
- passwords
- `.env`
- private media
- personal credentials

---

## 4. Folder structure rules

### Rule 4.1 - Source code must live under `src/`

All reusable engine code must live under:

```text
src/
```

### Rule 4.2 - Audio code lives in `src/audio/`

Audio extraction, audio conversion, and audio preparation live here.

### Rule 4.3 - Speech-to-text code lives in `src/speech/`

Whisper and future STT providers live here.

### Rule 4.4 - Timeline code lives in `src/timeline/`

Transcript cleanup, segment merging, scene splitting, and timeline validation live here.

### Rule 4.5 - AI director code lives in `src/director/`

LLM-based visual direction lives here.

### Rule 4.6 - Embedding code lives in `src/embedding/`

Icon search and semantic asset matching live here.

### Rule 4.7 - Renderer code lives in `src/renderer/`

Frame generation, text drawing, animations, layouts, icons, backgrounds, avatars, and visual composition live here.

### Rule 4.8 - Export code lives in `src/exporter/`

Final MP4 export and audio/video merge live here.

### Rule 4.9 - Shared utilities live in `src/common/`

Only generic helpers belong here.

Do not dump business logic into common.

### Rule 4.10 - Config loading lives in `src/config/`

Configuration parsing and defaults live here.

---

## 5. Pipeline rules

### Rule 5.1 - Pipeline stages must be explicit

The default pipeline is:

```text
input video/audio
→ extract audio
→ speech to text
→ transcript JSON
→ timeline analyzer
→ visual director
→ icon selector
→ final timeline JSON
→ renderer
→ exporter
→ final MP4
```

### Rule 5.2 - Each stage must have clear input and output

A stage should not depend on hidden global state.

### Rule 5.3 - Intermediate outputs should be saved

Important intermediate files should be saved for debugging:

```text
output/transcript.json
output/timeline.normalized.json
output/timeline.visual.json
output/render_report.json
```

### Rule 5.4 - Stages should be individually runnable

Eventually, each major stage should be callable independently.

Example:

```bash
ai-video transcribe input/video.mp4
ai-video analyze output/transcript.json
ai-video render output/timeline.visual.json
```

### Rule 5.5 - Stage boundaries require validation

Validate data after each major stage.

---

## 6. Audio rules

### Rule 6.1 - FFmpeg is the default audio/video tool

Use FFmpeg for:

- extracting audio
- converting audio
- merging audio and video
- final export when appropriate

### Rule 6.2 - Audio extraction must preserve original audio

The original audio should be preserved for final merge.

### Rule 6.3 - STT audio should be normalized

Speech-to-text input should generally be:

```text
mono
16000 Hz
WAV
```

unless a model requires otherwise.

### Rule 6.4 - Audio paths must use `pathlib.Path`

Do not concatenate paths manually with strings.

### Rule 6.5 - Missing FFmpeg must produce a clear error

If FFmpeg is unavailable, the error must explain how to install or configure it.

### Rule 6.6 - Do not overwrite source media

Never overwrite the original input video.

---

## 7. Speech-to-text rules

### Rule 7.1 - Faster Whisper is the first STT implementation

The first STT module should use Faster Whisper.

### Rule 7.2 - Vietnamese must be supported

Vietnamese transcription is a first-class requirement.

### Rule 7.3 - Model name must be configurable

Do not hardcode the Whisper model deep inside logic.

Accept model names such as:

```text
small
medium
large-v3
```

### Rule 7.4 - Device must be configurable

The STT module should allow CPU usage.

GPU must not be required.

### Rule 7.5 - Transcript must include timestamps

Every transcript segment must include:

```text
start
end
text
```

### Rule 7.6 - Transcript must be exportable to JSON

The output must be machine-readable and human-readable.

### Rule 7.7 - STT confidence should be supported when available

If confidence values are available, preserve them.

If not available, do not invent them.

### Rule 7.8 - Do not use STT output as final visual script

STT output is raw material.

Timeline analyzer and visual director must enrich it later.

---

## 8. Speaker rules

### Rule 8.1 - Speaker information may be uncertain

Early versions may not have accurate diarization.

If speaker is inferred, mark it as inferred.

### Rule 8.2 - Default speaker names should be neutral

Use:

```text
SPEAKER_00
SPEAKER_01
```

before manual mapping.

### Rule 8.3 - Do not assume gender from voice without explicit configuration

Gender inference can be wrong.

Speaker labels should be editable.

### Rule 8.4 - Speaker mapping should be configurable

Users should be able to map:

```text
SPEAKER_00 → Nam
SPEAKER_01 → Nữ
```

### Rule 8.5 - Speaker color should come from template

Do not hardcode speaker colors inside timeline logic.

---

## 9. Timeline rules

### Rule 9.1 - Every scene must have an ID

Example:

```text
scene_0001
```

### Rule 9.2 - Every scene must have timing

Required:

```text
start
end
duration
```

### Rule 9.3 - Duration must be valid

`duration` must equal:

```text
end - start
```

Duration must be positive.

### Rule 9.4 - Timeline must preserve chronological order

Scenes must be sorted by start time.

### Rule 9.5 - Timeline should not overlap unless explicitly allowed

Overlapping scenes should fail validation unless the schema supports overlays.

### Rule 9.6 - Scene text should be short enough for video

A visual scene should normally contain one or two sentences.

### Rule 9.7 - Long transcript segments should be split

If STT returns a long segment, timeline analyzer should split it.

### Rule 9.8 - Very short segments may be merged

If segments are too short to render meaningfully, merge them when appropriate.

### Rule 9.9 - Timeline analyzer must be deterministic

Timeline analyzer should not require LLM calls.

### Rule 9.10 - Timeline schema must be versioned

Timeline JSON should include:

```json
{
  "schema_version": "0.1.0"
}
```

---

## 10. Visual Director rules

### Rule 10.1 - Visual Director is allowed to use LLM

This is the main LLM-powered module.

### Rule 10.2 - Visual Director must return JSON

No markdown.

No prose explanations.

No comments.

### Rule 10.3 - Visual Director must preserve timing

It must not randomly change `start` and `end`.

### Rule 10.4 - Visual Director may suggest lines

It may convert text into large display lines.

Example:

```json
"lines": ["Ê!", "SAO HÔM NAY", "ĐẾN TRỄ?"]
```

### Rule 10.5 - Visual Director may choose keywords

Keywords should be important, funny, emotional, or visually meaningful.

### Rule 10.6 - Visual Director may choose emotion

Allowed emotions should come from a controlled list.

Example:

```text
neutral
happy
surprised
confused
angry
funny
sad
serious
```

### Rule 10.7 - Visual Director may choose effects

Effects must come from the effect registry.

### Rule 10.8 - Visual Director must not invent asset filenames

It should return icon queries, not exact filenames, unless the asset list is provided.

### Rule 10.9 - Visual Director output must be validated

Never trust raw LLM output.

### Rule 10.10 - Invalid LLM JSON must be repaired or rejected

Do not silently continue with invalid JSON.

---

## 11. Keyword rules

### Rule 11.1 - Keywords are emphasis targets

They are not plain subtitles.

### Rule 11.2 - Keywords should map to text

By default, a keyword should appear in the scene text.

### Rule 11.3 - Conceptual keywords must be marked

If a keyword is conceptual and not literal, mark it clearly.

### Rule 11.4 - Each keyword should have an effect

Example:

```json
{
  "text": "ĐẾN TRỄ",
  "effect": "pop"
}
```

### Rule 11.5 - Too many keywords should be avoided

Usually one to three keywords per scene is enough.

### Rule 11.6 - Keyword style should be template-controlled

Color, glow, stroke, and size should come from template defaults unless overridden.

---

## 12. Animation rules

### Rule 12.1 - All effects must be registered

Allowed effects should live in an effect registry.

### Rule 12.2 - Unknown effect must fail validation

Do not ignore unknown effects.

### Rule 12.3 - Effects should have clear semantics

Examples:

```text
pop      surprise or punchline
shake    chaos or anger
bounce   humor
glow     importance
slide    transition
fade     soft entrance
pulse    emphasis
```

### Rule 12.4 - Effects must be reproducible

If randomness is used, use a seed.

### Rule 12.5 - Effects should not make text unreadable

Animation must support readability.

### Rule 12.6 - Effects should respect scene duration

Do not create animations longer than the scene unless intentionally supported.

### Rule 12.7 - Per-word animation is optional early

Start with phrase-level animation.

Word-level animation can come later.

---

## 13. Renderer rules

### Rule 13.1 - Renderer consumes final timeline JSON

Renderer should not consume raw transcript directly.

### Rule 13.2 - Renderer must validate before rendering

Invalid timeline should fail before generating frames.

### Rule 13.3 - Renderer must support 9:16 default output

Default canvas:

```text
1080 x 1920
```

### Rule 13.4 - Renderer must support high-contrast text

Readable text is mandatory.

### Rule 13.5 - Renderer must support Vietnamese text

Fonts must handle Vietnamese accents.

### Rule 13.6 - Renderer should use safe zones

Avoid placing important text too close to edges.

### Rule 13.7 - Renderer must not assume one visual style

Styles belong in templates.

### Rule 13.8 - Renderer should generate silent video first

Audio merge should happen in exporter.

### Rule 13.9 - Renderer should produce debug previews eventually

Debug mode may show safe zones, bounding boxes, and scene IDs.

### Rule 13.10 - Renderer must not mutate input timeline unexpectedly

If renderer needs derived data, create render state separately.

---

## 14. Layout rules

### Rule 14.1 - Layouts should be named

Examples:

```text
center_stack
speaker_left_text_right
comic_panel
punchline_center
split_dialogue
```

### Rule 14.2 - Layouts should be registered

Renderer should know available layouts.

### Rule 14.3 - Unknown layout should fail validation or fallback explicitly

Do not silently choose random layout.

### Rule 14.4 - Layouts must consider mobile readability

Large text and safe zones matter more than decorative complexity.

### Rule 14.5 - Layout defaults should come from template

Not from hardcoded renderer values.

---

## 15. Template rules

### Rule 15.1 - Templates define visual style

Templates may define:

- resolution
- fps
- background
- font
- colors
- safe zones
- layout defaults
- animation defaults
- icon style
- avatar style

### Rule 15.2 - Templates should be data files

Prefer YAML/JSON/TOML over hardcoded styles.

### Rule 15.3 - Templates should be versioned

Template changes can affect output significantly.

### Rule 15.4 - Template names should be clear

Examples:

```text
tiktok_dark_comic
neon_dialogue
minimal_black
recruitment_clean
education_bold
```

### Rule 15.5 - Default template must exist

The engine should have a default working template.

---

## 16. Asset rules

### Rule 16.1 - Assets live under `assets/`

Expected folders:

```text
assets/icons/
assets/avatars/
assets/backgrounds/
assets/fonts/
assets/sfx/
assets/templates/
```

### Rule 16.2 - Assets should have metadata

Icon metadata is required for semantic search.

### Rule 16.3 - Do not hardcode absolute asset paths

Use relative paths or asset IDs.

### Rule 16.4 - Missing assets must be handled clearly

Fail or fallback with explicit warning.

### Rule 16.5 - Font licensing must be respected

Do not redistribute proprietary fonts without permission.

### Rule 16.6 - Asset filenames should be stable

Changing filenames can break timeline references.

### Rule 16.7 - Asset IDs are preferred over filenames

Long-term, timeline should refer to asset IDs.

---

## 17. Icon selection rules

### Rule 17.1 - LLM returns icon query

Example:

```json
"icon_query": "báo thức"
```

### Rule 17.2 - Embedding module maps query to icon

Do not expect LLM to know actual icon filenames.

### Rule 17.3 - Icon metadata should include Vietnamese tags

Example:

```json
{
  "id": "icon_alarm_001",
  "tags": ["báo thức", "đồng hồ", "trễ giờ"]
}
```

### Rule 17.4 - Icon match confidence should be stored when possible

Low confidence can allow fallback or manual review.

### Rule 17.5 - Icon selector must be deterministic given same model and database

Avoid random icon choice unless seeded.

---

## 18. Prompt rules

### Rule 18.1 - Prompts live in `prompts/`

Do not embed large prompts directly inside Python code.

### Rule 18.2 - Prompts must specify output schema

The model must know exactly what JSON to return.

### Rule 18.3 - Prompts must specify allowed values

For fields like emotion, effect, layout, and transition.

### Rule 18.4 - Prompts must say "no markdown"

LLM output should be raw JSON.

### Rule 18.5 - Prompts should include examples

Examples improve consistency.

### Rule 18.6 - Prompt changes must be documented

Update `docs/PromptGuide.md` when changing prompt behavior.

### Rule 18.7 - Prompts should be versioned

At minimum, keep prompt filenames stable and document changes.

---

## 19. JSON schema rules

### Rule 19.1 - Schema must be documented

The schema must be explained in `docs/JSONSchema.md`.

### Rule 19.2 - Schema must be validated in code

Use Pydantic or JSON Schema.

### Rule 19.3 - Unknown fields should be handled intentionally

Either allow extras explicitly or reject them.

### Rule 19.4 - Required fields must be clear

Renderer should not guess missing required fields.

### Rule 19.5 - Schema version must be present

Include:

```json
"schema_version": "0.1.0"
```

### Rule 19.6 - Breaking schema changes must be documented

Update `DecisionLog.md`.

---

## 20. Export rules

### Rule 20.1 - Exporter merges original audio by default

For input videos with voice, preserve original voice.

### Rule 20.2 - Exporter must validate duration

Final video duration should match audio duration closely.

### Rule 20.3 - Exporter must write final MP4

Default output:

```text
output/final.mp4
```

### Rule 20.4 - Exporter should write report

Default report:

```text
output/render_report.json
```

### Rule 20.5 - Exporter should not re-render visuals

Exporter handles final packaging, not visual composition.

---

## 21. Configuration rules

### Rule 21.1 - Config must be centralized

Avoid scattered constants.

### Rule 21.2 - Defaults must be documented

Default resolution, FPS, model names, and paths should be documented.

### Rule 21.3 - Config must support local development

A new user should be able to run the project with default config.

### Rule 21.4 - Config should be human-readable

Prefer YAML, TOML, or JSON.

### Rule 21.5 - Environment variables are for secrets and environment-specific values

Do not use environment variables for every normal setting.

---

## 22. CLI rules

### Rule 22.1 - CLI should be friendly

Error messages should help the user fix problems.

### Rule 22.2 - CLI should expose pipeline stages

Possible commands:

```text
extract-audio
transcribe
analyze
direct
render
export
build
```

### Rule 22.3 - CLI should support default paths

A beginner should not need to pass many flags.

### Rule 22.4 - CLI should support explicit paths

Advanced users should be able to control input/output.

---

## 23. Coding rules

### Rule 23.1 - Use Python 3.11+

Python 3.11 is the preferred baseline.

### Rule 23.2 - Use type hints for public functions

Type hints help Codex, IDEs, and human maintainers.

### Rule 23.3 - Prefer small focused modules

Avoid giant files.

### Rule 23.4 - Prefer clear names

Readable code beats clever code.

### Rule 23.5 - Avoid hidden global state

Pass config explicitly where practical.

### Rule 23.6 - Use `pathlib.Path`

Do not manually concatenate file paths.

### Rule 23.7 - Avoid broad `except Exception` unless re-raising with context

Do not hide errors.

### Rule 23.8 - Keep business logic out of CLI wrappers

CLI should call core functions.

### Rule 23.9 - Avoid circular imports

Module boundaries should be clean.

### Rule 23.10 - Do not over-engineer early

Build stable basics before complex abstractions.

---

## 24. Testing rules

### Rule 24.1 - Unit tests should not require large AI models

Mock model outputs where possible.

### Rule 24.2 - Unit tests should be fast

Fast tests encourage frequent testing.

### Rule 24.3 - Unit tests should not require internet

Local-only by default.

### Rule 24.4 - Integration tests may be slower

Mark them clearly.

### Rule 24.5 - Use small fixtures

Do not commit large videos for tests.

### Rule 24.6 - Test schema validation

Invalid timelines should fail.

### Rule 24.7 - Test renderer smoke path

At minimum, ensure renderer can create a tiny output from a tiny valid timeline.

### Rule 24.8 - Test FFmpeg command generation when possible

Avoid requiring full media processing in every unit test.

---

## 25. Documentation rules

### Rule 25.1 - Docs must not be empty placeholders

If a documentation file exists, it should contain useful content.

### Rule 25.2 - Update docs when architecture changes

Architecture changes without docs are incomplete.

### Rule 25.3 - DecisionLog is mandatory for major decisions

Use DecisionLog for:

- model choice
- renderer choice
- schema change
- dependency change
- pipeline change
- cloud/local decision

### Rule 25.4 - Docs should be beginner-friendly

The user may be new to Git, Python packaging, or AI tooling.

### Rule 25.5 - Docs should also support AI agents

Be explicit so Codex can follow instructions.

---

## 26. Git rules

### Rule 26.1 - Use meaningful commits

Avoid commit messages like:

```text
update
fix stuff
final
test
```

### Rule 26.2 - Use conventional commits

Examples:

```text
docs: expand project rules
feat: add audio extractor
fix: validate missing ffmpeg
test: add timeline validator tests
```

### Rule 26.3 - One logical change per commit

Do not mix unrelated changes.

### Rule 26.4 - Pull before major work

Avoid conflicts.

### Rule 26.5 - Push after meaningful milestones

GitHub is the long-term memory of the project.

### Rule 26.6 - Do not commit broken main intentionally

Keep main usable.

---

## 27. Branch rules

### Rule 27.1 - Early solo development may use main

Direct commits are acceptable during early bootstrap.

### Rule 27.2 - Later work should use branches

Example branches:

```text
feat/speech-to-text
feat/visual-director
docs/sprint0b
```

### Rule 27.3 - Branch names should describe intent

Avoid vague branch names.

---

## 28. CI rules

### Rule 28.1 - CI starts simple

Initial CI may only check Python setup.

### Rule 28.2 - CI should later run tests

Add pytest when tests exist.

### Rule 28.3 - CI should not download huge models by default

Model-dependent tests should be optional.

### Rule 28.4 - CI should protect main later

When project matures, require passing CI before merge.

---

## 29. Dependency rules

### Rule 29.1 - Dependencies must be intentional

Do not add packages casually.

### Rule 29.2 - Prefer stable widely used packages

Especially for core pipeline.

### Rule 29.3 - Large AI dependencies should be optional where possible

WhisperX, pyannote, and torch-heavy dependencies should not block basic workflow.

### Rule 29.4 - Update requirements when adding dependencies

`requirements.txt` and `pyproject.toml` should stay consistent.

### Rule 29.5 - Pin only when necessary

Use version ranges carefully.

---

## 30. Platform rules

### Rule 30.1 - Windows support is required

Commands and path handling must support Windows.

### Rule 30.2 - Mac M1 support is required

The project should work without NVIDIA GPU.

### Rule 30.3 - Linux support is desirable

But Windows and Mac are more important initially for the user.

### Rule 30.4 - GPU must be optional

Do not require CUDA.

---

## 31. Performance rules

### Rule 31.1 - Avoid unnecessary LLM calls

LLM calls are expensive and slow.

### Rule 31.2 - Cache repeated AI outputs

Cache where practical.

### Rule 31.3 - Load models once per batch

Do not reload Whisper or embedding models repeatedly.

### Rule 31.4 - Prefer simple rendering first

A reliable basic renderer is better than a slow complex renderer.

### Rule 31.5 - Measure before optimizing

Do not guess performance bottlenecks.

---

## 32. Security rules

### Rule 32.1 - Do not expose secrets

No API keys in code, docs, or logs.

### Rule 32.2 - Validate file paths

Avoid accidentally overwriting important files.

### Rule 32.3 - Be careful with subprocess

Use argument lists instead of shell strings.

### Rule 32.4 - Do not execute untrusted code from AI output

LLM output is data, not code.

---

## 33. Privacy rules

### Rule 33.1 - Treat input videos as private

Do not upload media to cloud services unless configured by user.

### Rule 33.2 - Local processing is default

Especially for voice and video.

### Rule 33.3 - Logs should avoid sensitive transcript exposure when possible

Debug mode may show more detail, but normal logs should be reasonable.

---

## 34. Error handling rules

### Rule 34.1 - Fail clearly

Bad error messages slow development.

### Rule 34.2 - Validate early

Catch invalid inputs before expensive processing.

### Rule 34.3 - Use domain-specific errors when useful

Examples:

```text
MissingFFmpegError
InvalidTimelineError
UnknownEffectError
MissingAssetError
ModelLoadError
RenderError
```

### Rule 34.4 - Do not silently ignore failures

If an icon is missing, log or fail based on config.

---

## 35. Logging rules

### Rule 35.1 - Logs should show pipeline progress

Example:

```text
Extracting audio...
Transcribing...
Normalizing timeline...
Rendering...
Exporting...
```

### Rule 35.2 - Logs should include durations

Useful for optimization.

### Rule 35.3 - Logs should be readable

Use `rich` or clear plain text.

### Rule 35.4 - Logs should not be noisy by default

Verbose logs should be optional.

---

## 36. Report rules

### Rule 36.1 - Generate report files eventually

Reports help debugging and reproducibility.

### Rule 36.2 - Render report should include warnings

Warnings are important when output is usable but imperfect.

### Rule 36.3 - Report should include version info

Include engine version, schema version, and template version.

---

## 37. Model rules

### Rule 37.1 - Ollama is the first local LLM runtime

Initial local LLM should use Ollama.

### Rule 37.2 - Qwen 2.5 3B is the first recommended director model

It is light enough for local use and good at structured JSON.

### Rule 37.3 - Model can be replaced

The architecture must not depend on Qwen-specific behavior.

### Rule 37.4 - Model output must be validated

Never trust LLM output directly.

### Rule 37.5 - LLM prompts should be tested with examples

Prompt reliability matters.

---

## 38. Embedding rules

### Rule 38.1 - Embedding model is for asset search

Do not use LLM for exact icon selection when embedding search is better.

### Rule 38.2 - Icon embeddings should be cached

Avoid recomputing for every run.

### Rule 38.3 - Embedding database should be rebuildable

Given asset metadata, the index can be regenerated.

### Rule 38.4 - Multilingual support matters

Vietnamese tags should work.

---

## 39. Version rules

### Rule 39.1 - Use semantic versioning later

Before v1.0, changes may be frequent.

After v1.0, schema stability matters.

### Rule 39.2 - Schema version and engine version are different

Do not confuse them.

### Rule 39.3 - Changelog should track user-visible changes

Technical docs can be more detailed.

---

## 40. Sprint rules

### Rule 40.1 - Sprint 0 is bootstrap

Already includes repository and structure.

### Rule 40.2 - Sprint 0B is documentation completion

No major code until docs are useful.

### Rule 40.3 - Sprint 1 is Speech To Text

Goal:

```text
video.mp4 → transcript.json
```

### Rule 40.4 - Sprint 2 is Timeline Analyzer

Goal:

```text
transcript.json → normalized timeline
```

### Rule 40.5 - Sprint 3 is Visual Director

Goal:

```text
normalized timeline → visual timeline
```

### Rule 40.6 - Sprint 4 is Icon Selector

Goal:

```text
icon_query → actual icon asset
```

### Rule 40.7 - Sprint 5 is Renderer

Goal:

```text
visual timeline → silent video
```

### Rule 40.8 - Sprint 6 is Exporter

Goal:

```text
silent video + original audio → final.mp4
```

---

## 41. Beginner-friendly workflow rules

### Rule 41.1 - Instructions should be step-by-step

The primary user is still learning Git and project structure.

### Rule 41.2 - Do not give ten commands when one is enough

When guiding the user interactively, one step at a time is preferred.

### Rule 41.3 - If an error appears, stop and fix it

Do not continue installing other parts.

### Rule 41.4 - Prefer concrete commands

Avoid vague instructions.

---

## 42. AI agent response rules

### Rule 42.1 - Keep explanations concise when the user asks

The user explicitly prefers less explanation during setup.

### Rule 42.2 - Provide files directly when requested

If the user asks for files, create files.

### Rule 42.3 - Do not overpromise file completeness

If a file is a draft, say it is a draft.

If a file is production-level, make it substantial.

### Rule 42.4 - Do not rely on hidden conversation context

Write important context into project files.

---

## 43. Quality bar

### Rule 43.1 - Avoid demo-only architecture

Even early versions should not block future growth.

### Rule 43.2 - Prefer reliable boring technology

FFmpeg, Pillow, MoviePy, Faster Whisper, Pydantic, and JSON are acceptable.

### Rule 43.3 - Keep the first version simple

Complex animation engine can come later.

### Rule 43.4 - Build vertical slices

Each sprint should produce a usable slice.

---

## 44. Review questions

Before accepting a change, ask:

1. Does this keep AI separate from renderer?
2. Does this preserve JSON as contract?
3. Does this support local-first workflow?
4. Does this avoid hardcoded machine-specific paths?
5. Does this keep Windows support?
6. Does this keep future templates possible?
7. Is it documented?
8. Is it testable?
9. Is it too broad for one commit?
10. Would Codex understand this later?

---

## 45. Final rule

If a shortcut makes the demo faster but damages the engine architecture, do not take it.

Build the engine correctly.
