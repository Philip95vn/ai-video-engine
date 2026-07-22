# ProjectVision.md

# AI Video Engine - Project Vision

## 0. Purpose

This document defines the long-term vision for **AI Video Engine**.

It explains:

- why this project exists
- what problem it solves
- who it is for
- what kind of product it should become
- what it should not become
- what principles guide development
- what the first successful version looks like
- what future versions may support

This document should be read together with:

```text
AGENTS.md
PROJECT_RULES.md
README.md
ROADMAP.md
docs/Architecture.md
docs/Pipeline.md
docs/AIDesign.md
docs/RendererDesign.md
docs/DecisionLog.md
```

---

## 1. Product vision in one sentence

AI Video Engine is a local-first automation engine that converts voice, dialogue, transcript, or structured content into short-form videos using AI-generated timeline JSON and deterministic rendering.

---

## 2. Product vision in one paragraph

AI Video Engine helps creators, recruiters, educators, marketers, and automation builders generate high-quality short-form videos without manually editing every scene. The engine uses AI to understand content, identify important keywords, choose visual emphasis, suggest icons, and create structured timeline instructions. A deterministic renderer then converts those instructions into a video with large readable text, motion, icons, templates, and synchronized original audio or generated voice.

---

## 3. Why this project exists

Short-form video is powerful, but manual editing is slow.

A single short video often requires:

- transcribing audio
- cutting scenes
- creating subtitles
- choosing keywords
- designing text layout
- adding icons
- timing animations
- syncing with voice
- exporting vertical video
- repeating the same process many times

Most tools either:

- require too much manual editing,
- produce generic subtitles,
- use AI video generation that cannot control text precisely,
- are not easy to automate,
- do not preserve a consistent brand style,
- or are expensive at scale.

AI Video Engine exists to solve this with a programmable, local-first, JSON-driven pipeline.

---

## 4. Primary product idea

The primary idea is:

```text
Input voice/video/script
        ↓
AI understands content
        ↓
AI creates structured visual timeline
        ↓
Renderer creates video deterministically
```

The AI acts like a director.

The renderer acts like an editor.

The JSON timeline acts like the production plan.

---

## 5. First user workflow

The first workflow starts from an existing video with voice.

```text
input/video.mp4
      ↓
extract original audio
      ↓
speech-to-text
      ↓
transcript with timestamps
      ↓
timeline analyzer
      ↓
visual director AI
      ↓
icon selector
      ↓
renderer
      ↓
merge original voice
      ↓
final.mp4
```

The original voice is preserved.

The visual style is redesigned.

---

## 6. First target video style

The first target style is:

- vertical 9:16
- dark background
- large full-screen text
- one or two sentences per scene
- highlighted keywords
- punchy animation
- speaker labels
- simple icons
- humorous dialogue support
- original voice sync

This is not traditional subtitle overlay.

This is kinetic text video.

---

## 7. Primary user

The initial primary user is a creator/operator who wants to automate many short videos.

The user may be:

- a recruiter
- a content creator
- a social media operator
- a marketer
- a teacher
- an automation builder
- a small business owner
- a developer using Codex/VS Code

The user may not be a professional video editor.

The system should therefore be powerful but understandable.

---

## 8. Special relevance for recruitment

The project owner is a recruiter.

This creates future product opportunities:

### 8.1 Job description to video

```text
job description
      ↓
script
      ↓
AI Video Engine
      ↓
recruitment short video
```

### 8.2 Candidate CV to video

```text
candidate CV
      ↓
summary script
      ↓
AI Video Engine
      ↓
candidate introduction video
```

### 8.3 Employer branding videos

```text
company information
      ↓
story script
      ↓
AI Video Engine
      ↓
short employer branding video
```

Recruitment is not the first engineering sprint, but it is a strong future direction.

---

## 9. Product positioning

AI Video Engine is not positioned as a general-purpose video editor.

It is positioned as:

```text
an automation engine for structured short-form video generation
```

It is closer to:

- a rendering engine
- a content automation pipeline
- a template-based motion graphics system
- a programmable CapCut-like automation backend

than to:

- a manual timeline editor
- a cinematic AI video generator
- a Photoshop replacement
- a Premiere Pro clone

---

## 10. Core differentiation

AI Video Engine differentiates through:

