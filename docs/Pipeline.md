# Pipeline.md

# AI Video Engine - Pipeline Design

## 0. Purpose

This document defines the pipeline of **AI Video Engine**.

It explains how data moves from an input video or audio file to a final rendered MP4.

This file is intended for:

- human maintainers
- ChatGPT
- Codex
- GitHub Copilot
- future contributors
- future UI/API developers

This document should be read together with:

```text
AGENTS.md
PROJECT_RULES.md
docs/Architecture.md
docs/JSONSchema.md
docs/AIDesign.md
docs/RendererDesign.md
docs/DecisionLog.md
```

---

## 1. Pipeline philosophy

The pipeline must be:

- explicit
- inspectable
- resumable
- modular
- testable
- local-first
- deterministic where possible

Each stage should have:

- clear input
- clear output
- clear responsibility
- clear failure behavior
- clear validation boundary

The pipeline should not be a hidden black box.

Intermediate files should be written to disk so users and AI agents can inspect them.

---

## 2. One-line pipeline

```text
Input media → Audio → Transcript → Normalized Timeline → Visual Timeline → Silent Video → Final MP4
```

---

## 3. Full pipeline

```text
input/video.mp4
      ↓
[01] Validate Input
      ↓
[02] Extract Audio
      ↓
temp/audio.wav
      ↓
[03] Speech To Text
      ↓
output/transcript.json
      ↓
[04] Transcript Validation
      ↓
[05] Timeline Analyzer
      ↓
output/timeline.normalized.json
      ↓
[06] Visual Director AI
      ↓
output/timeline.director.json
      ↓
[07] Icon Selector
      ↓
output/timeline.visual.json
      ↓
[08] Visual Timeline Validation
      ↓
[09] Renderer
      ↓
output/silent_video.mp4
      ↓
[10] Exporter
      ↓
output/final.mp4
      ↓
[11] Render Report
      ↓
output/render_report.json
```

---

## 4. Pipeline stage list

| Stage | Name | Module | Output |
|---|---|---|---|
| 01 | Validate Input | `src/common` | input metadata |
| 02 | Extract Audio | `src/audio` | `temp/audio.wav` |
| 03 | Speech To Text | `src/speech` | `output/transcript.json` |
| 04 | Validate Transcript | `src/timeline` | validated transcript |
| 05 | Timeline Analyzer | `src/timeline` | `output/timeline.normalized.json` |
| 06 | Visual Director AI | `src/director` | `output/timeline.director.json` |
| 07 | Icon Selector | `src/embedding` | `output/timeline.visual.json` |
| 08 | Validate Visual Timeline | `src/timeline` | validated visual timeline |
| 09 | Renderer | `src/renderer` | `output/silent_video.mp4` |
| 10 | Exporter | `src/exporter` | `output/final.mp4` |
| 11 | Render Report | `src/exporter` | `output/render_report.json` |

---

## 5. Pipeline design constraints

### Constraint 5.1 - AI only enriches data

AI is allowed in:

- speech-to-text
- visual direction
- optional JSON repair
- optional semantic classification

AI is not allowed in:

- renderer
- exporter
- direct video creation
- direct media mutation

### Constraint 5.2 - Renderer consumes final visual timeline only

Renderer should not consume:

- raw transcript
- raw LLM text
- prompt output before validation
- natural-language instructions

Renderer consumes:

```text
output/timeline.visual.json
```

### Constraint 5.3 - Original audio is preserved

For the current workflow, the input video already has voice.

The pipeline should keep original voice.

Final export should merge the rendered visual video with original audio.

### Constraint 5.4 - Intermediate outputs are important

Intermediate outputs are not temporary noise.

They are debugging tools.

They allow:

- manual correction
- repeatable rendering
- AI agent review
- future UI editing
- partial reruns

---

## 6. Default paths

Default input:

```text
input/video.mp4
```

Default temp audio:

```text
temp/audio.wav
```

Default transcript:

```text
output/transcript.json
```

Default normalized timeline:

```text
output/timeline.normalized.json
```

Default director output:

```text
output/timeline.director.json
```

Default visual timeline:

```text
output/timeline.visual.json
```

Default silent video:

```text
output/silent_video.mp4
```

Default final output:

```text
output/final.mp4
```

Default report:

```text
output/render_report.json
```

---

## 7. Pipeline outputs by maturity

### 7.1 Sprint 1 outputs

Sprint 1 only needs:

```text
temp/audio.wav
output/transcript.json
```

### 7.2 Sprint 2 outputs

Sprint 2 adds:

```text
output/timeline.normalized.json
```

### 7.3 Sprint 3 outputs

Sprint 3 adds:

```text
output/timeline.director.json
```

### 7.4 Sprint 4 outputs

Sprint 4 adds:

```text
output/timeline.visual.json
```

### 7.5 Sprint 5 outputs

Sprint 5 adds:

```text
output/silent_video.mp4
```

### 7.6 Sprint 6 outputs

Sprint 6 adds:

```text
output/final.mp4
output/render_report.json
```

---

## 8. Stage 01 - Validate Input

### 8.1 Purpose

Validate that the input file exists and is usable.

### 8.2 Input

```text
input/video.mp4
```

or:

```text
input/audio.wav
```

### 8.3 Output

A validated media reference.

Possible future object:

```json
{
  "path": "input/video.mp4",
  "type": "video",
  "exists": true,
  "duration": 28.4,
  "has_audio": true,
  "has_video": true
}
```

### 8.4 Responsibilities

