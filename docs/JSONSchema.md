# JSONSchema.md

# AI Video Engine - JSON Schema Design

## 0. Purpose

This document defines the JSON data contracts used by **AI Video Engine**.

The JSON files are the backbone of the project.

They allow the pipeline to be:

- inspectable
- resumable
- debuggable
- editable
- testable
- compatible with AI agents
- compatible with future UI/API layers

The renderer must consume structured JSON.

The AI Director must produce structured JSON.

The pipeline must validate structured JSON at stage boundaries.

This document should be read together with:

```text
AGENTS.md
PROJECT_RULES.md
docs/Architecture.md
docs/Pipeline.md
docs/AIDesign.md
docs/RendererDesign.md
```

---

## 1. Core principle

The most important contract in the project is:

```text
AI produces JSON.
Renderer consumes JSON.
```

The renderer must not consume raw LLM prose.

The renderer must not infer visual intent from natural language.

The renderer should receive all needed instructions through validated JSON.

---

## 2. JSON files in the pipeline

The default pipeline uses these JSON files:

```text
output/transcript.json
output/timeline.normalized.json
output/timeline.director.json
output/timeline.visual.json
output/render_report.json
```

Optional future files:

```text
output/transcript.validation.json
output/timeline.validation.json
output/debug/llm_raw_response.json
output/debug/prompt_input.json
output/debug/scene_previews.json
```

---

## 3. Schema maturity levels

The project may use schema maturity levels.

### Level 0 - Draft

Used during early prototyping.

Fields may change.

### Level 1 - Internal stable

Used by internal modules.

Fields are documented.

Validation exists.

### Level 2 - Public stable

Used by UI, API, plugins, or external tools.

Breaking changes require migration.

### Level 3 - Versioned contract

Used after v1.0.

Backward compatibility matters.

---

## 4. Schema versioning

Every major JSON file must include:

```json
{
  "schema_version": "0.1.0"
}
```

Schema version is not the same as engine version.

Example:

```json
{
  "schema_version": "0.1.0",
  "engine_version": "0.1.0"
}
```

### 4.1 When to change schema version

Change schema version when:

- required fields change
- field meaning changes
- enum values change
- object nesting changes
- renderer input contract changes
- output report structure changes

### 4.2 Where to document schema changes

Schema changes must be documented in:

```text
docs/JSONSchema.md
docs/DecisionLog.md
CHANGELOG.md
```

---

## 5. Encoding rules

All JSON files must be UTF-8.

Vietnamese characters should remain readable.

When writing JSON in Python, use:

```python
json.dumps(data, ensure_ascii=False, indent=2)
```

or with `orjson`, configure equivalent behavior.

Do not write escaped Vietnamese unnecessarily.

Good:

```json
{
  "text": "Tại báo thức!"
}
```

Bad:

```json
{
  "text": "T\u1ea1i b\u00e1o th\u1ee9c!"
}
```

The escaped version is valid JSON, but less readable.

---

## 6. Time format rules

All time values are seconds.

Use float seconds.

Example:

```json
{
  "start": 0.25,
  "end": 2.16,
  "duration": 1.91
}
```

Do not use:

```text
00:00:02.160
```

inside core JSON.

Human-readable timestamps may be added in reports, but the core schema uses seconds.

---

## 7. ID naming rules

IDs should be stable and predictable.

### 7.1 Segment IDs

```text
seg_0001
seg_0002
seg_0003
```

### 7.2 Scene IDs

```text
scene_0001
scene_0002
scene_0003
```

### 7.3 Speaker IDs

```text
SPEAKER_00
SPEAKER_01
SPEAKER_02
```

### 7.4 Icon IDs

```text
icon_alarm_001
icon_sleep_001
icon_money_001
```

### 7.5 Animation IDs

```text
anim_0001
anim_0002
```

### 7.6 Run IDs

```text
run_20260707_001
```

---

## 8. Top-level metadata pattern

Most JSON files should include metadata.

Example:

```json
{
  "schema_version": "0.1.0",
  "metadata": {
    "created_at": "2026-07-07T15:00:00Z",
    "engine_version": "0.1.0",
    "source": "input/video.mp4"
  }
}
```

Metadata should not be required for the renderer unless needed.

Renderer-required fields should be separate from informational metadata.

---

## 9. Common primitive types

### 9.1 Seconds

```json
{
  "type": "number",
  "minimum": 0
}
```

Used for:

- start
- end
- duration
- start_offset
- end_offset

### 9.2 Confidence

```json
{
  "type": "number",
  "minimum": 0,
  "maximum": 1
}
```

Used for:

- speaker confidence
- keyword confidence
- icon match score
- AI classification confidence

### 9.3 Relative path

```json
{
  "type": "string"
}
```

Paths should usually be repository-relative.

Example:

```text
assets/icons/alarm.png
```

Avoid absolute paths in committed JSON.

### 9.4 Enum string

Controlled string values.

Example:

```json
{
  "type": "string",
  "enum": ["neutral", "happy", "surprised"]
}
```

---

## 10. Common object: SourceReference

Represents source files used by a JSON file.

Example:

```json
{
  "input_video": "input/video.mp4",
  "source_audio": "temp/audio.wav",
  "transcript": "output/transcript.json"
}
```

Suggested schema:

```json
{
  "type": "object",
  "properties": {
    "input_video": { "type": "string" },
    "source_audio": { "type": "string" },
    "transcript": { "type": "string" },
    "normalized_timeline": { "type": "string" },
    "visual_timeline": { "type": "string" }
  },
  "additionalProperties": true
}
```

---

## 11. Common object: Speaker

Speaker object should be stable across pipeline stages.

### 11.1 Minimal speaker

```json
{
  "id": "SPEAKER_00"
}
```

### 11.2 Full speaker

```json
{
  "id": "SPEAKER_00",
  "label": "Nam",
  "source": "manual",
  "confidence": 0.92,
  "style": "speaker_a"
}
```

### 11.3 Speaker fields

| Field | Type | Required | Description |
|---|---|---:|---|
| id | string | yes | Internal speaker ID |
| label | string/null | no | Human-friendly label |
| source | string | no | unknown/manual/diarization/inferred |
| confidence | number/null | no | confidence 0-1 |
| style | string/null | no | template speaker style key |

### 11.4 Speaker source enum

Allowed values:

```text
unknown
manual
diarization
inferred
inferred_alternating
script
```