1. JSON-first pipeline.
2. AI/renderer separation.
3. Local-first processing.
4. Deterministic rendering.
5. Full-screen kinetic text.
6. Template-driven visual styles.
7. Intermediate files for editing.
8. Modular architecture.
9. Batch-friendly design.
10. Future recruitment/content automation workflows.

---

## 11. What the project should feel like

For the user, the project should feel like:

```text
I put in a video.
The system understands the voice.
It creates a visual script.
I can inspect or edit the JSON.
It renders a stylized short video.
I can repeat this for many videos.
```

For developers, it should feel like:

```text
I can replace one module without breaking the whole engine.
```

For AI agents, it should feel like:

```text
I can read AGENTS.md and docs/ and understand exactly what to build next.
```

---

## 12. What success looks like

The first major success is:

```text
input/video.mp4 → output/final.mp4
```

with:

- original voice preserved
- transcript generated
- timeline JSON generated
- visual direction JSON generated
- large text rendered
- keywords highlighted
- video exported 9:16
- intermediate files inspectable
- no manual video editing required

---

## 13. What failure looks like

The project is failing if:

- it becomes one giant script
- renderer calls LLM
- prompts are hidden in Python code
- JSON schema is unclear
- output is not reproducible
- setup requires too many fragile cloud services
- code only works on one machine
- generated text is unreadable
- videos look inconsistent
- future ChatGPT/Codex sessions cannot understand the repository
- documentation becomes stale

---

## 14. Product values

### 14.1 Clarity

Data flow should be clear.

Intermediate files should be visible.

Errors should be understandable.

### 14.2 Control

The user should be able to inspect and edit timeline JSON.

Templates should control style.

### 14.3 Repeatability

The same input should produce predictable output.

### 14.4 Local-first

User media should stay local by default.

### 14.5 Extensibility

Modules should be replaceable.

Templates should be addable.

Effects should be addable.

### 14.6 Automation

The system should support many videos, not just one demo.

### 14.7 Practicality

Build useful vertical slices before advanced features.

---

## 15. Non-negotiable principles

1. AI does not render video.
2. Renderer does not call AI.
3. JSON is the contract.
4. Original voice is preserved by default for existing-video workflow.
5. Vietnamese is first-class content.
6. Default output is vertical 9:16.
7. Local-first is default.
8. GPU is optional.
9. Documentation is project memory.
10. GitHub repository is source of truth.

---

## 16. Product modes

Long-term, the engine may support multiple modes.

### 16.1 Existing video mode

Input:

```text
video with voice
```

Output:

```text
stylized short-form video
```

This is the first mode.

### 16.2 Audio-only mode

Input:

```text
audio file
```

Output:

```text
video generated from voice
```

### 16.3 Dialogue text mode

Input:

```text
dialogue script
```

Output:

```text
TTS + visual video
```

### 16.4 Article/news mode

Input:

```text
article or summary
```

Output:

```text
short recap video
```

### 16.5 Recruitment mode

Input:

```text
job description or CV
```

Output:

```text
recruitment/candidate video
```

### 16.6 Batch mode

Input:

```text
folder of videos/scripts
```

Output:

```text
folder of rendered videos
```

---

## 17. First mode details: existing video mode

This mode takes a video that already has voice.

The system:

1. Extracts audio.
2. Transcribes speech.
3. Creates timestamped transcript.
4. Normalizes transcript into scenes.
5. Uses AI to enrich scenes visually.
6. Selects icons from local library.
7. Renders a new visual video.
8. Merges original audio.

The original video visuals may be ignored initially.

Future versions may use original video as blurred background.

---

## 18. Why original voice matters

Original voice contains:

- emotion
- timing
- personality
- natural pauses
- comedic rhythm
- speaker energy

Replacing it with TTS may reduce authenticity.

Therefore original voice is preserved by default.

---

## 19. Why large text matters

Short-form video is watched on mobile.

Small subtitles are easy to ignore.

Large text:

- grabs attention
- increases readability
- supports punchlines
- creates visual rhythm
- works without complex footage
- allows automated production

The engine should treat text as the main visual element.

---

## 20. Why not normal subtitles

Normal subtitles are:

- usually small
- often bottom-aligned
- visually passive
- not expressive enough
- not ideal for comedic timing
- not enough for the user's desired style

AI Video Engine should create kinetic full-screen text.