- check file exists
- check path is readable
- check extension
- optionally probe duration
- optionally check audio stream
- optionally check video stream

### 8.5 Failure cases

| Failure | Behavior |
|---|---|
| file missing | fail clearly |
| path is directory | fail clearly |
| no audio stream | warn or fail based on command |
| unsupported format | fail clearly |
| file unreadable | fail clearly |

### 8.6 Example error

```text
Input file not found: input/video.mp4
Please place a video in the input folder or pass --input.
```

### 8.7 Validation rules

The input path must be a file.

The input file must not be overwritten.

The input file should be treated as read-only.

---

## 9. Stage 02 - Extract Audio

### 9.1 Purpose

Extract an audio file suitable for speech-to-text.

### 9.2 Module

```text
src/audio/
```

### 9.3 Input

```text
input/video.mp4
```

### 9.4 Output

```text
temp/audio.wav
```

### 9.5 Recommended audio format

```text
WAV
mono
16000 Hz
```

### 9.6 FFmpeg command

```bash
ffmpeg -y -i input/video.mp4 -vn -ac 1 -ar 16000 temp/audio.wav
```

### 9.7 Responsibilities

- validate FFmpeg exists
- extract audio
- normalize to STT format
- create output folder if needed
- preserve original audio reference
- return audio metadata when possible

### 9.8 Non-responsibilities

This stage does not:

- transcribe audio
- detect speakers
- clean transcript
- render video
- call LLMs

### 9.9 Input contract

```json
{
  "input_path": "input/video.mp4",
  "output_audio_path": "temp/audio.wav",
  "sample_rate": 16000,
  "channels": 1
}
```

### 9.10 Output contract

```json
{
  "stage": "audio_extraction",
  "input_path": "input/video.mp4",
  "output_path": "temp/audio.wav",
  "sample_rate": 16000,
  "channels": 1,
  "success": true
}
```

### 9.11 Failure cases

| Failure | Behavior |
|---|---|
| FFmpeg not installed | fail with install guidance |
| input file missing | fail |
| no audio stream | fail or warn |
| permission denied | fail |
| output folder missing | create folder |
| FFmpeg process fails | show stderr summary |

### 9.12 Sprint 1 acceptance

This stage is complete when:

- it extracts `temp/audio.wav`
- command works on Windows
- command works when paths contain spaces
- missing FFmpeg error is clear
- output file exists after successful run

---

## 10. Stage 03 - Speech To Text

### 10.1 Purpose

Convert audio into timestamped transcript JSON.

### 10.2 Module

```text
src/speech/
```

### 10.3 Input

```text
temp/audio.wav
```

### 10.4 Output

```text
output/transcript.json
```

### 10.5 Initial implementation

Use Faster Whisper.

### 10.6 Recommended initial config

```yaml
speech:
  provider: faster_whisper
  model: medium
  language: vi
  device: cpu
  compute_type: int8
  vad_filter: true
```

### 10.7 Transcript JSON example

```json
{
  "schema_version": "0.1.0",
  "language": "vi",
  "source_audio": "temp/audio.wav",
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

### 10.8 Responsibilities

- load STT model
- transcribe audio
- preserve start/end timestamps
- clean basic whitespace
- assign segment IDs
- write JSON
- include metadata

### 10.9 Non-responsibilities

This stage does not:

- choose visual keywords
- choose effects
- choose icons
- generate display lines
- render video
- merge speakers unless diarization is explicitly included

### 10.10 Metadata

Transcript should eventually include:

```json
{
  "metadata": {
    "engine": "faster_whisper",
    "model": "medium",
    "language": "vi",
    "duration": 28.4,
    "created_at": "ISO_TIMESTAMP"
  }
}
```

### 10.11 Failure cases

| Failure | Behavior |
|---|---|
| model load fails | fail with model name |
| audio missing | fail |
| unsupported audio | fail |
| no speech found | output empty transcript with warning |
| language mismatch | warn if detected |
| memory error | suggest smaller model |

### 10.12 Sprint 1 acceptance

This stage is complete when:

- a video can become `transcript.json`
- transcript has `start`, `end`, `text`
- Vietnamese transcription works
- output JSON is valid UTF-8
- model name is configurable
- CPU mode works

---

## 11. Stage 04 - Transcript Validation

### 11.1 Purpose

Ensure transcript is structurally valid before timeline processing.

### 11.2 Module

```text
src/timeline/
```

### 11.3 Input

```text
output/transcript.json
```

### 11.4 Output

Validated transcript object.

### 11.5 Validation checks

Transcript must have:

- schema version
- language
- segments array

Each segment must have:

- id
- start
- end
- duration
- text

### 11.6 Timing checks

For each segment:

```text
start >= 0
end > start
duration = end - start
```

Segments should be sorted by start time.

### 11.7 Text checks

Text should be:

- string
- non-empty after trim
- valid Unicode

### 11.8 Failure cases

| Failure | Behavior |
|---|---|
| JSON invalid | fail |
| missing segments | fail |
| empty transcript | warn or fail based config |
| invalid duration | fail |
| unsorted segments | sort or fail based config |
| overlapping segments | warn or fail |

### 11.9 Output expectation

No new file is required unless validation report is enabled.

Possible future output:

```text
output/transcript.validation.json
```

---

## 12. Stage 05 - Timeline Analyzer

### 12.1 Purpose

Transform raw transcript segments into renderable scenes.

### 12.2 Module

```text
src/timeline/
```

### 12.3 Input

```text
output/transcript.json
```

### 12.4 Output

```text
output/timeline.normalized.json
```

### 12.5 Why this stage exists

Speech-to-text output is not ideal for rendering.

STT may produce:

- segments too long
- segments too short
- poor punctuation
- inconsistent speaker turns
- text too dense
- awkward timing

Timeline Analyzer prepares the transcript for visual direction.

### 12.6 Responsibilities

- clean text
- normalize punctuation
- split long segments
- merge short segments
- create scene IDs
- compute duration
- keep source segment references
- assign initial speaker IDs
- enforce max scene duration
- enforce minimum scene duration
- output normalized timeline

### 12.7 Non-responsibilities

This stage does not:

- call LLMs
- choose icons
- choose animations
- choose keyword colors
- render anything

### 12.8 Normalized timeline example

```json
{
  "schema_version": "0.1.0",
  "source": {
    "transcript_path": "output/transcript.json"
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
        "source": "unknown",
        "confidence": null
      },
      "text": "Ê! Sao hôm nay đến trễ?"
    }
  ]
}
```

### 12.9 Scene sizing

Recommended defaults:

```yaml
timeline:
  min_scene_duration: 0.6
  max_scene_duration: 4.0
  max_chars_per_scene: 80
  max_sentences_per_scene: 2
