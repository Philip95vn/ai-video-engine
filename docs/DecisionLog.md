# DecisionLog.md

# AI Video Engine - Decision Log

## 0. Purpose

This document records important technical, product, and architecture decisions for **AI Video Engine**.

It exists so that future contributors, AI coding agents, and the project owner can understand not only **what** was chosen, but **why** it was chosen.

This file is a long-term memory for the project.

Chat history is not the source of truth.

The repository is the source of truth.

Important decisions must be written here.

---

## 1. Decision record format

Use this format for every major decision.

```text
## ADR-000X - Title

Date:
Status:

Context:
Decision:
Reasons:
Alternatives considered:
Consequences:
Follow-up:
Related files:
```

---

## 2. Status values

Allowed status values:

```text
Proposed
Accepted
Superseded
Deprecated
Rejected
```

---

## 3. When to add a decision

Add an entry when deciding:

- architecture direction
- model choice
- dependency choice
- JSON schema change
- pipeline change
- renderer design change
- prompt behavior change
- asset structure change
- repository structure change
- Git workflow change
- cloud/local policy
- testing policy
- breaking change
- sprint scope

---

## 4. Current accepted decisions summary

| ID | Title | Status |
|---|---|---|
| ADR-0001 | Treat project as an engine, not a script | Accepted |
| ADR-0002 | Use repository documentation as source of truth | Accepted |
| ADR-0003 | Separate AI from renderer | Accepted |
| ADR-0004 | Use Timeline JSON as central contract | Accepted |
| ADR-0005 | Preserve original voice for existing-video workflow | Accepted |
| ADR-0006 | Default output is vertical 9:16 video | Accepted |
| ADR-0007 | Use local-first architecture | Accepted |
| ADR-0008 | Use GitHub + VS Code workflow | Accepted |
| ADR-0009 | Use AGENTS.md for AI agent context | Accepted |
| ADR-0010 | Use Python 3.11 as preferred baseline | Accepted |
| ADR-0011 | Use FFmpeg for media operations | Accepted |
| ADR-0012 | Use Faster Whisper for Sprint 1 STT | Accepted |
| ADR-0013 | Use Ollama for first local LLM runtime | Accepted |
| ADR-0014 | Use Qwen 2.5 3B as first Visual Director model | Accepted |
| ADR-0015 | Use embeddings for icon selection | Accepted |
| ADR-0016 | LLM returns icon_query, not icon filename | Accepted |
| ADR-0017 | Renderer must be deterministic | Accepted |
| ADR-0018 | Prompts live in prompt files | Accepted |
| ADR-0019 | Use docs-first Sprint 0B before coding more | Accepted |
| ADR-0020 | Use modular src folder structure | Accepted |
| ADR-0021 | Use intermediate JSON files for inspection | Accepted |
| ADR-0022 | Use original audio merge after silent render | Accepted |
| ADR-0023 | Do not require GPU | Accepted |
| ADR-0024 | Use conventional commits | Accepted |
| ADR-0025 | Keep cloud providers optional | Accepted |

---

## ADR-0001 - Treat project as an engine, not a script

Date: 2026-07-07  
Status: Accepted

### Context

The original idea started as a tool to generate TikTok/Reels style videos with large animated text, voice, icons, and effects.

During discussion, the scope became broader:

- speech-to-text
- timeline generation
- visual direction
- icon selection
- rendering
- audio merge
- template system
- future batch processing
- future recruitment videos
- future generated scripts

A single Python script would become unmaintainable.

### Decision

Treat the project as a reusable **AI Video Engine**, not a one-off script.

### Reasons

- The project will grow over multiple months.
- Modules need clear boundaries.
- Future Codex/ChatGPT sessions need repository context.
- The engine may support multiple content types later.
- A script-based design would become hard to test and extend.

### Alternatives considered

1. One Python file.
2. A small folder of scripts.
3. A proper modular engine.

Option 3 was chosen.

### Consequences

The repository needs:

- documentation
- architecture rules
- module structure
- schema definitions
- Git workflow
- tests
- roadmap

### Follow-up

Maintain engine structure from the beginning.

### Related files

```text
AGENTS.md
PROJECT_RULES.md
docs/Architecture.md
docs/Pipeline.md
```

---

## ADR-0002 - Use repository documentation as source of truth

Date: 2026-07-07  
Status: Accepted

### Context

The conversation became long and browser performance started to degrade.

The user may move to:

- a new ChatGPT conversation
- Codex inside VS Code
- future AI coding tools
- GitHub-based workflow

Chat history is fragile and cannot be relied on.

### Decision

The repository documentation is the source of truth.

Important project knowledge must be written into files.

### Reasons

- Future AI agents can read repository files.
- Codex can understand project rules without chat history.
- Architecture decisions remain visible.
- The project becomes portable.
- New contributors can onboard.

### Alternatives considered

1. Keep relying on ChatGPT memory.
2. Put all context in README only.
3. Create a full documentation knowledge base.

Option 3 was chosen.

### Consequences

The project must maintain:

```text
AGENTS.md
PROJECT_RULES.md
README.md
docs/
```

Documentation updates are part of development.

### Follow-up

Complete Sprint 0B documentation before heavy coding.

### Related files

```text
AGENTS.md
PROJECT_RULES.md
README.md
docs/
```

---

## ADR-0003 - Separate AI from renderer

Date: 2026-07-07  
Status: Accepted

### Context

The project needs AI for:

- speech-to-text
- keyword detection
- emotion classification
- layout suggestion
- icon query generation
- animation suggestion

But using AI directly to render video would be slow, costly, inconsistent, and hard to control.