### 11.5 Speaker schema

```json
{
  "$id": "Speaker",
  "type": "object",
  "required": ["id"],
  "properties": {
    "id": {
      "type": "string"
    },
    "label": {
      "type": ["string", "null"]
    },
    "source": {
      "type": "string",
      "enum": [
        "unknown",
        "manual",
        "diarization",
        "inferred",
        "inferred_alternating",
        "script"
      ]
    },
    "confidence": {
      "type": ["number", "null"],
      "minimum": 0,
      "maximum": 1
    },
    "style": {
      "type": ["string", "null"]
    }
  },
  "additionalProperties": false
}
```

---

## 12. Common object: VideoSpec

Defines output video settings.

Example:

```json
{
  "width": 1080,
  "height": 1920,
  "fps": 30,
  "aspect_ratio": "9:16"
}
```

Schema:

```json
{
  "$id": "VideoSpec",
  "type": "object",
  "required": ["width", "height", "fps"],
  "properties": {
    "width": {
      "type": "integer",
      "minimum": 1
    },
    "height": {
      "type": "integer",
      "minimum": 1
    },
    "fps": {
      "type": "number",
      "minimum": 1
    },
    "aspect_ratio": {
      "type": "string"
    },
    "codec": {
      "type": "string"
    },
    "pixel_format": {
      "type": "string"
    }
  },
  "additionalProperties": false
}
```

Default:

```json
{
  "width": 1080,
  "height": 1920,
  "fps": 30,
  "aspect_ratio": "9:16",
  "codec": "h264"
}
```

---

## 13. Common object: AudioSpec

Defines audio settings.

Example:

```json
{
  "sample_rate": 16000,
  "channels": 1,
  "format": "wav"
}
```

Schema:

```json
{
  "$id": "AudioSpec",
  "type": "object",
  "properties": {
    "sample_rate": {
      "type": "integer",
      "minimum": 1
    },
    "channels": {
      "type": "integer",
      "minimum": 1
    },
    "format": {
      "type": "string"
    },
    "codec": {
      "type": "string"
    }
  },
  "additionalProperties": false
}
```

---

## 14. Common object: TemplateReference

References a visual template.

Example:

```json
{
  "name": "tiktok_dark_comic",
  "version": "0.1.0"
}
```

Schema:

```json
{
  "$id": "TemplateReference",
  "type": "object",
  "required": ["name"],
  "properties": {
    "name": {
      "type": "string"
    },
    "version": {
      "type": "string"
    }
  },
  "additionalProperties": false
}
```

---

## 15. Common object: ValidationError

Used in validation reports.

Example:

```json
{
  "path": "scenes[3].animations[0].type",
  "message": "Unknown effect: explode_spin",
  "severity": "error"
}
```

Schema:

```json
{
  "$id": "ValidationError",
  "type": "object",
  "required": ["path", "message", "severity"],
  "properties": {
    "path": {
      "type": "string"
    },
    "message": {
      "type": "string"
    },
    "severity": {
      "type": "string",
      "enum": ["info", "warning", "error"]
    },
    "code": {
      "type": "string"
    }
  },
  "additionalProperties": false
}
```

---

## 16. Transcript JSON

### 16.1 Purpose

`transcript.json` is the raw output from speech-to-text.

It should not contain visual instructions.

It should preserve speech timing.

### 16.2 File path

```text
output/transcript.json
```

### 16.3 Producer

```text
src/speech/
```

### 16.4 Consumer

```text
src/timeline/
```

### 16.5 Example

```json
{
  "schema_version": "0.1.0",
  "metadata": {
    "engine_version": "0.1.0",
    "created_at": "2026-07-07T15:00:00Z",
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

## 17. TranscriptSegment

### 17.1 Purpose

Represents one speech-to-text segment.

### 17.2 Required fields

```text
id
start
end
duration
text
```

### 17.3 Optional fields

```text
speaker
words
confidence
no_speech_probability
```

### 17.4 Example

```json
{
  "id": "seg_0001",
  "start": 0.25,
  "end": 2.16,
  "duration": 1.91,
  "text": "Ê! Sao hôm nay đến trễ?",
  "speaker": {
    "id": "SPEAKER_00",
    "source": "diarization",
    "confidence": 0.91
  }
}
```

### 17.5 Schema

```json
{
  "$id": "TranscriptSegment",
  "type": "object",
  "required": ["id", "start", "end", "duration", "text"],
  "properties": {
    "id": {
      "type": "string"
    },
    "start": {
      "type": "number",
      "minimum": 0
    },
    "end": {
      "type": "number",
      "exclusiveMinimum": 0
    },
    "duration": {
      "type": "number",
      "exclusiveMinimum": 0
    },
    "text": {
      "type": "string",
      "minLength": 1
    },
    "speaker": {
      "$ref": "#/$defs/Speaker"
    },
    "words": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/WordTiming"
      }
    },
    "confidence": {
      "type": ["number", "null"],
      "minimum": 0,
      "maximum": 1
    },
    "no_speech_probability": {
      "type": ["number", "null"],
      "minimum": 0,
      "maximum": 1
    }
  },
  "additionalProperties": false
}
```

---

## 18. WordTiming

### 18.1 Purpose

Optional word-level timing.

Not required for early V1.

Useful later for word-level animation.

### 18.2 Example

```json
{
  "text": "ĐẾN",
  "start": 1.12,
  "end": 1.30,
  "confidence": 0.93
}
```

### 18.3 Schema

```json
{
  "$id": "WordTiming",
  "type": "object",
  "required": ["text", "start", "end"],
  "properties": {
    "text": {
      "type": "string",
      "minLength": 1
    },
    "start": {
      "type": "number",
      "minimum": 0
    },
    "end": {
      "type": "number",
      "exclusiveMinimum": 0
    },
    "confidence": {
      "type": ["number", "null"],
      "minimum": 0,
      "maximum": 1
    }
  },
  "additionalProperties": false
}
```

---

## 19. Transcript JSON full schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "Transcript",
  "type": "object",
  "required": ["schema_version", "segments"],
  "properties": {
    "schema_version": {
      "type": "string"
    },
    "metadata": {
      "type": "object",
      "additionalProperties": true
    },
    "segments": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/TranscriptSegment"
      }
    }
  },
  "$defs": {
    "TranscriptSegment": {
      "type": "object",
      "required": ["id", "start", "end", "duration", "text"],
      "properties": {
        "id": { "type": "string" },
        "start": { "type": "number", "minimum": 0 },
        "end": { "type": "number", "exclusiveMinimum": 0 },
        "duration": { "type": "number", "exclusiveMinimum": 0 },
        "text": { "type": "string", "minLength": 1 }
      },
      "additionalProperties": true
    }
  },
  "additionalProperties": false
}
```

