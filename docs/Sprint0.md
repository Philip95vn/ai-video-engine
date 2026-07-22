# Sprint0.md

# AI Video Engine - Sprint 0 Documentation

## 0. Purpose

This document records Sprint 0 for **AI Video Engine**.

Sprint 0 is the foundation sprint.

It explains:

- what was initialized
- why the repository structure exists
- what rules were created
- how GitHub and VS Code are used
- how future AI agents should continue
- what must be true before Sprint 1 begins

This file is part of the project knowledge base.

It should be read together with:

```text
AGENTS.md
PROJECT_RULES.md
README.md
ROADMAP.md
docs/ProjectVision.md
docs/Architecture.md
docs/Pipeline.md
docs/DecisionLog.md
docs/CodingStandard.md
```

---

## 1. Sprint 0 summary

Sprint 0 establishes the project foundation.

It is divided into two parts:

```text
Sprint 0A - Bootstrap
Sprint 0B - Knowledge Base
```

Sprint 0A creates the repository and folder structure.

Sprint 0B fills the repository with enough documentation for future work.

The goal is not to build video generation yet.

The goal is to make the project understandable, maintainable, and ready for implementation.

---

## 2. Sprint 0A status

```text
Completed
```

Sprint 0A created:

- Git repository
- GitHub remote
- VS Code project
- initial folder structure
- initial bootstrap commit
- basic project files

---

## 3. Sprint 0B status

```text
In progress / documentation completion
```

Sprint 0B creates substantial documentation.

This is necessary because:

- the original chat became long
- future work may move to a new ChatGPT conversation
- future work may happen in Codex inside VS Code
- the repository must become the source of truth
- AI agents need written project rules

---

## 4. Sprint 0 goal

The goal of Sprint 0 is:

```text
Create a professional project foundation before writing major engine code.
```

Sprint 0 is successful when:

```text
A future developer or AI agent can clone the repository, read the docs, and understand what to build next.
```

---

## 5. Sprint 0 non-goal

Sprint 0 does not implement:

- speech-to-text pipeline
- renderer
- visual director
- icon selector
- timeline analyzer
- exporter
- UI
- batch processing

Those start in later sprints.

---

## 6. Why Sprint 0 matters

Without Sprint 0, the project would likely become:

- one giant script
- undocumented prompts
- unclear JSON schema
- renderer calling AI
- hardcoded paths
- fragile local setup
- hard to continue in future chats
- hard for Codex to understand

Sprint 0 prevents this.

---

## 7. Sprint 0 design principle

The project starts with documentation because documentation is the memory of the architecture.

Core principle:

```text
Repository > chat memory
```

The repository should contain:

- project vision
- architecture
- pipeline
- rules
- roadmap
- JSON schema
- AI design
- renderer design
- prompt design
- asset design
- coding standard
- decision log

---

## 8. Sprint 0A deliverables

Sprint 0A deliverables:

```text
README.md
PROJECT_RULES.md
ROADMAP.md
CHANGELOG.md
LICENSE
pyproject.toml
requirements.txt
.gitignore
.github/workflows/python.yml
.vscode/
docs/
src/
assets/
prompts/
tests/
examples/
scripts/
output/
temp/
```

---

## 9. Sprint 0A repository setup

The GitHub repository was created under the project name:

```text
ai-video-engine
```

The local working folder was connected to GitHub.

The first project push was completed.

This establishes GitHub as the project memory.

---

## 10. Sprint 0A Git setup

The project was initialized using Git.

Commands used conceptually:

```bash
git init
git remote add origin <repo-url>
git add .
git commit -m "chore: bootstrap AI Video Engine project"
git branch -M main
git push -u origin main
```

The user completed the first push.

---

## 11. Sprint 0A Git identity setup

Git required identity configuration.

The configured identity was:

```text
user.name=Philip95vn
user.email=nhat20021995@gmail.com
```

This allowed commits to be created.

---

## 12. Sprint 0A FFmpeg setup note

During setup, FFmpeg was installed but not initially recognized by terminal because VS Code had not been restarted after PATH changes.

Lesson:

```text
After changing Windows PATH, restart VS Code or terminal.
```

FFmpeg is required later for Sprint 1.

---

## 13. Sprint 0A Python setup note

Python 3.11 was recommended as baseline.

Reason:

- better AI package compatibility
- stable Faster Whisper support
- stable PyTorch ecosystem support
- less risk than very new Python versions

---

## 14. Sprint 0 repository philosophy

The repository should be treated like a serious open-source project even if it remains private.

It should contain:

- docs
- rules
- roadmap
- decision log
- tests
- examples
- CI
- clear structure
- conventional commits

---

## 15. Sprint 0B documentation purpose

Sprint 0B fills the project with real documentation.

The purpose is to make the project understandable without needing the original chat.

This allows:

- new ChatGPT sessions to continue
- Codex to work in VS Code
- future contributors to onboard
- GitHub to preserve project knowledge
- architecture decisions to be visible

---

## 16. Sprint 0B required files

Sprint 0B should complete or substantially populate:

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

---

## 17. Sprint 0B completed file list

Files already produced during Sprint 0B:

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
```

Current file:

```text
docs/Sprint0.md
```

Remaining expected:

```text
docs/Sprint1.md
docs/Glossary.md
CHANGELOG.md
```

---

## 18. Sprint 0B quality bar

Sprint 0B documentation must not be empty placeholder text.

Bad:

```text
# Architecture
```

Good:

```text
Architecture document that explains modules, data flow, constraints, validation, and future evolution.
```

The user explicitly requested full files, not placeholders.

---

## 19. Sprint 0B source of truth rule

After Sprint 0B, future work should begin by reading:

```text
AGENTS.md
PROJECT_RULES.md
ROADMAP.md
docs/
```

Not by asking the user to repeat old context.

---

## 20. Sprint 0B AI agent handoff

A future AI agent should be told:

```text
Continue AI Video Engine.
Read AGENTS.md, PROJECT_RULES.md, ROADMAP.md, and docs before coding.
Current sprint: Sprint 1 - Speech To Text.
```

This should be enough context.

---

## 21. Sprint 0 architecture decisions

Sprint 0 established these key decisions:

1. The project is an engine, not a script.
2. AI generates JSON only.
3. Renderer consumes JSON only.
4. Renderer must not call LLMs.
5. Timeline JSON is the central contract.
6. Original voice is preserved by default.
7. Default output is 9:16 vertical.
8. Local-first processing is default.
9. GPU is optional.
10. Documentation is the source of truth.

---

## 22. Sprint 0 technical decisions

Sprint 0 selected these initial technologies:

```text
Python 3.11
FFmpeg
Faster Whisper
Ollama
Qwen 2.5 3B
sentence-transformers
Pillow
MoviePy
Pydantic
GitHub
VS Code
```

Some are used immediately; others appear in later sprints.

---

## 23. Sprint 0 product decisions

Sprint 0 clarified the first product direction:

```text
Existing video with voice
      ↓
new vertical kinetic text video
      ↓
original voice preserved
```

The first content style:

```text
humorous dialogue
large text
highlighted keywords
icons
dark background
```

---

## 24. Sprint 0 user workflow target

The first full target workflow:

```text
input/video.mp4
      ↓
temp/audio.wav
      ↓
output/transcript.json
      ↓
output/timeline.normalized.json
      ↓
output/timeline.director.json
      ↓
output/timeline.visual.json
      ↓
output/silent_video.mp4
      ↓