---

## 21. Why JSON matters

JSON makes the workflow:

- inspectable
- editable
- testable
- resumable
- AI-agent-friendly
- UI-ready
- renderer-friendly

A user can fix one scene without rerunning everything.

A future UI can edit the same JSON.

A future API can use the same JSON.

---

## 22. Why templates matter

Templates let one engine create many styles.

Examples:

```text
tiktok_dark_comic
minimal_black
neon_dialogue
recruitment_clean
education_bold
news_bold
```

Without templates, style becomes hardcoded.

With templates, the engine can scale across content types.

---

## 23. Why modularity matters

Different stages evolve at different speeds.

Speech-to-text may improve.

LLM model may change.

Renderer backend may change.

Icon library may grow.

Templates may multiply.

A modular design allows replacement without rewriting everything.

---

## 24. Why local-first matters

Local-first protects:

- privacy
- cost
- speed for batch tasks
- independence from API outages
- workflow portability
- private voice/video content

Cloud services can improve quality later, but must remain optional.

---

## 25. Why deterministic rendering matters

Video rendering should be predictable.

AI decisions can vary.

Renderer execution should not.

This makes it possible to:

- debug scenes
- compare versions
- rerender after manual edits
- run tests
- batch generate videos reliably

---

## 26. First technical milestone

The first technical milestone is Sprint 1:

```text
input/video.mp4 → output/transcript.json
```

This proves:

- FFmpeg works
- Faster Whisper works
- Vietnamese transcription works
- JSON output works
- local environment works

Everything else builds on this.

---

## 27. First product milestone

The first product milestone is:

```text
input/video.mp4 → output/final.mp4
```

with simple visual style.

It does not need perfect animation.

It needs to prove the full pipeline.

---

## 28. First quality milestone

The first quality milestone is:

```text
A 30-60 second Vietnamese dialogue video becomes a readable 9:16 animated text video with original voice.
```

Quality criteria:

- readable text
- decent timing
- meaningful keywords
- original audio sync
- no obvious broken scenes
- final MP4 export works

---

## 29. First scalability milestone

The first scalability milestone is:

```text
A folder of videos can be processed into final videos with minimal manual work.
```

This requires:

- batch mode
- caching
- reports
- error handling
- stable templates

---

## 30. First productization milestone

The first productization milestone is:

```text
A non-developer can run the workflow through a simple UI.
```

This is later.

Do not build UI before core engine works.

---

## 31. Ideal future user journey

A future user opens the app or CLI.

They choose:

```text
input video
template
language
style
```

They click build.

The system outputs:

```text
final video
transcript JSON
visual timeline JSON
render report
```

If something is wrong, user edits the timeline and rerenders.

---

## 32. Future UI vision

A future UI may include:

- video upload
- transcript view
- scene list
- keyword editor
- icon selector
- template selector
- preview window
- render button
- batch queue
- export settings

The UI should not replace the engine.

It should sit on top of the engine.

---

## 33. Future API vision

A future API may expose:

```text
POST /build
POST /transcribe
POST /timeline
POST /direct
POST /render
POST /export
GET /jobs/{id}
```

The API should call the same core modules.

---

## 34. Future recruitment product vision

Recruitment workflows could become a strong product track.

Examples:

### 34.1 Job ad video

Input:

```text
Job title
Salary
Location
Benefits
Requirements
Company tone
```

Output:

```text
Short recruitment video
```

### 34.2 Candidate intro video

Input:

```text
CV
Candidate highlights
Target role
```

Output:

```text
Candidate intro video
```

### 34.3 Employer branding video

Input:

```text
Company values
Culture notes
Hiring message
```

Output:

```text
Employer branding short video
```

This uses the same engine.

Only upstream script generation and templates differ.

---

## 35. Future content factory vision

AI Video Engine could become part of a content factory.

Example:

```text
content source
      ↓
summarizer
      ↓
script generator
      ↓
AI Video Engine
      ↓
video output
      ↓
scheduler/uploader
```

Sources might include:

- news
- blog posts
- job descriptions
- product descriptions
- interviews
- podcasts
- training documents
- customer testimonials

---

## 36. Future automation vision

The engine should eventually support:

- batch generation
- scheduled jobs
- template presets
- reusable asset packs
- automatic reports
- automatic naming
- cache reuse
- optional upload integrations

