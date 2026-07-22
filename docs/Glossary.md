# Glossary.md

# AI Video Engine - Glossary

## 0. Purpose

This glossary defines the terms used across **AI Video Engine**.

It is intended for:

- human contributors
- ChatGPT
- Codex in VS Code
- GitHub Copilot
- future maintainers
- future UI/API developers

The goal is to keep language consistent across:

```text
README.md
AGENTS.md
PROJECT_RULES.md
ROADMAP.md
docs/
src/
prompts/
schemas/
tests/
```

If a term is used in code, prompts, JSON schema, or documentation, it should have a consistent meaning.

---

## 1. Core project terms

### 1.1 AI Video Engine

The project itself.

A local-first, modular video automation engine that uses AI to generate structured JSON instructions and uses a deterministic renderer to create videos.

AI Video Engine is not a single script.

It is an engine made of modules.

---

### 1.2 Engine

A reusable system that can process inputs and generate outputs through defined stages.

In this project, the engine includes:

- audio extraction
- speech-to-text
- timeline analysis
- AI visual direction
- asset selection
- rendering
- exporting

---

### 1.3 Local-first

A design principle meaning the default workflow runs on the user's machine.

Local-first does not mean cloud services are forbidden.

It means cloud services are optional and explicit.

Default processing should not upload private video/audio to external services.

---

### 1.4 Deterministic

Predictable and repeatable.

A deterministic renderer should produce the same output when given the same:

- timeline JSON
- template
- assets
- renderer version
- config
- random seed

AI models may be non-deterministic.

Renderer should not be.

---

### 1.5 JSON-first

A design principle meaning structured JSON files are the main contracts between pipeline stages.

Important JSON files:

```text
transcript.json
timeline.normalized.json
timeline.director.json
timeline.visual.json
render_report.json
```

---

### 1.6 Source of truth

The authoritative place where project information lives.

For this project:

```text
GitHub repository is the source of truth.
```

Chat history is not the source of truth.

Important decisions must be written into repository files.

---

## 2. Pipeline terms

### 2.1 Pipeline

The ordered sequence of stages that turns input media into final video.

Default pipeline:

```text
input media
→ extract audio
→ speech-to-text
→ transcript JSON
→ timeline analyzer
→ visual director
→ icon selector
→ visual timeline JSON
→ renderer
→ exporter
→ final MP4
```

---

### 2.2 Stage

One step in the pipeline.

Examples:

- audio extraction
- speech-to-text
- timeline analysis
- visual direction
- icon selection
- rendering
- exporting

Each stage should have clear input and output.

---

### 2.3 Input media

The user-provided media file.

Examples:

```text
input/video.mp4
input/audio.wav
input/audio.mp3
```

In the first workflow, input media is usually a video with original voice.

---

### 2.4 Output

Generated files created by the engine.

Examples:

```text
output/transcript.json
output/timeline.visual.json
output/silent_video.mp4
output/final.mp4
```

Generated outputs should usually not be committed to Git.

---

### 2.5 Intermediate output

A file produced by one stage and consumed by another.

Examples:

```text
temp/audio.wav
output/transcript.json
output/timeline.normalized.json
```

Intermediate outputs are useful for debugging and manual editing.

---

### 2.6 Final output

The final rendered video.

Default:

```text
output/final.mp4
```

---

### 2.7 Run

One execution of the pipeline.

A run may produce:

```text
transcript.json
timeline.normalized.json
timeline.visual.json
final.mp4
render_report.json
```

---

### 2.8 Run ID

A unique identifier for one pipeline run.

Example:

```text
run_20260707_001
```

Useful for reports and batch processing.

---

### 2.9 Cache

Stored output from an expensive stage that can be reused.

Examples:

- transcript cache
- LLM response cache
- embedding cache
- rendered preview cache

Cache should be explicit and logged.

---

### 2.10 Validation checkpoint

A point in the pipeline where data is checked before continuing.

Examples:

- validate transcript after STT
- validate visual timeline before render
- validate output video after export

---

## 3. Audio terms

### 3.1 Audio extractor

The module that extracts audio from input media.

Location:

```text
src/audio/
```

It uses FFmpeg.

---

### 3.2 Source audio

The original or extracted audio used for speech-to-text and final merge.

Example:

```text
temp/audio.wav
```

---

### 3.3 Original audio

The voice/audio from the input video.

For existing-video workflow, original audio is preserved in final output.

---

### 3.4 Audio extraction

The process of turning a video file into an audio file.

Example FFmpeg command:

```bash
ffmpeg -y -i input/video.mp4 -vn -ac 1 -ar 16000 temp/audio.wav
```

---

### 3.5 Sample rate

Number of audio samples per second.

For STT, recommended:

```text
16000 Hz
```

---

### 3.6 Mono

