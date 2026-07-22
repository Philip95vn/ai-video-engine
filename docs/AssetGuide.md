# AssetGuide.md

# AI Video Engine - Asset Guide

## 0. Purpose

This document defines how assets are organized, named, described, selected, validated, and used in **AI Video Engine**.

Assets include:

- icons
- avatars
- backgrounds
- fonts
- sound effects
- music
- templates
- stickers
- overlays
- debug fixtures

This document exists because assets are not just files.

Assets are part of the engine contract.

The renderer cannot produce good video if assets are inconsistent, missing, poorly named, or undocumented.

This document should be read together with:

```text
AGENTS.md
PROJECT_RULES.md
docs/Architecture.md
docs/Pipeline.md
docs/JSONSchema.md
docs/AIDesign.md
docs/RendererDesign.md
docs/PromptGuide.md
docs/CodingStandard.md
```

---

## 1. Core asset principle

Assets must be discoverable, reusable, and metadata-driven.

The engine should not depend on random hardcoded file paths.

The AI should not be expected to remember asset filenames.

The renderer should not search semantically.

The asset system connects all of these parts.

Core rule:

```text
AI returns asset intent.
Asset system resolves actual asset.
Renderer consumes resolved asset.
```

Example:

```text
Visual Director AI
    ↓
icon_query: "báo thức"
    ↓
Icon Selector
    ↓
icon_id: "icon_alarm_001"
icon_path: "assets/icons/alarm.png"
    ↓
Renderer
    ↓
draw icon
```

---

## 2. Asset responsibilities by module

### 2.1 Visual Director

May return:

```json
{
  "icon_query": "báo thức"
}
```

May not return exact file paths by default.

### 2.2 Embedding / Asset selector

Maps:

```text
query → asset_id/path
```

### 2.3 Renderer

Loads and draws resolved assets.

Renderer does not choose assets semantically.

### 2.4 Template system

Defines how assets should look and where they should appear.

### 2.5 Asset registry

Stores metadata, IDs, tags, paths, and style information.

---

## 3. Default asset folders

Recommended structure:

```text
assets/
├── icons/
│   ├── icon_db.json
│   ├── alarm.png
│   ├── sleep.png
│   └── money.png
│
├── avatars/
│   ├── avatar_db.json
│   ├── speaker_a/
│   └── speaker_b/
│
├── backgrounds/
│   ├── background_db.json
│   ├── dark_001.png
│   └── gradient_001.png
│
├── fonts/
│   ├── font_db.json
│   └── BeVietnamPro-Bold.ttf
│
├── sfx/
│   ├── sfx_db.json
│   ├── pop.wav
│   └── whoosh.wav
│
├── music/
│   ├── music_db.json
│   └── funny_light.mp3
│
├── stickers/
│   ├── sticker_db.json
│   └── laugh_001.png
│
└── templates/
    ├── tiktok_dark_comic.yaml
    └── minimal_black.yaml
```

Early project may not include all folders.

The structure should allow growth.

---

## 4. Asset database files

Each asset category should eventually have a database file.

Recommended:

```text
assets/icons/icon_db.json
assets/avatars/avatar_db.json
assets/backgrounds/background_db.json
assets/fonts/font_db.json
assets/sfx/sfx_db.json
assets/music/music_db.json
assets/stickers/sticker_db.json
```

These files should be committed if they contain only metadata.

Large binary assets may be handled carefully.

---

## 5. Asset ID policy

Every reusable asset should have a stable ID.

Examples:

```text
icon_alarm_001
icon_sleep_001
avatar_male_surprised_001
bg_dark_001
font_be_vietnam_pro_bold
sfx_pop_001
music_funny_light_001
template_tiktok_dark_comic
```

IDs should be:

- lowercase
- snake_case
- stable
- descriptive
- category-prefixed
- not random UUIDs unless necessary

---

## 6. Asset filename policy

File names should be readable and stable.

Good:

```text
alarm_001.png
sleep_001.png
money_001.png
be_vietnam_pro_bold.ttf
dark_gradient_001.png
pop_001.wav
```

Bad:

```text
IMG_2938.png
final_final_icon.png
new2.png
download (3).png
```

File names may change during early development, but asset IDs should remain stable once used in timelines.

---

## 7. Relative path policy

Asset paths in JSON should be repository-relative.

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

Absolute paths should not appear in committed JSON.

---

## 8. Asset metadata principle

Assets should be selected using metadata.

Metadata should include:

- ID
- file path
- tags
- category
- style
- mood
- language tags
- license info
- optional dimensions
- optional duration
- optional usage notes

The metadata enables:

- search
- validation
- replacement
- UI display
- AI-assisted selection
- batch rendering

---

## 9. Icon assets

Icons are the first major asset type.

Icons help communicate meaning quickly.

Examples:

- báo thức
- ngủ
- tiền
- công việc
- cà phê
- điện thoại
- deadline
- sách
- xe
- trái tim
- cảnh báo
- dấu hỏi

Icons should be simple, readable, and high contrast.

---

## 10. Icon database schema

File:

```text
assets/icons/icon_db.json
```

Example:

```json
[
  {
    "id": "icon_alarm_001",
    "file": "assets/icons/alarm_001.png",
    "tags": ["báo thức", "đồng hồ", "trễ giờ", "dậy sớm"],
    "tags_en": ["alarm", "clock", "late", "wake up"],
    "category": "time",
    "style": "flat",
    "mood": ["funny", "urgent"],
    "license": "project_asset",
    "notes": "Good for late/wake-up jokes."
  }
]
```

---

## 11. Icon metadata fields

| Field | Required | Description |
|---|---:|---|
| `id` | yes | Stable asset ID |
| `file` | yes | Relative file path |
| `tags` | yes | Vietnamese search tags |
| `tags_en` | no | English search tags |
| `category` | no | Concept group |
| `style` | no | Visual style |
| `mood` | no | Emotional fit |
| `license` | no | License/source |
| `notes` | no | Human notes |
| `width` | no | Asset width |
| `height` | no | Asset height |

---

## 12. Icon tag rules

Tags should include Vietnamese words first.

Good:

```json
"tags": ["báo thức", "đồng hồ", "trễ giờ", "dậy sớm"]
```

Also useful:

```json
"tags_en": ["alarm", "clock", "late", "wake up"]
```

Tags should include:

- object name
- related concepts
- common Vietnamese phrasing
- slang if relevant
- mood if useful
- use cases

---

## 13. Icon query matching

Visual Director returns:

```json
{
  "icon_query": "báo thức"
}
```

Icon Selector searches icon DB.

Matching can use:

- exact match
- fuzzy match
- embedding similarity
- category boost
- mood boost
- template style filter

The first implementation can use embedding similarity.

---

## 14. Icon selection confidence

Icon selector should store score.

Example:

```json
{
  "icon_id": "icon_alarm_001",
  "icon_path": "assets/icons/alarm_001.png",
  "icon_score": 0.91
}
```

Low score should generate warning.

Suggested threshold:

```yaml
icon:
  min_score: 0.45
```

Threshold depends on embedding model.

---

## 15. Icon style consistency

A video should not randomly mix incompatible icon styles unless the template allows it.

Possible styles:

```text
flat
outline
filled
emoji
3d
neon
comic
minimal
line
duotone
```

Template can prefer:

```yaml
icon:
  preferred_style: flat
```

Icon selector may filter or boost by style.

---

## 16. Icon format

Recommended formats:

```text
PNG
SVG later
WEBP later
```

Initial renderer can support PNG.

SVG support may be added later.

PNG icons should ideally have transparency.

---

## 17. Icon size

Icons should be large enough for mobile.

Recommended source icon size:

```text
512x512
```

Renderer can resize to:

```text
120px - 260px
```

depending on layout.

---

## 18. Icon color

Icons should work on dark background.

If icon is too dark, it may be unreadable.

Asset review should check contrast.

Future renderer may recolor SVG icons.

---

## 19. Icon validation

Validate:

- file exists
- file opens
- format supported
- dimensions reasonable
- metadata ID unique
- tags not empty
- path relative
- no duplicate ID

---

## 20. Icon fallback policy

If icon is missing:

Normal mode:

```text
warn and skip icon
```

Strict mode:

```text
fail
```

Lenient mode:

```text
skip and report warning
```

Never crash with unclear file error.

---

## 21. Avatar assets

Avatars represent speakers or characters.

Avatars are optional in early versions.

Future avatar system should support:

- speaker identity
- emotion variant
- pose
- expression
- style
- side/position
- animation

---

## 22. Avatar folder structure

Recommended:

```text
assets/avatars/
├── avatar_db.json
├── speaker_a/
│   ├── neutral.png
│   ├── happy.png
│   ├── surprised.png
│   ├── confused.png
│   └── angry.png
└── speaker_b/
    ├── neutral.png
    ├── happy.png
    ├── surprised.png
    ├── confused.png
    └── angry.png
```

---

## 23. Avatar database example

```json
[
  {
    "id": "avatar_speaker_a_neutral",
    "file": "assets/avatars/speaker_a/neutral.png",
    "speaker_style": "speaker_a",
    "emotion": "neutral",
    "style": "comic",
    "license": "project_asset"
  },
  {
    "id": "avatar_speaker_a_surprised",
    "file": "assets/avatars/speaker_a/surprised.png",
    "speaker_style": "speaker_a",
    "emotion": "surprised",
    "style": "comic",
    "license": "project_asset"
  }
]
```

---

## 24. Avatar metadata fields

| Field | Required | Description |
|---|---:|---|
| `id` | yes | Stable avatar ID |
| `file` | yes | Relative file path |
| `speaker_style` | no | speaker_a/speaker_b |
| `emotion` | no | emotion variant |
| `style` | no | comic/flat/3d/etc |
| `license` | no | license/source |
| `notes` | no | human notes |

---

## 25. Avatar selection

Avatar selection may use:

```text
speaker ID
speaker style
emotion
template
manual config
```

Example:

```json
{
  "speaker": {
    "id": "SPEAKER_00",
    "style": "speaker_a"
  },
  "emotion": "surprised"
}
```

Maps to:

```text
avatar_speaker_a_surprised
```

Renderer draws resolved avatar.

---

## 26. Avatar fallback

Fallback order:

1. exact speaker + emotion
2. speaker + neutral
3. generic emotion
4. generic neutral
5. no avatar

Fallback should be reported.

---

## 27. Background assets

Backgrounds define video atmosphere.

Types:

- solid color
- gradient image
- pattern image
- original video background
- blurred video
- animated background later

Initial version can use solid color from template.

---

## 28. Background folder structure

```text
assets/backgrounds/
├── background_db.json
├── dark_001.png
├── dark_gradient_001.png
├── neon_001.png
└── comic_halftone_001.png
```

---

## 29. Background database example

```json
[
  {
    "id": "bg_dark_001",
    "file": "assets/backgrounds/dark_001.png",
    "tags": ["đen", "tối", "dark", "minimal"],
    "style": "minimal",
    "mood": ["neutral", "serious"],
    "dominant_color": "#080A12",
    "license": "project_asset"
  }
]
```

---

## 30. Background validation

Validate:

- file exists if image background
- dimensions reasonable
- readable format
- path relative
- ID unique
- license documented if needed

---

## 31. Background usage

Template may define:

```yaml
background:
  type: solid
  color: "#080A12"
```

or:

```yaml
background:
  type: image
  asset_id: bg_dark_001
```

Renderer resolves background through template/asset registry.

---

## 32. Font assets

Fonts are critical.

Text is the main visual element.

Fonts must support Vietnamese.

Recommended font families:

- Be Vietnam Pro
- Noto Sans
- Inter
- Roboto
- Arial fallback

Do not distribute proprietary fonts without permission.

---

## 33. Font folder structure

```text
assets/fonts/
├── font_db.json
├── BeVietnamPro-Bold.ttf
├── BeVietnamPro-ExtraBold.ttf
└── NotoSans-Bold.ttf
```

---

## 34. Font database example

```json
[
  {
    "id": "font_be_vietnam_pro_bold",
    "file": "assets/fonts/BeVietnamPro-Bold.ttf",
    "family": "Be Vietnam Pro",
    "weight": "bold",
    "supports_vietnamese": true,
    "license": "OFL",
    "usage": ["main_text", "keyword"]
  }
]
```

---

## 35. Font metadata fields

| Field | Required | Description |
|---|---:|---|
| `id` | yes | Stable font ID |
| `file` | yes | Relative path |
| `family` | yes | Font family |
| `weight` | no | regular/bold/etc |
| `supports_vietnamese` | yes | true/false |
| `license` | no | license |
| `usage` | no | main/keyword/label |