output/final.mp4
```

---

## 25. Sprint 0 current repository structure

Recommended structure after Sprint 0:

```text
ai-video-engine/
│
├── README.md
├── AGENTS.md
├── PROJECT_RULES.md
├── ROADMAP.md
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .gitignore
│
├── docs/
│   ├── ProjectVision.md
│   ├── Architecture.md
│   ├── Pipeline.md
│   ├── JSONSchema.md
│   ├── RendererDesign.md
│   ├── AIDesign.md
│   ├── PromptGuide.md
│   ├── AssetGuide.md
│   ├── CodingStandard.md
│   ├── DecisionLog.md
│   ├── Sprint0.md
│   ├── Sprint1.md
│   └── Glossary.md
│
├── src/
│   ├── audio/
│   ├── speech/
│   ├── timeline/
│   ├── director/
│   ├── embedding/
│   ├── renderer/
│   ├── exporter/
│   ├── assets/
│   ├── common/
│   └── config/
│
├── prompts/
├── assets/
├── tests/
├── examples/
├── scripts/
├── output/
└── temp/
```

---

## 26. Sprint 0 folder purpose

### 26.1 `docs/`

Stores project knowledge.

### 26.2 `src/`

Stores production code.

### 26.3 `prompts/`

Stores LLM prompts.

### 26.4 `assets/`

Stores icons, fonts, templates, avatars, backgrounds, SFX.

### 26.5 `tests/`

Stores test code and fixtures.

### 26.6 `scripts/`

Stores thin development scripts.

### 26.7 `output/`

Stores generated outputs.

### 26.8 `temp/`

Stores temporary intermediate files.

---

## 27. Sprint 0 `.gitignore` intent

The project should ignore:

```text
.venv/
__pycache__/
*.pyc
.env
output/
temp/
cache/
*.mp4
*.mov
*.wav
*.mp3
```

Generated media should not be committed by default.

Small fixtures may be committed intentionally under `tests/fixtures/`.

---

## 28. Sprint 0 requirements intent

Initial `requirements.txt` should support:

- STT
- LLM client
- embeddings
- rendering
- audio helpers
- JSON validation
- CLI/logging helpers

Possible dependencies:

```text
faster-whisper
requests
sentence-transformers
scikit-learn
numpy
Pillow
moviepy
pydub
rich
orjson
pydantic
edge-tts
```

Not every dependency is used immediately.

---

## 29. Sprint 0 pyproject intent

`pyproject.toml` should eventually define:

- project metadata
- Python version
- dependencies
- optional dependency groups
- CLI entry point
- test config
- formatting config

Initial pyproject can be minimal.

---

## 30. Sprint 0 CI intent

Initial CI can be minimal.

First CI may only check:

```text
Python setup
repository checkout
```

Later CI should run:

```text
pytest
ruff
black check
schema validation
```

CI should not download large models by default.

---

## 31. Sprint 0 Git workflow

Recommended workflow:

```bash
git pull
git status
git add .
git commit -m "type: message"
git push
```

Use conventional commits.

Examples:

```text
docs: complete Sprint 0B project knowledge base
feat: add audio extraction command builder
test: add transcript schema tests
fix: handle missing ffmpeg on Windows
```

---

## 32. Sprint 0 commit policy

One logical change per commit.

Do not mix unrelated work.

Good Sprint 0B commit:

```text
docs: complete Sprint 0B project knowledge base
```

---

## 33. Sprint 0 GitHub issue policy

Future work should use GitHub issues.

First issue after Sprint 0B:

```text
Sprint 1 - Speech To Text
```

Issue should include:

- goal
- input
- output
- tasks
- acceptance criteria

---

## 34. Sprint 0 documentation policy

Documentation must be updated when:

- architecture changes
- schema changes
- pipeline changes
- prompt behavior changes
- renderer behavior changes
- asset structure changes
- model choices change

DecisionLog must record major decisions.

---

## 35. Sprint 0 AGENTS.md purpose

`AGENTS.md` is the primary instruction file for AI coding agents.

It tells agents:

- project goal
- core architecture
- rules
- workflow
- what not to do
- how to continue in new chat
- how Codex should work

This file protects the project when using AI tools.

---

## 36. Sprint 0 PROJECT_RULES.md purpose

`PROJECT_RULES.md` defines mandatory project rules.

It is stricter than normal documentation.

If a quick implementation conflicts with project rules, project rules win.

---

## 37. Sprint 0 README purpose

`README.md` explains the project to new humans.

It should cover:

- what the project does
- status
- setup
- pipeline
- usage goals
- roadmap
- development workflow

---

## 38. Sprint 0 Architecture.md purpose

`docs/Architecture.md` explains system architecture.

It should describe:

- modules
- data flow
- responsibilities
- boundaries
- future extension points

---

## 39. Sprint 0 Pipeline.md purpose

`docs/Pipeline.md` explains the pipeline from input to final output.

It should define:

- stages
- inputs
- outputs
- validation checkpoints
- sprint mapping

---

## 40. Sprint 0 JSONSchema.md purpose

`docs/JSONSchema.md` defines structured data contracts.

It should document:

- transcript JSON
- normalized timeline JSON
- director timeline JSON
- visual timeline JSON
- render report JSON
- asset schemas

---

## 41. Sprint 0 RendererDesign.md purpose

`docs/RendererDesign.md` explains deterministic rendering.

It should define:

- renderer boundaries
- layout system
- effect system
- text rendering
- safe zones
- templates
- backend strategy

---

## 42. Sprint 0 AIDesign.md purpose

`docs/AIDesign.md` explains AI usage.

It should define:

- STT model
- Visual Director LLM
- embedding icon selector
- local-first policy
- validation strategy
- prompt output handling

---

## 43. Sprint 0 PromptGuide.md purpose

`docs/PromptGuide.md` explains prompt design.

It should define:

- prompt storage
- prompt versioning
- JSON-only rules
- Visual Director prompt
- JSON repair prompt
- prompt testing

---

## 44. Sprint 0 AssetGuide.md purpose

`docs/AssetGuide.md` explains asset management.

It should define:

- asset folders
- icon DB
- font DB
- templates
- metadata
- validation
- licensing
- asset selection flow

---

## 45. Sprint 0 CodingStandard.md purpose

`docs/CodingStandard.md` defines coding rules.

It should cover:

- Python version
- module boundaries
- naming
- type hints
- errors
- tests
- Git
- AI agent behavior
- renderer restrictions

---

## 46. Sprint 0 DecisionLog.md purpose

`docs/DecisionLog.md` records key decisions.

It should answer:

```text
Why did we choose this?
```

not just:

```text
What did we choose?
```

---

## 47. Sprint 0 ROADMAP.md purpose

`ROADMAP.md` defines sprint order and future milestones.

It should keep development focused.

---

## 48. Sprint 0 ProjectVision.md purpose

`docs/ProjectVision.md` defines product direction.

It should explain:

- why the project exists
- who it is for
- what it should become
- future recruitment direction
- long-term product tracks

---

## 49. Sprint 0 Sprint0.md purpose

This file records foundation work.

It helps future sessions understand why the project starts with documentation.

---

## 50. Sprint 0 Sprint1.md purpose

`docs/Sprint1.md` should define the next sprint in detail:

```text
Speech To Text
```

It should include:

- goal
- scope
- non-scope
- files to create
- commands
- acceptance criteria
- tests

---

## 51. Sprint 0 Glossary.md purpose

`docs/Glossary.md` should define key terms.

Examples:

- Timeline
- Scene
- Visual Director
- Renderer
- Exporter
- Keyword
- Template
- Asset
- Icon Query
- STT
- Diarization

---

## 52. Sprint 0 accepted architecture

The accepted architecture:

```text
Input Media
    ↓