Single-channel audio.

For STT, mono is usually enough.

---

### 3.7 WAV

Audio file format often used for speech-to-text.

Sprint 1 output:

```text
temp/audio.wav
```

---

### 3.8 Audio stream

The audio component inside a video file.

A video can have:

- video stream
- audio stream
- subtitle stream
- metadata stream

If input video has no audio stream, STT cannot run.

---

### 3.9 Audio sync

The alignment between audio and rendered visuals.

Audio sync is critical for final video quality.

---

### 3.10 Audio merge

Combining silent rendered video with audio.

Handled by exporter.

---

## 4. Speech-to-text terms

### 4.1 STT

Speech-to-text.

The process of converting spoken audio into written text.

---

### 4.2 Speech module

The module responsible for STT.

Location:

```text
src/speech/
```

---

### 4.3 Faster Whisper

The first planned STT implementation.

Used in Sprint 1.

It transcribes audio locally and outputs timestamped segments.

---

### 4.4 Whisper

A speech recognition model family.

Faster Whisper is an optimized implementation of Whisper.

---

### 4.5 WhisperX

A future optional tool for better alignment, word-level timing, and diarization.

Not required in Sprint 1.

---

### 4.6 Transcript

The written output from speech-to-text.

In this project, transcript is stored as JSON.

File:

```text
output/transcript.json
```

---

### 4.7 Transcript segment

One timestamped unit of transcript.

Example:

```json
{
  "id": "seg_0001",
  "start": 0.25,
  "end": 2.16,
  "duration": 1.91,
  "text": "Ê! Sao hôm nay đến trễ?"
}
```

---

### 4.8 Segment ID

Stable ID for a transcript segment.

Example:

```text
seg_0001
```

---

### 4.9 Segment timestamp

Start and end time of a transcript segment.

Measured in seconds.

---

### 4.10 Word-level timing

Timing for each word.

Example:

```json
{
  "text": "TRỄ",
  "start": 1.31,
  "end": 1.55
}
```

Not required in early V1.

---

### 4.11 Language code

Code identifying the spoken language.

Vietnamese:

```text
vi
```

English:

```text
en
```

---

### 4.12 VAD

Voice Activity Detection.

Used to identify speech regions in audio.

Faster Whisper can use:

```text
vad_filter=True
```

---

### 4.13 Beam size

A decoding parameter for speech recognition.

Common value:

```text
5
```

---

### 4.14 Compute type

Model computation precision.

For CPU-friendly mode:

```text
int8
```

---

### 4.15 STT provider

A service or model used for speech-to-text.

Examples:

- Faster Whisper
- WhisperX
- cloud STT provider later

---

## 5. Speaker terms

### 5.1 Speaker

A person or character speaking in the audio.

---

### 5.2 Speaker ID

Internal identifier for a speaker.

Examples:

```text
SPEAKER_00
SPEAKER_01
```

---

### 5.3 Speaker label

Human-friendly label.

Examples:

```text
Nam
Nữ
Host
Guest
Speaker A
Speaker B
```

---

### 5.4 Speaker mapping

Mapping from internal speaker ID to label/style.

Example:

```yaml
SPEAKER_00:
  label: Nam
  style: speaker_a
```

---

### 5.5 Diarization

The process of identifying who spoke when.

Future optional feature.

---

### 5.6 Speaker source

Where speaker information came from.

Examples:

```text
unknown
manual
diarization
inferred
inferred_alternating
script
```

---

### 5.7 Speaker style

Template-defined style for a speaker.

Example:

```text
speaker_a
speaker_b
```

May control:

- label color
- avatar
- text accent
- layout position

---

### 5.8 Manual speaker override

User-provided correction for speaker labels.

Useful when diarization is unavailable or wrong.

---

### 5.9 Alternating speaker inference

A simple fallback where speakers alternate by scene.

This is only a heuristic.

It must be marked as inferred.

---

### 5.10 Speaker confidence

A number from 0 to 1 indicating confidence in speaker assignment.

Optional.

---

## 6. Timeline terms

### 6.1 Timeline

Structured representation of scenes over time.

In this project, timeline is stored as JSON.

---

### 6.2 Normalized timeline

Deterministic timeline generated from transcript.

File:

```text
output/timeline.normalized.json
```

It does not contain final visual direction.

---

### 6.3 Director timeline

Timeline enriched by Visual Director AI.

File:

```text
output/timeline.director.json
```

It may contain:

- display lines
- keywords
- emotion
- layout
- icon_query

but may not yet contain actual icon file paths.

---

### 6.4 Visual timeline

Final renderer input.

File:

```text
output/timeline.visual.json
```

It should contain all renderer-needed visual instructions.

---

### 6.5 Scene

A timed visual unit in the video.

Example:

```json
{
  "id": "scene_0001",
  "start": 0.25,
  "end": 2.16,
  "duration": 1.91,
  "text": "Ê! Sao hôm nay đến trễ?"
}
```

---

### 6.6 Scene ID

Stable ID for a scene.

Example:

```text
scene_0001
```

---

### 6.7 Scene duration

Length of a scene in seconds.

Computed as:

```text
end - start
```

---

### 6.8 Source segment IDs

Transcript segment IDs used to create a scene.

Example:

```json
"source_segment_ids": ["seg_0001", "seg_0002"]
```

---

### 6.9 Timeline analyzer

Deterministic module that converts transcript segments into scenes.

Location:

```text
src/timeline/
```

---

### 6.10 Timeline validation

Checking that timeline data is valid.

Examples:

- durations are positive
- scenes are sorted
- IDs are unique
- text is not empty

---

### 6.11 Scene split

Dividing a long transcript segment into smaller scenes.

---

### 6.12 Scene merge

Combining very short transcript segments into one scene.

---

### 6.13 Scene overlap

When two scenes occupy overlapping times.

Not supported initially.

---

### 6.14 Scene gap

Time between scenes where no text is active.

Handling gaps is configurable later.

---

### 6.15 Scene-local time

Time measured relative to scene start.

Example:

```text
scene starts at 10.0s
global time is 10.5s
local time is 0.5s
```

Animation offsets usually use scene-local time.

---

## 7. AI terms

### 7.1 AI layer

Parts of the system that use AI models.

Includes:

- speech-to-text
- Visual Director
- embedding search

Does not include renderer.

---

### 7.2 Visual Director

The LLM-powered module that enriches timeline scenes with visual direction.

Location:

```text
src/director/
```

It selects:

- lines
- keywords
- emotion
- layout
- effects
- icon_query

---

### 7.3 LLM

Large Language Model.

Used for Visual Director tasks.

Initial local model:

```text
Qwen 2.5 3B
```

Runtime:

```text
Ollama
```

---

### 7.4 Ollama

Local runtime for running LLMs.

Used initially for Visual Director.

---

### 7.5 Qwen 2.5 3B

The first planned local LLM for Visual Director.

Chosen because it is lightweight and good at structured JSON tasks.

---

### 7.6 Prompt

Instruction text sent to an AI model.

Prompts live under:

```text
prompts/
```

---

### 7.7 Prompt version

Version number for a prompt file.

Example:

```text
visual_director v0.1.0
```

Prompt versions help reproduce output.

---

### 7.8 Prompt loader

Code that loads prompt files from disk.

Should live in:

```text
src/director/
```

---

### 7.9 Prompt renderer

Code that injects variables into prompt templates.

Example variable:

```text
{{timeline_json}}
```

---

### 7.10 JSON repair

Process of fixing malformed JSON returned by an LLM.

Must be followed by validation.

---

### 7.11 LLM output validation

Checking LLM output before using it.

Required because LLM output may be invalid or hallucinated.

---

### 7.12 Hallucination

When an AI model invents unsupported content.

Examples:

- nonexistent effect
- nonexistent icon file
- changed timestamps
- extra scenes
- invalid JSON fields

---

### 7.13 AI confidence

Optional score indicating model confidence.

Example:

```json
"confidence": 0.87
```

Do not over-trust confidence.

---

### 7.14 Local model

AI model running on user machine.

Examples:

- Faster Whisper
- Qwen through Ollama
- sentence-transformers embedding model

---

### 7.15 Cloud model

AI model accessed through online API.

Cloud models are optional only.

---

### 7.16 Provider

A model backend implementation.

Examples:

- Faster Whisper provider
- Ollama provider
- OpenAI provider later

---

### 7.17 Provider abstraction

Interface that allows replacing model providers without changing high-level logic.

---

## 8. Prompt terms

### 8.1 Visual Director prompt

Prompt that asks the LLM to enrich normalized timeline with visual directions.

File:

```text
prompts/visual_director.md
```

---

### 8.2 JSON repair prompt

Prompt used to repair malformed JSON.

File:

```text
prompts/json_repair.md
```

---

### 8.3 Keyword extractor prompt

Optional focused prompt for selecting keywords.

File:

```text
prompts/keyword_extractor.md
```

---

### 8.4 Emotion classifier prompt

Optional focused prompt for classifying emotion.

File:

```text
prompts/emotion_classifier.md
```

---

### 8.5 Icon query prompt

Optional focused prompt for generating icon query.

File:

```text
prompts/icon_query.md
```

---

### 8.6 Speaker mapping prompt

Optional prompt for mapping speaker IDs to labels.

---

### 8.7 Prompt injection

When text data tries to act as an instruction to the model.

Example transcript content:

```text
Ignore previous instructions.
```

Prompts must treat transcript as data only.