### Decision

AI must generate structured instructions only.

The renderer must render deterministically.

### Reasons

- AI-generated video models do not reliably render exact text.
- Motion text video is better handled by deterministic rendering.
- Output must be repeatable.
- Renderer should run without AI.
- Debugging is easier with JSON contracts.
- Batch production becomes more reliable.

### Alternatives considered

1. Use video diffusion models.
2. Use AI image generation per frame.
3. Use LLM to create JSON and Python renderer to render.

Option 3 was chosen.

### Consequences

Renderer must never call LLM.

AI modules must output JSON.

Schema validation becomes critical.

### Follow-up

Enforce this in:

```text
AGENTS.md
PROJECT_RULES.md
docs/RendererDesign.md
docs/AIDesign.md
```

### Related files

```text
docs/AIDesign.md
docs/RendererDesign.md
docs/JSONSchema.md
```

---

## ADR-0004 - Use Timeline JSON as central contract

Date: 2026-07-07  
Status: Accepted

### Context

The pipeline requires multiple stages:

```text
speech-to-text
timeline analyzer
visual director
icon selector
renderer
exporter
```

Each stage needs to communicate reliably.

Natural language is not reliable enough for renderer input.

### Decision

Use structured Timeline JSON as the central contract between modules.

### Reasons

- Human-readable.
- AI-agent-readable.
- Easy to validate.
- Easy to manually edit.
- Easy to store intermediate outputs.
- Easy to debug.
- Works well with renderer.
- Works well with future UI.

### Alternatives considered

1. Pass raw transcript strings.
2. Pass Python objects only in memory.
3. Use JSON files between stages.

Option 3 was chosen.

### Consequences

The project must maintain schema docs and validation.

Intermediate files should be written to output folder.

### Follow-up

Define schemas in `docs/JSONSchema.md`.

### Related files

```text
docs/JSONSchema.md
docs/Pipeline.md
```

---

## ADR-0005 - Preserve original voice for existing-video workflow

Date: 2026-07-07  
Status: Accepted

### Context

The initial user workflow starts from a video that already has voice.

The desired result is to redesign the visuals while keeping the original voice.

### Decision

For existing-video workflow, preserve original audio by default.

### Reasons

- Original voice contains emotion and timing.
- Avoids TTS quality issues.
- Avoids re-synchronization problems from generated audio.
- User asked specifically to use voice gốc.
- This matches common short-form editing workflows.

### Alternatives considered

1. Replace voice with TTS.
2. Use original audio.
3. Use hybrid original voice + TTS.

Option 2 was chosen for current workflow.

### Consequences

Pipeline must:

1. Extract audio.
2. Use audio for STT.
3. Render silent video.
4. Merge original audio back.

### Follow-up

Exporter must merge `silent_video.mp4` with original audio.

### Related files

```text
docs/Pipeline.md
docs/RendererDesign.md
```

---

## ADR-0006 - Default output is vertical 9:16 video

Date: 2026-07-07  
Status: Accepted

### Context

The target platforms are TikTok, Reels, and YouTube Shorts.

The user explicitly requested 9:16 ratio.

### Decision

Default output format is:

```text
1080x1920
30 FPS
MP4
H.264
AAC
```

### Reasons

- Matches TikTok/Reels/Shorts.
- Good mobile readability.
- Works well for full-screen large text.
- Standard export format.

### Alternatives considered

1. 16:9 landscape.
2. 1:1 square.
3. 9:16 vertical.

Option 3 was chosen.

### Consequences

Renderer defaults to 1080x1920.

Safe zones should consider mobile UI.

Templates can override later.

### Follow-up

Add template-controlled video spec.

### Related files

```text
docs/RendererDesign.md
docs/JSONSchema.md
```

---

## ADR-0007 - Use local-first architecture

Date: 2026-07-07  
Status: Accepted

### Context

The user wants to test on Windows and may use Mac M1.

The project should not require cloud services to function.

Input media may contain private voice or content.

### Decision

Default architecture is local-first.

### Reasons

- Privacy.
- Lower cost.
- Works offline after setup.
- Better for batch generation.
- Avoids API key dependency.
- Works on Mac M1 and Windows.
- More predictable for production.

### Alternatives considered

1. Cloud-first APIs.
2. Hybrid local/cloud by default.
3. Local-first with optional cloud providers.

Option 3 was chosen.

### Consequences

Local tools:

- FFmpeg
- Faster Whisper
- Ollama
- local embedding model

Cloud providers can be optional later.

### Follow-up

Document cloud providers as optional only.

### Related files

```text
docs/AIDesign.md
PROJECT_RULES.md
```

---

## ADR-0008 - Use GitHub + VS Code workflow

Date: 2026-07-07  
Status: Accepted

### Context

The user is new to Git but wants a reliable long-term workflow.

The project may be continued in Codex inside VS Code.

### Decision

Use GitHub as remote repository and VS Code as main development environment.

### Reasons

- GitHub is long-term memory.
- VS Code integrates with Codex/Copilot.
- Git history tracks decisions and code.
- Easy to move between machines.
- Easy to recover context in new chat.

### Alternatives considered

1. Local files only.
2. Zip files only.
3. GitHub repository.

Option 3 was chosen.

### Consequences

The user created and pushed the initial repository.

Development should use commits and push regularly.

### Follow-up

Continue using conventional commits.

### Related files

```text
README.md
AGENTS.md
```

---

## ADR-0009 - Use AGENTS.md for AI agent context

Date: 2026-07-07  
Status: Accepted

### Context

Codex, ChatGPT, and other AI coding agents need project rules.

Many coding tools automatically read or can be told to read `AGENTS.md`.

