# RendererDesign.md

# AI Video Engine - Renderer Design

## 0. Purpose

This document defines the renderer design for **AI Video Engine**.

The renderer is the part of the system that converts validated **Visual Timeline JSON** into a silent video file.

The renderer is intentionally separated from AI.

The renderer does not analyze meaning.

The renderer does not call LLMs.

The renderer does not transcribe audio.

The renderer does not choose icons semantically.

The renderer only consumes structured JSON, templates, assets, and configuration.

This document should be read together with:

```text
AGENTS.md
PROJECT_RULES.md
docs/Architecture.md
docs/Pipeline.md
docs/JSONSchema.md
docs/AIDesign.md
docs/AssetGuide.md
docs/CodingStandard.md
```

---

## 1. Renderer mission

The renderer's mission is:

```text
Visual Timeline JSON → Silent Video
```

Input:

```text
output/timeline.visual.json
```

Output:

```text
output/silent_video.mp4
```

The exporter later merges the silent video with original audio.

---

## 2. Renderer non-goals

The renderer must not:

- call LLMs
- call Ollama
- call OpenAI
- call Gemini
- call Claude
- run speech-to-text
- infer keywords from raw text
- select semantic icons
- mutate source transcript
- rewrite timeline content
- upload files to cloud services
- generate AI images
- directly depend on chat history
- silently ignore invalid data

---

## 3. Core renderer principle

The renderer is deterministic.

Given the same:

- visual timeline JSON
- renderer version
- template
- assets
- fonts
- config
- random seed

it should produce the same video.

If randomness is used, it must be controlled by a seed.

---

## 4. Renderer location

Renderer code should live under:

```text
src/renderer/
```

Recommended structure:

```text
src/renderer/
├── __init__.py
├── engine.py
├── context.py
├── canvas.py
├── scene.py
├── frame.py
├── timeline.py
├── template.py
├── validation.py
├── registry.py
├── text.py
├── keyword.py
├── icon.py
├── avatar.py
├── background.py
├── layout.py
├── safe_zone.py
├── debug.py
├── backends/
│   ├── __init__.py
│   ├── pillow_moviepy.py
│   ├── ffmpeg.py
│   └── opencv.py
├── effects/
│   ├── __init__.py
│   ├── base.py
│   ├── pop.py
│   ├── bounce.py
│   ├── shake.py
│   ├── glow.py
│   ├── slide.py
│   ├── fade.py
│   ├── pulse.py
│   ├── typewriter.py
│   └── zoom.py
└── layouts/
    ├── __init__.py
    ├── base.py
    ├── center_stack.py
    ├── punchline_center.py
    ├── speaker_label_top.py
    ├── comic_panel.py
    ├── split_speaker.py
    └── avatar_left_text_right.py
```

The exact structure can evolve, but responsibilities should remain clear.

---

## 5. Renderer pipeline

```text
Load Visual Timeline JSON
        ↓
Validate Renderer Input
        ↓
Load Template
        ↓
Load Assets
        ↓
Resolve Fonts
        ↓
Create Render Context
        ↓
For Each Scene:
    Build Scene State
    Compute Layout
    Resolve Styles
    Render Frames / Clip
        ↓
Concatenate Scene Clips
        ↓
Write Silent Video
        ↓
Write Render Metadata
```

---

## 6. Renderer input

The renderer input is:

```text
output/timeline.visual.json
```

Minimum valid example:

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

Renderer must validate this before rendering.

---

## 7. Renderer output

Primary output:

```text
output/silent_video.mp4
```

Optional debug outputs:

```text
output/debug/scene_0001.png
output/debug/scene_0001_layout.json
output/debug/safe_zones.png
output/debug/frame_000001.png
```

Optional renderer report:

```text
output/render_stage_report.json
```

Final export with audio is handled by `src/exporter`.

---

## 8. Renderer boundaries

### Renderer may read

```text
output/timeline.visual.json
assets/
templates/
config/
```

### Renderer may write

```text
output/silent_video.mp4
output/debug/
output/render_stage_report.json
```

### Renderer may not read

```text
prompts/
chat history
LLM raw output unless already validated as timeline
```

### Renderer may not write

```text
output/transcript.json
output/timeline.normalized.json
output/timeline.director.json
```

Those belong to earlier stages.

---

## 9. Renderer stages in detail

### 9.1 Stage 1 - Load timeline

Load JSON from disk.

Check UTF-8.

Parse JSON.

Fail if invalid JSON.

### 9.2 Stage 2 - Validate timeline

Validate required fields.

Validate timing.

Validate known layouts.

Validate known effects.

Validate asset paths.

Validate video spec.

### 9.3 Stage 3 - Load template

Find template by name.

Load template data.

Merge with default template.

Validate template.

### 9.4 Stage 4 - Resolve assets

Resolve icons.

Resolve avatars.

Resolve backgrounds.

Resolve fonts.

Prepare fallbacks.

### 9.5 Stage 5 - Build render context

Create a shared object with:

- video spec
- FPS
- canvas size
- safe zone
- template
- asset registry
- effect registry
- layout registry
- output paths
- random seed

### 9.6 Stage 6 - Render scenes

For each scene:

- compute scene duration
- compute frame count
- compute layout
- create base background
- draw elements
- apply animations
- create clip

### 9.7 Stage 7 - Concatenate scenes

Join clips in timeline order.

### 9.8 Stage 8 - Export silent video

Write MP4 without audio.

### 9.9 Stage 9 - Write renderer report

Write warnings, stats, and debug metadata.

---

## 10. Render context

The render context should contain shared renderer state.

Suggested object:

```python
@dataclass
class RenderContext:
    width: int
    height: int
    fps: float
    template: Template
    safe_zone: SafeZone
    assets: AssetRegistry
    effects: EffectRegistry
    layouts: LayoutRegistry
    output_dir: Path
    debug: bool = False
    seed: int | None = None
```

The context should not contain LLM clients.

---

## 11. Render request

Suggested input object:

```python
@dataclass
class RenderRequest:
    timeline_path: Path
    output_path: Path
    template_name: str | None = None
    debug: bool = False
    preview: bool = False
```

This is used by CLI or application layer.

---

## 12. Render result

Suggested output object:

```python
@dataclass
class RenderResult:
    output_path: Path
    duration: float
    scene_count: int
    width: int
    height: int
    fps: float
    warnings: list[str]
```

---

## 13. Coordinate system

The renderer uses a 2D coordinate system.

Origin:

```text
top-left corner
```

X axis:

```text
left → right
```

Y axis:

```text
top → bottom
```

Default canvas:

```text
width: 1080
height: 1920
```

Coordinates are pixels.

---

## 14. Safe zones

Short-form platforms overlay UI elements.

Text should avoid unsafe areas.

Default safe zone:

```json
{
  "top": 120,
  "bottom": 220,
  "left": 80,
  "right": 140
}
```

Safe content area:

```text
x_min = left
x_max = width - right
y_min = top
y_max = height - bottom
```

Renderer should place important content inside safe zone.

Debug mode should visualize safe zones.

---

## 15. Canvas

The canvas is the base image or frame.

For default 9:16:

```text
1080 x 1920
```

Canvas can be:

- RGB image
- RGBA image
- video frame array
- backend-specific surface

Initial implementation can use Pillow images.

---

## 16. Rendering backends

The renderer may support multiple backends.

### 16.1 Pillow + MoviePy backend

Good for early implementation.

Pros:

- easy to implement
- Python-friendly
- good text drawing through Pillow
- easy debugging

Cons:

- slower for complex animations
- MoviePy can be less stable for large batch rendering

### 16.2 Pillow + FFmpeg backend

Good for deterministic frame rendering.

Pros:

- explicit frame pipeline
- FFmpeg handles video encoding
- predictable output

Cons:

- frame generation can be disk-heavy unless piped

### 16.3 OpenCV backend

Good for frame-level effects.

Pros:

- fast array operations
- good for image/video processing
- useful for shake, blur, motion

Cons:

- text rendering is poor without Pillow/Freetype integration

### 16.4 FFmpeg filter backend

Good for performance later.

Pros:

- fast
- production-grade encoding
- powerful filter graph

Cons:

- complex animation logic
- harder debugging
- text effects can be hard

### 16.5 Recommended initial backend

Start with:

```text
Pillow + MoviePy
```

Later optimize.

---

## 17. Scene lifecycle

A scene is a timed render unit.

Scene lifecycle:

```text
Scene JSON
    ↓
Scene Validation
    ↓
Scene Style Resolution
    ↓
Scene Layout Computation
    ↓
Element Creation
    ↓
Animation Binding
    ↓
Frame Rendering
    ↓
Clip Output
```

---

## 18. Scene state

Suggested object:

```python
@dataclass
class SceneRenderState:
    scene_id: str
    start: float
    end: float
    duration: float
    frame_count: int
    text: str
    lines: list[str]
    layout_name: str
    elements: list[RenderElement]
    warnings: list[str]
```

This object is derived from JSON.

It should not mutate the original JSON.

---

## 19. Frame count

Frame count:

```text
frame_count = round(duration * fps)
```

Minimum frame count should be at least 1.

If duration is 0 or negative, validation should fail earlier.

---

## 20. Time values inside scene

Renderer can use scene-local time.

Example:

```text
global time: 12.50s
scene start: 10.00s
local time: 2.50s
```

Animations should usually use local time.

---

## 21. Render elements

A render element is a drawable object.

Possible element types:

```text
background
text_line
keyword
icon
avatar
speaker_label
shape
sticker
debug_overlay
```

Suggested base object:

```python
@dataclass
class RenderElement:
    id: str
    type: str
    bbox: Rect
    z_index: int
    style: dict
    animations: list[AnimationBinding]
```

Elements should be sorted by `z_index`.

---

## 22. Z-index system

Recommended z-index ranges:

```text
0-99       background
100-199    decorative shapes
200-299    original video background
300-399    icons
400-499    avatars
500-599    text
600-699    keyword overlays
700-799    speaker labels
800-899    effects overlays
900-999    debug overlays
```

The exact values can change, but ordering should be consistent.

---

## 23. Text rendering

Text is the most important visual element.

Text must be:

- large
- readable
- high contrast
- visually expressive
- safe-zone aware
- Vietnamese-compatible

Text rendering should support:

- font selection
- font size
- font weight
- fill color
- stroke color
- stroke width
- shadow
- line spacing
- alignment
- uppercase transform
- scaling
- rotation later
- opacity

---

## 24. Vietnamese text support

Vietnamese is required.

Renderer must support:

- accents
- punctuation
- uppercase accented text
- common Vietnamese dialogue
- UTF-8 input

Fonts must include Vietnamese glyphs.

Potential fonts:

- Arial
- Noto Sans
- Inter
- Be Vietnam Pro
- Roboto

Do not assume all fonts exist on every machine.

Fonts should be asset-managed where possible.

---

## 25. Font resolution

Font resolution order:

1. template font path
2. project asset font
3. configured system font
4. fallback system font
5. fail with clear error if no usable font

Do not silently render with a broken font.

---

## 26. Font object

Suggested object:

```python
@dataclass
class FontSpec:
    family: str | None
    path: Path | None
    size: int
    weight: str = "bold"
```

---

## 27. Text measurement

Before drawing text, renderer must measure it.

Pillow supports:

```python
draw.textbbox(...)
```

Text measurement is required for:

- center alignment
- line wrapping
- keyword positioning
- bounding box debug
- collision detection
- layout computation

---

## 28. Line wrapping

Line wrapping may be done earlier by Visual Director.

Renderer should still protect against oversized text.

If a line is too wide:

Options:

1. reduce font size
2. wrap line
3. use narrower layout
4. fail validation
5. warn and auto-fit

Early renderer can auto-fit by reducing font size.

---

## 29. Auto-fit strategy

Auto-fit should be deterministic.

Example:

```python
while text_width > max_width and font_size > min_font_size:
    font_size -= 4
```

Use clear minimum font size.

If text still does not fit, warn.

---

## 30. Text stroke

Text stroke improves readability.

Default:

```yaml
text:
  stroke_width: 4
  stroke_color: "#000000"
```

For keyword:

```yaml
keyword:
  stroke_width: 6
  stroke_color: "#000000"
```

---

## 31. Text shadow

Shadow improves contrast.

Example:

```yaml
shadow:
  enabled: true
  offset_x: 0
  offset_y: 8
  blur: 12
  color: "#000000"
  opacity: 0.55
```

Initial implementation may approximate shadow by drawing text multiple times.

---

## 32. Text alignment

Supported alignments:

```text
left
center
right
```

Default:

```text
center
```

---

## 33. Keyword rendering

Keywords are emphasis targets.

A keyword can be rendered as:

- larger text
- different color
- glow
- stroke
- scale animation
- shake animation
- separate line
- badge
- sticker-like overlay

Keyword style should come from template.

---

## 34. Keyword target resolution

Keyword target can be resolved by:

1. exact text match in line
2. case-insensitive match
3. accent-insensitive match later
4. manual target ID later

Initial implementation can highlight entire line if keyword is inside that line.

Advanced implementation can highlight only substring.

---

## 35. Keyword styling

Example template:

```yaml
keyword_styles:
  keyword_primary:
    fill: "#FFD400"
    stroke: "#000000"
    stroke_width: 6
    scale: 1.15
    glow: true
```

---

## 36. Keyword animation

A keyword may have animation:

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

Renderer resolves this to an element and applies effect.

---

## 37. Icon rendering

Icons are optional.

If present, renderer should:

- load icon path
- resize icon
- place according to layout/template
- preserve aspect ratio
- apply optional animation
- use fallback if missing and configured

Icon rendering should not perform semantic search.

That belongs to `src/embedding`.

---

## 38. Icon placement

Icon placement can be determined by layout.

Common positions:

```text
above text
below text
left of keyword
right of keyword
corner accent
speaker side
```

Default for early version:

```text
small icon near lower safe-zone or near keyword
```

---

## 39. Icon size

Icon size should be template-controlled.

Example:

```yaml
icon:
  max_width: 220
  max_height: 220
```

---

## 40. Avatar rendering

Avatar support is optional early.

When implemented, avatar rendering should support:

- speaker avatar
- emotion-based avatar variant
- position from layout
- simple entrance animation
- optional bounce

Avatar selection should be done before renderer or through asset mapping.

Renderer only loads and draws the selected avatar.

---

## 41. Speaker label rendering

Speaker labels help dialogue clarity.

Example:

```text
NAM
NỮ
SPEAKER_00
SPEAKER_01
```

Speaker label style should come from template.

Example:

```yaml
speaker_styles:
  speaker_a:
    background: "#3291FF"
    text: "#FFFFFF"
  speaker_b:
    background: "#FF5A8C"
    text: "#FFFFFF"
```