```

### 12.10 Merge logic

Very short segments may be merged if:

- same speaker if known
- close in time
- total duration remains acceptable
- combined text remains readable

### 12.11 Split logic

Long segments may be split by:

- punctuation
- sentence boundaries
- pauses
- max character count
- max duration

### 12.12 Speaker fallback

If no diarization exists:

- keep speaker as unknown, or
- optionally infer alternating speaker in dialogue mode

If speaker is inferred, mark:

```json
"source": "inferred"
```

### 12.13 Sprint 2 acceptance

This stage is complete when:

- transcript becomes normalized timeline
- every scene has ID
- every scene has valid timing
- long text is split
- very short text is handled
- output validates against schema

---

## 13. Stage 06 - Visual Director AI

### 13.1 Purpose

Use LLM to enrich scenes with visual decisions.

### 13.2 Module

```text
src/director/
```

### 13.3 Input

```text
output/timeline.normalized.json
```

### 13.4 Output

```text
output/timeline.director.json
```

### 13.5 Initial runtime

```text
Ollama
```

### 13.6 Initial model

```text
qwen2.5:3b
```

### 13.7 Visual Director responsibilities

For each scene, choose:

- display lines
- keywords
- emotion
- layout
- effect
- icon query
- optional speaker mood
- optional transition

### 13.8 Visual Director does not

It does not:

- render video
- pick exact icon file unless given asset list
- change timestamps randomly
- execute code
- create MP4
- download assets

### 13.9 Prompt input

Prompt should include:

- normalized timeline JSON
- allowed effects
- allowed layouts
- allowed emotions
- language
- template name
- output schema
- examples

### 13.10 Prompt output rule

Output must be JSON only.

No markdown.

No explanation.

No code fence.

### 13.11 Director output example

```json
{
  "schema_version": "0.1.0",
  "source": {
    "timeline_path": "output/timeline.normalized.json"
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
          "importance": 0.95,
          "effect": "pop",
          "style": "primary"
        }
      ],
      "assets": {
        "icon_query": "đồng hồ báo thức"
      }
    }
  ]
}
```

### 13.12 JSON repair

LLM output can fail.

If invalid:

1. attempt JSON extraction
2. attempt JSON repair
3. validate schema
4. fail if still invalid

Never send invalid output to renderer.

### 13.13 Sprint 3 acceptance

This stage is complete when:

- normalized timeline becomes director timeline
- LLM returns valid JSON
- output has lines
- output has keywords
- output has emotion
- output has effect suggestions
- output has icon_query
- output validates

---

## 14. Stage 07 - Icon Selector

### 14.1 Purpose

Map icon queries to actual available icons.

### 14.2 Module

```text
src/embedding/
```

### 14.3 Input

```text
output/timeline.director.json
assets/icons/icon_db.json
```

### 14.4 Output

```text
output/timeline.visual.json
```

### 14.5 Why separate from Visual Director

The LLM should not be expected to know every icon filename.

Instead:

```text
LLM → icon_query
Embedding search → icon_id / icon_path
```

### 14.6 Icon database example

```json
[
  {
    "id": "icon_alarm_001",
    "file": "assets/icons/alarm.png",
    "tags": ["báo thức", "đồng hồ", "trễ giờ", "dậy sớm"],
    "style": "flat",
    "mood": ["funny", "urgent"]
  },
  {
    "id": "icon_sleep_001",
    "file": "assets/icons/sleep.png",
    "tags": ["ngủ", "buồn ngủ", "zzz", "mệt"]
  }
]
```

### 14.7 Icon selector output

```json
{
  "assets": {
    "icon_query": "đồng hồ báo thức",
    "icon_id": "icon_alarm_001",
    "icon_path": "assets/icons/alarm.png",
    "icon_score": 0.87
  }
}
```

### 14.8 Recommended first embedding model

```text
paraphrase-multilingual-MiniLM-L12-v2
```

### 14.9 Later options

```text
bge-m3
multilingual-e5-small
faiss-cpu
chromadb
```

### 14.10 Failure cases

| Failure | Behavior |
|---|---|
| icon database missing | warn and continue without icons or fail based config |
| no good match | fallback icon or no icon |
| icon file missing | warn/fail |
| embedding model missing | fail with install guidance |

### 14.11 Sprint 4 acceptance

This stage is complete when:

- icon query maps to real icon
- icon path is added to timeline
- icon score is stored
- missing icon database is handled clearly

---

## 15. Stage 08 - Visual Timeline Validation

### 15.1 Purpose

Validate final renderer input before rendering.

### 15.2 Input

```text
output/timeline.visual.json
```

### 15.3 Output

Validated visual timeline object.

### 15.4 Validation checks

Check:

- schema version
- video settings
- scene IDs
- start/end/duration
- sorted scenes
- text
- display lines
- layout names
- effect names
- keyword targets
- asset references
- template exists

### 15.5 Effect validation

If a scene requests:

```json
"effect": "pop"
```

then `pop` must exist in the effect registry.

### 15.6 Layout validation

If a scene requests:

```json
"layout": { "name": "center_stack" }
```

then `center_stack` must exist in layout registry.

### 15.7 Asset validation

If a scene references:

```json
"icon_path": "assets/icons/alarm.png"
```

then the file should exist.

### 15.8 Failure behavior

Invalid renderer input must fail before rendering.

Do not create half-broken videos silently.

---

## 16. Stage 09 - Renderer

### 16.1 Purpose

Render validated visual timeline into silent video.

### 16.2 Module

```text
src/renderer/
```

### 16.3 Input

```text
output/timeline.visual.json
```

### 16.4 Output

```text
output/silent_video.mp4
```

### 16.5 Responsibilities

- load visual timeline
- load template
- load assets
- prepare canvas
- render backgrounds
- render text
- render keyword emphasis
- render icons
- render speaker labels
- apply animations
- write silent video

### 16.6 Renderer restrictions

Renderer must not:

- call LLM
- transcribe audio
- choose semantic icons
- mutate source transcript
- ignore validation errors

### 16.7 Initial renderer scope

The first renderer can be simple.

Minimum:

- black/dark background
- large text
- highlighted keyword
- basic speaker label
- simple icon label or icon
- output 1080x1920 video

### 16.8 Initial effects

Start with:

```text
pop
fade
slide
shake
bounce
```

### 16.9 Initial layouts

Start with:

```text
center_stack
punchline_center
speaker_label_top
```

### 16.10 Rendering approaches

Possible approaches:

```text
Pillow + MoviePy
Pillow + FFmpeg
OpenCV
FFmpeg filter_complex
```

Initial approach can use Pillow + MoviePy for simplicity.

Later optimization can use FFmpeg/OpenCV.

### 16.11 Scene render logic

For each scene:

1. compute duration
2. create base canvas
3. apply background
4. compute layout positions
5. render text lines
6. render keyword styles
7. render icons
8. generate frames or clip
9. append to video timeline

### 16.12 Timing

Renderer uses scene timing but typically renders scenes sequentially.

If original timeline includes gaps, renderer should decide whether to:

- preserve gaps
- fill gaps with background
- stretch nearby scene
- cut gaps

This should be configurable.

### 16.13 Sprint 5 acceptance

This stage is complete when:

- `timeline.visual.json` produces `silent_video.mp4`
- output is 1080x1920
- text is readable
- at least one keyword effect works
- renderer does not call AI

---

## 17. Stage 10 - Exporter

### 17.1 Purpose

Merge silent rendered video with original audio and create final MP4.

### 17.2 Module

```text
src/exporter/
```

### 17.3 Input

```text
output/silent_video.mp4
temp/audio.wav
```

### 17.4 Output

```text
output/final.mp4
```

### 17.5 Responsibilities

- validate silent video exists
- validate audio exists
- merge audio/video
- encode final MP4
- validate output duration
- write report

### 17.6 FFmpeg command

```bash
ffmpeg -y -i output/silent_video.mp4 -i temp/audio.wav -c:v copy -c:a aac -shortest output/final.mp4
```

### 17.7 Duration validation

Compare:

- original audio duration
- silent video duration
- final video duration

Warn if mismatch exceeds threshold.

### 17.8 Sprint 6 acceptance

This stage is complete when:

- final MP4 is created
- original voice is preserved
- video duration is acceptable
- report is written

---

## 18. Stage 11 - Render Report

### 18.1 Purpose

Record what happened during the run.

### 18.2 Output

```text
output/render_report.json
```

### 18.3 Report example

```json
{
  "schema_version": "0.1.0",
  "input": "input/video.mp4",
  "output": "output/final.mp4",
  "duration": 28.4,
  "scene_count": 14,
  "template": "tiktok_dark_comic",
  "speech_model": "medium",
  "director_model": "qwen2.5:3b",
  "warnings": [],
  "errors": []
}
```

### 18.4 Report responsibilities

Report should include:

- input file
- output file
- duration
- scene count
- model names
- template
- warnings
- errors
- engine version
- schema version

---

## 19. Pipeline modes

The engine should eventually support multiple run modes.

### 19.1 Full build mode

```bash
ai-video build input/video.mp4
```

Runs all stages.

### 19.2 Transcribe-only mode

```bash
ai-video transcribe input/video.mp4
```

Runs:

```text
validate input
extract audio
speech-to-text
```

### 19.3 Render-only mode

```bash
ai-video render output/timeline.visual.json
```

Runs:

```text
validate visual timeline
render silent video
```

### 19.4 Export-only mode

```bash
ai-video export output/silent_video.mp4 temp/audio.wav
```

Runs:

```text
merge audio and video
```

### 19.5 Debug mode

```bash
ai-video build input/video.mp4 --debug
```

May output:

```text
debug frames
safe zone previews
timeline validation report
prompt input/output
```

### 19.6 Preview mode

```bash
ai-video build input/video.mp4 --preview
```

May render:

```text
540 x 960
lower fps
shorter range
```

---

## 20. Pipeline caching

### 20.1 Purpose

Caching avoids repeated expensive work.

### 20.2 Cache candidates

```text
temp/audio.wav
output/transcript.json
output/timeline.normalized.json
output/timeline.director.json
output/timeline.visual.json
cache/icon_embeddings.json
cache/llm_responses/
```

### 20.3 Cache strategy

A stage may be skipped if:

- output exists
- input has not changed
- config has not changed
- model has not changed
- user allows cache

### 20.4 Cache invalidation

Cache should be invalidated when:

- input file changes
- model changes
- prompt changes
- template changes
- asset database changes
- schema version changes

### 20.5 Cache warning

Do not hide cache behavior.

Logs should show:

```text
Using cached transcript: output/transcript.json
```

---

## 21. Pipeline configuration

### 21.1 Example config

```yaml
pipeline:
  cache: true
  stop_on_warning: false
  save_intermediate: true