---

## 20. Transcript validation rules

Validation must check:

1. JSON parses.
2. `schema_version` exists.
3. `segments` exists and is an array.
4. Every segment has unique ID.
5. `start >= 0`.
6. `end > start`.
7. `duration > 0`.
8. `duration ≈ end - start`.
9. Text is not empty.
10. Segments are sorted by start time.
11. Overlaps are handled or reported.

---

## 21. Normalized Timeline JSON

### 21.1 Purpose

`timeline.normalized.json` is the deterministic timeline created from transcript.

It prepares data for the Visual Director.

It should not contain final visual decisions.

### 21.2 File path

```text
output/timeline.normalized.json
```

### 21.3 Producer

```text
src/timeline/
```

### 21.4 Consumer

```text
src/director/
```

### 21.5 Example

```json
{
  "schema_version": "0.1.0",
  "metadata": {
    "created_at": "2026-07-07T15:00:00Z",
    "source_transcript": "output/transcript.json"
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

---

## 22. NormalizedScene

### 22.1 Required fields

```text
id
source_segment_ids
start
end
duration
text
```

### 22.2 Optional fields

```text
speaker
words
notes
```

### 22.3 Schema

```json
{
  "$id": "NormalizedScene",
  "type": "object",
  "required": [
    "id",
    "source_segment_ids",
    "start",
    "end",
    "duration",
    "text"
  ],
  "properties": {
    "id": {
      "type": "string"
    },
    "source_segment_ids": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "start": {
      "type": "number",
      "minimum": 0
    },
    "end": {
      "type": "number",
      "exclusiveMinimum": 0
    },
    "duration": {
      "type": "number",
      "exclusiveMinimum": 0
    },
    "speaker": {
      "$ref": "#/$defs/Speaker"
    },
    "text": {
      "type": "string",
      "minLength": 1
    },
    "words": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/WordTiming"
      }
    },
    "notes": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "additionalProperties": false
}
```

---

## 23. Normalized timeline validation rules

Check:

1. Scene IDs are unique.
2. Scenes are sorted by start time.
3. Every scene has valid duration.
4. Every scene text is non-empty.
5. Source segment IDs exist in transcript.
6. Scene duration matches end-start.
7. No scene has negative time.
8. Scene count is reasonable.
9. Speaker field is valid if present.
10. Word timings are inside scene boundaries if present.

---

## 24. Director Timeline JSON

### 24.1 Purpose

`timeline.director.json` is AI-enriched but may not yet have actual asset matches.

It contains visual direction from LLM.

### 24.2 File path

```text
output/timeline.director.json
```

### 24.3 Producer

```text
src/director/
```

### 24.4 Consumer

```text
src/embedding/
```

### 24.5 Example

```json
{
  "schema_version": "0.1.0",
  "metadata": {
    "director_model": "qwen2.5:3b",
    "prompt_name": "visual_director",
    "prompt_version": "0.1.0"
  },
  "template": {
    "name": "tiktok_dark_comic",
    "version": "0.1.0"
  },
  "video": {
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "aspect_ratio": "9:16"
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
        "label": "Nam",
        "source": "manual",
        "style": "speaker_a"
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
          "style": "keyword_primary"
        }
      ],
      "assets": {
        "icon_query": "đồng hồ báo thức"
      },
      "transition": {
        "type": "cut"
      }
    }
  ]
}
```

---

## 25. VisualScene

VisualScene is the main renderer-ready scene object after icon selection.

### 25.1 Required fields

```text
id
start
end
duration
text
lines
layout
keywords
```

### 25.2 Recommended fields

```text
speaker
emotion
assets
animations
transition
style
```

### 25.3 Example

```json
{
  "id": "scene_0001",
  "start": 0.25,
  "end": 2.16,
  "duration": 1.91,
  "speaker": {
    "id": "SPEAKER_00",
    "label": "Nam",
    "style": "speaker_a"
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
      "style": "keyword_primary"
    }
  ],
  "assets": {
    "icon_query": "đồng hồ báo thức",
    "icon_id": "icon_alarm_001",
    "icon_path": "assets/icons/alarm.png",
    "icon_score": 0.87
  },
  "animations": [
    {
      "id": "anim_0001",
      "target": {
        "type": "keyword",
        "text": "ĐẾN TRỄ"
      },
      "type": "pop",
      "start_offset": 1.1,
      "duration": 0.35,
      "params": {
        "scale": 1.25
      }
    }
  ],
  "transition": {
    "type": "cut"
  }
}
```

---

## 26. Display lines

### 26.1 Purpose

`lines` controls how text appears on screen.

It is not necessarily identical to raw transcript.

Example:

```json
"lines": ["Ê!", "SAO HÔM NAY", "ĐẾN TRỄ?"]
```

### 26.2 Rules

- Should be readable.
- Usually 1 to 4 lines.
- Uppercase is allowed.
- Must preserve meaning.
- Should not be too long.

### 26.3 Schema

```json
{
  "$id": "DisplayLines",
  "type": "array",
  "minItems": 1,
  "maxItems": 6,
  "items": {
    "type": "string",
    "minLength": 1
  }
}
```

---

## 27. Emotion

### 27.1 Purpose

Emotion helps select avatar, colors, and animation defaults.

### 27.2 Initial enum

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

### 27.3 Schema

```json
{
  "$id": "Emotion",
  "type": "string",
  "enum": [
    "neutral",
    "happy",
    "surprised",
    "confused",
    "angry",
    "funny",
    "sad",
    "serious",
    "dramatic",
    "excited"
  ]
}
```

---

## 28. Layout

### 28.1 Purpose

Layout defines where visual elements go.

### 28.2 Example

```json
{
  "name": "center_stack",
  "params": {
    "vertical_align": "center"
  }
}
```

### 28.3 Initial layout names

```text
center_stack
punchline_center
speaker_label_top
comic_panel
split_speaker
avatar_left_text_right
```

### 28.4 Schema

```json
{
  "$id": "Layout",
  "type": "object",
  "required": ["name"],
  "properties": {
    "name": {
      "type": "string",
      "enum": [
        "center_stack",
        "punchline_center",
        "speaker_label_top",
        "comic_panel",
        "split_speaker",
        "avatar_left_text_right"
      ]
    },
    "params": {
      "type": "object",
      "additionalProperties": true
    }
  },
  "additionalProperties": false
}
```

---

## 29. Keyword

### 29.1 Purpose

A keyword is a text target for emphasis.

### 29.2 Example

```json
{
  "text": "BÁO THỨC",
  "importance": 0.98,
  "effect": "shake",
  "style": "keyword_primary"
}
```

### 29.3 Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| text | string | yes | target keyword |
| importance | number | no | 0-1 importance |
| effect | string | no | effect name |
| style | string | no | visual style key |
| conceptual | boolean | no | true if not literal text |
| confidence | number | no | AI confidence |

### 29.4 Schema

```json
{
  "$id": "Keyword",
  "type": "object",
  "required": ["text"],
  "properties": {
    "text": {
      "type": "string",
      "minLength": 1
    },
    "importance": {
      "type": ["number", "null"],
      "minimum": 0,
      "maximum": 1
    },
    "effect": {
      "type": ["string", "null"]
    },
    "style": {
      "type": ["string", "null"]
    },
    "conceptual": {
      "type": "boolean"
    },
    "confidence": {
      "type": ["number", "null"],
      "minimum": 0,
      "maximum": 1
    }
  },
  "additionalProperties": false
}
```

---

## 30. Animation

### 30.1 Purpose

Animation describes motion or emphasis over time.

### 30.2 Example

```json
{
  "id": "anim_0001",
  "target": {
    "type": "keyword",
    "text": "ĐẾN TRỄ"
  },
  "type": "pop",
  "start_offset": 1.1,
  "duration": 0.35,
  "params": {
    "scale": 1.25
  }
}
```

### 30.3 Initial animation types

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

### 30.4 Target types

```text
scene
line
keyword
icon
avatar
speaker_label
background
```

### 30.5 Animation schema

```json
{
  "$id": "Animation",
  "type": "object",
  "required": ["type", "target"],
  "properties": {
    "id": {
      "type": "string"
    },
    "target": {
      "$ref": "#/$defs/AnimationTarget"
    },
    "type": {
      "type": "string",
      "enum": [
        "pop",
        "bounce",
        "shake",
        "glow",
        "slide",
        "fade",
        "pulse",
        "typewriter",
        "zoom"
      ]
    },
    "start_offset": {
      "type": "number",
      "minimum": 0
    },
    "duration": {
      "type": "number",
      "exclusiveMinimum": 0
    },
    "params": {
      "type": "object",
      "additionalProperties": true
    }
  },
  "additionalProperties": false
}
```

---

## 31. AnimationTarget

### 31.1 Example

```json
{
  "type": "keyword",
  "text": "ĐẾN TRỄ"
}
```

### 31.2 Schema

```json
{
  "$id": "AnimationTarget",
  "type": "object",
  "required": ["type"],
  "properties": {
    "type": {
      "type": "string",
      "enum": [
        "scene",
        "line",
        "keyword",
        "icon",
        "avatar",
        "speaker_label",
        "background"
      ]
    },
    "id": {
      "type": "string"
    },
    "text": {
      "type": "string"
    },
    "index": {
      "type": "integer",
      "minimum": 0
    }
  },
  "additionalProperties": false
}
```

---

## 32. AssetReference

### 32.1 Purpose

Stores visual/audio asset references for a scene.

### 32.2 Example

```json
{
  "icon_query": "báo thức",
  "icon_id": "icon_alarm_001",
  "icon_path": "assets/icons/alarm.png",
  "icon_score": 0.87,
  "avatar_id": "avatar_male_surprised",
  "background_id": "bg_dark_001"
}
```

### 32.3 Schema

```json
{
  "$id": "AssetReference",
  "type": "object",
  "properties": {
    "icon_query": {
      "type": ["string", "null"]
    },
    "icon_id": {
      "type": ["string", "null"]
    },
    "icon_path": {
      "type": ["string", "null"]
    },
    "icon_score": {
      "type": ["number", "null"],
      "minimum": 0,
      "maximum": 1
    },
    "avatar_id": {
      "type": ["string", "null"]
    },
    "avatar_path": {
      "type": ["string", "null"]
    },
    "background_id": {
      "type": ["string", "null"]
    },
    "background_path": {
      "type": ["string", "null"]
    },
    "sfx_id": {
      "type": ["string", "null"]
    },
    "sfx_path": {
      "type": ["string", "null"]
    }
  },
  "additionalProperties": false
}
```

---

## 33. Transition

### 33.1 Purpose

Controls scene transition.

### 33.2 Initial transition types

```text
cut
fade
slide
zoom
none
```

### 33.3 Example

```json
{
  "type": "cut"
}
```

### 33.4 Schema

```json
{
  "$id": "Transition",
  "type": "object",
  "required": ["type"],
  "properties": {
    "type": {
      "type": "string",
      "enum": ["cut", "fade", "slide", "zoom", "none"]
    },
    "duration": {
      "type": "number",
      "minimum": 0
    },
    "params": {
      "type": "object",
      "additionalProperties": true
    }
  },
  "additionalProperties": false
}
```

---

## 34. Visual Timeline JSON

### 34.1 Purpose

`timeline.visual.json` is the renderer input.

This is one of the most important files in the project.

### 34.2 File path

```text
output/timeline.visual.json
```

### 34.3 Producer

```text
src/embedding/
```

or after visual director if no icon selector is used.

### 34.4 Consumer

```text
src/renderer/
```

### 34.5 Example

```json
{
  "schema_version": "0.1.0",
  "metadata": {
    "engine_version": "0.1.0",
    "created_at": "2026-07-07T15:00:00Z",
    "source_input": "input/video.mp4",
    "source_audio": "temp/audio.wav",
    "source_transcript": "output/transcript.json"
  },
  "template": {
    "name": "tiktok_dark_comic",
    "version": "0.1.0"
  },
  "video": {
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "aspect_ratio": "9:16"
  },
  "render_seed": 12345,
  "scenes": [
    {
      "id": "scene_0001",
      "source_segment_ids": ["seg_0001"],
      "start": 0.25,
      "end": 2.16,
      "duration": 1.91,
      "speaker": {
        "id": "SPEAKER_00",
        "label": "Nam",
        "source": "manual",
        "style": "speaker_a"
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
          "style": "keyword_primary"
        }
      ],
      "assets": {
        "icon_query": "đồng hồ báo thức",
        "icon_id": "icon_alarm_001",
        "icon_path": "assets/icons/alarm.png",
        "icon_score": 0.87
      },
      "animations": [
        {
          "id": "anim_0001",
          "target": {
            "type": "keyword",
            "text": "ĐẾN TRỄ"
          },
          "type": "pop",
          "start_offset": 1.1,
          "duration": 0.35,
          "params": {
            "scale": 1.25
          }
        }
      ],
      "transition": {
        "type": "cut"
      }
    }
  ]
}
```

---

## 35. VisualTimeline schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "VisualTimeline",
  "type": "object",
  "required": [
    "schema_version",
    "template",
    "video",
    "scenes"
  ],
  "properties": {
    "schema_version": {
      "type": "string"
    },
    "metadata": {
      "type": "object",
      "additionalProperties": true
    },
    "template": {
      "$ref": "#/$defs/TemplateReference"
    },
    "video": {
      "$ref": "#/$defs/VideoSpec"
    },
    "render_seed": {
      "type": ["integer", "null"]
    },
    "scenes": {
      "type": "array",
      "minItems": 1,
      "items": {
        "$ref": "#/$defs/VisualScene"
      }
    }
  },
  "additionalProperties": false,
  "$defs": {
    "TemplateReference": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": { "type": "string" },
        "version": { "type": "string" }
      },
      "additionalProperties": false
    },
    "VideoSpec": {
      "type": "object",
      "required": ["width", "height", "fps"],
      "properties": {
        "width": { "type": "integer", "minimum": 1 },
        "height": { "type": "integer", "minimum": 1 },
        "fps": { "type": "number", "minimum": 1 },
        "aspect_ratio": { "type": "string" },
        "codec": { "type": "string" }
      },
      "additionalProperties": false
    },
    "VisualScene": {
      "type": "object",
      "required": [
        "id",
        "start",
        "end",
        "duration",
        "text",
        "lines",
        "layout",
        "keywords"
      ],
      "properties": {
        "id": { "type": "string" },
        "source_segment_ids": {
          "type": "array",
          "items": { "type": "string" }
        },
        "start": { "type": "number", "minimum": 0 },
        "end": { "type": "number", "exclusiveMinimum": 0 },
        "duration": { "type": "number", "exclusiveMinimum": 0 },
        "speaker": { "$ref": "#/$defs/Speaker" },
        "text": { "type": "string", "minLength": 1 },
        "lines": {
          "type": "array",
          "minItems": 1,
          "items": { "type": "string", "minLength": 1 }
        },
        "emotion": { "$ref": "#/$defs/Emotion" },
        "layout": { "$ref": "#/$defs/Layout" },
        "keywords": {
          "type": "array",
          "items": { "$ref": "#/$defs/Keyword" }
        },
        "assets": { "$ref": "#/$defs/AssetReference" },
        "animations": {
          "type": "array",
          "items": { "$ref": "#/$defs/Animation" }
        },
        "transition": { "$ref": "#/$defs/Transition" },
        "style": {
          "type": "object",
          "additionalProperties": true
        }
      },
      "additionalProperties": false
    },
    "Speaker": {
      "type": "object",
      "required": ["id"],
      "properties": {
        "id": { "type": "string" },
        "label": { "type": ["string", "null"] },
        "source": { "type": "string" },
        "confidence": { "type": ["number", "null"], "minimum": 0, "maximum": 1 },
        "style": { "type": ["string", "null"] }
      },
      "additionalProperties": false
    },
    "Emotion": {
      "type": "string",
      "enum": [
        "neutral",
        "happy",
        "surprised",
        "confused",
        "angry",
        "funny",
        "sad",
        "serious",
        "dramatic",
        "excited"
      ]
    },
    "Layout": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": { "type": "string" },
        "params": {
          "type": "object",
          "additionalProperties": true
        }
      },
      "additionalProperties": false
    },
    "Keyword": {
      "type": "object",
      "required": ["text"],
      "properties": {
        "text": { "type": "string", "minLength": 1 },
        "importance": { "type": ["number", "null"], "minimum": 0, "maximum": 1 },
        "effect": { "type": ["string", "null"] },
        "style": { "type": ["string", "null"] },
        "conceptual": { "type": "boolean" },
        "confidence": { "type": ["number", "null"], "minimum": 0, "maximum": 1 }
      },
      "additionalProperties": false
    },
    "AssetReference": {
      "type": "object",
      "properties": {
        "icon_query": { "type": ["string", "null"] },
        "icon_id": { "type": ["string", "null"] },
        "icon_path": { "type": ["string", "null"] },
        "icon_score": { "type": ["number", "null"], "minimum": 0, "maximum": 1 },
        "avatar_id": { "type": ["string", "null"] },
        "avatar_path": { "type": ["string", "null"] },
        "background_id": { "type": ["string", "null"] },
        "background_path": { "type": ["string", "null"] },
        "sfx_id": { "type": ["string", "null"] },
        "sfx_path": { "type": ["string", "null"] }
      },
      "additionalProperties": false
    },
    "Animation": {
      "type": "object",
      "required": ["type", "target"],
      "properties": {
        "id": { "type": "string" },
        "target": { "$ref": "#/$defs/AnimationTarget" },
        "type": { "type": "string" },
        "start_offset": { "type": "number", "minimum": 0 },
        "duration": { "type": "number", "exclusiveMinimum": 0 },
        "params": {
          "type": "object",
          "additionalProperties": true
        }
      },
      "additionalProperties": false
    },
    "AnimationTarget": {
      "type": "object",
      "required": ["type"],
      "properties": {
        "type": { "type": "string" },
        "id": { "type": "string" },
        "text": { "type": "string" },
        "index": { "type": "integer", "minimum": 0 }
      },
      "additionalProperties": false
    },
    "Transition": {
      "type": "object",
      "required": ["type"],
      "properties": {
        "type": { "type": "string" },
        "duration": { "type": "number", "minimum": 0 },
        "params": {
          "type": "object",
          "additionalProperties": true
        }
      },
      "additionalProperties": false
    }
  }
}
```