---

## 42. Background rendering

Background can be:

- solid color
- gradient
- image
- blurred input video
- animated pattern later

Initial default:

```text
solid dark background
```

Example:

```yaml
background:
  type: solid
  color: "#080A12"
```

---

## 43. Gradient background

Future template example:

```yaml
background:
  type: gradient
  colors:
    - "#080A12"
    - "#15183A"
  direction: vertical
```

Initial implementation can skip gradient.

---

## 44. Original video background

Future feature.

The renderer may use the original video as:

- blurred background
- cropped background
- dimmed background
- overlay source

This should be template-controlled.

This must not be mixed into early basic renderer unless needed.

---

## 45. Shape rendering

Shapes can support comic style.

Examples:

- rounded rectangles
- speech bubbles
- underline
- highlight blocks
- burst shapes
- arrows
- dividers

Initial renderer may only need rounded rectangles for speaker labels.

---

## 46. Layout system

Layout computes element positions.

Layout receives:

- scene
- canvas
- safe zone
- template
- measured text sizes
- assets

Layout returns:

- bounding boxes
- alignment
- element order
- optional constraints

Layout should not draw.

It only computes positions.

---

## 47. Layout interface

Suggested interface:

```python
class Layout:
    name: str

    def compute(self, scene: VisualScene, context: RenderContext) -> LayoutResult:
        ...
```

---

## 48. Layout result

Suggested object:

```python
@dataclass
class LayoutResult:
    elements: list[RenderElement]
    warnings: list[str]
```

---

## 49. Initial layouts

### 49.1 center_stack

Large centered stacked text.

Good for:

- simple dialogue
- strong statements
- short scenes

### 49.2 punchline_center

Keyword or punchline dominates center.

Good for:

- comedy punchline
- twist
- surprise

### 49.3 speaker_label_top

Speaker label near top with text in center.

Good for:

- dialogue clarity

### 49.4 comic_panel

More playful panel style.

Good for:

- humorous dialogue

### 49.5 split_speaker

Two speaker zones.

Good for:

- back-and-forth conversation

### 49.6 avatar_left_text_right

Avatar on left, text on right.

Good for:

- character-driven scenes

---

## 50. center_stack layout

Default algorithm:

1. Determine safe content rectangle.
2. Measure all text lines.
3. Compute total text height.
4. Center block vertically.
5. Center each line horizontally.
6. Apply keyword style to keyword lines.
7. Place optional icon near block.

Pseudo:

```python
safe = context.safe_zone.rect
line_boxes = measure_lines(scene.lines)
block_height = sum(line.height for line in line_boxes) + line_spacing
y = safe.center_y - block_height / 2
for line in lines:
    x = safe.center_x - line.width / 2
    place(line, x, y)
    y += line.height + line_spacing
```

---

## 51. punchline_center layout

Default algorithm:

1. Identify strongest keyword.
2. Render non-keyword text smaller.
3. Render keyword largest.
4. Put keyword in visual center.
5. Add icon or burst around keyword.

Good for scenes like:

```text
TẠI
BÁO THỨC!
```

---

## 52. speaker_label_top layout

Default algorithm:

1. Put speaker label in upper safe zone.
2. Put text block in center.
3. Use speaker style color.
4. Optionally place avatar near label.

---

## 53. comic_panel layout

Future layout.

Possible features:

- panel borders
- speech bubble
- sticker icons
- playful rotations
- burst keyword background

Do not implement too early unless needed.

---

## 54. split_speaker layout

Future layout.

Good for two-person dialogue.

Possible design:

```text
top half: speaker A
bottom half: speaker B
```

or:

```text
left side: speaker A
right side: speaker B
```

For vertical 9:16, top/bottom is often safer.

---

## 55. Effect system

Effects modify element properties over time.

Effects should not know about AI.

Effects receive:

- element
- local time
- effect params
- scene duration
- FPS

Effects return transformed element state.

---

## 56. Effect interface

Suggested interface:

```python
class Effect:
    name: str

    def transform(
        self,
        element: RenderElement,
        local_time: float,
        animation: Animation,
        context: RenderContext,
    ) -> RenderElementState:
        ...
```

Alternative simpler first version:

```python
def apply_pop(progress: float, params: dict) -> Transform:
    ...
```

---

## 57. Animation progress

For an animation:

```text
start_offset = 0.5
duration = 0.3
```

At local scene time:

```text
progress = (local_time - start_offset) / duration
```

Clamp progress:

```text
0 ≤ progress ≤ 1
```

If local time is outside animation window, return base state.

---

## 58. Transform properties

Effects may modify:

- x
- y
- scale
- opacity
- rotation
- blur later
- glow intensity
- color later

Initial implementation can support:

```text
x
y
scale
opacity
```

---

## 59. Pop effect

Purpose:

- punchline
- surprise
- keyword emphasis

Behavior:

```text
scale 1.0 → 1.25 → 1.0
```

Possible easing:

```text
ease out then ease in
```

Parameters:

```json
{
  "scale": 1.25
}
```

---

## 60. Bounce effect

Purpose:

- humor
- playful motion

Behavior:

```text
y offset moves up/down with damping
```

Parameters:

```json
{
  "amplitude": 24,
  "bounces": 2
}
```

---

## 61. Shake effect

Purpose:

- chaos
- anger
- alarm
- comedic emphasis

Behavior:

```text
x/y jitter around base position
```

Parameters:

```json
{
  "amplitude": 8,
  "frequency": 18
}
```

Use deterministic pseudo-random or sine wave.

---

## 62. Glow effect

Purpose:

- importance
- magic
- key concept
- visual focus

Behavior:

```text
draw blurred colored text or surrounding glow
```

Initial implementation may approximate with multiple offset strokes.

---

## 63. Slide effect

Purpose:

- entrance
- transition
- conversational flow

Behavior:

```text
x or y position moves from offscreen or offset to final position
```

Parameters:

```json
{
  "direction": "left",
  "distance": 120
}
```

---

## 64. Fade effect

Purpose:

- soft entrance
- subtle exit

Behavior:

```text
opacity 0 → 1
```

Parameters:

```json
{
  "from": 0,
  "to": 1
}
```

---

## 65. Pulse effect

Purpose:

- repeated emphasis

Behavior:

```text
scale or brightness oscillates
```

Parameters:

```json
{
  "scale": 1.08,
  "frequency": 2
}
```

---

## 66. Typewriter effect

Future effect.

Purpose:

- suspense
- reveal
- narration sync

Behavior:

```text
characters appear progressively
```

Requires text-level clipping or substring rendering.

---

## 67. Zoom effect

Can apply to:

- scene camera
- text element
- icon
- background

Initial version can implement element zoom only.

Scene camera zoom can come later.

---

## 68. Easing functions

Effects should use easing functions.

Initial easing functions:

```text
linear
ease_in
ease_out
ease_in_out
ease_out_back
```

Suggested utility:

```python
def ease_out_back(t: float) -> float:
    ...
```

---

## 69. Effect registry

Effects should be registered centrally.

Example:

```python
EFFECT_REGISTRY = {
    "pop": PopEffect(),
    "bounce": BounceEffect(),
    "shake": ShakeEffect(),
    "glow": GlowEffect(),
    "slide": SlideEffect(),
    "fade": FadeEffect(),
    "pulse": PulseEffect(),
}
```

Renderer validation checks against this registry.

---

## 70. Unknown effect behavior

If timeline contains:

```json
"type": "explode_spin"
```