This requires stable core architecture.

---

## 37. Future template marketplace vision

If templates become powerful, users could create or share:

- TikTok templates
- recruitment templates
- education templates
- sales templates
- news templates
- podcast templates
- quote templates

This is not an early priority.

But architecture should not block it.

---

## 38. Future plugin vision

Plugins may eventually support:

- new effects
- new layouts
- new render backends
- new STT providers
- new LLM providers
- new asset search providers
- new exporters

Do not overbuild plugin system early.

But keep modules separable.

---

## 39. Future render backend vision

Initial renderer may use Pillow + MoviePy.

Future backend may use:

- FFmpeg frame pipe
- OpenCV
- GPU acceleration
- browser/WebGL
- native rendering

Backend replacement should not change timeline JSON.

---

## 40. Future AI provider vision

Initial AI providers:

```text
Faster Whisper
Ollama + Qwen
sentence-transformers
```

Future optional providers:

```text
WhisperX
pyannote
OpenAI
Claude
Gemini
Azure Speech
ElevenLabs
```

Provider changes should not break core JSON contracts.

---

## 41. Long-term architecture vision

Long-term architecture:

```text
Core Engine
    ↓
CLI
    ↓
Desktop UI
    ↓
API
    ↓
Batch Platform
```

Core engine remains independent.

---

## 42. Long-term repository vision

The repository should contain:

- code
- docs
- tests
- prompts
- schemas
- templates
- examples
- small sample assets
- release notes

It should be understandable without reading old chats.

---

## 43. Long-term data vision

The engine's data should remain inspectable.

Important data files:

```text
transcript.json
timeline.normalized.json
timeline.director.json
timeline.visual.json
render_report.json
```

These files are a product feature, not just debug output.

---

## 44. Long-term editing vision

A user should be able to edit:

- transcript text
- speaker labels
- display lines
- keywords
- effects
- icons
- layout
- timing
- template

and rerender.

This is why JSON must remain human-readable.

---

## 45. Long-term quality vision

Output should become:

- visually consistent
- fast to generate
- easy to customize
- readable on mobile
- synchronized with voice
- brandable
- reusable across content types

---

## 46. Product constraints

The project must respect:

- local-first default
- Windows support
- Mac M1 support
- optional GPU
- Vietnamese support
- manageable setup
- beginner-friendly workflow
- modular architecture
- GitHub-based memory
- AI/renderer separation

---

## 47. Technical constraints

Initial development should avoid:

- mandatory CUDA
- mandatory cloud APIs
- huge model downloads
- complex UI
- large binary commits
- fragile dependencies
- hidden prompts
- unvalidated JSON
- renderer-LLM coupling

---

## 48. Design constraints

Output should avoid:

- tiny subtitles
- too much text per frame
- low contrast
- unreadable fonts
- irrelevant icons
- over-animation
- inconsistent styles
- broken safe zones
- audio desync

---

## 49. Business constraints

If the project becomes productized later, it should be:

- cost-efficient
- batch-friendly
- reusable
- brandable
- not dependent on expensive per-video APIs
- adaptable to recruitment and content workflows

---

## 50. Development constraints

The project owner is learning Git and development workflow.

Therefore:

- instructions should be step-by-step
- docs should be clear
- each sprint should have one focus
- errors should be handled patiently
- setup should avoid unnecessary complexity

---

## 51. Vision for AI agents

AI agents should be productive because the repository contains:

- AGENTS.md
- PROJECT_RULES.md
- ROADMAP.md
- docs
- prompts
- schemas
- tests

Future agent instruction:

```text
Read AGENTS.md and docs before coding.
Current sprint: Sprint 1 - Speech To Text.
```

The agent should not need old chat history.

---

## 52. Vision for code quality

The codebase should be:

- small modules
- clear names
- typed public APIs
- validated JSON
- good errors
- no hidden state
- no giant scripts
- no cross-boundary imports
- testable

---

## 53. Vision for documentation quality

Documentation should be:

- substantial
- practical
- current
- specific
- useful for humans
- useful for AI agents
- connected to code
- connected to decisions

Docs should not be empty placeholders.

---

## 54. Vision for testing

Testing should focus on:

- JSON schemas
- pipeline stages
- command builders
- prompt parsers
- renderer validation
- asset validation
- smoke rendering