---

## 36. Font validation

Validate:

- file exists
- font can be loaded
- Vietnamese glyphs render
- license is documented
- ID unique

Test strings:

```text
Tiếng Việt có dấu
ĐẾN TRỄ?
BÁO THỨC!
ỦA?
```

---

## 37. Font fallback

Fallback order:

1. template font
2. project font asset
3. configured system font
4. known system fallback
5. fail clearly

Do not silently use broken font.

---

## 38. SFX assets

Sound effects are optional.

SFX can emphasize:

- pop
- shake
- whoosh
- punchline
- alert
- click
- bounce

SFX mixing belongs to audio/exporter, not renderer.

Renderer may output timing metadata later.

---

## 39. SFX folder structure

```text
assets/sfx/
├── sfx_db.json
├── pop_001.wav
├── whoosh_001.wav
├── shake_001.wav
└── bell_001.wav
```

---

## 40. SFX database example

```json
[
  {
    "id": "sfx_pop_001",
    "file": "assets/sfx/pop_001.wav",
    "tags": ["pop", "bật", "nhấn mạnh"],
    "duration": 0.25,
    "style": "cartoon",
    "license": "project_asset"
  }
]
```

---

## 41. SFX metadata fields

| Field | Required | Description |
|---|---:|---|
| `id` | yes | Stable ID |
| `file` | yes | Relative path |
| `tags` | yes | Search tags |
| `duration` | no | seconds |
| `style` | no | cartoon/cinematic/etc |
| `license` | no | source/license |
| `volume` | no | suggested default |

---

## 42. SFX policy

SFX should not overpower voice.

Default voice is primary.

If SFX is used, volume should be low enough.

Future audio mixer should support ducking and gain control.

---

## 43. Music assets

Background music is optional.

For current existing-video workflow, original voice is primary.

Music should be subtle.

---

## 44. Music database example

```json
[
  {
    "id": "music_funny_light_001",
    "file": "assets/music/funny_light_001.mp3",
    "tags": ["hài hước", "vui", "nhẹ"],
    "mood": ["funny", "happy"],
    "bpm": 110,
    "license": "project_asset"
  }
]
```

---

## 45. Music policy

Do not add background music by default in early versions.

If enabled:

- keep volume low
- avoid copyright issues
- document license
- allow user to disable
- do not overpower original voice

---

## 46. Sticker assets

Stickers are optional visual decorations.

Examples:

- laugh burst
- question mark
- exclamation
- arrow
- comic burst
- star
- fire
- warning

Stickers differ from icons because they are decorative.

---

## 47. Sticker database example

```json
[
  {
    "id": "sticker_laugh_burst_001",
    "file": "assets/stickers/laugh_burst_001.png",
    "tags": ["cười", "hài", "haha"],
    "style": "comic",
    "mood": ["funny"]
  }
]
```

---

## 48. Template assets

Templates define visual system.

Template files may live under:

```text
assets/templates/
```

or:

```text
templates/
```

One location should be chosen and documented.

Recommended early path:

```text
assets/templates/
```

---

## 49. Template file example

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
  stroke: "#000000"
  speaker_a: "#3291FF"
  speaker_b: "#FF5A8C"

font:
  main: font_be_vietnam_pro_bold
  keyword: font_be_vietnam_pro_bold
  label: font_be_vietnam_pro_bold

safe_zone:
  top: 120
  bottom: 220
  left: 80
  right: 140

defaults:
  layout: center_stack
  keyword_effect: pop
  transition: cut
```

---

## 50. Template metadata

Template should define:

- name
- version
- video spec
- colors
- fonts
- safe zone
- default layout
- default effects
- asset style preferences
- speaker styles
- keyword styles

---

## 51. Speaker style assets

Speaker style may define colors, labels, and avatar mapping.

Example:

```yaml
speaker_styles:
  speaker_a:
    label_background: "#3291FF"
    label_text: "#FFFFFF"
    avatar_group: speaker_a

  speaker_b:
    label_background: "#FF5A8C"
    label_text: "#FFFFFF"
    avatar_group: speaker_b
```

---

## 52. Keyword style assets

Keyword style may define:

```yaml
keyword_styles:
  keyword_primary:
    fill: "#FFD400"
    stroke: "#000000"
    stroke_width: 6
    glow: true
    font_scale: 1.2
```

---

## 53. Asset manifest

A global asset manifest may eventually exist.

Example:

```text
assets/manifest.json
```

Purpose:

- list asset DB files
- define asset root
- define version
- help validation

Example:

```json
{
  "schema_version": "0.1.0",
  "asset_root": "assets",
  "databases": {
    "icons": "assets/icons/icon_db.json",
    "avatars": "assets/avatars/avatar_db.json",
    "backgrounds": "assets/backgrounds/background_db.json",
    "fonts": "assets/fonts/font_db.json",
    "sfx": "assets/sfx/sfx_db.json",
    "templates": "assets/templates"
  }
}
```

---

## 54. Asset registry

Asset registry is a runtime object.

Responsibilities:

- load databases
- validate asset metadata
- resolve asset ID to path
- check file existence
- provide fallback assets
- provide style filters
- expose assets to renderer/selector

Suggested interface:

```python
class AssetRegistry:
    def get_icon(self, icon_id: str) -> IconAsset:
        ...

    def resolve_path(self, asset_path: str) -> Path:
        ...

    def validate(self) -> AssetValidationReport:
        ...
```

---

## 55. Asset validation report

Example:

```json
{
  "schema_version": "0.1.0",
  "valid": false,
  "errors": [
    {
      "asset_id": "icon_alarm_001",
      "message": "File not found: assets/icons/alarm_001.png"
    }
  ],
  "warnings": [
    {
      "asset_id": "font_default",
      "message": "License field missing."
    }
  ]
}
```

---

## 56. Asset validation checklist

For each asset database:

- JSON parses
- IDs unique
- required fields exist
- paths are relative
- files exist
- tags not empty
- license documented if required
- unsupported formats reported
- duplicate files detected
- missing metadata reported

---

## 57. Asset selection flow

### 57.1 Icon flow

```text
Visual Director
    ↓
icon_query
    ↓
Icon Selector
    ↓
icon_id, icon_path, icon_score
    ↓
Visual Timeline
    ↓
Renderer
```

### 57.2 Avatar flow

```text
speaker + emotion
    ↓