---

### 8.8 JSON-only prompt

Prompt that instructs model to return only JSON.

No markdown.

No explanation.

No code fence.

---

### 8.9 Allowed values

Controlled enum values passed into prompt.

Examples:

```text
pop
shake
center_stack
funny
surprised
```

---

### 8.10 Prompt fixture

Test input/output used to evaluate prompt behavior.

---

## 9. Text and visual direction terms

### 9.1 Display lines

Text lines shown on screen.

Example:

```json
"lines": ["Ê!", "SAO HÔM NAY", "ĐẾN TRỄ?"]
```

Display lines are not necessarily identical to raw transcript.

---

### 9.2 Raw text

Original text from transcript or timeline.

Should be preserved in `text`.

---

### 9.3 Kinetic text

Animated text used as the main visual element.

The project creates kinetic text videos, not normal subtitles.

---

### 9.4 Subtitle

Traditional text overlay usually placed at the bottom.

This project does not focus on normal subtitles.

---

### 9.5 Full-screen text

Large text occupying a major part of the frame.

The first visual style uses full-screen text.

---

### 9.6 Keyword

Important word or phrase to emphasize visually.

Example:

```text
ĐẾN TRỄ
BÁO THỨC
```

---

### 9.7 Keyword target

The specific text element that an animation or style applies to.

---

### 9.8 Conceptual keyword

A keyword idea that may not appear literally in the scene text.

Early renderer may ignore conceptual keywords.

---

### 9.9 Highlight

Visual emphasis applied to text.

Examples:

- yellow color
- larger font
- glow
- stroke
- animation

---

### 9.10 Emotion

Scene mood used for visual direction.

Allowed examples:

```text
neutral
happy
surprised
confused
angry
funny
sad
serious
dramatic
excited
```

---

### 9.11 Punchline

The funny or surprising point of a scene.

Punchlines often deserve stronger visual emphasis.

---

### 9.12 Layout suggestion

AI-generated suggestion for how scene elements should be arranged.

Example:

```json
"layout": {
  "name": "punchline_center"
}
```

---

### 9.13 Icon query

Short semantic phrase used to search for an icon.

Example:

```json
"icon_query": "báo thức"
```

This is not an icon filename.

---

## 10. Renderer terms

### 10.1 Renderer

The deterministic module that turns visual timeline JSON into silent video.

Location:

```text
src/renderer/
```

---

### 10.2 Silent video

Rendered video without audio.

File:

```text
output/silent_video.mp4
```

Exporter later merges audio.

---

### 10.3 Render context

Runtime object containing render settings.

May include:

- width
- height
- fps
- template
- safe zone
- asset registry
- effect registry
- layout registry

---

### 10.4 Render element

A drawable object in a scene.

Examples:

- background
- text line
- keyword
- icon
- avatar
- speaker label

---

### 10.5 Canvas

The frame surface where elements are drawn.

Default:

```text
1080 x 1920
```

---

### 10.6 Frame

One image in a video sequence.

At 30 FPS, one second has 30 frames.

---

### 10.7 FPS

Frames per second.

Default:

```text
30
```

---

### 10.8 Resolution

Video dimensions.

Default:

```text
1080 x 1920
```

---

### 10.9 Aspect ratio

Width-to-height ratio.

Default:

```text
9:16
```

---

### 10.10 Safe zone

Area where important visual content should appear.

Avoids platform UI overlays.

Example:

```json
{
  "top": 120,
  "bottom": 220,
  "left": 80,
  "right": 140
}
```

---

### 10.11 Template

Reusable visual style definition.

Controls:

- colors
- fonts
- safe zones
- default layout
- default effects
- speaker styles
- keyword styles

---

### 10.12 Layout

Positioning system for scene elements.

Examples:

```text
center_stack
punchline_center
speaker_label_top
comic_panel
split_speaker
avatar_left_text_right
```

---

### 10.13 Layout registry

Mapping of layout names to layout implementations.

---

### 10.14 Effect

Animation or visual transformation.

Examples:

```text
pop
bounce
shake
glow
slide
fade
pulse
typewriter
zoom
```

---

### 10.15 Effect registry

Mapping of effect names to effect implementations.

Renderer validates effects against this registry.

---

### 10.16 Transform

Change applied to a visual element.

May include:

- x movement
- y movement
- scale
- opacity
- rotation

---

### 10.17 Z-index

Drawing order value.

Higher z-index appears above lower z-index.

---

### 10.18 Layer

An intermediate image surface used for compositing.

Useful for text scaling, opacity, glow, and rotation.

---

### 10.19 Preview mode

Lower-resolution or faster rendering mode for testing.

---

### 10.20 Debug mode

Mode that writes debug outputs such as:

- safe zone preview
- bounding boxes
- prompt files
- raw model output
- scene preview images