### Decision

Create and maintain `AGENTS.md` as the primary AI-agent instruction file.

### Reasons

- AI agents need concise but complete context.
- Avoids repeated explanations.
- Protects architecture boundaries.
- Helps future chat sessions continue work.
- Works well with Codex in VS Code.

### Alternatives considered

1. Only README.
2. Only PROJECT_RULES.
3. Dedicated AGENTS.md plus docs.

Option 3 was chosen.

### Consequences

Every future AI agent should read `AGENTS.md` before coding.

### Follow-up

Keep AGENTS.md updated when architecture changes.

### Related files

```text
AGENTS.md
PROJECT_RULES.md
```

---

## ADR-0010 - Use Python 3.11 as preferred baseline

Date: 2026-07-07  
Status: Accepted

### Context

The user initially had Python 3.14 path visible.

Many AI packages may not fully support very new Python versions.

### Decision

Use Python 3.11 as preferred baseline.

### Reasons

- Stable AI package support.
- Better compatibility with Faster Whisper, PyTorch ecosystem, MoviePy, sentence-transformers.
- Works on Windows and Mac.
- Reduces setup errors.

### Alternatives considered

1. Python 3.14.
2. Python 3.12.
3. Python 3.11.

Option 3 was chosen.

### Consequences

Docs and environment setup should recommend Python 3.11+ with 3.11 preferred.

### Follow-up

Keep `pyproject.toml` requiring Python >= 3.11.

### Related files

```text
docs/CodingStandard.md
README.md
```

---

## ADR-0011 - Use FFmpeg for media operations

Date: 2026-07-07  
Status: Accepted

### Context

The project needs to extract audio, convert formats, merge audio/video, and export final MP4.

### Decision

Use FFmpeg as the core media tool.

### Reasons

- Industry standard.
- Fast.
- Cross-platform.
- Handles many formats.
- Works from Python through subprocess.
- Required for audio extraction and final merge.

### Alternatives considered

1. MoviePy only.
2. pydub only.
3. FFmpeg.

Option 3 was chosen.

### Consequences

FFmpeg must be installed and available in PATH.

Python should call FFmpeg with subprocess argument lists.

### Follow-up

Add clear missing-FFmpeg errors.

### Related files

```text
docs/Pipeline.md
docs/CodingStandard.md
```

---

## ADR-0012 - Use Faster Whisper for Sprint 1 STT

Date: 2026-07-07  
Status: Accepted

### Context

Sprint 1 goal is:

```text
video/audio → transcript.json
```

The project needs local Vietnamese speech-to-text.

### Decision

Use Faster Whisper for first STT implementation.

### Reasons

- Good transcription quality.
- Local.
- Faster than standard Whisper implementation.
- Supports Vietnamese.
- CPU-friendly.
- Good enough before adding WhisperX complexity.

### Alternatives considered

1. OpenAI Whisper package.
2. Faster Whisper.
3. WhisperX.
4. Cloud STT.

Option 2 was chosen.

### Consequences

Install `faster-whisper`.

Use configurable model name.

Default should support CPU.

### Follow-up

Add WhisperX later for word-level timing and diarization.

### Related files

```text
docs/AIDesign.md
docs/Pipeline.md
```

---

## ADR-0013 - Use Ollama for first local LLM runtime

Date: 2026-07-07  
Status: Accepted

### Context

The Visual Director needs a local LLM for JSON generation.

The user wants lightweight local models.

### Decision

Use Ollama as the first local LLM runtime.

### Reasons

- Easy installation.
- Good local model management.
- Simple HTTP API.
- Works on Windows and Mac.
- Supports small models like Qwen 2.5 3B.
- Suitable for Codex/VS Code development.

### Alternatives considered

1. Direct Transformers.
2. llama.cpp.
3. LM Studio.
4. Ollama.
5. Cloud LLM only.

Option 4 was chosen.

### Consequences

Visual Director should use an abstract LLM client so Ollama can be replaced later.

### Follow-up

Implement `OllamaClient` under `src/director/`.

### Related files

```text
docs/AIDesign.md
docs/PromptGuide.md
```

---

## ADR-0014 - Use Qwen 2.5 3B as first Visual Director model

Date: 2026-07-07  
Status: Accepted

### Context

The Visual Director needs to:

- read timeline JSON
- select keywords
- choose effects
- choose emotion
- suggest icon_query
- output JSON

The model should be light and local.

### Decision

Use Qwen 2.5 3B as first Visual Director model.

### Reasons

- Lightweight.
- Works locally through Ollama.
- Good at structured JSON tasks.
- Sufficient for visual direction.
- Runs without GPU on many machines.
- Replaceable later.

### Alternatives considered

1. Qwen 2.5 3B.
2. Phi-3 Mini.
3. Gemma small models.
4. Llama 3.2 3B.
5. Cloud model.

Option 1 was chosen for initial implementation.

### Consequences

Prompts should be explicit and schema-driven.

Model name must be configurable.

### Follow-up

Evaluate alternatives later if output quality is weak.

### Related files

```text
docs/AIDesign.md
docs/PromptGuide.md
```

---

## ADR-0015 - Use embeddings for icon selection

Date: 2026-07-07  
Status: Accepted

### Context

The user wants a local icon library.

AI should select relevant icons for scenes.

A large icon library may contain hundreds or thousands of assets.

### Decision

Use embedding-based semantic search for icon selection.

### Reasons

- LLM should not memorize filenames.
- Works with large asset libraries.
- Supports Vietnamese tags.
- More scalable than keyword-only matching.
- More deterministic than asking LLM for exact file.
- Icon DB can be updated without changing prompt.