Avatar Mapper
    ↓
avatar_id, avatar_path
    ↓
Visual Timeline
    ↓
Renderer
```

### 57.3 Background flow

```text
template
    ↓
background_id/path or solid color
    ↓
Renderer
```

### 57.4 Font flow

```text
template
    ↓
font_id/path
    ↓
Renderer
```

---

## 58. Asset selector vs renderer

Asset selector chooses assets.

Renderer uses chosen assets.

Bad:

```python
# inside renderer
icon = semantic_search(scene.text)
```

Good:

```python
# before renderer
scene.assets.icon_id = icon_selector.search(scene.assets.icon_query)
```

---

## 59. Asset metadata and embeddings

Embedding models search text metadata.

For icons, text may include:

```text
tags + tags_en + category + mood + notes
```

Example searchable string:

```text
báo thức đồng hồ trễ giờ dậy sớm alarm clock late wake up funny urgent
```

---

## 60. Embedding index

Embedding index may be cached.

Possible cache:

```text
cache/icon_embeddings.json
```

or:

```text
cache/icon_embeddings.npy
```

Cache key should include:

- icon DB hash
- model name
- model version
- embedding settings

---

## 61. Asset cache invalidation

Invalidate asset cache when:

- asset DB changes
- asset file path changes
- tags change
- embedding model changes
- style filters change
- schema version changes

---

## 62. Asset search score

Icon selection should record score.

Example:

```json
{
  "icon_score": 0.87
}
```

This helps:

- debugging
- manual review
- fallback decisions
- UI display

---

## 63. Low-confidence icon behavior

If score is low:

Options:

- no icon
- fallback icon
- generic icon
- warning
- manual review

Recommended normal behavior:

```text
warn and skip icon if below threshold
```

---

## 64. Generic fallback icons

Optional generic icons:

```text
icon_question_001
icon_exclamation_001
icon_smile_001
icon_warning_001
```

Use only if template allows.

Avoid irrelevant icons.

---

## 65. Asset licensing

Licensing matters.

Every asset source should be known.

Possible license values:

```text
project_asset
open_source
public_domain
OFL
CC0
CC-BY
commercial_license
unknown
```

Avoid using assets with unknown license in production.

---

## 66. Font licensing

Do not share proprietary font files unless license permits.

Open fonts are safer.

Recommended:

- SIL Open Font License fonts
- Google Fonts with proper license
- project-created fonts if available

Never expose system font files to users.

---

## 67. Icon licensing

Icons may come from:

- self-created assets
- open-source icon packs
- purchased icon packs
- generated assets
- public domain assets

Document source/license.

If license requires attribution, store it.

---

## 68. SFX and music licensing

Audio assets are often copyrighted.

Use only:

- self-created
- licensed
- royalty-free with documentation
- public domain
- CC0

Do not commit copyrighted music without permission.

---

## 69. Asset attribution

If needed, store attribution metadata.

Example:

```json
{
  "license": "CC-BY-4.0",
  "author": "Author Name",
  "source_url": "stored separately or documented",
  "attribution_required": true
}
```

Do not expose raw URLs in renderer output unless needed.

---

## 70. Large asset policy

Large files should not be committed casually.

Possible strategies:

- keep small starter assets in Git
- use Git LFS
- use external storage
- document download process
- use generated placeholders for tests

Early project can use small placeholder assets.

---

## 71. Git ignore policy for assets

Do not ignore all assets by default if small placeholder assets are needed.

But ignore generated files:

```text
output/
temp/
cache/
```

Large local asset packs can be ignored:

```text
assets/local/
assets/downloaded/
```

if documented.

---

## 72. Test assets

Test assets should be tiny.

Recommended:

```text
tests/fixtures/assets/icons/test_icon.png
tests/fixtures/assets/fonts/test_font.ttf
tests/fixtures/assets/templates/test_template.yaml
```

Do not rely on full production asset library for unit tests.

---

## 73. Placeholder assets

The project may include simple placeholders:

```text
placeholder_icon.png
placeholder_avatar.png
placeholder_background.png
```

These should be clearly labeled.

---

## 74. Asset dimensions

Record dimensions when useful.

Example:

```json
{
  "width": 512,
  "height": 512
}
```

Dimensions can be auto-filled by asset validation.

---

## 75. Asset duration

For audio assets:

```json
{
  "duration": 0.25
}
```

Duration can be auto-filled by validation/probe.

---

## 76. Asset style compatibility

Templates may prefer specific asset style.

Example:

```yaml
icon:
  preferred_styles: ["flat", "comic"]