paths:
  input_dir: input
  temp_dir: temp
  output_dir: output

audio:
  sample_rate: 16000
  channels: 1

speech:
  provider: faster_whisper
  model: medium
  language: vi
  device: cpu
  compute_type: int8
  vad_filter: true

director:
  provider: ollama
  model: qwen2.5:3b

embedding:
  model: paraphrase-multilingual-MiniLM-L12-v2

renderer:
  template: tiktok_dark_comic
  width: 1080
  height: 1920
  fps: 30

export:
  codec: h264
  audio_codec: aac
```

---

## 22. Pipeline state

A future pipeline runner may track state.

Example:

```json
{
  "run_id": "run_20260707_001",
  "input": "input/video.mp4",
  "stages": {
    "validate_input": "success",
    "extract_audio": "success",
    "speech_to_text": "success",
    "timeline_analyzer": "pending",
    "visual_director": "pending",
    "icon_selector": "pending",
    "renderer": "pending",
    "exporter": "pending"
  }
}
```

This can help resume failed runs.

---

## 23. Pipeline errors

### 23.1 Error categories

```text
InputError
DependencyError
AudioError
SpeechToTextError
TranscriptValidationError
TimelineValidationError
DirectorError
EmbeddingError
RenderError
ExportError
```

### 23.2 Error behavior

By default:

- fatal errors stop the pipeline
- warnings are logged
- reports include warnings
- partial outputs remain for debugging

### 23.3 Example fatal error

```text
FFmpeg not found.
Install FFmpeg and ensure it is available in PATH.
```

### 23.4 Example warning

```text
No icon match above threshold for scene_0004.
Scene will render without icon.
```

---

## 24. Validation checkpoints

### 24.1 Checkpoint after audio extraction

Validate:

- audio file exists
- audio file size > 0
- audio duration > 0

### 24.2 Checkpoint after STT

Validate:

- transcript JSON parses
- segments list exists
- each segment has valid timing
- text is not empty

### 24.3 Checkpoint after timeline analyzer

Validate:

- scenes exist
- scenes sorted
- durations valid
- scene IDs unique

### 24.4 Checkpoint after Visual Director

Validate:

- lines exist
- keywords valid
- emotion enum valid
- layout enum valid
- effect enum valid

### 24.5 Checkpoint after Icon Selector

Validate:

- icon path exists if provided
- icon score is numeric if provided

### 24.6 Checkpoint before render

Validate entire visual timeline.

### 24.7 Checkpoint after render

Validate silent video exists and has duration.

### 24.8 Checkpoint after export

Validate final MP4 exists and has audio.

---

## 25. Human editing workflow

Because intermediate files are JSON, users can manually edit them.

Example flow:

```text
run STT
edit transcript.json
run timeline analyzer
edit timeline.visual.json
render
```

Possible manual edits:

- fix transcript text
- fix speaker labels
- adjust keywords
- change effect
- change icon query
- change layout
- adjust timing

The JSON should remain human-readable.

---

## 26. AI agent workflow

AI agents should use the pipeline outputs as context.

Example:

```text
Read output/transcript.json.
Update output/timeline.visual.json.
Do not edit renderer code unless asked.
```

AI agents should not depend on hidden chat memory.

They should inspect repository files.

---

## 27. Development sprint mapping

### Sprint 1 - Speech To Text

Pipeline stages:

```text
01 Validate Input
02 Extract Audio
03 Speech To Text
04 Transcript Validation
```

Deliverables:

```text
temp/audio.wav
output/transcript.json
```

### Sprint 2 - Timeline Analyzer

Pipeline stage:

```text
05 Timeline Analyzer
```

Deliverables:

```text
output/timeline.normalized.json
```

### Sprint 3 - Visual Director

Pipeline stage:

```text
06 Visual Director AI
```

Deliverables:

```text
output/timeline.director.json
```

### Sprint 4 - Icon Selector

Pipeline stage:

```text
07 Icon Selector
```

Deliverables:

```text
output/timeline.visual.json
```

### Sprint 5 - Renderer

Pipeline stages:

```text
08 Visual Timeline Validation
09 Renderer
```

Deliverables:

```text
output/silent_video.mp4
```

### Sprint 6 - Exporter

Pipeline stages:

```text
10 Exporter
11 Render Report
```

Deliverables:

```text
output/final.mp4
output/render_report.json
```

---

## 28. Expected CLI evolution

### 28.1 Early script usage

Early development may use:

```bash
python scripts/transcribe.py input/video.mp4
```

### 28.2 Module usage

Later:

```bash
python -m ai_video_engine transcribe input/video.mp4
```

### 28.3 Final CLI

Eventually:

```bash
ai-video build input/video.mp4
```

---

## 29. Pipeline file naming rules

### 29.1 Transcript

```text
transcript.json
```

### 29.2 Normalized timeline

```text
timeline.normalized.json
```

### 29.3 Director timeline

```text
timeline.director.json
```

### 29.4 Visual timeline

```text
timeline.visual.json
```

### 29.5 Silent video

```text
silent_video.mp4
```

### 29.6 Final video

```text
final.mp4
```

### 29.7 Report

```text
render_report.json
```

---

## 30. Pipeline and templates

Templates affect:

- renderer output
- layout choices
- colors
- fonts
- effect defaults
- safe zones

Templates should not affect:

- raw transcript
- source audio
- STT timing

Visual Director may receive template name so it can choose compatible layouts.

---

## 31. Pipeline and prompts

Prompts affect:

- keyword choices
- emotion labels
- icon queries
- layout suggestions
- animation suggestions

Prompt changes should produce a new director output.

If prompt changes, cached director output may be invalid.

---

## 32. Pipeline and assets

Assets affect:

- icon matching
- avatar rendering
- background rendering
- SFX
- fonts

Asset metadata changes may invalidate icon selector output.

Renderer should fail or warn if referenced assets are missing.

---

## 33. Pipeline and speaker support

Speaker information can enter pipeline in multiple ways:

### 33.1 Unknown speaker

```json
"speaker": {
  "id": "SPEAKER_UNKNOWN"
}
```

### 33.2 Alternating speaker fallback

```json
"speaker": {
  "id": "SPEAKER_00",
  "source": "inferred_alternating"
}
```

### 33.3 Manual mapping

```json
"speaker": {
  "id": "SPEAKER_00",
  "label": "Nam",
  "source": "manual"
}
```

### 33.4 Diarization

```json
"speaker": {
  "id": "SPEAKER_00",
  "source": "diarization",
  "confidence": 0.91
}
```

Speaker support should evolve without breaking pipeline.

---

## 34. Pipeline and word-level timing

Word-level timing is not required for V1.

Later, word-level timing enables:

- per-word pop
- karaoke-style highlight
- exact keyword timing
- better motion sync

Possible future output:

```json
"words": [
  {
    "text": "ĐẾN",
    "start": 1.12,
    "end": 1.30
  },
  {
    "text": "TRỄ",
    "start": 1.31,
    "end": 1.55
  }
]
```

This should be optional.

---

## 35. Pipeline and original video

The current pipeline uses original video primarily as audio source.

The rendered output may completely replace visuals.

Future versions may support:

- using original video as background
- blurring original video
- cropping original video
- overlaying text over original video
- cutting original video clips

These are future renderer/template features.

---

## 36. Pipeline and generated voice

The current workflow preserves original audio.

A future workflow may start from text dialogue and generate TTS.

Future text-to-video pipeline:

```text
dialogue.txt
      ↓