---

## 36. Visual timeline validation rules

Renderer must validate:

1. `schema_version` exists.
2. `template.name` exists.
3. `video.width`, `video.height`, `video.fps` are valid.
4. `scenes` is not empty.
5. Scene IDs are unique.
6. Scene times are valid.
7. Scene durations match end-start.
8. Scenes are sorted.
9. Every scene has text.
10. Every scene has display lines.
11. Every layout exists in layout registry.
12. Every effect exists in effect registry.
13. Every animation target exists or is resolvable.
14. Every referenced asset exists or has fallback.
15. Every keyword is valid.
16. UTF-8 text is preserved.
17. Vietnamese glyph support is available through font/template.

---

## 37. Icon DB JSON

### 37.1 Purpose

Icon DB maps available icons to metadata for semantic search.

### 37.2 File path

```text
assets/icons/icon_db.json
```

### 37.3 Example

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
    "tags": ["ngủ", "buồn ngủ", "zzz", "mệt"],
    "style": "flat",
    "mood": ["funny", "tired"]
  }
]
```

### 37.4 Icon item schema

```json
{
  "$id": "IconItem",
  "type": "object",
  "required": ["id", "file", "tags"],
  "properties": {
    "id": {
      "type": "string"
    },
    "file": {
      "type": "string"
    },
    "tags": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "style": {
      "type": "string"
    },
    "mood": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "category": {
      "type": "string"
    }
  },
  "additionalProperties": true
}
```

---

## 38. Template JSON/YAML schema

Templates may use YAML or JSON.

### 38.1 Template example

```json
{
  "name": "tiktok_dark_comic",
  "version": "0.1.0",
  "video": {
    "width": 1080,
    "height": 1920,
    "fps": 30
  },
  "colors": {
    "background": "#080A12",
    "text_primary": "#FFFFFF",
    "keyword_primary": "#FFD400",
    "speaker_a": "#3291FF",
    "speaker_b": "#FF5A8C"
  },
  "safe_zone": {
    "top": 120,
    "bottom": 220,
    "left": 80,
    "right": 140
  },
  "defaults": {
    "layout": "center_stack",
    "keyword_effect": "pop"
  }
}
```

### 38.2 Template schema

```json
{
  "$id": "Template",
  "type": "object",
  "required": ["name", "version", "video"],
  "properties": {
    "name": {
      "type": "string"
    },
    "version": {
      "type": "string"
    },
    "video": {
      "$ref": "#/$defs/VideoSpec"
    },
    "colors": {
      "type": "object",
      "additionalProperties": {
        "type": "string"
      }
    },
    "font": {
      "type": "object",
      "additionalProperties": true
    },
    "safe_zone": {
      "$ref": "#/$defs/SafeZone"
    },
    "defaults": {
      "type": "object",
      "additionalProperties": true
    }
  },
  "additionalProperties": true
}
```

---

## 39. SafeZone

### 39.1 Example

```json
{
  "top": 120,
  "bottom": 220,
  "left": 80,
  "right": 140
}
```

### 39.2 Schema

```json
{
  "$id": "SafeZone",
  "type": "object",
  "required": ["top", "bottom", "left", "right"],
  "properties": {
    "top": {
      "type": "integer",
      "minimum": 0
    },
    "bottom": {
      "type": "integer",
      "minimum": 0
    },
    "left": {
      "type": "integer",
      "minimum": 0
    },
    "right": {
      "type": "integer",
      "minimum": 0
    }
  },
  "additionalProperties": false
}
```

---

## 40. Render Report JSON

### 40.1 Purpose

Render report records what happened.

### 40.2 File path

```text
output/render_report.json
```

### 40.3 Example

```json
{
  "schema_version": "0.1.0",
  "engine_version": "0.1.0",
  "run_id": "run_20260707_001",
  "input": {
    "video": "input/video.mp4",
    "audio": "temp/audio.wav"
  },
  "output": {
    "silent_video": "output/silent_video.mp4",
    "final_video": "output/final.mp4"
  },
  "models": {
    "speech": "medium",
    "director": "qwen2.5:3b",
    "embedding": "paraphrase-multilingual-MiniLM-L12-v2"
  },
  "template": {
    "name": "tiktok_dark_comic",
    "version": "0.1.0"
  },
  "stats": {
    "duration": 28.4,
    "scene_count": 14,
    "render_time_sec": 11.2
  },
  "warnings": [],
  "errors": []
}
```

### 40.4 Schema

```json
{
  "$id": "RenderReport",
  "type": "object",
  "required": [
    "schema_version",
    "input",
    "output",
    "stats",
    "warnings",
    "errors"
  ],
  "properties": {
    "schema_version": {
      "type": "string"
    },
    "engine_version": {
      "type": "string"
    },
    "run_id": {
      "type": "string"
    },
    "input": {
      "type": "object",
      "additionalProperties": true
    },
    "output": {
      "type": "object",
      "additionalProperties": true
    },
    "models": {
      "type": "object",
      "additionalProperties": true
    },
    "template": {
      "$ref": "#/$defs/TemplateReference"
    },
    "stats": {
      "type": "object",
      "additionalProperties": true
    },
    "warnings": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/ValidationError"
      }
    },
    "errors": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/ValidationError"
      }
    }
  },
  "additionalProperties": false
}
```

---

## 41. Validation Report JSON

### 41.1 Purpose

Validation report explains schema and data issues.

### 41.2 Example

```json
{
  "schema_version": "0.1.0",
  "valid": false,
  "target": "output/timeline.visual.json",
  "errors": [
    {
      "path": "scenes[2].animations[0].type",
      "message": "Unknown effect: explode_spin",
      "severity": "error",
      "code": "UNKNOWN_EFFECT"
    }
  ],
  "warnings": [
    {
      "path": "scenes[3].assets.icon_score",
      "message": "Icon match score is low",
      "severity": "warning",
      "code": "LOW_ICON_SCORE"
    }
  ]
}
```

### 41.3 Schema

```json
{
  "$id": "ValidationReport",
  "type": "object",
  "required": ["schema_version", "valid", "target", "errors", "warnings"],
  "properties": {
    "schema_version": {
      "type": "string"
    },
    "valid": {
      "type": "boolean"
    },
    "target": {
      "type": "string"
    },
    "errors": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/ValidationError"
      }
    },
    "warnings": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/ValidationError"
      }
    }
  },
  "additionalProperties": false
}
```

---

## 42. Pydantic model direction

The Python implementation may use Pydantic.

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
            raise ValueError("duration must match end-start")
        return self
```