### Alternatives considered

1. LLM picks exact filename.
2. Manual keyword dictionary only.
3. Embedding search over icon metadata.

Option 3 was chosen.

### Consequences

Create `assets/icons/icon_db.json`.

Embedding module maps `icon_query` to actual icon asset.

### Follow-up

Implement icon selector in Sprint 4.

### Related files

```text
docs/AssetGuide.md
docs/AIDesign.md
```

---

## ADR-0016 - LLM returns icon_query, not icon filename

Date: 2026-07-07  
Status: Accepted

### Context

The Visual Director should suggest icons, but it cannot reliably know local asset filenames.

### Decision

LLM returns `icon_query`.

Embedding module returns `icon_id`, `icon_path`, and score.

### Reasons

- Avoids hallucinated filenames.
- Scales to large asset library.
- Decouples AI from local assets.
- Easier to validate.
- Easier to replace icons.

### Alternatives considered

1. LLM outputs exact filename.
2. LLM outputs category only.
3. LLM outputs semantic query.

Option 3 was chosen.

### Consequences

Visual timeline has two stages:

```text
timeline.director.json
timeline.visual.json
```

### Follow-up

Document `icon_query` in schema.

### Related files

```text
docs/JSONSchema.md
docs/PromptGuide.md
docs/AssetGuide.md
```

---

## ADR-0017 - Renderer must be deterministic

Date: 2026-07-07  
Status: Accepted

### Context

The renderer creates the final visible video.

For debugging, testing, and batch production, output should be reproducible.

### Decision

Renderer must be deterministic.

### Reasons

- Repeatable outputs.
- Easier testing.
- Easier debugging.
- Works with JSON contract.
- Avoids model unpredictability during render.
- Supports render-only workflow.

### Alternatives considered

1. Renderer calls AI dynamically.
2. Renderer uses random choices.
3. Renderer consumes fixed JSON and seeded randomness.

Option 3 was chosen.

### Consequences

If randomness is used, seed it.

Renderer must not call LLM.

### Follow-up

Add render_seed to schema.

### Related files

```text
docs/RendererDesign.md
docs/JSONSchema.md
```

---

## ADR-0018 - Prompts live in prompt files

Date: 2026-07-07  
Status: Accepted

### Context

Prompts are essential project behavior.

Hardcoding prompts inside Python makes them hard to review and update.

### Decision

Prompts must live under:

```text
prompts/
```

### Reasons

- Versionable.
- Reviewable.
- Editable by non-programmers.
- Easier for Codex/ChatGPT to inspect.
- Keeps code cleaner.
- Prompt changes can be tracked.

### Alternatives considered

1. Hardcode prompts in Python.
2. Store prompts in config strings.
3. Store prompts as Markdown files.

Option 3 was chosen.

### Consequences

Need prompt loader and prompt rendering logic.

### Follow-up

Create `prompts/visual_director.md` in Sprint 3.

### Related files

```text
docs/PromptGuide.md
docs/AIDesign.md
```

---

## ADR-0019 - Use docs-first Sprint 0B before coding more

Date: 2026-07-07  
Status: Accepted

### Context

The bootstrap project initially had mostly empty Markdown files.

The user correctly noted that empty rules would not help future ChatGPT/Codex sessions.

### Decision

Complete Sprint 0B documentation before implementing more code.

### Reasons

- Prevents context loss.
- Gives Codex clear rules.
- Protects architecture.
- Makes future chats shorter.
- Converts chat discussion into repository knowledge.

### Alternatives considered

1. Start Sprint 1 immediately.
2. Add small placeholder docs.
3. Complete substantial docs first.

Option 3 was chosen.

### Consequences

Several substantial docs must be created before moving on:

```text
AGENTS.md
PROJECT_RULES.md
README.md
Architecture.md
Pipeline.md
JSONSchema.md
RendererDesign.md
AIDesign.md
PromptGuide.md
AssetGuide.md
CodingStandard.md
DecisionLog.md
ROADMAP.md
```

### Follow-up

Commit docs as Sprint 0B.

### Related files

```text
docs/
```

---

## ADR-0020 - Use modular src folder structure

Date: 2026-07-07  
Status: Accepted

### Context

Earlier script naming used numbered files like:

```text
01_extract_audio.py
02_speech_to_text.py
```

This is useful for tutorials but not ideal for a long-term engine.

### Decision

Use modular source folders:

```text
src/audio
src/speech
src/timeline
src/director
src/embedding
src/renderer
src/exporter
src/common
src/config
```

### Reasons

- Clear ownership.
- Easier testing.
- Easier Codex navigation.
- Better maintainability.
- Better long-term package structure.

### Alternatives considered

1. Numbered scripts.
2. One pipeline folder.
3. Modular src folders.

Option 3 was chosen.

### Consequences

Scripts should be thin wrappers.

Core logic goes under `src/`.

### Follow-up

Refactor any script logic into modules as project grows.

### Related files

```text
docs/Architecture.md
docs/CodingStandard.md
```

---

## ADR-0021 - Use intermediate JSON files for inspection

Date: 2026-07-07  
Status: Accepted

### Context

The pipeline has multiple AI and deterministic stages.

Debugging will be hard if everything happens in memory.

### Decision

Write intermediate JSON files.

### Reasons

- Human inspection.
- Manual correction.
- AI agent inspection.
- Pipeline resumability.
- Easier debugging.
- Easier future UI.
- Easier test fixtures.

### Alternatives considered

1. In-memory only.
2. Database only.
3. JSON files per stage.

Option 3 was chosen.

### Consequences

Default outputs:

```text
output/transcript.json
output/timeline.normalized.json
output/timeline.director.json
output/timeline.visual.json
output/render_report.json
```

### Follow-up

Implement JSON read/write helpers.

### Related files

```text
docs/Pipeline.md
docs/JSONSchema.md
```

---

## ADR-0022 - Use original audio merge after silent render

Date: 2026-07-07  
Status: Accepted

### Context

Renderer should focus on visuals.

Audio handling should be separate.

### Decision

Renderer produces silent video.

Exporter merges original audio.

### Reasons

- Clear module boundary.
- Renderer can be tested without audio.
- Exporter handles FFmpeg merge.
- Original audio sync can be validated separately.
- Future TTS/audio mixing remains separate.

### Alternatives considered

1. Renderer writes video with audio.
2. Exporter handles final merge.
3. Use MoviePy for everything.

Option 2 was chosen.

### Consequences

Renderer output:

```text
output/silent_video.mp4
```

Exporter output:

```text
output/final.mp4
```

### Follow-up

Build exporter in Sprint 6.

### Related files

```text
docs/RendererDesign.md
docs/Pipeline.md
```

---

## ADR-0023 - Do not require GPU

Date: 2026-07-07  
Status: Accepted

### Context

The user may test on Windows without GPU and may use Mac M1.

The desired video style is mostly text, icons, and 2D animation.

### Decision

GPU is optional.

The core pipeline must run on CPU.

### Reasons

- Wider accessibility.
- Easier setup.
- Works on Mac M1.
- Avoids CUDA dependency.
- Text rendering does not need GPU.
- Local AI models selected are lightweight.

### Alternatives considered

1. GPU-required pipeline.
2. CPU-first pipeline.
3. Cloud-only compute.

Option 2 was chosen.

### Consequences

Use CPU-friendly models and rendering.

Large AI models remain optional.

### Follow-up

Avoid mandatory CUDA dependencies.

### Related files

```text
docs/AIDesign.md
docs/CodingStandard.md
```

---

## ADR-0024 - Use conventional commits

Date: 2026-07-07  
Status: Accepted

### Context

The project will use GitHub and may grow over many commits.

Clear commit messages help future review.

### Decision

Use conventional commit prefixes.

### Prefixes

```text
feat:
fix:
docs:
refactor:
test:
chore:
ci:
perf:
```

### Reasons

- Clear history.
- Easy changelog generation later.
- Better communication with AI agents.
- Helps separate docs/code/test changes.

### Alternatives considered

1. Random commit messages.
2. Conventional commits.

Option 2 was chosen.

### Consequences

Commit messages should be meaningful.

### Follow-up

Use this in every future commit.

### Related files

```text
docs/CodingStandard.md
README.md
```

---

## ADR-0025 - Keep cloud providers optional

Date: 2026-07-07  
Status: Accepted

### Context

Cloud AI providers may improve quality but introduce cost, privacy, and API key dependency.

### Decision

Cloud providers are optional integrations only.

### Reasons

- Local-first policy.
- Privacy.
- No required API key.
- Offline-friendly.
- Easier beginner setup.
- Lower operating cost.

### Alternatives considered

1. Use cloud by default.
2. Local-only forever.
3. Local-first with optional cloud.

Option 3 was chosen.

### Consequences

Provider interfaces should allow future cloud options.

Default config uses local providers.

### Follow-up

Do not add cloud provider without docs and config.

### Related files

```text
docs/AIDesign.md
PROJECT_RULES.md
```

---

## ADR-0026 - Use English for core project documentation

Date: 2026-07-07  
Status: Accepted

### Context

The user speaks Vietnamese, but coding tools and AI agents often perform best with English technical documentation.

### Decision

Core repository documentation is written in English.

User-facing chat guidance can remain Vietnamese.

### Reasons

- Better compatibility with Codex and AI coding agents.
- Technical terms are clearer.
- Easier open-source collaboration later.
- Prompts/code comments align with common developer practice.

### Alternatives considered

1. Vietnamese-only docs.
2. English-only docs.
3. English project docs, Vietnamese user guidance.

Option 3 was chosen.

### Consequences

Docs are in English.

Future user manual may include Vietnamese.

### Follow-up

Keep README technical content English.

### Related files

```text
docs/CodingStandard.md
README.md
```

---

## ADR-0027 - Use Vietnamese as first-class content language

Date: 2026-07-07  
Status: Accepted

### Context

The user’s target content is Vietnamese dialogue.

The engine must preserve accents and natural Vietnamese text.

### Decision

Vietnamese is a first-class content language.

### Reasons

- Primary user content is Vietnamese.
- STT must support Vietnamese.
- Fonts must support Vietnamese glyphs.
- Prompts must preserve Vietnamese.
- JSON must be written as UTF-8.

### Alternatives considered

1. English-first content only.
2. Multilingual without priority.
3. Vietnamese first-class plus future multilingual support.

Option 3 was chosen.

### Consequences

Need Vietnamese-capable fonts.

Use `ensure_ascii=False`.

Prompts must say not to translate.

### Follow-up

Test Vietnamese rendering.

### Related files

```text
docs/AIDesign.md
docs/RendererDesign.md
docs/CodingStandard.md
```

---

## ADR-0028 - Use full-screen kinetic text, not traditional subtitles

Date: 2026-07-07  
Status: Accepted

### Context

The user does not want simple subtitles.

They want each frame to show one or two sentences with large text across the screen, with keyword effects.

### Decision

The renderer targets full-screen kinetic text scenes, not traditional subtitle overlays.

### Reasons