```

Icon selector can boost matching assets with preferred style.

---

## 77. Asset mood compatibility

Visual Director may output emotion.

Icon selector may use mood.

Example:

```json
"emotion": "funny"
```

Prefer icons with:

```json
"mood": ["funny"]
```

Mood should be a boost, not a hard requirement.

---

## 78. Asset language tags

For Vietnamese project, include Vietnamese tags.

For broader support, include English tags.

Example:

```json
{
  "tags": ["ngủ", "buồn ngủ", "mệt"],
  "tags_en": ["sleep", "sleepy", "tired"]
}
```

---

## 79. Asset categories

Suggested icon categories:

```text
time
sleep
money
work
emotion
food
technology
transport
education
warning
weather
social
health
home
office
communication
```

Categories help filtering.

---

## 80. Asset naming examples

### Icons

```text
icon_alarm_001
icon_clock_001
icon_sleep_001
icon_money_001
icon_phone_001
```

### Avatars

```text
avatar_speaker_a_neutral
avatar_speaker_a_happy
avatar_speaker_a_surprised
```

### Backgrounds

```text
bg_dark_001
bg_neon_gradient_001
bg_comic_halftone_001
```

### Fonts

```text
font_be_vietnam_pro_bold
font_noto_sans_bold
```

### SFX

```text
sfx_pop_001
sfx_whoosh_001
sfx_bell_001
```

---

## 81. Asset ID collision

IDs must be unique within category.

Prefer globally unique IDs across all assets.

If two asset DB files have same ID, validation should fail.

---

## 82. Asset path normalization

Use forward slashes in JSON:

```text
assets/icons/alarm_001.png
```

Python `pathlib` can handle conversion.

---

## 83. Asset root resolution

Asset paths should be resolved relative to project root.

Do not assume current working directory.

Suggested:

```python
asset_path = project_root / relative_path
```

---

## 84. Missing project root

If project root cannot be found, use explicit config.

Do not guess randomly.

---

## 85. Asset loading errors

Errors should be clear.

Bad:

```text
FileNotFoundError
```

Good:

```text
Icon asset not found: assets/icons/alarm_001.png
Referenced by scene_0003 assets.icon_path.
```

---

## 86. Asset preview tooling

Future script:

```bash
python scripts/preview_assets.py
```

Could generate:

```text
output/asset_preview/icons.html
output/asset_preview/fonts.png
```

Useful for reviewing library quality.

---

## 87. Icon DB generation

Future script:

```bash
python scripts/build_icon_db.py assets/icons/
```

Could:

- scan PNG files
- create missing IDs
- prompt user for tags
- validate paths
- write icon_db.json

---

## 88. Embedding DB generation

Future script:

```bash
python scripts/build_icon_embeddings.py
```

Could:

- read icon_db.json
- load embedding model
- encode metadata
- save cache
- report duplicates/low metadata

---

## 89. Asset linting

Future command:

```bash
ai-video assets validate
```

Checks all asset DBs.

---

## 90. Asset lint output

Example:

```text
[assets] icons: 120 assets
[assets] icons: 3 warnings
[assets] fonts: 2 assets
[assets] fonts: ok
[assets] backgrounds: 5 assets
```

---

## 91. Asset quality checklist

Before adding asset:

1. Is file needed?
2. Is filename clean?
3. Is ID stable?
4. Is path relative?
5. Are tags useful?
6. Are Vietnamese tags included?
7. Is license known?
8. Does it work on dark background?
9. Is file size reasonable?
10. Is it validated?

---

## 92. Icon quality checklist

1. Transparent background if possible.
2. Readable at small size.
3. High contrast.
4. Style consistent.
5. Good tags.
6. No copyright problem.
7. Works with template colors.
8. Not too detailed.
9. Not blurry.
10. Not misleading.

---

## 93. Avatar quality checklist

1. Consistent character style.
2. Emotion variants aligned.
3. Transparent background.
4. Similar framing across emotions.
5. Works at video resolution.
6. Speaker mapping clear.
7. License known.
8. Not too visually distracting.

---

## 94. Background quality checklist

1. Does not reduce text readability.
2. Not too bright behind white text.
3. Fits 9:16.
4. Works with safe zones.
5. Style matches template.
6. File size reasonable.
7. License known.

---

## 95. Font quality checklist

1. Supports Vietnamese.
2. Bold enough for mobile.
3. Readable in uppercase.
4. Looks good with stroke.
5. License known.
6. Cross-platform available if not bundled.
7. Does not break with accents.

---

## 96. SFX quality checklist

1. Short.
2. Clean.
3. Not too loud.
4. Matches animation.
5. License known.
6. Does not overpower speech.
7. Format supported.

---

## 97. Asset and renderer relationship

Renderer needs assets that are:

- resolved
- validated
- local
- readable
- compatible with template

Renderer should not be responsible for:

- tagging
- semantic search
- license checking
- downloading
- AI asset choice

---

## 98. Asset and Visual Director relationship

Visual Director should output intent.

Example:

```json
{
  "icon_query": "ngủ"
}
```

Visual Director should not output:

```json
{
  "icon_path": "assets/icons/sleep_001.png"
}
```

unless asset list is explicitly provided.

---

## 99. Asset and embedding relationship

Embedding search should use asset metadata, not image pixels initially.

Later image embeddings may be possible, but text metadata is simpler.

---

## 100. Asset and templates relationship

Template can:

- prefer icon style
- define icon size
- define font IDs
- define background
- define speaker colors
- define keyword styles
- define fallback assets

Asset DB stores available assets.

Template defines how to use them.

---

## 101. Asset and JSON timeline relationship

Visual timeline may include:

```json
"assets": {
  "icon_query": "báo thức",
  "icon_id": "icon_alarm_001",
  "icon_path": "assets/icons/alarm_001.png",
  "icon_score": 0.91
}
```

Renderer should use `icon_path` or resolve `icon_id`.

Long-term, prefer `icon_id` with registry resolution.

---

## 102. Asset reference strategy

Early version may include both:

```json
"icon_id": "icon_alarm_001",
"icon_path": "assets/icons/alarm_001.png"
```

This is easier to debug.

Long-term renderer may only require `icon_id`.

---

## 103. Asset path duplication

If both ID and path exist, validation should check they match.

If mismatch:

```text
icon_id icon_alarm_001 points to assets/icons/alarm_001.png but timeline has assets/icons/clock.png
```

Fail or warn.

---

## 104. Asset manifest versioning

Asset manifest can include version:

```json
{
  "asset_pack_version": "0.1.0"
}
```

Useful when asset library changes.

---

## 105. Asset pack concept

An asset pack is a collection of assets and metadata.

Example:

```text
asset_pack_dark_comic_v1
asset_pack_recruitment_clean_v1
asset_pack_education_bold_v1
```

Future templates may depend on asset packs.

---

## 106. Asset pack structure

```text
asset_packs/
└── dark_comic_v1/
    ├── manifest.json
    ├── icons/
    ├── avatars/
    ├── backgrounds/
    ├── fonts/
    └── templates/