and it is not registered, renderer must fail before rendering.

Error:

```text
Unknown effect 'explode_spin' in scene_0004.
Allowed effects: pop, bounce, shake, glow, slide, fade, pulse.
```

---

## 71. Template system

Template controls visual style.

Renderer should not hardcode all colors and sizes.

Template example:

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

font:
  primary:
    path: assets/fonts/BeVietnamPro-Bold.ttf
    size: 108
  keyword:
    path: assets/fonts/BeVietnamPro-ExtraBold.ttf
    size: 136

colors:
  text_primary: "#FFFFFF"
  keyword_primary: "#FFD400"
  stroke: "#000000"
  speaker_a: "#3291FF"
  speaker_b: "#FF5A8C"

safe_zone:
  top: 120
  bottom: 220
  left: 80
  right: 140

defaults:
  layout: center_stack
  keyword_effect: pop
```

---

## 72. Template merge

Renderer may merge:

```text
built-in defaults
→ base template
→ selected template
→ timeline overrides
→ CLI overrides
```

Later values override earlier values.

---

## 73. Style resolution

When rendering a text line, style may come from:

1. keyword style
2. scene style
3. speaker style
4. layout default
5. template default
6. engine fallback

Resolution must be deterministic.

---

## 74. Color handling

Colors should be parsed from:

```text
#RRGGBB
#RRGGBBAA
rgb(...)
named style keys
```

Initial version can support hex only.

---

## 75. Alpha handling

If using Pillow RGBA, alpha should be supported.

Opacity effects require alpha.

---

## 76. Image loading

Image assets should be loaded safely.

Rules:

- check file exists
- handle unsupported format
- convert to RGBA where needed
- preserve aspect ratio
- cache loaded images if repeated

---

## 77. Asset cache

Renderer may cache loaded assets in memory.

Examples:

```text
font cache
image cache
template cache
```

This improves performance.

---

## 78. Missing asset behavior

Configurable policies:

```text
fail
warn_and_skip
use_fallback
```

Default for early renderer:

```text
warn_and_skip icon
fail missing font if no fallback
```

---

## 79. Background rendering order

For each frame:

1. draw background
2. draw background decorations
3. draw avatars/icons behind text if needed
4. draw text
5. draw keyword overlays
6. draw foreground effects
7. draw debug overlays

---

## 80. Text block rendering

Text block includes multiple lines.

Properties:

- lines
- line spacing
- alignment
- max width
- x/y
- style per line
- keyword highlight

The renderer should treat text block as a group for some effects.

---

## 81. Per-line rendering

Each line can have:

- text
- font
- fill color
- stroke
- shadow
- bbox
- animation
- z-index

---

## 82. Per-keyword rendering

Initial renderer can highlight whole lines containing keywords.

Later renderer can highlight substrings.

Substring highlighting is harder because it requires measuring text fragments.

---

## 83. Substring keyword highlighting future

Algorithm:

1. Split line into before/keyword/after.
2. Measure each segment.
3. Draw before normal.
4. Draw keyword highlighted.
5. Draw after normal.
6. Apply keyword animation only to keyword fragment.

This can be implemented after basic renderer.

---

## 84. Motion timing

Scene-level motion should be tied to scene local time.

Keyword-level motion can use:

```json
"start_offset": 0.8
```

If absent, default timing may be chosen by renderer/template.

---

## 85. Default animation timing

If a keyword has effect but no explicit animation object:

Renderer may create default animation:

```json
{
  "target": {
    "type": "keyword",
    "text": "KEYWORD"
  },
  "type": "pop",
  "start_offset": 0.2,
  "duration": 0.35
}
```

This behavior should be documented and deterministic.

---

## 86. FPS handling

Renderer uses FPS from timeline or template.

Default:

```text
30
```

Frame timestamp:

```python
t = frame_index / fps
```

Scene local time:

```python
local_t = frame_index / fps
```

---

## 87. Scene duration and frame count

Example:

```text
duration = 1.91
fps = 30
frame_count = round(1.91 * 30) = 57
```

Be careful that concatenated frame counts may slightly differ from audio duration.

Exporter should validate final duration.

---

## 88. Gaps between scenes

If timeline scenes have gaps:

```text
scene_1 ends at 1.5
scene_2 starts at 2.0
gap = 0.5
```

Possible behavior:

- preserve gap as blank/background
- extend previous scene
- start next scene immediately
- configurable

Initial renderer can render scenes sequentially by duration and ignore absolute gaps.

But this must be documented.

---

## 89. Overlapping scenes

Overlapping scenes are not supported initially.

Validation should fail unless overlays are explicitly introduced later.

---

## 90. Preview mode

Preview mode renders faster.

Possible settings:

```yaml
preview:
  width: 540
  height: 960
  fps: 15
```

Preview should preserve layout ratios.

---

## 91. Debug mode

Debug mode may render:

- safe zone rectangle
- element bounding boxes
- scene ID
- timestamp
- layout name
- asset IDs
- keyword targets

Debug overlays should not appear in production output.

---

## 92. Debug frame export

Useful for layout debugging.

Example:

```text
output/debug/scene_0001_frame_0000.png
```

This allows quick inspection without rendering full video.

---

## 93. Render report

Renderer may produce:

```text
output/render_stage_report.json
```

Example:

```json
{
  "scene_count": 14,
  "width": 1080,
  "height": 1920,
  "fps": 30,
  "duration": 28.4,
  "warnings": [
    "scene_0004 icon missing, skipped"
  ]
}
```

Final exporter writes full `render_report.json`.

---

## 94. Error handling

Renderer errors should be explicit.

Examples:

```text
InvalidVisualTimelineError
UnknownLayoutError
UnknownEffectError
MissingFontError
MissingAssetError
TextOverflowWarning
RenderBackendError
```

---

## 95. Validation before rendering

Before rendering, validate:

- timeline JSON is valid
- video spec exists
- template exists
- scenes exist
- scene durations valid
- layouts known
- effects known
- fonts resolvable
- assets exist or have fallback
- output path writable

---

## 96. Renderer should fail early

Do not render 90% of a video and then fail due to unknown effect.

Validate everything before heavy rendering.

---

## 97. Warning policy

Warnings are acceptable for recoverable issues.

Examples:

- icon missing but configured to skip icons
- text auto-fit reduced font size
- low icon score
- optional avatar missing

Warnings should be reported.

---

## 98. Text overflow policy

If text does not fit:

1. reduce font size
2. wrap if allowed
3. reduce line spacing if allowed
4. warn
5. fail if still impossible and strict mode is on

Do not let text go offscreen silently.

---

## 99. Font fallback policy

If configured font missing:

1. try fallback font from template
2. try system fallback
3. fail if no usable font

Renderer must not use a font that cannot display Vietnamese.

---

## 100. Renderer backend interface

Suggested interface:

```python
class RenderBackend:
    def render(self, timeline: VisualTimeline, context: RenderContext) -> RenderResult:
        ...
```

Backend-specific implementations:

```python
PillowMoviePyBackend
PillowFFmpegBackend
OpenCVBackend
```

---

## 101. First implementation plan

The first renderer should be simple.

Scope:

- read `timeline.visual.json`
- load dark template
- create 1080x1920 canvas
- render large text
- render keyword lines in yellow
- render speaker label
- render optional icon
- implement simple `pop` effect
- export `silent_video.mp4`

Do not implement everything at once.

---

## 102. First renderer pseudo-code

```python
def render_video(timeline_path: Path, output_path: Path):
    timeline = load_visual_timeline(timeline_path)
    validate_visual_timeline(timeline)

    template = load_template(timeline.template.name)
    context = build_context(timeline, template)

    clips = []

    for scene in timeline.scenes:
        clip = render_scene(scene, context)
        clips.append(clip)

    final = concatenate(clips)
    final.write_videofile(output_path, fps=context.fps, audio=False)