- Matches TikTok/Reels style.
- More visually engaging.
- Supports keyword emphasis.
- Better for humorous dialogue.
- Aligns with user's stated vision.

### Alternatives considered

1. Normal bottom subtitles.
2. Full-screen text scenes.
3. Hybrid subtitle + large text.

Option 2 was chosen for the main product style.

### Consequences

Timeline scenes should be short.

Visual Director should create display lines.

Renderer should prioritize large readable text.

### Follow-up

Use `lines` field in visual timeline.

### Related files

```text
docs/RendererDesign.md
docs/PromptGuide.md
```

---

## ADR-0029 - Each frame should normally contain one or two sentences

Date: 2026-07-07  
Status: Accepted

### Context

The user explicitly clarified that each frame should have only one or two sentences.

### Decision

Each visual scene should normally contain one or two sentences.

### Reasons

- Better readability.
- Better short-form pacing.
- Easier keyword emphasis.
- Less subtitle-like.
- Works with large typography.

### Alternatives considered

1. Dense subtitle blocks.
2. One or two sentences per frame.
3. Word-by-word display only.

Option 2 was chosen.

### Consequences

Timeline analyzer should split long segments.

Visual Director should avoid dense lines.

### Follow-up

Add max scene text rules.

### Related files

```text
docs/Pipeline.md
docs/PromptGuide.md
```

---

## ADR-0030 - Delay WhisperX and diarization until after basic STT

Date: 2026-07-07  
Status: Accepted

### Context

The user wants speaker roles eventually.

WhisperX and pyannote can help but are more complex to install.

### Decision

Do not add WhisperX/pyannote in Sprint 1.

Start with Faster Whisper.

Add diarization later.

### Reasons

- Reduce setup complexity.
- Get first vertical slice working.
- Avoid dependency problems.
- Sprint 1 should be focused.
- Speaker diarization can be added later.

### Alternatives considered

1. Start with WhisperX immediately.
2. Start with Faster Whisper.
3. Use cloud diarization.

Option 2 was chosen.

### Consequences

Initial speaker labels may be unknown or inferred.

Diarization becomes future sprint.

### Follow-up

Document diarization as optional future feature.

### Related files

```text
docs/AIDesign.md
docs/Pipeline.md
```

---

## ADR-0031 - Start renderer with Pillow + MoviePy

Date: 2026-07-07  
Status: Accepted

### Context

Renderer needs to draw text, icons, backgrounds, and simple animations.

Multiple backend options exist.

### Decision

Initial renderer can use Pillow + MoviePy.

### Reasons

- Easy to implement.
- Good for text rendering.
- Good for early prototyping.
- Simple Python workflow.
- Enough for V1 proof-of-concept.

### Alternatives considered

1. FFmpeg filter_complex only.
2. OpenCV only.
3. Pillow + MoviePy.
4. Custom frame pipe to FFmpeg.

Option 3 was selected for first renderer.

### Consequences

May need performance optimization later.

Renderer backend should be replaceable.

### Follow-up

Keep backend abstraction in mind.

### Related files

```text
docs/RendererDesign.md
```

---

## ADR-0032 - Start with solid dark background

Date: 2026-07-07  
Status: Accepted

### Context

Early generated concepts used dark backgrounds with high-contrast text.

The user liked that direction.

### Decision

Use solid dark background as the default first visual template.

### Reasons

- High readability.
- Easy to render.
- Works with white/yellow text.
- Avoids asset dependency.
- Good for TikTok-style bold typography.

### Alternatives considered

1. Complex backgrounds.
2. Original video background.
3. Solid dark background.

Option 3 was chosen for early renderer.

### Consequences

Default template can render without background image assets.

### Follow-up

Add backgrounds later through templates.

### Related files

```text
docs/RendererDesign.md
docs/AssetGuide.md
```

---

## ADR-0033 - Use speaker colors for dialogue clarity

Date: 2026-07-07  
Status: Accepted

### Context

The content is often a dialogue between two people.

Visual clarity is important.

### Decision

Use speaker styles/colors in templates.

Default:

```text
speaker_a: blue
speaker_b: pink
```

### Reasons

- Helps distinguish speakers.
- Works without avatars.
- Good for short scenes.
- Easy to implement in speaker labels.

### Alternatives considered

1. No speaker styling.
2. Avatar-only speaker identity.
3. Speaker colors and labels.

Option 3 was chosen.

### Consequences

Speaker styles belong to template.

Do not hardcode colors deep in renderer.

### Follow-up

Add speaker label rendering in renderer.

### Related files

```text
docs/RendererDesign.md
docs/AssetGuide.md
```

---

## ADR-0034 - Use yellow as default keyword highlight

Date: 2026-07-07  
Status: Accepted

### Context

Early visual direction used white text with yellow keyword emphasis.

This is common in short-form content.

### Decision

Use yellow as default primary keyword color in the default template.

### Reasons

- High contrast on dark background.
- Easy to notice.
- Works well with white main text.
- Fits TikTok style.

### Alternatives considered

1. Red.
2. Yellow.
3. Neon blue.
4. Template-specific only.

Option 2 chosen as default; templates can override.

### Consequences

Default template defines keyword color.

Renderer should use template style, not hardcoded value.

### Follow-up

Add keyword style token.

### Related files

```text
docs/RendererDesign.md
docs/AssetGuide.md
```

---

## ADR-0035 - Use schema validation before rendering

Date: 2026-07-07  
Status: Accepted

### Context

LLM output can be invalid.

Renderer should not fail halfway through video generation.

### Decision

Validate visual timeline before rendering.

### Reasons

- Fail early.
- Clear errors.
- Protects renderer.
- Easier debugging.
- Prevents bad output.