script parser
      ↓
TTS
      ↓
timeline with generated audio
      ↓
renderer
      ↓
final MP4
```

This should be a separate pipeline mode.

---

## 37. Pipeline and batch mode

Batch mode should process many inputs.

Example:

```bash
ai-video build input_folder/ --template tiktok_dark_comic
```

Batch architecture should:

- load models once
- process files sequentially or in parallel
- create output folder per input
- write batch report

Possible output:

```text
output/video_001/final.mp4
output/video_002/final.mp4
output/video_003/final.mp4
```

---

## 38. Pipeline and debugging

Debug outputs may include:

```text
output/debug/prompt_visual_director.txt
output/debug/llm_raw_response.json
output/debug/scene_0001.png
output/debug/safe_zones.png
output/debug/timeline_validation.json
```

Debug mode should be optional.

---

## 39. Pipeline and reports

Reports should capture:

- stage status
- durations
- warnings
- errors
- file paths
- model names
- template names
- schema versions
- output media metadata

Reports are useful for:

- debugging
- batch processing
- UI display
- automated QA

---

## 40. Pipeline and quality control

Quality issues may include:

- transcript incorrect
- speaker wrong
- keyword weak
- icon irrelevant
- text too long
- animation too aggressive
- audio sync mismatch

The pipeline should make these inspectable and correctable.

---

## 41. Pipeline and manual override

Manual override should be supported by editing JSON.

Examples:

### Change keyword

```json
"keywords": [
  {
    "text": "BÁO THỨC",
    "effect": "shake"
  }
]
```

### Change icon

```json
"assets": {
  "icon_id": "icon_alarm_002"
}
```

### Change layout

```json
"layout": {
  "name": "punchline_center"
}
```

The renderer should respect manual JSON edits.

---

## 42. Pipeline and reproducibility

To reproduce output, preserve:

- input file
- transcript JSON
- visual timeline JSON
- template
- assets
- renderer version
- config
- random seed if used

Render report should include enough metadata to debug.

---

## 43. Pipeline and performance

Expected expensive stages:

- STT
- LLM director
- embedding model loading
- rendering

Optimization strategy:

1. Make correct output first.
2. Cache STT.
3. Cache LLM output.
4. Cache embeddings.
5. Optimize renderer after pipeline works.

---

## 44. Pipeline and failure recovery

If a later stage fails, earlier outputs should remain.

Example:

If renderer fails:

```text
output/transcript.json
output/timeline.normalized.json
output/timeline.visual.json
```

should still exist.

This allows fixing renderer without rerunning STT.

---

## 45. Pipeline and validation reports

Validation failures should be readable.

Example:

```json
{
  "valid": false,
  "errors": [
    {
      "path": "scenes[3].animations[0].type",
      "message": "Unknown effect: explode_spin"
    }
  ]
}
```

This helps both humans and AI agents.

---

## 46. Pipeline and schema versions

Every major JSON file should include schema version.

Example:

```json
{
  "schema_version": "0.1.0"
}
```

If schema changes, update:

```text
docs/JSONSchema.md
docs/DecisionLog.md
```

---

## 47. Pipeline and engine versions

Render report should include engine version.

Example:

```json
{
  "engine_version": "0.1.0"
}
```

Engine version is not the same as schema version.

---

## 48. Pipeline and template versions

Template version should be recorded.

Example:

```json
{
  "template": {
    "name": "tiktok_dark_comic",
    "version": "0.1.0"
  }
}
```

This helps explain visual differences after template changes.

---

## 49. Pipeline and model versions

Reports should record:

```json
{
  "speech_model": "medium",
  "director_model": "qwen2.5:3b",
  "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2"
}
```

Model changes can change output.

---

## 50. Pipeline and prompts versions

Director output should record prompt version or prompt hash.

Example:

```json
{
  "prompt": {
    "name": "visual_director",
    "version": "0.1.0"
  }
}
```

Prompt changes can alter results even if model stays the same.

---

## 51. Pipeline and deterministic random seed

If renderer uses random values, timeline or config should include seed.

Example:

```json
{
  "render_seed": 12345
}
```

Without a seed, exact reproducibility is harder.

---

## 52. Pipeline and localization

Vietnamese is first-class.

Pipeline should preserve UTF-8.

JSON should be written with Vietnamese characters, not escaped unnecessarily.

Use:

```python
ensure_ascii=False
```

when writing JSON.

---

## 53. Pipeline and file encoding

All text files should use:

```text
UTF-8
```

This includes:

- JSON
- Markdown
- prompts
- config
- logs

---

## 54. Pipeline and Windows paths

Use `pathlib.Path`.

Avoid hardcoded slash assumptions.

Do not assume paths have no spaces.

FFmpeg subprocess calls should pass argument lists.

---

## 55. Pipeline and subprocess

Use:

```python
subprocess.run([...], check=True)
```

Avoid:

```python
subprocess.run("ffmpeg ...", shell=True)
```

unless there is a specific reason.

---

## 56. Pipeline and user experience

Beginner-friendly behavior matters.

If a dependency is missing, tell the user exactly what to do.

Bad:

```text
FileNotFoundError
```

Good:

```text
FFmpeg was not found.
Install it with:
winget install Gyan.FFmpeg
Then restart VS Code.
```

---

## 57. Pipeline and Codex

Codex should be able to understand the pipeline by reading:

```text
AGENTS.md
PROJECT_RULES.md
docs/Pipeline.md
docs/JSONSchema.md
```

Do not rely on chat memory.

---

## 58. Pipeline and future UI

Future UI can expose pipeline stages:

- Upload video
- Transcribe
- Edit transcript
- Generate visual script
- Edit timeline
- Preview
- Render
- Export

Because intermediate JSON exists, UI can edit without changing core architecture.

---

## 59. Pipeline and future API

Future API endpoints may map to stages:

```text
POST /extract-audio
POST /transcribe
POST /timeline
POST /direct
POST /render
POST /export
POST /build
```

Core logic should remain independent of API framework.

---

## 60. Pipeline and recruitment use cases

Future recruitment workflow:

```text
job description
      ↓