```

---

## 103. First scene pseudo-code

```python
def render_scene(scene, context):
    duration = scene.duration

    def make_frame(t):
        canvas = create_background(context)
        layout = compute_layout(scene, context)
        elements = build_elements(scene, layout, context)

        for element in sorted(elements, key=lambda e: e.z_index):
            state = apply_animations(element, t, scene, context)
            draw_element(canvas, state, context)

        return np.array(canvas)

    return VideoClip(make_frame, duration=duration)
```

---

## 104. Drawing order pseudo-code

```python
draw_background()
draw_decorations()
draw_icon()
draw_avatar()
draw_speaker_label()
draw_text_lines()
draw_keyword_highlights()
draw_debug_overlay()
```

---

## 105. Rendering text with Pillow

Example concept:

```python
img = Image.new("RGBA", (width, height), background)
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(font_path, font_size)

draw.text(
    (x, y),
    text,
    font=font,
    fill=fill,
    stroke_width=stroke_width,
    stroke_fill=stroke_fill,
)
```

Need to ensure Vietnamese font support.

---

## 106. MoviePy integration

For dynamic frames:

```python
from moviepy import VideoClip

clip = VideoClip(make_frame, duration=scene.duration)
```

For static scene with simple image:

```python
from moviepy import ImageClip

clip = ImageClip(image_path).with_duration(scene.duration)
```

MoviePy v2 API differs from older examples.

Use the installed version carefully.

---

## 107. Static vs dynamic rendering

### Static scene

Only one image for whole scene.

Fast.

Useful for early renderer.

### Dynamic scene

Frame function changes over time.

Needed for animation.

Initial renderer may mix both.

---

## 108. Efficient simple animation

Instead of re-layout every frame:

1. compute layout once
2. compute base elements once
3. apply transforms per frame
4. draw transformed elements

This is faster and more stable.

---

## 109. Element transform

Suggested object:

```python
@dataclass
class Transform:
    x: float = 0
    y: float = 0
    scale: float = 1
    rotation: float = 0
    opacity: float = 1
```

---

## 110. Rendering transformed text

For scale/opacity:

1. render text to transparent layer
2. scale layer
3. adjust opacity
4. composite onto canvas

This is more flexible than drawing text directly every time.

---

## 111. Layer-based rendering

A layer is an RGBA image.

Render each element onto a layer.

Apply transform.

Composite onto canvas.

This supports:

- opacity
- scaling
- rotation
- glow
- shadows
- shake

---

## 112. Layer compositing

Use Pillow:

```python
base.alpha_composite(layer, dest=(x, y))
```

For opacity:

```python
alpha = layer.getchannel("A")
alpha = alpha.point(lambda p: int(p * opacity))
layer.putalpha(alpha)
```

---

## 113. Scaling layer

Use Pillow resize.

```python
scaled = layer.resize((new_w, new_h), Image.Resampling.LANCZOS)
```

---

## 114. Rotation layer

Use Pillow rotate.

```python
rotated = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
```

Rotation can come later.

---

## 115. Glow implementation

Simple glow:

1. render text mask
2. blur mask
3. colorize blur
4. composite glow behind text
5. draw text on top

Pillow:

```python
ImageFilter.GaussianBlur(radius)
```

---

## 116. Shadow implementation

Simple shadow:

1. draw text in shadow color at offset
2. optionally blur layer
3. draw text on top

---

## 117. Rounded rectangle speaker label

Use:

```python
draw.rounded_rectangle(...)
```

Speaker label should use template colors.

---

## 118. Icon resizing

Preserve aspect ratio.

```python
ratio = min(max_w / w, max_h / h)
new_size = (int(w * ratio), int(h * ratio))
```

---

## 119. Icon compositing

Use RGBA.

If icon has transparency, preserve alpha.

If icon has no alpha, convert to RGBA.

---

## 120. Background solid color

Initial background:

```python
Image.new("RGBA", (width, height), color)
```

---

## 121. Background gradient future

Gradient can be generated line by line.

But early version can skip.

---

## 122. Background image future

If template uses image:

1. load image
2. resize/crop to canvas
3. optionally darken/blur
4. composite

---

## 123. Original video background future

This requires reading frames from original video.

It should be a separate backend or template mode.

Not required for first renderer.

---

## 124. Safe zone debug overlay

Draw rectangle:

```python
draw.rectangle(safe_rect, outline="red", width=3)
```

Also draw labels:

```text
SAFE ZONE
```

---

## 125. Bounding box debug overlay

For each element:

```python
draw.rectangle(element.bbox, outline=color)
draw.text((x, y), element.id)
```

---

## 126. Time debug overlay

Show:

```text
scene_0001 | t=0.42s | frame=13
```

---

## 127. Renderer validation object

Suggested:

```python
@dataclass
class RenderValidationResult:
    valid: bool
    errors: list[ValidationIssue]
    warnings: list[ValidationIssue]
```

---

## 128. Validation issue

```python
@dataclass
class ValidationIssue:
    path: str
    message: str
    severity: Literal["info", "warning", "error"]
    code: str | None = None
```

---

## 129. Unknown layout handling

If unknown layout:

```text
Unknown layout 'crazy_grid' in scene_0007.
Allowed layouts: center_stack, punchline_center, speaker_label_top.
```

Fail before render.

---

## 130. Unknown animation handling

If unknown animation:

```text
Unknown effect 'explode' in scene_0002.
Allowed effects: pop, bounce, shake, glow, slide, fade, pulse.
```

Fail before render.

---

## 131. Duration mismatch handling

Renderer produces silent video.

Exporter validates with audio.

Renderer should still report total expected duration:

```python
sum(scene.duration for scene in timeline.scenes)
```

---

## 132. Total duration

Visual timeline duration:

```text
last_scene.end - first_scene.start
```

or sequential duration:

```text
sum(scene.duration)
```

The project should decide how to treat gaps.

Early renderer can use sequential duration.

Document this in report.

---

## 133. Scene gaps policy

Recommended early policy:

```text
Render scenes sequentially using each scene.duration.
Ignore absolute gaps.
```

Later:

```text
preserve_gaps: true/false
```

---

## 134. Audio sync concern

If ignoring gaps, final video may not exactly match original audio timing.

For Sprint 5 basic renderer, this is acceptable.

For Sprint 6 exporter, sync should be reviewed.

Long-term, renderer should preserve absolute timing or timeline analyzer should remove gaps intentionally.

---

## 135. Preserving absolute timing future

A future renderer can:

- create blank scene for gaps
- align scenes to global timeline
- preserve exact speech timing
- allow background during silence

---

## 136. Renderer quality priorities

Priority order:

1. readable text
2. correct timing
3. no crashes
4. visual consistency
5. simple animation
6. icon/avatar polish
7. performance optimization

---

## 137. First visual style

Default style:

```text
dark background
white main text
yellow keyword
black stroke
blue speaker A
pink speaker B
large bold font
centered layout
```

---

## 138. Default colors

```yaml
colors:
  background: "#080A12"
  text_primary: "#FFFFFF"
  keyword_primary: "#FFD400"
  stroke: "#000000"
  speaker_a: "#3291FF"
  speaker_b: "#FF5A8C"