```

This is future architecture.

For now, use `assets/`.

---

## 107. Asset import workflow

Suggested workflow:

1. Add files to correct folder.
2. Rename files cleanly.
3. Add metadata to DB.
4. Run asset validation.
5. Test rendering.
6. Commit metadata and allowed assets.
7. Document source/license.

---

## 108. Asset removal workflow

Before removing an asset:

1. Search timeline/examples/templates referencing it.
2. Search DB references.
3. Update fallback.
4. Run validation.
5. Commit removal with explanation.

---

## 109. Asset replacement workflow

To replace visual file without changing ID:

1. Keep same ID.
2. Replace file if same semantic meaning.
3. Update dimensions if needed.
4. Update notes if visual style changes.
5. Run render smoke test.

If semantic meaning changes, create new ID.

---

## 110. Asset migration

If moving assets:

- update DB paths
- update templates
- update examples
- update tests
- update docs if structure changes

Do not leave broken paths.

---

## 111. Asset source documentation

Recommended source fields:

```json
{
  "source": "self_created",
  "source_url": null,
  "author": "project",
  "license": "project_asset"
}
```

For third-party assets, document license carefully.

---

## 112. Asset safety

Do not include:

- copyrighted music without license
- trademarked logos without permission
- private photos without consent
- sensitive personal media
- offensive symbols unless intentionally allowed for a specific use case

---

## 113. Asset privacy

User-provided media should not be committed.

If user uploads private assets, store locally and ignore unless explicitly intended.

---

## 114. Asset backup

Important project-created assets should be backed up.

GitHub may not be suitable for very large binary files.

Consider:

- Git LFS
- cloud storage
- local backup
- release assets

---

## 115. Asset review for video style

The desired early style:

```text
dark background
large white/yellow text
simple icons
comic/humorous energy
speaker colors
high contrast
```

Assets should support this style first.

---

## 116. Starter icon set

Recommended starter icons:

```text
alarm
clock
sleep
money
briefcase
coffee
phone
question
exclamation
laugh
warning
book
car
heart
fire
lightbulb
calendar
chat
robot
home
```

These cover many short videos.

---

## 117. Starter avatar set

Optional starter avatars:

```text
speaker_a_neutral
speaker_a_happy
speaker_a_surprised
speaker_a_confused
speaker_a_angry
speaker_b_neutral
speaker_b_happy
speaker_b_surprised
speaker_b_confused
speaker_b_angry
```

---

## 118. Starter background set

Recommended:

```text
solid_dark
dark_gradient
comic_halftone
neon_blue_purple
minimal_black
```

---

## 119. Starter SFX set

Optional:

```text
pop
whoosh
click
bell
shake
boing
ding
```

---

## 120. Starter templates

Recommended:

```text
tiktok_dark_comic
minimal_black
neon_dialogue
recruitment_clean
education_bold
```

Only one template is required for V1.

---

## 121. Template `tiktok_dark_comic`

Purpose:

- humorous dialogue
- bold text
- dark background
- speaker colors
- keyword emphasis

Recommended assets:

- flat icons
- comic avatars
- bold Vietnamese font
- pop/shake/bounce SFX later

---

## 122. Template `minimal_black`

Purpose:

- simple videos
- fast rendering
- no distractions

Recommended assets:

- no icons or minimal icons
- bold font
- black background
- white/yellow text

---

## 123. Template `neon_dialogue`

Purpose:

- energetic social videos
- glow effects
- neon colors

Recommended assets:

- neon icons
- gradient background
- glow keyword style

---

## 124. Template `recruitment_clean`

Purpose:

- professional recruitment content

Recommended assets:

- clean icons
- professional backgrounds
- calm transitions
- no comic avatars by default

---

## 125. Template `education_bold`

Purpose:

- learning and explainer videos

Recommended assets:

- book/lightbulb/checklist icons
- clean layouts
- highlighted terms

---

## 126. Asset DB example - starter icons

```json
[
  {
    "id": "icon_alarm_001",
    "file": "assets/icons/alarm_001.png",
    "tags": ["báo thức", "đồng hồ", "trễ giờ", "dậy sớm"],
    "tags_en": ["alarm", "clock", "late", "wake up"],
    "category": "time",
    "style": "flat",
    "mood": ["funny", "urgent"],
    "license": "project_asset"
  },
  {
    "id": "icon_sleep_001",
    "file": "assets/icons/sleep_001.png",
    "tags": ["ngủ", "buồn ngủ", "zzz", "mệt"],
    "tags_en": ["sleep", "sleepy", "tired"],
    "category": "sleep",
    "style": "flat",
    "mood": ["funny", "tired"],
    "license": "project_asset"
  },
  {
    "id": "icon_money_001",
    "file": "assets/icons/money_001.png",
    "tags": ["tiền", "lương", "thưởng", "thu nhập"],
    "tags_en": ["money", "salary", "bonus", "income"],
    "category": "money",
    "style": "flat",
    "mood": ["happy", "serious"],
    "license": "project_asset"
  }
]
```

---

## 127. Asset DB example - fonts

```json
[
  {
    "id": "font_be_vietnam_pro_bold",
    "file": "assets/fonts/BeVietnamPro-Bold.ttf",
    "family": "Be Vietnam Pro",
    "weight": "bold",
    "supports_vietnamese": true,
    "license": "OFL",
    "usage": ["main_text", "keyword", "speaker_label"]
  }
]
```

---

## 128. Asset DB example - avatars

```json
[
  {
    "id": "avatar_speaker_a_neutral",
    "file": "assets/avatars/speaker_a/neutral.png",
    "speaker_style": "speaker_a",
    "emotion": "neutral",
    "style": "comic",
    "license": "project_asset"
  },
  {
    "id": "avatar_speaker_b_funny",
    "file": "assets/avatars/speaker_b/funny.png",
    "speaker_style": "speaker_b",
    "emotion": "funny",
    "style": "comic",
    "license": "project_asset"
  }
]
```

---

## 129. Asset DB example - SFX

```json
[
  {
    "id": "sfx_pop_001",
    "file": "assets/sfx/pop_001.wav",
    "tags": ["pop", "bật", "nhấn mạnh"],
    "duration": 0.25,
    "style": "cartoon",
    "license": "project_asset",
    "volume": 0.35
  }
]
```

---

## 130. Asset DB example - backgrounds

```json
[
  {
    "id": "bg_dark_001",
    "file": "assets/backgrounds/dark_001.png",
    "tags": ["đen", "tối", "dark", "minimal"],
    "style": "minimal",
    "mood": ["neutral", "serious", "funny"],
    "dominant_color": "#080A12",
    "license": "project_asset"
  }
]
```

---

## 131. Asset manifest example

```json
{
  "schema_version": "0.1.0",
  "asset_root": "assets",
  "databases": {
    "icons": "assets/icons/icon_db.json",
    "avatars": "assets/avatars/avatar_db.json",
    "backgrounds": "assets/backgrounds/background_db.json",
    "fonts": "assets/fonts/font_db.json",
    "sfx": "assets/sfx/sfx_db.json",
    "music": "assets/music/music_db.json",
    "stickers": "assets/stickers/sticker_db.json"
  }
}
```

---

## 132. Asset validation command future

Possible future CLI:

```bash
ai-video assets validate
```

Possible output:

```text
icons: 20 assets, 0 errors, 2 warnings
fonts: 2 assets, 0 errors
backgrounds: 3 assets, 0 errors
```

---

## 133. Asset search command future

Possible CLI:

```bash
ai-video assets search-icon "báo thức"
```

Possible output:

```text
icon_alarm_001 score=0.91 path=assets/icons/alarm_001.png
icon_clock_001 score=0.76 path=assets/icons/clock_001.png
```

---

## 134. Asset preview command future

Possible CLI:

```bash
ai-video assets preview
```

Possible output:

```text
output/asset_preview/index.html
```

---

## 135. Asset and CI

CI should not require large assets.

CI can validate:

- JSON metadata syntax
- required fields
- duplicate IDs
- relative paths
- small test assets

CI should not download large asset packs by default.

---

## 136. Asset and tests

Use small generated test images.

Example Python test can create a 64x64 PNG icon.

This avoids committing large fixtures.

---

## 137. Asset and docs

When adding a new asset category, update:

```text
docs/AssetGuide.md
docs/JSONSchema.md
docs/RendererDesign.md
docs/DecisionLog.md
```

If renderer behavior changes, update RendererDesign.

---

## 138. Asset and DecisionLog

Major asset decisions should be recorded.

Examples:

- choosing default font family
- choosing icon metadata strategy
- choosing icon embedding model
- adding asset pack structure
- changing asset folder layout

---

## 139. Asset anti-patterns

Avoid:

### 139.1 Random filenames

```text
download.png
new_icon2.png
```

### 139.2 No metadata

Icons without tags cannot be searched well.

### 139.3 Absolute paths

Breaks portability.

### 139.4 Unknown license

Dangerous for production.

### 139.5 Mixed visual styles

Can make output look messy.

### 139.6 Too detailed icons

Unreadable on mobile.

### 139.7 Renderer semantic search

Wrong module responsibility.

### 139.8 LLM exact filename guessing

Unreliable.

### 139.9 Committing private assets

Privacy risk.

### 139.10 Large binary dump

Bloats repository.

---

## 140. Asset review checklist before commit

1. Are files in correct folder?
2. Are filenames clean?
3. Is metadata updated?
4. Are IDs unique?
5. Are paths relative?
6. Are tags useful?
7. Are Vietnamese tags included?
8. Is license known?
9. Do files exist?
10. Do assets work with default template?
11. Are large files avoided?
12. Are docs updated if needed?

---

## 141. Asset setup for Sprint 4

Sprint 4 requires:

```text
assets/icons/icon_db.json
```

Minimum icon DB can contain:

```text
alarm
sleep
money
laugh
question
warning
briefcase
coffee
```

Sprint 4 success:

```text
icon_query → icon_id/icon_path/icon_score
```

Actual rendering of icons happens in Sprint 5.

---

## 142. Asset setup for Sprint 5

Sprint 5 renderer needs:

- at least one font
- optional icon
- default template
- dark background or solid color
- safe zone settings

Minimum:

```text
font fallback
solid dark background
no required icon
```

This keeps renderer simple.

---

## 143. Minimal asset requirement for first renderer

First renderer can work with no external assets if it uses:

- solid color background
- system font fallback
- no icons

But production-quality output needs project fonts and icons.

---

## 144. Asset priority order

For early development:

1. Font with Vietnamese support.
2. Default template.
3. Basic icon DB.
4. Basic icons.
5. Backgrounds.
6. Avatars.
7. SFX.
8. Music.
9. Stickers.

---

## 145. Default font recommendation

Use a Vietnamese-supported bold font.

Recommended candidates:

```text
Be Vietnam Pro
Noto Sans
Roboto
Arial fallback
```

Do not include licensed font files without permission.

---

## 146. Default icon recommendation

Start with simple flat PNG icons.

Keep them readable on dark backgrounds.

---

## 147. Default background recommendation

Start with solid dark color.

This avoids text readability problems.

---

## 148. Default avatar recommendation

Skip avatars for earliest renderer.

Add after text rendering is stable.

---

## 149. Default SFX recommendation

Skip SFX until final audio pipeline works.

Original voice sync is more important.

---

## 150. Final asset rule

Assets should make the video better without making the engine fragile.

If an asset is hard to validate, hard to license, hard to render, or hard to maintain, do not make it required for the core pipeline.

---

# Appendix A - Starter `icon_db.json`

```json
[
  {
    "id": "icon_alarm_001",
    "file": "assets/icons/alarm_001.png",
    "tags": [
      "báo thức",
      "đồng hồ",
      "trễ giờ",
      "dậy sớm"
    ],
    "tags_en": [
      "alarm",
      "clock",
      "late",
      "wake up"
    ],
    "category": "time",
    "style": "flat",
    "mood": [
      "funny",
      "urgent"
    ],
    "license": "project_asset"
  },
  {
    "id": "icon_sleep_001",
    "file": "assets/icons/sleep_001.png",
    "tags": [
      "ngủ",
      "buồn ngủ",
      "zzz",
      "mệt"
    ],
    "tags_en": [
      "sleep",
      "sleepy",
      "tired"
    ],
    "category": "sleep",
    "style": "flat",
    "mood": [
      "funny",
      "tired"
    ],
    "license": "project_asset"
  },
  {
    "id": "icon_money_001",
    "file": "assets/icons/money_001.png",
    "tags": [
      "tiền",
      "lương",
      "thưởng",
      "thu nhập"
    ],
    "tags_en": [
      "money",
      "salary",
      "bonus",
      "income"
    ],
    "category": "money",
    "style": "flat",
    "mood": [
      "happy",
      "serious"
    ],
    "license": "project_asset"
  },
  {
    "id": "icon_briefcase_001",
    "file": "assets/icons/briefcase_001.png",
    "tags": [
      "đi làm",
      "công việc",
      "văn phòng",
      "sự nghiệp"
    ],
    "tags_en": [
      "work",
      "job",
      "office",
      "career"
    ],
    "category": "work",
    "style": "flat",
    "mood": [
      "serious",
      "neutral"
    ],
    "license": "project_asset"
  },
  {
    "id": "icon_coffee_001",
    "file": "assets/icons/coffee_001.png",
    "tags": [
      "cà phê",
      "tỉnh ngủ",
      "buổi sáng"
    ],
    "tags_en": [
      "coffee",
      "morning",
      "wake up"
    ],
    "category": "food",
    "style": "flat",
    "mood": [
      "funny",
      "tired"
    ],
    "license": "project_asset"
  },
  {
    "id": "icon_phone_001",
    "file": "assets/icons/phone_001.png",
    "tags": [
      "điện thoại",
      "gọi điện",
      "tin nhắn"
    ],
    "tags_en": [
      "phone",
      "call",
      "message"
    ],
    "category": "technology",
    "style": "flat",
    "mood": [
      "neutral"
    ],
    "license": "project_asset"
  },
  {
    "id": "icon_question_001",
    "file": "assets/icons/question_001.png",
    "tags": [
      "hỏi",
      "thắc mắc",
      "ủa",
      "không hiểu"
    ],
    "tags_en": [
      "question",
      "confused",
      "why"
    ],
    "category": "emotion",
    "style": "flat",
    "mood": [
      "confused"
    ],
    "license": "project_asset"
  },
  {
    "id": "icon_warning_001",
    "file": "assets/icons/warning_001.png",
    "tags": [
      "cảnh báo",
      "nguy hiểm",
      "chú ý"
    ],
    "tags_en": [
      "warning",
      "danger",
      "alert"
    ],
    "category": "warning",
    "style": "flat",
    "mood": [
      "urgent"
    ],
    "license": "project_asset"
  },
  {
    "id": "icon_laugh_001",
    "file": "assets/icons/laugh_001.png",
    "tags": [
      "cười",
      "hài",
      "vui",
      "haha"
    ],
    "tags_en": [
      "laugh",
      "funny",
      "haha"
    ],
    "category": "emotion",
    "style": "flat",
    "mood": [
      "funny",
      "happy"
    ],
    "license": "project_asset"
  },
  {
    "id": "icon_book_001",
    "file": "assets/icons/book_001.png",
    "tags": [
      "sách",
      "học",
      "học bài",
      "kiến thức"
    ],
    "tags_en": [
      "book",
      "study",
      "knowledge"
    ],
    "category": "education",
    "style": "flat",
    "mood": [
      "serious"
    ],
    "license": "project_asset"
  }
]
```

---

# Appendix B - Starter `font_db.json`

```json
[
  {
    "id": "font_be_vietnam_pro_bold",
    "file": "assets/fonts/BeVietnamPro-Bold.ttf",
    "family": "Be Vietnam Pro",
    "weight": "bold",
    "supports_vietnamese": true,
    "license": "OFL",
    "usage": [
      "main_text",
      "keyword",
      "speaker_label"
    ]
  },
  {
    "id": "font_noto_sans_bold",
    "file": "assets/fonts/NotoSans-Bold.ttf",
    "family": "Noto Sans",
    "weight": "bold",
    "supports_vietnamese": true,
    "license": "OFL",
    "usage": [
      "fallback",
      "main_text"
    ]
  }
]
```

---

# Appendix C - Starter template `tiktok_dark_comic.yaml`

```yaml
name: tiktok_dark_comic
version: 0.1.0