Audio Extractor
    ↓
Speech To Text
    ↓
Transcript JSON
    ↓
Timeline Analyzer
    ↓
Visual Director AI
    ↓
Icon Selector
    ↓
Visual Timeline JSON
    ↓
Renderer
    ↓
Silent Video
    ↓
Exporter
    ↓
Final MP4
```

---

## 53. Sprint 0 accepted module boundaries

```text
src/audio       → audio extraction
src/speech      → speech-to-text
src/timeline    → timeline normalization
src/director    → LLM visual direction
src/embedding   → semantic icon search
src/renderer    → deterministic rendering
src/exporter    → final MP4 export
src/assets      → asset registry
src/common      → shared utilities
src/config      → config loading
```

---

## 54. Sprint 0 critical rule: renderer is AI-free

Renderer must never call:

- Ollama
- OpenAI
- Gemini
- Claude
- LLM clients
- prompt loader
- speech-to-text model
- embedding model

Renderer consumes validated `timeline.visual.json`.

---

## 55. Sprint 0 critical rule: prompts are external

Prompts must live under:

```text
prompts/
```

Prompt text should not be embedded as giant strings inside Python modules.

---

## 56. Sprint 0 critical rule: assets are metadata-driven

AI returns:

```text
icon_query
```

Asset selector returns:

```text
icon_id
icon_path
icon_score
```

Renderer draws the resolved icon.

---

## 57. Sprint 0 critical rule: JSON is inspectable

Important files:

```text
output/transcript.json
output/timeline.normalized.json
output/timeline.director.json
output/timeline.visual.json
output/render_report.json
```

These are part of the product design.

---

## 58. Sprint 0 critical rule: original voice preserved

For existing-video workflow:

```text
input voice → preserved in final output
```

The renderer creates silent video.

Exporter merges original audio.

---

## 59. Sprint 0 critical rule: local-first

Default processing is local.

Cloud providers may be optional later, but must not be required.

---

## 60. Sprint 0 critical rule: no GPU required

The engine must work on CPU.

GPU acceleration can be optional later.

---

## 61. Sprint 0 development environment

Target development environments:

```text
Windows + VS Code
Mac M1 + VS Code
```

Windows is important because the user is testing there.

---

## 62. Sprint 0 external tools

Required now or soon:

```text
Git
Python 3.11
FFmpeg
Ollama
```

Sprint 1 requires:

```text
FFmpeg
Faster Whisper
```

Sprint 3 requires:

```text
Ollama
Qwen 2.5 3B
```

---

## 63. Sprint 0 Windows notes

Important Windows lessons:

1. Add FFmpeg to PATH.
2. Restart VS Code after PATH changes.
3. Use PowerShell carefully.
4. Use `pathlib.Path` in Python.
5. Avoid shell string commands.
6. Use Python 3.11 virtual environment.

---

## 64. Sprint 0 Mac notes

Mac M1 should be supported.

Avoid mandatory CUDA.

Use CPU-friendly models.

FFmpeg can be installed through Homebrew.

Ollama supports Mac.

---

## 65. Sprint 0 package layout decision pending

One decision remains important before substantial coding:

```text
Should code stay under src/audio, src/speech, etc.,
or move under src/ai_video_engine/audio, etc.?
```

Recommended future structure:

```text
src/ai_video_engine/
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