script generator
      ↓
visual director
      ↓
renderer
      ↓
recruitment video
```

Future candidate workflow:

```text
CV
      ↓
summary script
      ↓
voice or original audio
      ↓
visual timeline
      ↓
video
```

The same engine should support these through templates and pipeline modes.

---

## 61. Minimum V1 pipeline

The minimum useful V1 is:

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

V1 can be simple visually.

Correct pipeline matters more than flashy animation.

---

## 62. Sprint 1 detailed pipeline

Sprint 1 includes:

```text
Validate Input
Extract Audio
Speech To Text
Write Transcript JSON
```

### Sprint 1 input

```text
input/video.mp4
```

### Sprint 1 output

```text
temp/audio.wav
output/transcript.json
```

### Sprint 1 success criteria

- Works on Windows
- Uses FFmpeg
- Uses Faster Whisper
- Supports Vietnamese
- Writes valid JSON
- Does not require GPU
- Does not call LLM
- Has clear errors

---

## 63. Sprint 2 detailed pipeline

Sprint 2 includes:

```text
Read Transcript JSON
Validate Transcript
Normalize Timeline
Write Normalized Timeline JSON
```

### Sprint 2 input

```text
output/transcript.json
```

### Sprint 2 output

```text
output/timeline.normalized.json
```

### Sprint 2 success criteria

- scene IDs created
- durations computed
- scenes sorted
- long segments handled
- short segments handled
- schema validation exists

---

## 64. Sprint 3 detailed pipeline

Sprint 3 includes:

```text
Read Normalized Timeline
Load Visual Director Prompt
Call Ollama
Parse JSON
Validate Director Output
Write Director Timeline
```

### Sprint 3 input

```text
output/timeline.normalized.json
```

### Sprint 3 output

```text
output/timeline.director.json
```

### Sprint 3 success criteria

- LLM returns JSON
- JSON validates
- keywords exist
- effects exist
- icon_query exists
- no renderer dependency

---

## 65. Sprint 4 detailed pipeline

Sprint 4 includes:

```text
Read Director Timeline
Load Icon DB
Build/Load Embeddings
Search Icons
Write Visual Timeline
```

### Sprint 4 input

```text
output/timeline.director.json
assets/icons/icon_db.json
```

### Sprint 4 output

```text
output/timeline.visual.json
```

### Sprint 4 success criteria

- icon_query maps to icon_id
- icon path exists
- score stored
- no exact filename guessing by LLM

---

## 66. Sprint 5 detailed pipeline

Sprint 5 includes:

```text
Read Visual Timeline
Validate Renderer Input
Load Template
Render Scenes
Write Silent Video
```

### Sprint 5 input

```text
output/timeline.visual.json
```

### Sprint 5 output

```text
output/silent_video.mp4
```

### Sprint 5 success criteria

- 1080x1920 output
- readable text
- keyword highlight
- at least one animation
- no LLM calls

---

## 67. Sprint 6 detailed pipeline

Sprint 6 includes:

```text
Read Silent Video
Read Original Audio
Merge Audio/Video
Write Final MP4
Write Render Report
```

### Sprint 6 input

```text
output/silent_video.mp4
temp/audio.wav
```

### Sprint 6 output

```text
output/final.mp4
output/render_report.json
```

### Sprint 6 success criteria

- final video has audio
- original voice preserved
- duration acceptable
- report exists

---

## 68. Pipeline quality gates

A quality gate is a required check before moving forward.

### Gate 1

Input media exists.

### Gate 2

Audio extracted.

### Gate 3

Transcript valid.

### Gate 4

Normalized timeline valid.

### Gate 5

Director JSON valid.

### Gate 6

Visual timeline valid.

### Gate 7

Silent video exists.

### Gate 8

Final video exists and has audio.

---

## 69. Pipeline command examples

### Full build

```bash
ai-video build input/video.mp4
```

### Reuse transcript

```bash
ai-video build input/video.mp4 --reuse-transcript
```

### Render from existing visual timeline

```bash
ai-video render output/timeline.visual.json
```

### Export only

```bash
ai-video export output/silent_video.mp4 temp/audio.wav
```

### Preview

```bash
ai-video build input/video.mp4 --preview
```

### Debug

```bash
ai-video build input/video.mp4 --debug
```

---

## 70. Pipeline logs example

```text
[00:00] AI Video Engine started
[00:00] input: input/video.mp4
[00:01] validating input
[00:01] extracting audio
[00:04] audio written: temp/audio.wav
[00:04] loading Faster Whisper model: medium
[00:18] transcript written: output/transcript.json
[00:18] validating transcript
[00:19] normalizing timeline
[00:19] timeline written: output/timeline.normalized.json
[00:20] calling visual director: qwen2.5:3b
[00:24] director timeline written: output/timeline.director.json
[00:25] matching icons
[00:26] visual timeline written: output/timeline.visual.json
[00:26] rendering silent video
[00:38] silent video written: output/silent_video.mp4
[00:39] merging audio
[00:40] final video written: output/final.mp4
```

---

## 71. Pipeline report example

```json
{
  "schema_version": "0.1.0",
  "engine_version": "0.1.0",
  "input": "input/video.mp4",
  "output": "output/final.mp4",
  "stages": [
    {
      "name": "validate_input",
      "status": "success",
      "duration_sec": 0.1
    },
    {
      "name": "extract_audio",
      "status": "success",
      "duration_sec": 3.2
    },
    {
      "name": "speech_to_text",
      "status": "success",
      "duration_sec": 14.1
    }
  ],
  "warnings": [],
  "errors": []
}
```

---

## 72. Pipeline anti-patterns

Avoid:

### Anti-pattern 1

Single script that does everything.

### Anti-pattern 2

LLM returns prose and renderer parses it.

### Anti-pattern 3

Renderer calls the LLM.

### Anti-pattern 4

No intermediate files.

### Anti-pattern 5

Hardcoded local paths.

### Anti-pattern 6

No schema validation.

### Anti-pattern 7

Skipping reports.

### Anti-pattern 8

Committing output videos.

### Anti-pattern 9

Changing prompt behavior without documentation.

### Anti-pattern 10

Building advanced animations before the basic pipeline works.

---

## 73. Pipeline design checklist

Before implementing a stage, answer:

1. What is the input?
2. What is the output?
3. Where is the output saved?
4. What module owns it?
5. What validation is required?
6. What errors can happen?
7. Can it be run independently?
8. Does it require AI?
9. Does it require FFmpeg?
10. Does it preserve architecture rules?

---

## 74. Pipeline implementation checklist

Before committing a pipeline stage:

- code exists
- output file exists
- errors are clear
- docs updated
- tests added where practical
- no hardcoded absolute paths
- no large files committed
- JSON is UTF-8
- Windows path handling works
- README or sprint doc updated

---

## 75. Final pipeline rule

The pipeline should always be understandable from files in the repository.

If a future developer cannot understand what happens by reading:

```text
AGENTS.md
PROJECT_RULES.md
docs/Architecture.md
docs/Pipeline.md
docs/JSONSchema.md
```

then the documentation is incomplete.