Pydantic models should be the runtime validation layer.

Markdown schemas are documentation.

---

## 43. Cross-field validation rules

JSON Schema alone may not validate all logic.

Runtime validation should check:

- duration equals end-start
- scenes sorted by time
- animation offset inside scene duration
- keyword exists in text or marked conceptual
- asset files exist
- effect names exist in registry
- layout names exist in registry
- template exists
- video duration matches audio duration

---

## 44. Unknown field policy

During early development, unknown fields may be allowed in some intermediate schemas.

For renderer input, be stricter.

Recommended:

| File | Unknown fields |
|---|---|
| transcript.json | allow limited metadata |
| timeline.normalized.json | reject unexpected scene fields |
| timeline.director.json | reject unexpected core fields |
| timeline.visual.json | reject unexpected renderer fields |
| render_report.json | allow additional stats |

---

## 45. Manual editing policy

JSON should remain human-editable.

Good:

```json
"effect": "pop"
```

Bad:

```json
"effect": {
  "engine_internal_class_path": "src.renderer.effects.PopEffectInternalV9"
}
```

Avoid exposing internal implementation details in user-facing JSON.

---

## 46. LLM output schema rules

Prompts must require:

- valid JSON only
- no markdown
- no explanation
- allowed enum values
- preserved IDs
- preserved timing
- no invented fields