---

## 11. Animation terms

### 11.1 Animation

A timed visual change applied to an element.

Example:

```json
{
  "target": {
    "type": "keyword",
    "text": "BÁO THỨC"
  },
  "type": "shake",
  "start_offset": 0.2,
  "duration": 0.3
}
```

---

### 11.2 Animation target

The element an animation applies to.

Examples:

```text
scene
line
keyword
icon
avatar
speaker_label
background
```

---

### 11.3 Start offset

When animation begins relative to scene start.

Measured in seconds.

---

### 11.4 Animation duration

Length of animation.

Measured in seconds.

---

### 11.5 Pop

Effect where element quickly scales up then returns.

Good for surprise or punchline.

---

### 11.6 Bounce

Playful motion effect.

Good for humorous content.

---

### 11.7 Shake

Jitter motion effect.

Good for chaos, alarm, anger, or comedic emphasis.

---

### 11.8 Glow

Light or halo around element.

Good for emphasis or importance.

---

### 11.9 Slide

Element moves into position.

Good for entrances and transitions.

---

### 11.10 Fade

Opacity transition.

Good for subtle scenes.

---

### 11.11 Pulse

Repeated scale or brightness change.

Good for emphasis.

---

### 11.12 Typewriter

Text appears progressively.

Future effect.

---

### 11.13 Zoom

Scale change for element or scene camera.

---

### 11.14 Easing

Function controlling animation speed curve.

Examples:

```text
linear
ease_in
ease_out
ease_in_out
ease_out_back
```

---

## 12. Asset terms

### 12.1 Asset

A reusable media file used by renderer or pipeline.

Examples:

- icon
- avatar
- background
- font
- sound effect
- music
- template

---

### 12.2 Asset ID

Stable identifier for an asset.

Example:

```text
icon_alarm_001
```

---

### 12.3 Asset path

File path to asset.

Should be repository-relative.

Example:

```text
assets/icons/alarm_001.png
```

---

### 12.4 Asset registry

Runtime system that loads asset metadata and resolves asset IDs to paths.

---

### 12.5 Asset database

JSON file listing assets and metadata.

Examples:

```text
assets/icons/icon_db.json
assets/fonts/font_db.json
```

---

### 12.6 Icon

Small visual symbol representing a concept.

Example:

```text
alarm
sleep
money
coffee
warning
```

---

### 12.7 Icon DB

Metadata database for icons.

File:

```text
assets/icons/icon_db.json
```

---

### 12.8 Icon selector

Module that maps icon_query to icon_id/path.

Location:

```text
src/embedding/
```

---

### 12.9 Embedding

Vector representation of text.

Used to search icon metadata semantically.

---

### 12.10 Embedding model

Model used to produce embeddings.

Example:

```text
paraphrase-multilingual-MiniLM-L12-v2
```

---

### 12.11 Icon score

Similarity score between icon query and icon metadata.

Example:

```json
"icon_score": 0.91
```

---

### 12.12 Avatar

Character image representing a speaker.

Optional early.

---

### 12.13 Background

Visual base behind text.

Can be solid color, gradient, image, or video.

---

### 12.14 Font

Typeface used to render text.

Must support Vietnamese.

---

### 12.15 SFX

Sound effect.

Optional.

Audio mixing belongs to exporter/audio module, not renderer.

---

### 12.16 BGM

Background music.

Optional future feature.

---

### 12.17 Sticker

Decorative visual element.

Different from icon because it is more decorative than semantic.

---

### 12.18 Asset pack

Collection of assets and metadata.

Future concept.

---

### 12.19 Asset metadata

Information describing an asset.

Examples:

- tags
- license
- style
- mood
- category
- file path

---

### 12.20 Asset validation

Checking asset DB and files.

Examples:

- IDs unique
- paths exist
- tags not empty
- licenses documented

---

## 13. Template terms

### 13.1 Template

Data file defining visual style.

Example:

```text
tiktok_dark_comic
```

---

### 13.2 Template name

Identifier of template.

Example:

```text
minimal_black
neon_dialogue
```

---

### 13.3 Template version

Version of template.

Example:

```text
0.1.0
```

---

### 13.4 Style token

Named visual style value.

Example:

```text
keyword_primary
speaker_a
text_main
```

---

### 13.5 Keyword style

Template-defined style for keywords.

May include:

- color
- stroke
- glow
- font scale

---

### 13.6 Speaker style

Template-defined style for speakers.

May include:

- label background
- label text color
- avatar group

---

### 13.7 Color token

Named color in a template.

Example:

```text
text_primary
keyword_primary
speaker_a
```

---

### 13.8 Font token

Named font style in a template.

Example:

```text
main
keyword
label
```

---

### 13.9 Default layout

Template layout used when scene does not specify one.

---