### Alternatives considered

1. Renderer tries to handle everything.
2. Validate before render.

Option 2 was chosen.

### Consequences

Need validation for:

- required fields
- timing
- known layouts
- known effects
- asset references
- text fields

### Follow-up

Implement Pydantic models or validators.

### Related files

```text
docs/JSONSchema.md
docs/RendererDesign.md
```

---

## ADR-0036 - Use Pydantic for runtime schema validation

Date: 2026-07-07  
Status: Accepted

### Context

The project uses structured JSON across stages.

Runtime validation is needed.

### Decision

Use Pydantic for Python runtime validation.

### Reasons

- Strong typed models.
- Good error messages.
- Python-first.
- Works well for JSON.
- Helpful for Codex and IDEs.

### Alternatives considered

1. Manual validation only.
2. JSON Schema only.
3. Pydantic plus docs.

Option 3 was chosen.

### Consequences

Add Pydantic dependency.

Keep docs in `JSONSchema.md`.

### Follow-up

Implement Pydantic models in relevant modules.

### Related files

```text
docs/JSONSchema.md
docs/CodingStandard.md
```

---

## ADR-0037 - Keep prompts external and versioned

Date: 2026-07-07  
Status: Accepted

### Context

Prompts affect behavior just like code.

They should be reviewable and versioned.

### Decision

Prompt files should include name/version metadata and live under `prompts/`.

### Reasons

- Easier review.
- Easier testing.
- Easier iteration.
- Clear behavior history.
- Supports prompt cache invalidation.

### Alternatives considered

1. Hardcoded prompt strings.
2. External prompt files without versions.
3. External versioned prompt files.

Option 3 was chosen.

### Consequences

Prompt version should be recorded in AI output metadata.

### Follow-up

Add prompt loader in Sprint 3.

### Related files

```text
docs/PromptGuide.md
docs/AIDesign.md
```

---

## ADR-0038 - Use semantic icon metadata with Vietnamese tags

Date: 2026-07-07  
Status: Accepted

### Context

Icon selection must work for Vietnamese content.

### Decision

Icon DB should include Vietnamese tags as first-class metadata.

### Reasons

- User content is Vietnamese.
- Embedding search needs meaningful text.
- Avoids requiring English query translation.
- Improves icon matching quality.

### Alternatives considered

1. English-only icon tags.
2. Vietnamese-only icon tags.
3. Vietnamese tags plus optional English tags.

Option 3 was chosen.

### Consequences

`icon_db.json` should include:

```json
"tags": ["báo thức", "đồng hồ"],
"tags_en": ["alarm", "clock"]
```

### Follow-up

Create starter icon DB.

### Related files

```text
docs/AssetGuide.md
docs/AIDesign.md
```

---

## ADR-0039 - Keep first renderer visually simple

Date: 2026-07-07  
Status: Accepted

### Context

The project has many possible visual features.

Building them all before the pipeline works would slow progress.

### Decision

First renderer should be simple:

- dark background
- large text
- keyword highlight
- speaker label
- one or two basic effects
- optional icon

### Reasons

- Establish end-to-end pipeline.
- Easier debugging.
- Avoid premature complexity.
- User can see first result faster.
- Future animation engine can improve later.

### Alternatives considered

1. Build advanced renderer first.
2. Build simple renderer first.

Option 2 was chosen.

### Consequences

Sprint 5 scope should stay focused.

### Follow-up

Implement effect registry later.

### Related files

```text
docs/RendererDesign.md
docs/ROADMAP.md
```

---

## ADR-0040 - Use one logical change per commit

Date: 2026-07-07  
Status: Accepted

### Context

The project is being developed with GitHub and AI agents.

Large mixed commits are harder to understand.

### Decision

Use one logical change per commit.

### Reasons

- Easier review.
- Easier rollback.
- Better history.
- Helps Codex understand changes.
- Supports issue-based development.

### Alternatives considered

1. Commit everything at end.
2. Small logical commits.

Option 2 was chosen.

### Consequences

Docs, code, tests may be separate commits when appropriate.

### Follow-up

Maintain clean Git history.

### Related files

```text
docs/CodingStandard.md
```

---

## 5. Proposed future decisions

The following are not accepted yet.

They may become ADRs later.

---

## Proposed - Package layout under `src/ai_video_engine/`

Status: Proposed

### Context

Current bootstrap may have direct folders under `src/`.

Long-term Python packaging may prefer:

```text
src/ai_video_engine/
```

### Possible decision

Move all source modules under `src/ai_video_engine/`.

### Reason to consider

- Standard Python packaging.
- Cleaner imports.
- Easier `pip install -e .`.

### Consequence

Would require restructuring imports and docs.

---

## Proposed - Add Ruff and Black

Status: Proposed

### Context

Code formatting and linting will matter as code grows.

### Possible decision

Use Ruff and Black.

### Reason to consider

- Consistent formatting.
- Better CI.
- Catches simple errors.

### Consequence

Need pyproject config and CI update.

---

## Proposed - Add CLI package command

Status: Proposed

### Context

Pipeline should eventually be runnable as:

```bash
ai-video build input/video.mp4
```

### Possible decision

Add CLI entry point.

### Reason to consider

Better user experience.

### Consequence

Need package structure and pyproject script entry.

---

## Proposed - Add WhisperX for word-level timing

Status: Proposed

### Context

Word-level timing enables per-word animation.

### Possible decision

Add WhisperX as optional provider.

### Reason to consider

Better animation sync.

### Consequence

More dependencies and setup complexity.

---

## Proposed - Add pyannote for diarization