Example prompt instruction:

```text
Return JSON only.
Do not wrap in markdown.
Preserve every scene id, start, end, and duration.
Use only allowed effects: pop, bounce, shake, glow, slide, fade.
```

---

## 47. JSON repair policy

If LLM returns invalid JSON:

1. store raw response for debug if debug mode enabled
2. attempt extraction if wrapped in markdown
3. attempt simple repair
4. parse JSON
5. validate schema
6. fail if invalid

Do not silently accept invalid data.

---

## 48. Backward compatibility

Before v1.0, schema may change.

After v1.0, breaking changes should include:

- new schema version
- migration notes
- DecisionLog entry
- tests

---

## 49. Migration strategy

Future migrations may convert:

```text
timeline.visual.v0.1.json
→ timeline.visual.v0.2.json
```

Migration functions should be explicit.

Example:

```python
migrate_visual_timeline_0_1_to_0_2(data: dict) -> dict
```

---

## 50. Schema storage recommendation

Future repository may contain machine-readable schemas:

```text
schemas/
├── transcript.schema.json
├── timeline.normalized.schema.json
├── timeline.visual.schema.json
├── render_report.schema.json
└── icon_db.schema.json
```

This documentation file explains them.

The `schemas/` folder can store strict JSON Schema files later.

---