Do not require huge models in unit tests.

---

## 55. Vision for templates

Templates should let users switch style without changing code.

Example:

```text
same timeline JSON
      ↓
template A: funny TikTok
template B: recruitment clean
template C: education bold
```

The content remains.

The style changes.

---

## 56. Vision for assets

Assets should be metadata-driven.

A large icon library should still be searchable.

AI should say:

```text
báo thức
```

The system should find:

```text
icon_alarm_001
```

This supports large scalable asset collections.

---

## 57. Vision for prompts

Prompts should be versioned and tested.

Prompt changes should be treated like product changes.

The Visual Director prompt is a core product asset.

---

## 58. Vision for renderer

The renderer should be internally boring.

The output can be exciting.

Renderer code should be:

- predictable
- deterministic
- modular
- testable
- template-driven
- AI-free

---

## 59. Vision for user control

The user should be able to choose:

- template
- model
- language
- speaker mapping
- icon pack
- output resolution
- preview/full render
- manual or automatic mode

But defaults should work.

---

## 60. Vision for beginner experience

A beginner should eventually be able to run:

```bash
ai-video build input/video.mp4
```

and get:

```text
output/final.mp4
```

If something fails, the system should explain what to fix.

---

## 61. Vision for advanced users

Advanced users should be able to:

- edit JSON directly
- create templates
- add icons
- change prompts
- swap models
- batch process videos
- integrate with scripts
- build APIs on top

---

## 62. Vision for open-source quality

Even if the project remains private, it should be structured like a serious open-source project:

- clear README
- rules
- roadmap
- decision log
- docs
- tests
- issues
- conventional commits
- reproducible setup

---

## 63. Vision for first demo

The first demo should show:

1. A short Vietnamese video with voice.
2. Transcript generated automatically.
3. Timeline JSON created.
4. Visual text video rendered.
5. Original voice preserved.
6. Final MP4 exported.

It can be visually simple.

It must prove the architecture.

---

## 64. Vision for first impressive demo

The first impressive demo should include:

- two speakers
- speaker labels
- highlighted punchlines
- icons
- pop/shake animation
- dark comic template
- original voice sync
- final TikTok-ready MP4

---

## 65. Vision for first useful product

The first useful product allows the user to process real videos repeatedly.

It should support:

- input folder
- output folder
- transcript review
- template selection
- render
- report

---

## 66. Vision for first recruitment product

The first recruitment product allows:

```text
job description → short video script → recruitment video
```

It should include:

- job title
- salary/benefits
- location
- role highlights
- CTA
- clean template
- icons

---

## 67. Vision for maintainability

Future developers should be able to answer:

- where does STT happen?
- where does AI direction happen?
- where does renderer start?
- what JSON does renderer need?
- where are prompts?
- where are templates?
- what decisions were made?
- what sprint is next?

by reading repository files.

---

## 68. Vision for failure recovery

If a stage fails, earlier outputs should remain.

Example:

If renderer fails, user still has:

```text
transcript.json
timeline.normalized.json
timeline.visual.json
```

They can fix and rerun render only.

---

## 69. Vision for debugging

Debugging should be file-based.

Possible debug outputs:

```text
visual_director_prompt.txt
visual_director_raw_response.txt
icon_matches.json
safe_zone_preview.png
scene_preview.png
validation_report.json
```

---

## 70. Vision for reports

Reports should answer:

- what input was used?
- what models were used?
- what template was used?
- how many scenes?
- how long did rendering take?
- were there warnings?
- where is final output?

---

## 71. Vision for schema stability

Before v1.0, schema can evolve.

After v1.0, schema should stabilize.

Breaking changes should be documented.

Migration may be needed later.

---

## 72. Vision for platform support

Required:

- Windows
- Mac M1

Desired:

- Linux

Not required initially:

- GPU
- cloud machine
- mobile app

---

## 73. Vision for performance

Initial performance goal:

```text
works reliably
```

Later performance goal:

```text
renders short videos quickly enough for batch use
```

Optimization should come after correctness.

---

## 74. Vision for install process

Install should become:

```bash
git clone <repo>
cd ai-video-engine
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Plus external tools:

```text
FFmpeg
Ollama
```

The docs should make setup clear.

---

## 75. Vision for content styles

Future styles:

```text
funny dialogue
motivational
news recap
education
recruitment
sales
review
podcast clip
storytelling
```

The engine should support these through templates and prompts.

---

## 76. Vision for monetization possibilities

If productized, possible directions:

- internal automation tool
- SaaS with local agent
- template marketplace
- recruitment video generator
- agency tool
- batch content production system
- desktop app
- API service

This is future thinking.

Engineering should focus on core engine first.

---

## 77. Vision for user trust

The system should be honest and inspectable.

AI decisions should not be mysterious.

Users should be able to see:

- transcript
- keywords
- icon choices
- timeline
- warnings
- reports

This builds trust.

---

## 78. Vision for AI trust

AI output should always be validated.

AI can help, but deterministic code protects the pipeline.

The system should never blindly trust an LLM.

---

## 79. Vision for manual correction

Manual correction is not a failure.

It is a feature.

The system should allow users to fix:

- STT errors
- speaker labels
- wrong keyword
- wrong icon
- wrong effect
- bad layout

and rerender quickly.

---

## 80. Vision for speed of iteration

The project should support fast iteration:

```text
edit timeline JSON
      ↓