Status: Proposed

### Context

The user wants clear speaker roles.

### Possible decision

Add pyannote-based diarization later.

### Reason to consider

Better speaker separation.

### Consequence

More setup complexity, possible token/account requirements.

---

## Proposed - Add frame-pipe FFmpeg renderer backend

Status: Proposed

### Context

Pillow + MoviePy may be slow for batch generation.

### Possible decision

Add faster frame-pipe backend later.

### Reason to consider

Performance.

### Consequence

More complex renderer backend.

---

## Proposed - Add web or desktop UI

Status: Proposed

### Context

Manual review/editing of JSON may benefit from UI.

### Possible decision

Add UI after core pipeline works.

### Reason to consider

Better non-technical user workflow.

### Consequence

Must keep core engine independent from UI.

---

## Proposed - Use Git LFS for large assets

Status: Proposed

### Context

Asset library may grow large.

### Possible decision

Use Git LFS or external asset storage.

### Reason to consider

Avoid bloating Git repository.

### Consequence

More setup complexity.

---

## 6. Decision template for future entries

Copy this template.

```text
## ADR-00XX - Title

Date: YYYY-MM-DD
Status: Proposed | Accepted | Superseded | Deprecated | Rejected

### Context

Describe the situation.

### Decision

Describe the decision.

### Reasons

- Reason 1
- Reason 2
- Reason 3

### Alternatives considered

1. Option A
2. Option B
3. Option C

### Consequences

Describe trade-offs and impact.

### Follow-up

Describe next actions.

### Related files

```text
path/to/file
```
```

---

## 7. Decision governance rules

### Rule 7.1

Do not delete old decisions.

If a decision changes, mark old one as Superseded and create a new ADR.

### Rule 7.2

Do not silently change architecture.

Record major changes here.

### Rule 7.3

Prompts, schemas, renderer backends, and model choices require DecisionLog updates.

### Rule 7.4

Sprint scope decisions should be recorded if they affect roadmap.

### Rule 7.5

If Codex or another AI agent makes a major design change, it must update this file.

---

## 8. Current next decision needed

The next likely decision is:

```text
ADR-0041 - Choose package layout for Sprint 1 implementation
```

Options:

1. keep current `src/audio`, `src/speech`, etc.
2. move to `src/ai_video_engine/audio`, etc.

This should be decided before significant code is added.

---

## 9. Current Sprint 0B status

Sprint 0B goal:

```text
Complete project knowledge base before moving to Sprint 1.
```

Completed or in progress docs:

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
```

Remaining likely docs:

```text
ROADMAP.md
docs/ProjectVision.md
docs/Sprint0.md
docs/Sprint1.md
docs/Glossary.md
```

---

## 10. Final note

This file should help future maintainers understand the project without reading the original chat.

If an important reason exists only in someone’s memory, it should be added here.

---

# Appendix A - Decision impact matrix

| Decision | Impact | Affected area | Note |
|---|---|---|---|
| AI/renderer separation | Very high | All modules | Never break. |
| Timeline JSON contract | Very high | Pipeline, renderer, AI | Schema changes require docs. |
| Local-first | High | AI, privacy, setup | Cloud optional only. |
| Faster Whisper first | Medium | Speech | Can be replaced later. |
| Ollama first | Medium | Director | Provider abstraction required. |
| Qwen 2.5 3B first | Medium | Director | Model configurable. |
| Embeddings for icons | High | Assets, director | Icon DB required. |
| 9:16 default | Medium | Renderer | Templates can override. |
| Original audio preserved | High | Exporter | TTS optional later. |
| Docs as source of truth | Very high | All work | Keep docs updated. |

---

# Appendix B - Decision categories


## B.1 Architecture

- AI/renderer separation
- Timeline JSON contract
- Module boundaries
- Renderer determinism

## B.2 AI

- Faster Whisper
- Ollama
- Qwen 2.5 3B
- Embedding icon search
- Optional cloud providers

## B.3 Renderer

- Pillow + MoviePy first
- Dark template first
- Keyword highlight
- Silent video output

## B.4 Repository

- GitHub workflow
- AGENTS.md
- Docs-first Sprint 0B
- Conventional commits

## B.5 Product

- 9:16 vertical video
- Full-screen kinetic text
- Original voice preserved
- Vietnamese first-class

---

# Appendix C - Future ADR checklist

1. Does the decision affect module boundaries?
2. Does it affect JSON schema?
3. Does it affect renderer determinism?
4. Does it add or remove a dependency?
5. Does it add a cloud provider?
6. Does it affect privacy?
7. Does it affect Windows support?
8. Does it affect Mac M1 support?
9. Does it affect prompt behavior?
10. Does it affect asset structure?
11. Does it affect Git workflow?
12. Does it affect roadmap?
13. Does it require migration?
14. Does it require tests?
15. Does it require docs updates?

---

# Appendix D - ADR numbering policy

ADR IDs are sequential.

Use four digits:

```text
ADR-0001
ADR-0002
ADR-0003
```

Do not reuse numbers.

If a decision is superseded, keep the old record and reference the new one.

---

# Appendix E - Example superseded decision format

```text
## ADR-0042 - Use MoviePy as only renderer backend

Date: 2026-08-01
Status: Superseded by ADR-0051

Context:
Earlier renderer used MoviePy only.

Decision:
Use MoviePy only.

Reasons:
Simple first implementation.

Consequences:
Performance was limited for batch rendering.

Superseded because:
ADR-0051 introduced backend abstraction.
```

---

# Appendix F - Final DecisionLog rule

When in doubt, write the decision down.

A short recorded decision is better than a forgotten conversation.