This should be decided before Sprint 1 implementation if possible.

---

## 66. Sprint 0 proposed ADR

Potential next ADR:

```text
ADR-0041 - Use src/ai_video_engine package layout
```

Reason:

- standard Python packaging
- cleaner imports
- easier CLI entry point
- easier `pip install -e .`

This is not yet final unless accepted.

---

## 67. Sprint 0 Definition of Done

Sprint 0 is complete when:

- repository is on GitHub
- bootstrap structure exists
- major docs are complete
- decisions are recorded
- next sprint is clear
- user can move to new chat
- Codex can understand project from files
- Sprint 1 issue can be created
- no major context remains only in chat

---

## 68. Sprint 0B commit checklist

Before committing Sprint 0B docs:

```bash
git status
```

Check files:

```text
AGENTS.md
PROJECT_RULES.md
README.md
ROADMAP.md
docs/*.md
```

Do not commit:

```text
output/
temp/
cache/
.venv/
```

Commit:

```bash
git add .
git commit -m "docs: complete Sprint 0B project knowledge base"
git push
```

---

## 69. Sprint 0B validation checklist

Before finishing Sprint 0B:

1. AGENTS.md exists.
2. PROJECT_RULES.md exists.
3. README.md exists.
4. ROADMAP.md exists.
5. DecisionLog exists.
6. Architecture doc exists.
7. Pipeline doc exists.
8. JSON schema doc exists.
9. AI design doc exists.
10. Renderer design doc exists.
11. Prompt guide exists.
12. Asset guide exists.
13. Coding standard exists.
14. Sprint 1 doc exists or is next.
15. Docs are substantial, not placeholders.

---

## 70. Sprint 0 known limitations

Sprint 0 does not prove:

- STT works
- renderer works
- final export works
- icon selector works
- Visual Director works