## 51. Minimum valid transcript example

```json
{
  "schema_version": "0.1.0",
  "segments": [
    {
      "id": "seg_0001",
      "start": 0.0,
      "end": 1.5,
      "duration": 1.5,
      "text": "Xin chào."
    }
  ]
}
```

---

## 52. Minimum valid normalized timeline example

```json
{
  "schema_version": "0.1.0",
  "scenes": [
    {
      "id": "scene_0001",
      "source_segment_ids": ["seg_0001"],
      "start": 0.0,
      "end": 1.5,
      "duration": 1.5,
      "text": "Xin chào."
    }
  ]
}
```

---

## 53. Minimum valid visual timeline example

```json
{
  "schema_version": "0.1.0",
  "template": {
    "name": "tiktok_dark_comic"
  },
  "video": {
    "width": 1080,
    "height": 1920,
    "fps": 30
  },
  "scenes": [
    {
      "id": "scene_0001",
      "start": 0.0,
      "end": 1.5,
      "duration": 1.5,
      "text": "Xin chào.",
      "lines": ["XIN CHÀO."],
      "layout": {
        "name": "center_stack"
      },
      "keywords": []
    }
  ]
}
```

---

## 54. Invalid examples

### 54.1 Missing duration

```json
{
  "id": "scene_0001",
  "start": 0.0,
  "end": 1.5,
  "text": "Xin chào."
}
```

Invalid because duration is missing.

### 54.2 Negative duration

```json
{
  "start": 2.0,
  "end": 1.0,
  "duration": -1.0
}
```

Invalid.

### 54.3 Unknown effect

```json
{
  "type": "explode_spin"
}
```

Invalid unless registered.

### 54.4 Renderer input without lines

```json
{
  "text": "Xin chào."
}
```

Invalid for visual timeline.

### 54.5 Asset path absolute

```json
{
  "icon_path": "C:\\Users\\PC\\Desktop\\alarm.png"
}
```

Avoid in committed JSON.

Use repository-relative paths.

---

## 55. Schema design checklist

Before adding a new field:

1. Which module produces it?
2. Which module consumes it?
3. Is it required or optional?
4. Does it belong in transcript, timeline, or render report?
5. Does it need validation?
6. Does it affect renderer determinism?
7. Does it need documentation?
8. Does it need migration later?
9. Can users edit it manually?
10. Does it expose internal implementation details?

---

## 56. Renderer input checklist

Before rendering, validate:

- schema version exists
- video spec valid
- template exists
- scenes exist
- scene IDs unique
- timing valid
- lines non-empty
- layouts known
- effects known
- keyword targets valid
- assets exist or fallback
- fonts support Vietnamese
- scene durations positive

---

## 57. Visual Director output checklist

Before accepting LLM output:

- JSON parses
- IDs preserved
- timing preserved
- text preserved or safely transformed
- lines exist
- keywords reasonable
- effects allowed
- layouts allowed
- icon_query exists where useful
- no markdown
- no extra prose

---

## 58. File examples by stage

### 58.1 After STT

```text
output/transcript.json
```

### 58.2 After Timeline Analyzer

```text
output/timeline.normalized.json
```

### 58.3 After Visual Director

```text
output/timeline.director.json
```

### 58.4 After Icon Selector

```text
output/timeline.visual.json
```

### 58.5 After Exporter

```text
output/render_report.json
```

---

## 59. Final schema principle

A good schema makes the engine easier for both humans and AI agents to understand.

When in doubt, choose:

```text
explicit fields
clear enum values
human-readable JSON
strong validation
small composable objects
```

Avoid:

```text
implicit behavior
magic strings
unvalidated model output
renderer guessing
large opaque blobs
```

---

## 60. Controlled value registry

The following values are recommended for early versions.

### Emotion values