```

---

## 139. Default font sizes

For 1080x1920:

```yaml
font:
  main_size: 108
  keyword_size: 136
  label_size: 54
  small_size: 36
```

Auto-fit may reduce sizes.

---

## 140. Default spacing

```yaml
layout:
  line_spacing: 28
  block_spacing: 48
  icon_spacing: 32
```

---

## 141. Default speaker label

Position:

```text
top safe zone
x = 80
y = 90
```

Style:

```text
rounded rectangle
white text
speaker color background
```

---

## 142. Default keyword behavior

If a line contains keyword:

- line fill becomes keyword color
- font size increases
- pop animation if requested

---

## 143. Default icon behavior

If icon exists:

- place near text block
- max size 200px
- optional bounce/pop
- skip if missing with warning

---

## 144. Default background behavior

Use solid dark background.

Add subtle decorative shapes later.

---

## 145. Renderer testing

Renderer tests should include:

- loading minimal visual timeline
- validating required fields
- rejecting unknown effect
- rejecting unknown layout
- rendering one frame
- rendering one short video
- handling Vietnamese text
- missing icon warning
- missing font fallback

---

## 146. Unit tests

Unit tests should not render long videos.

Use tiny durations:

```text
0.3s
```

Use preview size if needed:

```text
270x480
```

---

## 147. Golden image tests

Future tests may compare output frames.

Be careful because font rendering can vary across platforms.

Golden image tests may be brittle.

Use them selectively.

---

## 148. Smoke tests

A smoke test should ensure:

```text
minimal visual timeline → silent_video.mp4
```

This can be optional if video encoding is slow in CI.

---

## 149. CI considerations

CI should not require:

- large assets
- big videos
- GPU
- external model downloads

Renderer unit tests should use generated assets.

---

## 150. Generated test assets

Tests can generate:

- simple PNG icon
- simple font fallback
- simple JSON timeline

Do not commit large binary fixtures.

---

## 151. Performance considerations

Potential bottlenecks:

- per-frame text rendering
- repeated font loading
- repeated image loading
- MoviePy overhead
- video encoding

Optimization steps:

1. cache fonts
2. cache images
3. pre-render text layers
4. reuse static background
5. render static scenes as images
6. switch backend if needed

---

## 152. Pre-render text layers

For each line:

1. render text to transparent layer once
2. transform layer per frame
3. composite layer

This avoids redrawing text every frame.

---

## 153. Static scene optimization

If scene has no animations:

- render one image
- create ImageClip
- set duration

No need for per-frame rendering.

---

## 154. Animated scene optimization

If only one element animates:

- pre-render static background
- pre-render static elements
- composite animated element per frame

---

## 155. Batch rendering optimization

For many videos:

- load templates once
- load fonts once
- load common icons once
- reuse model outputs where possible
- avoid reinitializing backend

---

## 156. Memory management

Long videos can use memory.

Avoid storing all frames in memory.

Prefer streaming or MoviePy clip generation.

Close clips when done.

---

## 157. Temporary files

Renderer may write temp files under:

```text
temp/render/
```

Do not commit temp files.

Clean up optionally.

---

## 158. Renderer CLI future

Possible commands:

```bash
ai-video render output/timeline.visual.json
ai-video render output/timeline.visual.json --template tiktok_dark_comic
ai-video render output/timeline.visual.json --preview
ai-video render output/timeline.visual.json --debug
```

---

## 159. Renderer configuration future

Example:

```yaml
renderer:
  backend: pillow_moviepy
  template: tiktok_dark_comic
  preview: false
  debug: false
  preserve_gaps: false
  strict_assets: false
  output_path: output/silent_video.mp4
```

---

## 160. Renderer and exporter separation

Renderer output is silent.

Exporter merges audio.

This separation allows:

- visual preview without audio
- replacing audio later
- using generated TTS later
- testing renderer independently
- debugging sync issues

---

## 161. Renderer and AI separation

This is non-negotiable.

Bad:

```python
if scene.text contains funny:
    call_llm_to_choose_effect()
```

Good:

```python
effect = scene.keywords[0].effect
effect_registry.apply(effect)
```

---

## 162. Renderer and timeline validation

Renderer should not try to "fix" timeline deeply.

It can apply safe visual fallbacks.

But timeline structure errors should fail.

Examples:

- missing scene ID → fail
- unknown effect → fail
- missing optional icon → warn
- text slightly too wide → auto-fit and warn

---

## 163. Renderer and templates

Renderer should rely on templates for style.

Bad:

```python
keyword_color = (255, 215, 0)
```

Good:

```python
keyword_color = template.colors.keyword_primary
```

Default values can exist, but should be centralized.

---

## 164. Renderer and assets

Renderer should not search the web for assets.

Renderer should not generate assets.

Renderer should load local assets only.

---

## 165. Renderer and prompts

Renderer should never read prompt files.

Prompt files belong to AI Director.

---

## 166. Renderer and reports

Renderer should report:

- scene count
- duration
- resolution
- backend
- template
- warnings
- missing assets
- auto-fit events
- output file

---

## 167. Renderer and accessibility

Readable text is key.

Good practices:

- high contrast
- stroke/shadow
- large font
- avoid excessive motion
- safe zone
- avoid too much text
- avoid low contrast backgrounds

---

## 168. Renderer and comedy timing

The director decides what to emphasize.

Renderer executes timing.

Effects should be quick and punchy.

For short-form dialogue:

```text
0.2s - 0.5s effects often work well
```

Avoid long animations that delay readability.

---

## 169. Renderer and mobile UI

Avoid important content in areas where platform UI appears.

For TikTok/Reels/Shorts, right side and bottom may be obstructed.

Safe zone should be template-controlled.

---

## 170. Renderer and aspect ratios

Default is 9:16.

Later support:

```text
1:1
16:9
4:5
```

Templates should define aspect ratio.

Renderer should not assume 1080x1920 everywhere.

---

## 171. Renderer and resolution scaling

Layout should scale with resolution.

If preview mode uses 540x960, positions and font sizes should scale.

Recommended:

```text
scale_x = width / 1080
scale_y = height / 1920
```

Use consistent scaling rules.

---

## 172. Renderer and style tokens

Templates should define style tokens.

Example:

```yaml
styles:
  text_main:
    font_size: 108
    fill: text_primary
  keyword_primary:
    font_size: 136
    fill: keyword_primary