It only establishes foundation.

That is intentional.

---

## 71. Sprint 0 risk: over-documentation

There is a risk of writing too much documentation before coding.

Mitigation:

```text
Stop Sprint 0B after essential docs are complete.
Start Sprint 1 immediately after.
```

Documentation should guide implementation, not delay it forever.

---

## 72. Sprint 0 risk: stale docs

Docs can become stale.

Mitigation:

- update docs with code changes
- DecisionLog for major decisions
- keep sprint docs current
- avoid changing behavior silently

---

## 73. Sprint 0 risk: structure too complex

The project may look large before code exists.

Mitigation:

- implement simple vertical slices
- keep modules small
- do not over-engineer early
- use docs to clarify, not complicate

---

## 74. Sprint 0 transition to Sprint 1

After Sprint 0B:

1. Commit docs.
2. Create GitHub issue for Sprint 1.
3. Decide package layout.
4. Implement audio extraction.
5. Implement STT.
6. Produce `output/transcript.json`.

---

## 75. Sprint 1 starting point

Sprint 1 starts with:

```text
input/video.mp4
```

and should produce:

```text
temp/audio.wav
output/transcript.json
```

No renderer.

No Visual Director.

No icons.

No exporter.

---

## 76. Sprint 1 first task

First task:

```text
Build FFmpeg audio extraction module.
```

Suggested files:

```text
src/audio/commands.py
src/audio/extractor.py
src/common/errors.py
```

---

## 77. Sprint 1 second task

Second task:

```text
Build Faster Whisper transcription module.
```

Suggested files:

```text
src/speech/schema.py
src/speech/faster_whisper_engine.py
```

---

## 78. Sprint 1 third task

Third task:

```text
Write transcript JSON.
```

Suggested helper:

```text
src/common/json_io.py
```

---

## 79. Sprint 1 fourth task

Fourth task:

```text
Add basic tests.
```

Suggested tests:

```text
tests/test_audio_commands.py
tests/test_transcript_schema.py
```

---

## 80. Sprint 1 fifth task

Fifth task:

```text
Create simple script or CLI wrapper.
```

Suggested:

```text
scripts/transcribe.py
```

Later this becomes real CLI.

---

## 81. Sprint 0 lessons learned

Lessons from setup:

1. Go one step at a time.
2. Do not install everything before basics work.
3. Restart VS Code after PATH changes.
4. Python version matters.
5. Git needs user name/email.
6. Docs must not be empty placeholders.
7. File generation should produce real content.
8. Repository should hold context.

---

## 82. Sprint 0 communication style

The user prefers:

- direct files
- fewer long explanations
- step-by-step execution
- one step at a time
- practical commands
- no unnecessary theory during setup

Future assistant should respect this.

---

## 83. Sprint 0 user preference

Important user preference:

```text
Do not over-explain when sending files.
Send the file directly.
```

For implementation guidance:

```text
Guide step by step.
```

---

## 84. Sprint 0 AI memory note

A memory entry was created that the project is:

```text
AI Video Engine
```

with principles:

```text
AI generates JSON
Renderer deterministic
GitHub + VS Code workflow
Modular architecture
Documentation-driven
```

However, the repository documentation should still be the primary source.

---

## 85. Sprint 0 new chat handoff message

Recommended message for new chat:

```text
Continue AI Video Engine.
Read AGENTS.md, PROJECT_RULES.md, ROADMAP.md, and docs before coding.
Current sprint: Sprint 1 - Speech To Text.
Repository: https://github.com/Philip95vn/ai-video-engine
```

---

## 86. Sprint 0 Codex handoff message

Recommended message for Codex:

```text
Read AGENTS.md first.
Then read PROJECT_RULES.md, ROADMAP.md, docs/Architecture.md, docs/Pipeline.md, and docs/Sprint1.md.
Do not code until you understand Sprint 1.
Implement Speech To Text as the smallest useful vertical slice.
```

---

## 87. Sprint 0 final repository expectation

After Sprint 0B, repository should answer:

- What is this project?
- What is the architecture?
- What are the rules?
- What is the roadmap?
- What is the next sprint?
- What JSON does the renderer consume?
- Where does AI belong?
- Where does renderer belong?
- What models are planned?
- How should assets be managed?
- How should code be written?

---

## 88. Sprint 0 final decision summary

Sprint 0 confirms:

```text
AI Video Engine is a local-first, JSON-driven, deterministic rendering engine for short-form video automation.
```

This statement should guide all future work.

---

## 89. Sprint 0 final checklist

Before closing Sprint 0:

1. Commit all docs.
2. Push to GitHub.
3. Confirm repository displays docs.
4. Create Sprint 1 issue.
5. Decide package layout.
6. Start Sprint 1.

---

## 90. Sprint 0 closing note

Sprint 0 is not about visible video output.

Sprint 0 is about creating a foundation strong enough that visible video output can be built without chaos.

After Sprint 0, the project should be ready for real implementation.

---

# Appendix A - Sprint 0 task list

| ID | Task | Status |
|---|---|---|
| S0-001 | Create GitHub repository | done |
| S0-002 | Connect local project to remote | done |
| S0-003 | Create initial project skeleton | done |
| S0-004 | Push initial commit | done |
| S0-005 | Create AGENTS.md | done |
| S0-006 | Create PROJECT_RULES.md | done |
| S0-007 | Create README.md | done |
| S0-008 | Create Architecture.md | done |
| S0-009 | Create Pipeline.md | done |
| S0-010 | Create JSONSchema.md | done |
| S0-011 | Create RendererDesign.md | done |
| S0-012 | Create AIDesign.md | done |
| S0-013 | Create PromptGuide.md | done |
| S0-014 | Create AssetGuide.md | done |
| S0-015 | Create CodingStandard.md | done |
| S0-016 | Create DecisionLog.md | done |
| S0-017 | Create ROADMAP.md | done |
| S0-018 | Create ProjectVision.md | done |
| S0-019 | Create Sprint0.md | current |
| S0-020 | Create Sprint1.md | next |
| S0-021 | Create Glossary.md | next |
| S0-022 | Create CHANGELOG.md | next |
| S0-023 | Commit Sprint 0B docs | pending |

---

# Appendix B - Sprint 0 artifacts

| Artifact | Description |
|---|---|
| Repository | GitHub repository for AI Video Engine. |
| Bootstrap zip | Initial project skeleton. |
| Docs | Markdown project knowledge base. |
| DecisionLog | Architecture decision records. |
| Roadmap | Sprint sequence. |
| Rules | Mandatory engineering rules. |
| Agent instructions | AGENTS.md for Codex/ChatGPT. |

---

# Appendix C - Sprint 0 done criteria

1. GitHub repo exists.
2. Local repo connected to GitHub.
3. Initial commit pushed.
4. Docs are substantial.
5. Architecture documented.
6. Pipeline documented.
7. JSON contracts documented.
8. AI boundaries documented.
9. Renderer boundaries documented.
10. Coding standards documented.
11. Roadmap documented.
12. DecisionLog populated.
13. Sprint 1 scope clear.
14. Future chat handoff message exists.
15. Codex handoff message exists.

---

# Appendix D - Sprint 0 anti-patterns avoided

1. Starting with one giant script.
2. Skipping documentation.
3. Letting renderer call AI.
4. Hardcoding prompts in Python.
5. Using hidden chat memory as project source of truth.
6. Committing generated outputs.
7. Choosing heavy diarization before basic STT.
8. Building UI before pipeline.
9. Building advanced renderer before transcript pipeline.
10. Ignoring Windows setup.

---

# Appendix E - Sprint 0 to Sprint 1 command reminder

After adding Sprint 0B docs:

```bash
git status
git add .
git commit -m "docs: complete Sprint 0B project knowledge base"
git push
```

Then create GitHub issue:

```text
Sprint 1 - Speech To Text
```

Then start implementation.

---

# Appendix F - Final Sprint 0 note

Sprint 0 turns an idea into a project.

Sprint 1 turns the project into a working pipeline.

Do not skip Sprint 1 discipline.