### 13.10 Default effect

Template effect used when keyword does not specify one.

---

## 14. Export terms

### 14.1 Exporter

Module that creates the final video output.

Location:

```text
src/exporter/
```

---

### 14.2 Final MP4

Final user-facing video file.

Default:

```text
output/final.mp4
```

---

### 14.3 H.264

Common video codec.

Default planned codec.

---

### 14.4 AAC

Common audio codec.

Default planned audio codec.

---

### 14.5 Container

File format holding video/audio streams.

Default:

```text
MP4
```

---

### 14.6 Render report

JSON report describing pipeline output.

File:

```text
output/render_report.json
```

---

### 14.7 Duration mismatch

When video duration and audio duration differ.

Should be reported.

---

### 14.8 Audio/video merge

Process of combining silent video with audio.

Handled by exporter.

---

## 15. Repository and workflow terms

### 15.1 Repository

Git project stored locally and on GitHub.

---

### 15.2 Git

Version control system.

Used to track project changes.

---

### 15.3 GitHub

Remote hosting for repository.

Also long-term memory for the project.

---

### 15.4 Commit

A saved change in Git history.

Use conventional commit messages.

---

### 15.5 Conventional commit

Commit message format.

Examples:

```text
feat: add speech-to-text module
fix: handle missing ffmpeg
docs: update pipeline documentation
```

---

### 15.6 Branch

Separate line of development.

Early solo development may use `main`.

Later features can use branches.

---

### 15.7 Issue

GitHub task or ticket.

Each sprint should have issue(s).

---

### 15.8 Pull request

Request to merge code changes.

May be used later.

---

### 15.9 Sprint

Time-boxed or scope-boxed development stage.

Examples:

- Sprint 1: Speech To Text
- Sprint 2: Timeline Analyzer
- Sprint 5: Renderer

---

### 15.10 Definition of Done

Checklist that defines when a task/sprint is complete.

---

### 15.11 CI

Continuous integration.

GitHub Actions may run tests automatically.

---

### 15.12 GitHub Actions

GitHub automation system.

Used for CI.

---

### 15.13 VS Code

Primary development editor.

May use Codex or Copilot.

---

### 15.14 Codex

AI coding assistant in VS Code.

Should read `AGENTS.md` before coding.

---

### 15.15 AGENTS.md

Main instruction file for AI coding agents.

---

### 15.16 PROJECT_RULES.md

Mandatory project rules.

---

### 15.17 DecisionLog

Document recording major decisions and reasons.

File:

```text
docs/DecisionLog.md
```

---

### 15.18 ADR

Architecture Decision Record.

A structured decision entry inside DecisionLog.

Example:

```text
ADR-0003 - Separate AI from renderer
```

---

## 16. Coding terms

### 16.1 Module

A folder or file responsible for a focused area.

Example:

```text
src/audio/
```

---

### 16.2 Package

Importable Python package.

Recommended long-term:

```text
ai_video_engine
```

---

### 16.3 `src` layout

Python project structure where source package lives under:

```text
src/
```

Recommended:

```text
src/ai_video_engine/
```

---

### 16.4 Virtual environment

Isolated Python environment.

Folder:

```text
.venv/
```

---

### 16.5 Dependency

External package or tool the project needs.

Examples:

- faster-whisper
- pydantic
- Pillow
- MoviePy

---

### 16.6 Optional dependency

Dependency required only for optional feature.

Example:

- WhisperX for word timing
- pyannote for diarization

---

### 16.7 Pydantic

Python library used for runtime data validation.

---

### 16.8 Dataclass

Python structure useful for internal runtime state.

---

### 16.9 Type hint

Python annotation describing expected types.

Example:

```python
def extract_audio(input_path: Path) -> AudioExtractionResult:
    ...
```

---

### 16.10 Unit test

Fast test for a small piece of code.

Should not require big models.

---

### 16.11 Integration test

Test that uses multiple components.

May require FFmpeg or AI models.

---

### 16.12 Smoke test

Simple test checking that a basic path works.

---

### 16.13 Fixture

Test input data.

Example:

```text
tests/fixtures/transcript_simple.json
```

---

### 16.14 Mock

Fake object used in tests.

Example:

```text
FakeLLMClient
```

---

### 16.15 Validation

Checking input/output data for correctness.

---

### 16.16 Schema

Formal structure definition for JSON data.

---

### 16.17 Enum

Controlled set of allowed values.

Example:

```text
pop
shake
fade
```

---

### 16.18 Config

Settings controlling behavior.

Example:

```yaml
speech:
  model: medium
```

---

### 16.19 CLI

Command-line interface.

Future command:

```bash
ai-video build input/video.mp4
```

---

### 16.20 Subprocess

Python mechanism for running external commands like FFmpeg.

---

## 17. File terms