```

Timeline can refer to style names.

---

## 173. Renderer and element IDs

Elements should have stable IDs.

Examples:

```text
scene_0001.line_0
scene_0001.keyword_0
scene_0001.icon_0
scene_0001.speaker_label
```

Useful for debugging and animation targeting.

---

## 174. Renderer and animation targets

Animation target resolution:

```json
{
  "target": {
    "type": "keyword",
    "text": "BÁO THỨC"
  }
}
```

Renderer resolves to element ID.

If no match, validation should warn or fail.

---

## 175. Renderer and line-level targeting

Example:

```json
{
  "target": {
    "type": "line",
    "index": 1
  }
}
```

This targets second line.

Useful when keyword matching is difficult.

---

## 176. Renderer and scene-level targeting

Example:

```json
{
  "target": {
    "type": "scene"
  },
  "type": "zoom"
}
```

Applies to whole scene/camera.

Can be implemented later.

---

## 177. Renderer and camera movement

Camera movement is optional.

Future scene-level effects:

- slow zoom in
- slow zoom out
- shake scene
- pan
- rotate

Initial renderer can skip camera movement.

---

## 178. Renderer and transitions

Transitions can happen between scenes.

Initial support:

```text
cut
```

Later:

```text
fade
slide
zoom
wipe
```

Transitions complicate timing.

Implement after basic scene rendering.

---

## 179. Renderer and sound effects

SFX are not renderer's core responsibility.

Visual renderer may output SFX timing metadata later.

Audio mixing belongs to exporter/audio module.

---

## 180. Renderer and background music

BGM belongs to exporter/audio mixing, not renderer.

Renderer may include visual hints but should not mix audio.

---

## 181. Renderer and subtitles

This project is not simple subtitles.

Renderer creates full-screen kinetic text.

Do not implement standard subtitle overlay as the main design.

---

## 182. Renderer and manual timeline edits

If user manually edits `timeline.visual.json`, renderer should respect it.

This is why schema must be human-readable.

---

## 183. Renderer and validation strictness

Suggested modes:

```text
strict
normal
lenient
```

### strict

Fail on any missing optional asset.

### normal

Fail on structural errors, warn on optional assets.

### lenient

Try to render as much as possible.

Default:

```text
normal
```

---

## 184. Renderer and fallback layout

If layout is missing, renderer may use template default.

If layout is unknown, renderer should fail.

---

## 185. Renderer and fallback effect

If keyword has no effect, template default may be used.

If effect is unknown, fail.

---

## 186. Renderer and fallback icon

If icon missing:

- normal mode: warn and skip
- strict mode: fail
- lenient mode: skip silently? no, still report warning

---

## 187. Renderer and fallback text

If lines missing but text exists, renderer may generate lines in lenient mode.

But final visual timeline should include lines.

---

## 188. Renderer and renderer-owned defaults

Renderer-owned defaults should be centralized.

Example:

```python
DEFAULT_VIDEO_WIDTH = 1080
DEFAULT_VIDEO_HEIGHT = 1920
DEFAULT_FPS = 30
```

But prefer config/template.

---

## 189. Renderer and asset paths

Use `pathlib.Path`.

Resolve relative paths against project root.

Do not assume current working directory.

---

## 190. Renderer and project root

There should be a project root resolver.

Example:

```python
project_root = find_project_root()
```

or pass root explicitly through config.

---

## 191. Renderer and output overwrite

If output exists:

- overwrite if `--overwrite`
- fail if not allowed
- default can overwrite during development

Be explicit.

---

## 192. Renderer and file permissions

If output directory is not writable, fail clearly.

---

## 193. Renderer and temporary previews

Preview images can be saved under:

```text
output/debug/
```

Do not write them into source folders.

---

## 194. Renderer and dependency isolation

Renderer should not require Faster Whisper.

Renderer should not require sentence-transformers.

Renderer should not require Ollama.

This keeps renderer lightweight.

---

## 195. Renderer and imports

Bad:

```python
from src.director import VisualDirector
```

inside renderer.

Good:

```python
from src.timeline.models import VisualTimeline
```

if shared schema models exist.

---

## 196. Shared schema models

Timeline data models may live in:

```text
src/timeline/schema.py
```

or:

```text
src/common/schema.py
```

Renderer can import schema models but not AI modules.

---

## 197. Renderer and package design

Renderer should be importable:

```python
from ai_video_engine.renderer import render_video
```

Long-term package name may be:

```text
ai_video_engine
```

---

## 198. Renderer and command line

CLI should call renderer service.

Bad:

```python
# all rendering code inside cli.py
```

Good:

```python
result = renderer.render(request)
```

---

## 199. Renderer and unit test sample timeline

A minimal test timeline should be stored or generated.

Example:

```python
def make_minimal_timeline():
    return {
        "schema_version": "0.1.0",
        "template": {"name": "test"},
        "video": {"width": 270, "height": 480, "fps": 10},
        "scenes": [...]
    }
```

---

## 200. Renderer and test template

Use a test template with:

- tiny resolution
- simple colors
- system font fallback
- no external large assets

---

## 201. Renderer and future plugin discovery

Effect plugins may later be discovered dynamically.

Early version can use static registry.

Do not over-engineer plugin loading too early.

---

## 202. Renderer and deterministic seed

If effect uses random shake, seed it.

Example:

```python
random.Random(context.seed + scene_index)
```

Better yet, use sine functions for deterministic shake.

---

## 203. Deterministic shake

Example:

```python
dx = math.sin(t * frequency * 2 * math.pi) * amplitude
dy = math.cos(t * frequency * 2 * math.pi) * amplitude * 0.6
```

No random needed.

---

## 204. Pop easing example

```python
def pop_scale(progress: float, max_scale: float = 1.25) -> float:
    if progress < 0.5:
        return 1 + (max_scale - 1) * (progress / 0.5)
    return max_scale - (max_scale - 1) * ((progress - 0.5) / 0.5)