| Value | Meaning |
|---|---|
| `neutral` | default neutral delivery |
| `happy` | positive or cheerful scene |
| `surprised` | unexpected or shocked response |
| `confused` | questioning or unclear response |
| `angry` | anger or frustration |
| `funny` | humorous or punchline scene |
| `sad` | sad or disappointed scene |
| `serious` | important or sober scene |
| `dramatic` | over-the-top emphasis |
| `excited` | high-energy scene |

### Effect values

| Value | Meaning |
|---|---|
| `pop` | scale up quickly then settle |
| `bounce` | playful vertical bounce |
| `shake` | small jitter or vibration |
| `glow` | soft highlight around text |
| `slide` | move element into position |
| `fade` | opacity transition |
| `pulse` | repeated subtle scale/brightness |
| `typewriter` | reveal text progressively |
| `zoom` | camera or element zoom |

### Layout values

| Value | Meaning |
|---|---|
| `center_stack` | large centered stacked text |
| `punchline_center` | keyword or punchline dominant center |
| `speaker_label_top` | speaker label near top with text center |
| `comic_panel` | comic-like composition |
| `split_speaker` | two speaker areas |
| `avatar_left_text_right` | avatar left, text right |

### Transition values

| Value | Meaning |
|---|---|
| `cut` | instant cut |
| `fade` | fade between scenes |
| `slide` | slide transition |
| `zoom` | zoom transition |
| `none` | no transition |

### Speaker source values

| Value | Meaning |
|---|---|
| `unknown` | speaker not known |
| `manual` | user configured |
| `diarization` | speaker diarization model |
| `inferred` | heuristic inference |
| `inferred_alternating` | alternating speaker heuristic |
| `script` | known from script input |

---

## 61. Example complete lifecycle

### 61.1 Transcript

```json
{
  "schema_version": "0.1.0",
  "segments": [
    {
      "id": "seg_0001",
      "start": 0.20,
      "end": 1.40,
      "duration": 1.20,
      "text": "Ê, sao hôm nay đến trễ?"
    },
    {
      "id": "seg_0002",
      "start": 1.60,
      "end": 2.30,
      "duration": 0.70,
      "text": "Tại báo thức."
    }
  ]
}
```

### 61.2 Normalized timeline

```json
{
  "schema_version": "0.1.0",
  "scenes": [
    {
      "id": "scene_0001",
      "source_segment_ids": ["seg_0001"],
      "start": 0.20,
      "end": 1.40,
      "duration": 1.20,
      "speaker": {
        "id": "SPEAKER_00",
        "source": "unknown"
      },
      "text": "Ê, sao hôm nay đến trễ?"
    },
    {
      "id": "scene_0002",
      "source_segment_ids": ["seg_0002"],
      "start": 1.60,
      "end": 2.30,
      "duration": 0.70,
      "speaker": {
        "id": "SPEAKER_01",
        "source": "unknown"
      },
      "text": "Tại báo thức."
    }
  ]
}
```

### 61.3 Visual timeline

```json
{
  "schema_version": "0.1.0",
  "template": {
    "name": "tiktok_dark_comic"
  },
  "video": {
    "width": 1080,
    "height": 1920,
    "fps": 30
  },
  "scenes": [
    {
      "id": "scene_0001",
      "source_segment_ids": ["seg_0001"],
      "start": 0.20,
      "end": 1.40,
      "duration": 1.20,
      "speaker": {
        "id": "SPEAKER_00",
        "label": "Nam",
        "style": "speaker_a"
      },
      "text": "Ê, sao hôm nay đến trễ?",
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
        "icon_query": "trễ giờ",
        "icon_id": "icon_alarm_001",
        "icon_path": "assets/icons/alarm.png",
        "icon_score": 0.84
      },
      "animations": [
        {
          "id": "anim_0001",
          "target": {
            "type": "keyword",
            "text": "ĐẾN TRỄ"
          },
          "type": "pop",
          "start_offset": 0.80,
          "duration": 0.30,
          "params": {
            "scale": 1.25
          }
        }
      ],
      "transition": {
        "type": "cut"
      }
    },
    {
      "id": "scene_0002",
      "source_segment_ids": ["seg_0002"],
      "start": 1.60,
      "end": 2.30,
      "duration": 0.70,
      "speaker": {
        "id": "SPEAKER_01",
        "label": "Nữ",
        "style": "speaker_b"
      },
      "text": "Tại báo thức.",
      "lines": ["TẠI", "BÁO THỨC!"],
      "emotion": "funny",
      "layout": {
        "name": "punchline_center"
      },
      "keywords": [
        {
          "text": "BÁO THỨC",
          "importance": 0.98,
          "effect": "shake",
          "style": "keyword_primary"
        }
      ],
      "assets": {
        "icon_query": "báo thức",
        "icon_id": "icon_alarm_001",
        "icon_path": "assets/icons/alarm.png",
        "icon_score": 0.91
      },
      "animations": [
        {
          "id": "anim_0002",
          "target": {
            "type": "keyword",
            "text": "BÁO THỨC"
          },
          "type": "shake",
          "start_offset": 0.20,
          "duration": 0.30,
          "params": {
            "amplitude": 8
          }
        }
      ],
      "transition": {
        "type": "cut"
      }
    }
  ]
}
```

---

## 62. Future schema extensions

### 62.1 Speaker diarization extension

Add speaker segments, diarization confidence, and speaker embeddings.

### 62.2 Word-level animation extension

Add per-word timing and targetable word spans.

### 62.3 Avatar extension

Add avatar state, pose, expression, and speaker mapping.

### 62.4 SFX extension

Add sound effects linked to animation events.

### 62.5 BGM extension

Add background music, ducking, and volume automation.

### 62.6 Original video background extension

Allow input video to be used as blurred/cropped background.

### 62.7 Interactive editor extension

Add editor metadata for manual UI edits.

### 62.8 Batch render extension

Add batch-level report and per-item output state.

### 62.9 Template inheritance extension

Allow templates to inherit defaults from base templates.

### 62.10 Plugin extension

Allow registered plugin metadata in schema.

---

## 63. Schema governance


Schema changes should follow this process:

1. Open or define an issue.
2. Describe why the schema must change.
3. Update this document.
4. Update Pydantic models or JSON Schema files.
5. Update examples.
6. Update tests.
7. Update DecisionLog.
8. Commit with a clear message.

Example commit:

```text
docs: update visual timeline schema for animation targets
```