### 17.1 `input/`

Folder for local input files.

Generated examples should not commit private input.

---

### 17.2 `temp/`

Folder for temporary intermediate files.

Should be ignored by Git.

---

### 17.3 `output/`

Folder for generated outputs.

Should be ignored by Git.

---

### 17.4 `cache/`

Folder for cached expensive results.

Should be ignored unless intentionally committed.

---

### 17.5 `scripts/`

Folder for thin development scripts.

Scripts should call core modules.

---

### 17.6 `examples/`

Folder for examples.

Should avoid large private media.

---

### 17.7 `tests/`

Folder for tests.

---

### 17.8 `prompts/`

Folder for prompt files.

Prompt source files are committed.

Generated prompt debug outputs are not.

---

### 17.9 `assets/`

Folder for local media assets.

---

### 17.10 `docs/`

Folder for project documentation.

---

### 17.11 `requirements.txt`

Simple dependency installation file.

---

### 17.12 `pyproject.toml`

Modern Python project configuration file.

---

### 17.13 `.gitignore`

Git ignore configuration.

Should exclude generated files and secrets.

---

### 17.14 `.env`

Local environment variables file.

Should not be committed.

---

### 17.15 `.editorconfig`

Editor formatting configuration.

---

## 18. Media format terms

### 18.1 MP4

Common video container.

Default final output format.

---

### 18.2 MOV

Apple video container.

May be supported as input.

---

### 18.3 WAV

Uncompressed audio format.

Used for STT input.

---

### 18.4 MP3

Compressed audio format.

May be supported as input.

---

### 18.5 PNG

Image format.

Recommended for icons with transparency.

---

### 18.6 SVG

Vector image format.

May be supported later.

---

### 18.7 WEBP

Image format.

May be supported later.

---

### 18.8 TTF

Font file format.

---

### 18.9 OTF

Font file format.

---

## 19. Platform terms

### 19.1 Windows support

The project must work on Windows.

Important:

- use `pathlib.Path`
- avoid shell-only syntax
- handle PATH issues
- document PowerShell commands

---

### 19.2 Mac M1 support

The project should work on Apple Silicon Macs.

Important:

- no mandatory CUDA
- CPU-friendly models
- FFmpeg through Homebrew

---

### 19.3 Linux support

Desirable but not the first user environment.

---

### 19.4 GPU

Graphics processing unit.

Optional.

Not required by core pipeline.

---

### 19.5 CUDA

NVIDIA GPU acceleration platform.

Must not be required.

---

### 19.6 CPU mode

Running models and rendering without GPU.

Required.

---

## 20. Product terms

### 20.1 Short-form video

Video designed for TikTok, Reels, Shorts.

Usually vertical and short.

---

### 20.2 TikTok video

Vertical short video, often 9:16.

---

### 20.3 YouTube Shorts

YouTube short-form vertical video.

---

### 20.4 Instagram Reels

Instagram short-form vertical video.

---

### 20.5 Recruitment video

Video designed to attract candidates or promote jobs.

Future product track.

---

### 20.6 Candidate intro video

Video summarizing a candidate profile.

Future product track.

---

### 20.7 Employer branding video

Video promoting a company as an employer.

Future product track.

---

### 20.8 Content factory

Automated system for producing many pieces of content.

Long-term vision.

---

### 20.9 Batch processing

Processing many inputs in one run.

Future feature.

---

### 20.10 Template marketplace

Future concept where templates may be reused or shared.

Not an early priority.

---

## 21. Quality terms

### 21.1 Readability

How easy text is to read on mobile.

Most important visual quality metric.

---

### 21.2 Contrast

Difference between text and background.

High contrast is required.

---

### 21.3 Safe zone compliance

Important content stays away from screen edges and platform UI overlays.

---

### 21.4 Timing

How well visual changes match voice/audio.

---

### 21.5 Relevance

How well a keyword, icon, or effect matches scene meaning.

---

### 21.6 Consistency

Visual style remains stable across scenes and videos.

---

### 21.7 Sync

Alignment between audio and video.

---

### 21.8 Latency

Delay or processing time.

---

### 21.9 Throughput

Number of videos processed over time.

Important for batch mode.

---

### 21.10 Reproducibility

Ability to reproduce same output from same inputs.

---

## 22. Common abbreviations

### 22.1 AI

Artificial Intelligence.

---

### 22.2 LLM

Large Language Model.

---

### 22.3 STT

Speech-to-text.

---

### 22.4 TTS

Text-to-speech.

---

### 22.5 VAD

Voice Activity Detection.

---

### 22.6 BGM

Background music.

---

### 22.7 SFX

Sound effects.

---

### 22.8 FPS

Frames per second.

---

### 22.9 UI

User interface.

---

### 22.10 API

Application programming interface.

---