```

Later use better easing.

---

## 205. Bounce easing example

```python
offset = -abs(math.sin(progress * math.pi * bounces)) * amplitude * (1 - progress)
```

---

## 206. Fade example

```python
opacity = start + (end - start) * progress
```

---

## 207. Slide example

For slide from left:

```python
x = final_x - distance * (1 - eased_progress)
```

---

## 208. Renderer development phases

### Phase 1

Static scene renderer.

### Phase 2

Basic keyword highlight.

### Phase 3

Basic animations.

### Phase 4

Icons.

### Phase 5

Templates.

### Phase 6

Avatars.

### Phase 7

Advanced transitions.

### Phase 8

Optimized backend.

---

## 209. Phase 1 deliverables

- render one scene
- dark background
- centered text
- output image
- output short silent video

---

## 210. Phase 2 deliverables

- detect keyword line
- render keyword color
- different font size
- stroke

---

## 211. Phase 3 deliverables

- pop effect
- shake effect
- simple frame-based animation

---

## 212. Phase 4 deliverables

- load icon
- resize icon
- place icon
- missing icon warning

---

## 213. Phase 5 deliverables

- load template
- style tokens
- safe zone
- speaker colors

---

## 214. Phase 6 deliverables

- speaker avatar
- emotion avatar mapping
- avatar layout

---

## 215. Phase 7 deliverables

- fade transition
- slide transition
- scene camera zoom

---

## 216. Phase 8 deliverables

- faster backend
- frame pipe to FFmpeg
- batch optimization

---

## 217. Renderer acceptance for Sprint 5

Sprint 5 renderer is acceptable when:

- reads `timeline.visual.json`
- writes `output/silent_video.mp4`
- renders at 1080x1920
- renders Vietnamese text correctly
- highlights keywords
- applies at least one animation
- validates unknown effects
- validates unknown layouts
- does not call AI
- has basic docs/tests

---

## 218. Renderer acceptance for V1

V1 renderer is acceptable when:

- template system works
- effect registry works
- layout registry works
- icons render
- speaker labels render
- safe zones work
- debug mode exists
- render report exists
- preview mode exists
- original audio export works through exporter
- pipeline can create final MP4 end-to-end

---

## 219. Renderer anti-patterns

Avoid:

### 219.1 One giant render function

Renderer should be modular.

### 219.2 Hardcoded colors everywhere

Use templates.

### 219.3 Hardcoded absolute font paths

Use font resolution.

### 219.4 LLM call inside renderer

Forbidden.

### 219.5 Silent failure on missing assets

Warn or fail.

### 219.6 Ignoring safe zones

Bad mobile output.

### 219.7 Rendering text too small

This project is about large text.

### 219.8 Overusing effects

Readable content matters more.

### 219.9 Optimizing before basic correctness

Do not prematurely rewrite backend.

### 219.10 Coupling renderer to CLI

Keep renderer importable.

---

## 220. Renderer review checklist

Before accepting renderer code, ask:

1. Does renderer consume only visual timeline JSON?
2. Does renderer avoid LLM calls?
3. Does renderer validate input?
4. Are unknown effects rejected?
5. Are unknown layouts rejected?
6. Are assets resolved safely?
7. Does text fit safe zones?
8. Does Vietnamese render correctly?
9. Are styles template-driven?
10. Is output deterministic?
11. Are warnings reported?
12. Is code modular?
13. Are tests included?
14. Is documentation updated?

---

## 221. Renderer future features

Future features may include:

- word-level text highlighting
- karaoke timing
- audio-reactive animation
- particle effects
- confetti
- camera movement
- original video background
- dynamic comic panels
- auto-layout optimization
- collision detection
- advanced subtitle styles
- Lottie support
- vector icons
- GPU acceleration
- WebGL renderer
- browser preview

Do not implement these before the basic renderer is stable.

---

## 222. Renderer compatibility

Renderer should work on:

- Windows
- Mac M1
- Linux

Renderer should not require:

- NVIDIA GPU
- CUDA
- internet
- cloud account

---

## 223. Renderer output quality principles

Good output should feel:

- bold
- readable
- punchy
- rhythmic
- high contrast
- mobile-friendly
- visually consistent
- not overloaded

---

## 224. Renderer final rule

The renderer should be boring internally and exciting externally.

The code should be predictable.

The video can be energetic.

Do not sacrifice architecture for flashy effects.

---

## 225. Initial effect parameter reference

### 225.1 `pop`

| Param | Type | Default | Meaning |
|---|---|---|---|
| `scale` | number | `1.25` | maximum scale |
| `easing` | string | `ease_out_back` | easing function |

### 225.2 `bounce`

| Param | Type | Default | Meaning |
|---|---|---|---|
| `amplitude` | number | `24` | vertical movement in pixels |
| `bounces` | integer | `2` | number of bounces |
| `decay` | number | `1.0` | bounce decay factor |

### 225.3 `shake`

| Param | Type | Default | Meaning |
|---|---|---|---|
| `amplitude` | number | `8` | shake movement in pixels |
| `frequency` | number | `18` | shake frequency |
| `axis` | string | `xy` | x, y, or xy |

### 225.4 `glow`

| Param | Type | Default | Meaning |
|---|---|---|---|
| `radius` | number | `12` | blur radius |
| `color` | string | `keyword color` | glow color |
| `intensity` | number | `0.8` | glow alpha |

### 225.5 `slide`

| Param | Type | Default | Meaning |
|---|---|---|---|
| `direction` | string | `left` | left/right/up/down |
| `distance` | number | `120` | movement distance |
| `easing` | string | `ease_out` | easing function |

### 225.6 `fade`

| Param | Type | Default | Meaning |
|---|---|---|---|
| `from` | number | `0` | start opacity |
| `to` | number | `1` | end opacity |

### 225.7 `pulse`

| Param | Type | Default | Meaning |
|---|---|---|---|
| `scale` | number | `1.08` | pulse scale |
| `frequency` | number | `2` | pulse frequency |


---

## 226. Initial layout parameter reference

### 226.1 `center_stack`

| Param | Type | Default | Meaning |
|---|---|---|---|
| `vertical_align` | string | `center` | top/center/bottom |
| `line_spacing` | number | `28` | space between lines |
| `max_width_ratio` | number | `0.85` | max text width relative to safe width |

### 226.2 `punchline_center`

| Param | Type | Default | Meaning |
|---|---|---|---|
| `keyword_scale` | number | `1.25` | size multiplier for punchline |
| `supporting_text_scale` | number | `0.85` | size multiplier for non-keyword text |

### 226.3 `speaker_label_top`

| Param | Type | Default | Meaning |
|---|---|---|---|
| `label_position` | string | `top_left` | speaker label position |
| `text_vertical_align` | string | `center` | text vertical alignment |

### 226.4 `comic_panel`

| Param | Type | Default | Meaning |
|---|---|---|---|
| `panel_padding` | number | `48` | inner padding |
| `border_width` | number | `6` | panel border width |

### 226.5 `split_speaker`

| Param | Type | Default | Meaning |
|---|---|---|---|
| `split_direction` | string | `vertical` | vertical/horizontal |
| `gap` | number | `24` | gap between zones |

### 226.6 `avatar_left_text_right`

| Param | Type | Default | Meaning |
|---|---|---|---|
| `avatar_width_ratio` | number | `0.28` | avatar area ratio |
| `gap` | number | `32` | gap between avatar and text |


---

## 227. Suggested Python files and responsibilities

| File | Responsibility |
|---|---|
| `engine.py` | Main RendererEngine class and high-level render flow. |
| `context.py` | RenderContext, render settings, and shared render state. |
| `canvas.py` | Canvas creation, RGBA utilities, compositing helpers. |
| `scene.py` | Scene render state creation and per-scene render orchestration. |
| `frame.py` | Frame timestamp utilities and frame-level helpers. |
| `template.py` | Template loading, merging, and style resolution. |
| `validation.py` | Renderer input validation. |
| `registry.py` | Effect and layout registries. |
| `text.py` | Text measurement, text layer rendering, Vietnamese text handling. |
| `keyword.py` | Keyword target resolution and keyword rendering. |
| `icon.py` | Icon loading, resizing, and drawing. |
| `avatar.py` | Avatar loading and drawing. |
| `background.py` | Background drawing. |
| `layout.py` | Layout base helpers. |
| `safe_zone.py` | Safe zone data and debug drawing. |
| `debug.py` | Debug overlays and debug frame export. |

---

## 228. Suggested class list

| Class | Purpose |
|---|---|
| `RendererEngine` | Main renderer service. |
| `RenderContext` | Shared render context. |
| `RenderRequest` | Input request to renderer. |
| `RenderResult` | Output result from renderer. |
| `RenderElement` | Drawable element. |
| `ElementState` | Element state after transforms. |
| `Transform` | Position/scale/opacity/rotation. |
| `Layout` | Base layout interface. |
| `LayoutResult` | Computed layout result. |
| `Effect` | Base effect interface. |
| `EffectRegistry` | Registered effects. |
| `LayoutRegistry` | Registered layouts. |
| `Template` | Loaded visual template. |
| `SafeZone` | Safe content rectangle. |
| `RendererValidationResult` | Validation output. |

---

## 229. Implementation sequence for Sprint 5

1. Create minimal VisualTimeline Pydantic model or loader.
2. Create renderer validation function.
3. Create simple template defaults.
4. Create canvas/background renderer.
5. Create text measurement and centered text drawing.
6. Create center_stack layout.
7. Create keyword line detection.
8. Create pop effect.
9. Create simple MoviePy output.
10. Create one smoke test.
11. Create debug frame export.
12. Update docs and DecisionLog.

---

## 230. Renderer final implementation note

The first renderer should be intentionally small.

It should prove that:

```text
timeline.visual.json → silent_video.mp4
```

works reliably.

After that, improve style, animation, templates, icons, avatars, and performance.

Do not build a complex animation framework before the basic end-to-end pipeline works.