rerender
```

without rerunning STT or LLM every time.

---

## 81. Vision for cache

Cache should save expensive stages:

- STT
- LLM output
- embeddings
- rendered previews

Cache use should be explicit and logged.

---

## 82. Vision for batch scale

Batch scale requires:

- model reuse
- cache
- reports
- error isolation
- output organization
- template consistency

This should come after V1 pipeline.

---

## 83. Vision for content quality

Good output should have:

- clear text
- strong hierarchy
- relevant keywords
- meaningful motion
- relevant icon
- no clutter
- good timing
- consistent style
- preserved voice

---

## 84. Vision for product quality

Good product should have:

- easy setup
- clear docs
- reliable commands
- helpful errors
- reproducible output
- practical examples
- stable defaults

---

## 85. Vision for engineering quality

Good engineering should have:

- module boundaries
- schema validation
- tests
- decision log
- conventional commits
- small changes
- no hidden dependencies
- no hardcoded local paths

---

## 86. Vision for AI quality

Good AI layer should have:

- valid JSON
- preserved IDs
- preserved timing
- meaningful keywords
- useful icon queries
- correct language preservation
- no hallucinated effects
- no hallucinated assets
- low-temperature stability

---

## 87. Vision for renderer quality

Good renderer should have:

- large readable text
- accurate safe zones
- good font handling
- high contrast
- deterministic animation
- clear failures
- template-driven style
- no AI calls

---

## 88. Vision for asset quality

Good assets should be:

- licensed
- tagged
- consistent
- readable
- metadata-driven
- validated
- not too large
- useful for content

---

## 89. Vision for future collaboration

If another developer joins, they should:

1. clone repo
2. read README
3. read AGENTS.md
4. read ROADMAP
5. pick issue
6. code within rules
7. commit clearly

---

## 90. Vision for future chat continuation

A new ChatGPT session should start with:

```text
Continue AI Video Engine.
Read AGENTS.md, PROJECT_RULES.md, ROADMAP.md, and docs before coding.
Current sprint: Sprint 1 - Speech To Text.
```

That should be enough.

---

## 91. Vision for Codex continuation

Codex should be able to read repository files and continue.

It should not need this original conversation.

This is why Sprint 0B exists.

---

## 92. Vision for first GitHub issues

Initial issues:

```text
Sprint 1 - Speech To Text
Sprint 2 - Timeline Analyzer
Sprint 3 - Visual Director
Sprint 4 - Icon Selector
Sprint 5 - Basic Renderer
Sprint 6 - Exporter
```

Each issue should have:

- goal
- scope
- non-scope
- deliverables
- acceptance criteria

---

## 93. Vision for releases

Releases should mark working milestones.

Example:

```text
v0.2.0 - Speech to Text
v0.3.0 - Timeline Analyzer
v0.4.0 - Visual Director
v0.5.0 - Icon Selector
v0.6.0 - Renderer
v0.7.0 - Exporter
v1.0.0 - First complete engine
```

---

## 94. Vision for examples

Examples should eventually include:

```text
examples/funny_dialogue/
examples/recruitment_clean/
examples/education_bold/
```

Each example should include:

- input sample or instructions
- transcript
- timeline
- final output notes
- template

Large media may be external.

---

## 95. Vision for troubleshooting

Troubleshooting docs should cover:

- FFmpeg not found
- Python version issue
- Faster Whisper install issue
- Ollama not running
- Qwen model missing
- invalid JSON
- font missing Vietnamese glyphs
- renderer failure
- audio/video sync mismatch

---

## 96. Vision for sustainable development

The project should avoid burnout and chaos.

Development should be:

```text
one sprint
one goal
one deliverable
one commit sequence
```

Do not try to finish everything in one session.

---

## 97. Vision for near-term success

Near-term success means:

```text
Sprint 1 works on user's Windows machine.
```

This is the next concrete step after docs.

---

## 98. Vision for mid-term success

Mid-term success means:

```text
A full video can be generated end-to-end with simple visual style.
```

This is Sprint 6/V1-alpha.

---

## 99. Vision for long-term success

Long-term success means:

```text
The engine can generate many types of short videos through templates and automation.
```

This includes recruitment and batch workflows.

---

## 100. Final product vision

AI Video Engine should become a reliable, local-first, modular automation engine that turns spoken or written content into short-form videos through structured AI decisions and deterministic rendering.

The project should be simple to use, powerful to extend, and clear enough that future AI agents can help build it without breaking its architecture.

---

# Appendix A - Product principles checklist

1. AI generates JSON, not video.
2. Renderer consumes JSON, not prompts.
3. Original audio is preserved by default.
4. Vietnamese content is first-class.
5. Default output is 9:16.
6. Local-first is default.
7. GPU is optional.
8. Templates define visual style.
9. Assets are metadata-driven.
10. Prompts are external and versioned.
11. Intermediate files are inspectable.
12. Manual correction is supported.
13. Documentation is source of truth.
14. GitHub stores long-term memory.
15. Each sprint delivers one vertical slice.

---

# Appendix B - User stories

| User | Story |
|---|---|
| Creator | I want to turn a voiced video into a bold text video so I can publish it quickly. |
| Recruiter | I want to turn a job description into a short recruitment video so I can attract candidates. |
| Recruiter | I want to turn a CV into a candidate intro video so I can present candidates better. |
| Educator | I want to turn lesson content into short videos so learners can absorb key points. |
| Marketer | I want to batch generate product videos so I can test multiple messages. |
| Developer | I want JSON contracts so I can automate and debug the pipeline. |
| Video editor | I want editable timeline JSON so I can correct AI decisions before rendering. |
| AI agent | I want clear docs so I can safely modify the project. |

---

# Appendix C - Product capability map


## C.1 Input

- video input
- audio input
- dialogue text input later
- document input later

## C.2 Understanding

- speech-to-text
- speaker mapping
- keyword detection
- emotion classification

## C.3 Direction

- layout suggestion
- animation suggestion
- icon query
- template selection later

## C.4 Assets

- icon search
- avatar mapping later
- background selection
- font selection

## C.5 Rendering

- large text
- keyword highlight
- animation
- safe zones
- silent video

## C.6 Export

- original audio merge
- final MP4
- render report

## C.7 Automation

- batch mode
- cache
- reports
- future API

---

# Appendix D - Future product tracks

| Track | Name | Priority |
|---|---|---|
| Track A | Existing video redesign | First priority |
| Track B | Audio-only video generation | After core pipeline |
| Track C | Dialogue text + TTS | After exporter stable |
| Track D | Recruitment videos | Strong future direction |
| Track E | Education videos | Template-driven future |
| Track F | News recap videos | Requires summarization input |
| Track G | Batch content factory | Requires stable V1 |

---

# Appendix E - Vision acceptance checklist

1. Repository contains enough context to continue in a new chat.
2. Codex can understand the project by reading AGENTS.md and docs.
3. Sprint 1 has a clear goal.
4. Architecture prevents renderer from calling AI.
5. JSON contracts are documented.
6. Default user workflow is clear.
7. Future recruitment direction is documented.
8. Local-first policy is documented.
9. Vietnamese support is documented.
10. Roadmap is clear.

---

# Appendix F - Final vision note

The project should not chase every possible AI video feature.

It should first become excellent at one thing:

```text
turning voice/dialogue into structured, readable, stylish short-form videos
```

Once that foundation is strong, the engine can expand into many workflows.