### 22.11 CLI

Command-line interface.

---

### 22.12 CI

Continuous integration.

---

### 22.13 ADR

Architecture Decision Record.

---

### 22.14 JSON

JavaScript Object Notation.

Structured data format used as project contract.

---

### 22.15 YAML

Human-readable configuration format.

May be used for templates/config.

---

## 23. Term usage rules

### 23.1 Use "scene" consistently

Use `scene` for renderable timeline unit.

Do not alternate randomly with:

```text
frame
clip
segment
```

unless the distinction matters.

---

### 23.2 Use "segment" for STT output

Use `segment` for speech-to-text output unit.

Use `scene` after timeline analyzer.

---

### 23.3 Use "line" for display text line

Use `line` for on-screen text line.

---

### 23.4 Use "keyword" for emphasis target

Use `keyword` for text to highlight or animate.

---

### 23.5 Use "effect" for animation behavior

Use `effect` for named animation or visual emphasis.

---

### 23.6 Use "template" for visual style

Use `template` for reusable style definition.

---

### 23.7 Use "asset" for reusable media

Use `asset` for icons, avatars, backgrounds, fonts, SFX, music.

---

### 23.8 Use "renderer" only for visual rendering

Do not call AI modules renderers.

---

### 23.9 Use "exporter" for final media packaging

Exporter merges audio/video and writes final MP4.

---

### 23.10 Use "director" for AI visual decision module

Visual Director is AI layer, not renderer.

---

## 24. Example term flow

```text
Input video
    ↓
Audio extractor creates source audio
    ↓
Speech module creates transcript segments
    ↓
Timeline analyzer creates scenes
    ↓
Visual Director adds display lines, keywords, emotion, layout, icon_query
    ↓
Icon selector resolves icon_query to icon_id/icon_path
    ↓
Renderer draws visual timeline into silent video
    ↓
Exporter merges silent video with original audio
    ↓
Final MP4
```

---

## 25. Final glossary rule

If a new term becomes important enough to appear in code, schema, prompts, or docs, add it to this glossary.

Consistent language keeps the project understandable.

---

# Appendix A - Quick reference table

| Term | Meaning | Module | Example |
|---|---|---|---|
| Transcript segment | Raw STT text unit | `speech` | `seg_0001` |
| Scene | Renderable timeline unit | `timeline` | `scene_0001` |
| Display line | Text line shown on screen | `director/renderer` | `ĐẾN TRỄ?` |
| Keyword | Text emphasis target | `director/renderer` | `BÁO THỨC` |
| Icon query | Semantic search phrase | `director/embedding` | `báo thức` |
| Icon ID | Resolved asset ID | `embedding/assets` | `icon_alarm_001` |
| Effect | Animation behavior | `renderer` | `pop` |
| Layout | Element positioning strategy | `renderer` | `center_stack` |
| Template | Visual style definition | `renderer/assets` | `tiktok_dark_comic` |
| Silent video | Rendered video without audio | `renderer` | `silent_video.mp4` |
| Final video | Video with audio merged | `exporter` | `final.mp4` |

---

# Appendix B - Vietnamese terms in project context

| Vietnamese | English meaning | Project use |
|---|---|---|
| báo thức | alarm | common icon query |
| đến trễ | late | common keyword |
| ngủ | sleep | common icon query |
| tiền | money | common icon query |
| đi làm | go to work | work icon query |
| cà phê | coffee | coffee icon query |
| ủa | huh? | confused emotion |
| trời ơi | oh my god | surprised emotion |
| hài hước | funny | content style |
| nhấn mạnh | emphasis | keyword/effect purpose |

---

# Appendix C - Common file mapping

| File | Meaning |
|---|---|
| `input/video.mp4` | User input video |
| `temp/audio.wav` | Extracted audio for STT |
| `output/transcript.json` | STT output |
| `output/timeline.normalized.json` | Timeline analyzer output |
| `output/timeline.director.json` | Visual Director output |
| `output/timeline.visual.json` | Renderer input |
| `output/silent_video.mp4` | Renderer output |
| `output/final.mp4` | Final exported video |
| `output/render_report.json` | Run report |

---

# Appendix D - Module mapping

| Module | Meaning |
|---|---|
| `src/audio` | Audio extraction |
| `src/speech` | Speech-to-text |
| `src/timeline` | Timeline analysis and validation |
| `src/director` | LLM visual direction |
| `src/embedding` | Semantic icon search |
| `src/renderer` | Deterministic visual rendering |
| `src/exporter` | Final MP4 export |
| `src/assets` | Asset registry |
| `src/common` | Shared utilities |
| `src/config` | Configuration loading |

---

# Appendix E - Final note

This glossary should evolve with the project.

When a term becomes ambiguous, clarify it here before ambiguity spreads into code.