video:
  width: 1080
  height: 1920
  fps: 30

background:
  type: solid
  color: "#080A12"

colors:
  text_primary: "#FFFFFF"
  keyword_primary: "#FFD400"
  stroke: "#000000"
  speaker_a: "#3291FF"
  speaker_b: "#FF5A8C"

font:
  main: font_be_vietnam_pro_bold
  keyword: font_be_vietnam_pro_bold
  label: font_be_vietnam_pro_bold

safe_zone:
  top: 120
  bottom: 220
  left: 80
  right: 140

text:
  main_size: 108
  keyword_size: 136
  label_size: 54
  stroke_width: 4
  keyword_stroke_width: 6
  line_spacing: 28

icon:
  enabled: true
  max_width: 220
  max_height: 220
  preferred_styles:
    - flat
    - comic

speaker_styles:
  speaker_a:
    label_background: "#3291FF"
    label_text: "#FFFFFF"
  speaker_b:
    label_background: "#FF5A8C"
    label_text: "#FFFFFF"

keyword_styles:
  keyword_primary:
    fill: "#FFD400"
    stroke: "#000000"
    stroke_width: 6
    glow: true
    font_scale: 1.2

defaults:
  layout: center_stack
  keyword_effect: pop
  transition: cut
```

---

# Appendix D - Asset validation pseudo-code

```python
def validate_asset_db(items: list[dict], project_root: Path) -> AssetValidationReport:
    errors = []
    warnings = []
    seen_ids = set()

    for index, item in enumerate(items):
        path_prefix = f"items[{index}]"

        asset_id = item.get("id")
        if not asset_id:
            errors.append((path_prefix + ".id", "Missing asset id"))
            continue

        if asset_id in seen_ids:
            errors.append((path_prefix + ".id", f"Duplicate asset id: {asset_id}"))
        seen_ids.add(asset_id)

        file_value = item.get("file")
        if not file_value:
            errors.append((path_prefix + ".file", "Missing asset file"))
            continue

        if Path(file_value).is_absolute():
            errors.append((path_prefix + ".file", "Asset path must be relative"))

        file_path = project_root / file_value
        if not file_path.exists():
            errors.append((path_prefix + ".file", f"File not found: {file_value}"))

        tags = item.get("tags")
        if tags is not None and not tags:
            warnings.append((path_prefix + ".tags", "Tags are empty"))

        if not item.get("license"):
            warnings.append((path_prefix + ".license", "License is missing"))

    return AssetValidationReport(errors=errors, warnings=warnings)
```

---

# Appendix E - Asset work plan by sprint

| Sprint | Asset work |
|---|---|
| Sprint 1 | No major assets required. Only input/output/temp folders. |
| Sprint 2 | No major assets required. Timeline JSON only. |
| Sprint 3 | Prompt files required. Assets optional. |
| Sprint 4 | Icon DB and starter icons required. |
| Sprint 5 | Default template, font fallback, and optional icons required. |
| Sprint 6 | Optional SFX/music still not required. Export original audio. |
| Sprint 7 | Speaker label assets and optional avatars. |
| Sprint 8 | Multiple templates and asset style packs. |

---

# Appendix F - Final checklist for asset system v1

1. assets/icons/icon_db.json exists.
2. Icon IDs are unique.
3. Icon paths are relative.
4. Vietnamese tags exist.
5. Default template exists.
6. Default font strategy exists.
7. Renderer can work without optional icons.
8. Missing icon behavior is documented.
9. Asset validation command or function exists.
10. No private assets are committed.
11. No unknown-license production assets are committed.
12. Docs updated.
