# CHANGELOG.md

# AI Video Engine - Changelog

All notable changes to **AI Video Engine** will be documented in this file.

This project follows the spirit of [Keep a Changelog](https://keepachangelog.com/) and semantic versioning once releases begin.

The changelog is written for:

- project owner
- human contributors
- ChatGPT
- Codex in VS Code
- GitHub Copilot
- future maintainers
- future release reviewers

---

## Changelog principles

### 1. The changelog is product memory

The changelog records what changed between versions or important development milestones.

It should help someone answer:

```text
What changed?
When did it change?
Why does it matter?
What should I test?
```

---

### 2. The changelog is not the DecisionLog

Use:

```text
docs/DecisionLog.md
```

to explain why major decisions were made.

Use:

```text
CHANGELOG.md
```

to explain what changed in the project.

Both are important.

---

### 3. The changelog should be useful to future AI agents

Codex or ChatGPT should be able to read this file and quickly understand recent project movement.

This matters because the project may continue across many chat sessions.

---

### 4. The changelog should not contain every tiny edit

Do not log every typo.

Do log:

- new modules
- new pipeline stages
- schema changes
- prompt changes
- renderer changes
- dependency changes
- breaking changes
- release milestones
- important documentation changes
- setup changes

---

## Changelog format

Use sections:

```text
Added
Changed
Deprecated
Removed
Fixed
Security
Docs
Internal
Breaking
Known Issues
Next
```

Not every version needs every section.

---

## Version status labels

Use these status labels when useful:

```text
Planned
In Progress
Released
Deprecated
Superseded
```

---

## Current project phase

Current phase:

```text
Sprint 0B - Documentation and Knowledge Base
```

Next phase:

```text
Sprint 1 - Speech To Text
```

---

## [Unreleased]

### Status

```text
In development
```

### Current focus

Prepare the project to start Sprint 1.

The immediate goal is to commit the completed Sprint 0B documentation and then begin Speech To Text implementation.

---

### Added

- Added substantial project documentation for Sprint 0B.
- Added AI agent instructions through `AGENTS.md`.
- Added mandatory project rules through `PROJECT_RULES.md`.
- Added expanded project overview through `README.md`.
- Added technical architecture documentation.
- Added pipeline design documentation.
- Added JSON schema design documentation.
- Added renderer design documentation.
- Added AI design documentation.
- Added prompt guide documentation.
- Added asset guide documentation.
- Added coding standard documentation.
- Added decision log documentation.
- Added roadmap documentation.
- Added project vision documentation.
- Added Sprint 0 documentation.
- Added Sprint 1 planning documentation.
- Added project glossary.
- Added clear Sprint 1 direction: Speech To Text.
- Added guidance for continuing the project in a new ChatGPT conversation.
- Added guidance for continuing the project in Codex inside VS Code.
- Added repository-as-source-of-truth rule.
- Added AI/renderer separation rule.
- Added JSON-first pipeline rule.
- Added local-first AI policy.
- Added default 9:16 video output policy.
- Added original audio preservation policy.
- Added Vietnamese-first content support requirement.
- Added no-GPU-required principle.
- Added conventional commit guidance.
- Added package layout recommendation for `src/ai_video_engine/`.
- Added Sprint 1 code skeletons in documentation.
- Added Sprint 1 test skeletons in documentation.
- Added asset metadata design.
- Added prompt versioning design.
- Added visual timeline schema design.
- Added render report schema design.
- Added icon selection architecture.
- Added embedding-based icon matching plan.
- Added renderer effect registry plan.
- Added layout registry plan.
- Added template system plan.
- Added future recruitment workflow direction.
- Added future batch processing direction.

---

### Changed

- Changed the project framing from a simple TikTok text video script to a full **AI Video Engine**.
- Changed development approach from ad hoc scripting to modular sprint-based engineering.
- Changed knowledge storage approach from chat memory to GitHub repository documentation.
- Changed video generation strategy from AI-rendered video to deterministic renderer controlled by JSON.
- Changed icon selection strategy from LLM filename guessing to embedding-based asset lookup.
- Changed prompt strategy from hardcoded prompt strings to external versioned prompt files.
- Changed renderer target from subtitles to full-screen kinetic text scenes.
- Changed implementation order to prioritize Speech To Text before renderer.
- Changed setup strategy to support Windows and Mac M1 without mandatory GPU.
- Changed Git workflow to conventional commits.
- Changed project structure direction toward package-style Python architecture.

---

### Docs

Created or expanded the following documentation:

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

### Internal

- Established GitHub as the long-term project memory.
- Established VS Code as primary development environment.
- Established Codex/AI-agent compatibility through documentation.
- Established sprint-based development process.
- Established one-logical-change-per-commit policy.
- Established major-decision logging through ADR-style entries.
- Established output and temp folders as generated artifacts that should not be committed.
- Established documentation-first Sprint 0B before major implementation.

---

### Breaking

No runtime breaking changes yet because implementation has not started.

Future breaking changes may occur before v1.0.

---

### Known Issues

- Sprint 1 code is not implemented yet.
- No CLI exists yet.
- No transcript generator exists yet.
- No renderer exists yet.
- No icon selector exists yet.
- No final video export exists yet.
- Documentation files need to be committed into the GitHub repository.
- Package layout decision should be finalized before major code implementation.
- Existing bootstrap may need restructuring to `src/ai_video_engine/`.

---

### Next

Immediate next steps:

1. Add all completed documentation files to the repository.
2. Commit documentation.

```bash
git add .
git commit -m "docs: complete Sprint 0B project knowledge base"
git push
```

3. Create GitHub issue:

```text
Sprint 1 - Speech To Text
```

4. Decide Python package layout.
5. Start Sprint 1 implementation.

---

## [0.1.0-foundation] - Planned

### Status

```text
Planned release tag
```

### Goal

Mark the project foundation as complete.

This version should represent:

- repository initialized
- documentation complete enough for future work
- project rules established
- roadmap established
- Sprint 1 ready to begin

---

### Expected contents

- Project skeleton.
- Documentation knowledge base.
- Roadmap.
- DecisionLog.
- Coding standard.
- Sprint 1 plan.
- GitHub repository setup.
- AI agent instructions.

---

### Release criteria

This release can be tagged when:

- Sprint 0B docs are committed.
- Repository opens correctly on GitHub.
- Future chat/Codex handoff is possible.
- Sprint 1 issue is ready.
- No major context remains only in chat.

---

## [0.2.0-transcription] - Planned

### Status

```text
Planned
```

### Goal

Implement Speech To Text.

One-line output:

```text
input/video.mp4 → output/transcript.json
```

---

### Planned Added

- Audio extraction module.
- FFmpeg command builder.
- FFmpeg availability check.
- Faster Whisper transcription module.
- Transcript schema.
- Transcript JSON writer.
- Transcript validation.
- `scripts/transcribe.py`.
- Basic tests for audio command builder.
- Basic tests for transcript schema.
- Clear missing-FFmpeg error.
- Clear missing-input error.
- Vietnamese UTF-8 transcript output.

---

### Planned Changed

- Update README with Sprint 1 usage.
- Update Pipeline docs with actual command.
- Update DecisionLog with package layout decision if accepted.
- Update pyproject if package layout is changed.

---

### Planned Known Issues

- No speaker diarization.
- No word-level timing.
- No renderer.
- No final MP4 export.
- Transcript punctuation may be imperfect.

---

### Planned Release Criteria

This version is complete when:

```text
python scripts/transcribe.py input/video.mp4
```

creates:

```text
temp/audio.wav
output/transcript.json
```

with valid Vietnamese transcript JSON.

---

## [0.3.0-timeline] - Planned

### Status

```text
Planned
```

### Goal

Implement Timeline Analyzer.

One-line output:

```text
output/transcript.json → output/timeline.normalized.json
```

---

### Planned Added

- Transcript loader.
- Timeline schema.
- Scene schema.
- Scene ID generation.
- Timeline validation.
- Segment-to-scene conversion.
- Merge short segments.
- Split long segments.
- Speaker placeholder structure.
- Normalized timeline writer.
- Timeline analyzer tests.

---

### Planned Known Issues

- No LLM direction yet.
- Speaker labels may remain unknown.
- Scene splitting may be rule-based and simple.

---

### Planned Release Criteria

This version is complete when a valid transcript can be transformed into normalized scene timeline JSON.

---

## [0.4.0-director] - Planned

### Status

```text
Planned
```

### Goal

Implement Visual Director AI.

One-line output:

```text
output/timeline.normalized.json → output/timeline.director.json
```

---

### Planned Added

- Prompt loader.
- Prompt renderer.
- Ollama client.
- Visual Director service.
- Visual Director prompt.
- JSON repair prompt.
- LLM output parser.
- LLM output validator.
- Allowed emotion/effect/layout enum validation.
- Fake LLM tests.
- Debug output for raw model response.

---

### Planned Known Issues

- LLM output quality may vary.
- Prompt iteration will be needed.
- Long videos may need batching.

---

### Planned Release Criteria

This version is complete when Visual Director can enrich scenes with:

- display lines
- emotion
- keywords
- effects
- layout
- icon_query

while preserving IDs and timing.

---

## [0.5.0-icon-selector] - Planned

### Status

```text
Planned
```

### Goal

Implement embedding-based icon selection.

One-line output:

```text
timeline.director.json + icon_db.json → timeline.visual.json
```

---

### Planned Added

- Icon DB schema.
- Starter icon DB.
- Asset registry basics.
- Embedding provider.
- Icon embedding cache.
- Icon semantic search.
- Icon match score.
- Visual timeline writer.
- Icon selector tests.

---

### Planned Known Issues

- Initial icon DB may be small.
- Icon matching quality depends on metadata.
- Missing icons should warn or skip.

---

### Planned Release Criteria

This version is complete when `icon_query` values can be mapped to real local icon assets.

---

## [0.6.0-renderer] - Planned

### Status

```text
Planned
```

### Goal

Implement basic renderer.

One-line output:

```text
output/timeline.visual.json → output/silent_video.mp4
```

---

### Planned Added

- Visual timeline loader.
- Renderer validation.
- Default dark template.
- 1080x1920 canvas.
- Safe zone logic.
- Text renderer.
- Keyword highlight renderer.
- Speaker label renderer.
- Basic `pop` effect.
- Basic `shake` effect if time allows.
- Silent video writer.
- Renderer smoke test.

---

### Planned Known Issues

- Visual style may be simple.
- Performance may not be optimized.
- Advanced effects will come later.

---

### Planned Release Criteria

This version is complete when visual timeline can render a readable silent vertical video.

---

## [0.7.0-exporter] - Planned

### Status

```text
Planned
```

### Goal

Implement final export.

One-line output:

```text
output/silent_video.mp4 + temp/audio.wav → output/final.mp4
```

---

### Planned Added

- FFmpeg audio/video merge command.
- Exporter module.
- Final MP4 writer.
- Duration check.
- Render report.
- Exporter tests.

---

### Planned Known Issues

- Audio sync may need refinement.
- Scene gap handling may affect duration.
- SFX/BGM not included yet.

---

### Planned Release Criteria

This version is complete when final MP4 is created with original audio preserved.

---

## [0.8.0-template-system] - Planned

### Status

```text
Planned
```

### Goal

Make visual style template-driven.

---

### Planned Added

- Template loader.
- Template schema.
- Default template file.
- Style tokens.
- Font tokens.
- Color tokens.
- Keyword style tokens.
- Speaker style tokens.
- Safe zone config.
- Template validation.

---

### Planned Release Criteria

Renderer uses template values instead of hardcoded style constants.

---

## [0.9.0-beta] - Planned

### Status

```text
Planned
```

### Goal

Create first beta end-to-end engine.

---

### Planned Added

- Full pipeline runner.
- Basic CLI.
- End-to-end script.
- Sample timeline.
- Example documentation.
- Pipeline report.
- Basic troubleshooting docs.

---

### Planned Release Criteria

One command can process an input video into a final video using local models and deterministic rendering.

---

## [1.0.0] - Planned

### Status

```text
Planned
```

### Goal

First stable release.

---

### Planned Added

- Stable local workflow.
- Stable visual timeline schema.
- Working CLI.
- Default template.
- Basic icon selection.
- Basic renderer.
- Audio merge.
- Documentation.
- Tests.
- Example project.

---

### Planned Release Criteria

The project can reliably produce short-form videos from input media with inspectable intermediate JSON and original voice preserved.

---

# Development history

## 2026-07-07 - Project idea clarified

### Added

- Initial concept of automated short-form video generator.
- Defined target video style:
  - vertical 9:16
  - voice + large text
  - full-frame text
  - keyword emphasis
  - icon support
  - humorous two-person dialogue

### Changed

- Moved from simple subtitle concept to kinetic text scene concept.
- Clarified that each frame should contain only one or two sentences.

### Notes

This shaped the entire renderer and timeline design.

---

## 2026-07-07 - Hardware direction clarified

### Added

- Confirmed that GPU is not required for the core workflow.
- Mac M1 is suitable.
- CPU rendering is acceptable.
- GPU is optional.

### Notes

This influenced the choice of deterministic renderer and lightweight AI models.

---

## 2026-07-07 - AI role clarified

### Added

- AI should act as Visual Director.
- AI should select keywords, effects, emotion, icon queries.
- AI should not render video.
- AI should output JSON.

### Notes

This became the core architecture rule.

---

## 2026-07-07 - STT workflow clarified

### Added

- Input workflow starts from existing video with voice.
- Need speech-to-text.
- Need transcript with timestamps.
- Need speaker support later.
- Need original audio preserved.

### Notes

This led to Sprint 1.

---

## 2026-07-07 - Pipeline clarified

### Added

Initial full pipeline:

```text
Video
→ Audio Extract
→ Speech To Text
→ Transcript
→ Timeline Analyzer
→ Visual Director
→ Icon Selector
→ Renderer
→ Merge Original Audio
→ Final MP4
```

---

## 2026-07-07 - Windows setup started

### Added

- FFmpeg setup through winget.
- PATH troubleshooting.
- VS Code restart lesson.
- Faster Whisper installation planning.

### Fixed

- Identified that FFmpeg was installed but VS Code terminal had stale PATH.

---

## 2026-07-07 - GitHub workflow started

### Added

- GitHub repository.
- VS Code workflow.
- Git identity setup.
- First push completed.

### Fixed

- Git commit failure due to missing user.name/user.email.

---

## 2026-07-07 - Project bootstrap created

### Added

- Initial project skeleton.
- requirements.txt.
- pyproject.toml.
- docs folder.
- src folders.
- assets folders.
- prompts folder.
- tests folder.
- GitHub Actions placeholder.
- VS Code settings placeholder.

### Notes

Initial docs were placeholders and later expanded during Sprint 0B.

---

## 2026-07-07 - Sprint 0B started

### Added

- Decision to complete documentation before moving to new chat or Codex.
- Decision to create full Markdown knowledge base.
- Decision to make repository self-explanatory.

### Changed

- Documentation quality bar increased from placeholder to substantial.

---

# Important project changes by category

## Architecture

### Added

- AI/renderer separation.
- JSON timeline contract.
- Modular pipeline.
- Intermediate JSON files.
- Renderer determinism.
- Exporter separation.

### Changed

- Reframed project as AI Video Engine.

---

## AI

### Added

- Faster Whisper planned for STT.
- Ollama planned for local LLM runtime.
- Qwen 2.5 3B planned for Visual Director.
- Embedding model planned for icon search.
- JSON validation required after LLM output.

### Changed

- LLM no longer expected to know icon filenames.
- LLM returns icon_query instead.

---

## Renderer

### Added

- Deterministic renderer design.
- 9:16 default.
- Full-screen text scenes.
- Keyword highlight.
- Effect registry plan.
- Layout registry plan.
- Template system plan.

### Changed

- Renderer is not subtitle renderer.
- Renderer is kinetic text renderer.

---

## Assets

### Added

- Icon DB design.
- Font DB design.
- Avatar DB design.
- Background DB design.
- SFX DB design.
- Asset metadata rules.
- Asset validation rules.
- Licensing rules.

---

## Prompts

### Added

- Prompt files under `prompts/`.
- Visual Director prompt design.
- JSON repair prompt design.
- Prompt versioning.
- Prompt testing guidance.

---

## Documentation

### Added

- Full documentation architecture.
- DecisionLog.
- Sprint docs.
- Glossary.
- Coding standard.
- Roadmap.
- Project vision.

---

# Breaking change log

No runtime breaking changes yet.

Potential future breaking changes:

- moving source layout to `src/ai_video_engine/`
- changing JSON schema fields
- changing timeline file names
- changing template schema
- changing renderer backend
- changing prompt output schema

All future breaking changes must be recorded here and in `docs/DecisionLog.md`.

---

# Migration notes

## Possible migration: source layout

Current bootstrap may contain direct folders:

```text
src/audio/
src/speech/
...
```

Recommended future layout:

```text
src/ai_video_engine/audio/
src/ai_video_engine/speech/
...
```

This should be decided before substantial Sprint 1 code.

If migration happens, update:

```text
pyproject.toml
tests
imports
docs
DecisionLog
```

---

# Changelog maintenance rules

## Rule 1

Update changelog before or during meaningful commits.

## Rule 2

Do not record every typo.

## Rule 3

Record schema changes.

## Rule 4

Record prompt behavior changes.

## Rule 5

Record dependency changes.

## Rule 6

Record renderer behavior changes.

## Rule 7

Record breaking changes clearly.

## Rule 8

Record known issues for incomplete releases.

## Rule 9

Keep Unreleased section current.

## Rule 10

Move Unreleased items into version section when releasing.

---

# Release checklist template

Use this template for future release notes.

```markdown
## [x.y.z] - YYYY-MM-DD

### Added

- ...

### Changed

- ...

### Fixed

- ...

### Removed

- ...

### Breaking

- ...

### Docs

- ...

### Known Issues

- ...

### Migration

- ...
```

---

# Sprint changelog template

Use this template for sprint completion.

```markdown
## Sprint N - Sprint Name

### Goal

...

### Added

- ...

### Changed

- ...

### Fixed

- ...

### Tests

- ...

### Docs

- ...

### Output

- ...

### Known Issues

- ...

### Next

- ...
```

---

# Dependency changelog template

Use this template when adding dependencies.

```markdown
## Dependency change - Package name

Date:

### Added

- Package:

### Reason

- ...

### Alternatives considered

- ...

### Impact

- ...

### Follow-up

- ...
```

---

# Prompt changelog template

Use this template when changing prompt behavior.

```markdown
## Prompt change - Prompt name vX.Y.Z

Date:

### Changed

- ...

### Reason

- ...

### Schema impact

- ...

### Validation impact

- ...

### Known risk

- ...
```

---

# Schema changelog template

Use this template when changing JSON schema.

```markdown
## Schema change - Schema name vX.Y.Z

Date:

### Added

- ...

### Changed

- ...

### Removed

- ...

### Breaking

- ...

### Migration

- ...
```

---

# Renderer changelog template

Use this template when changing renderer.

```markdown
## Renderer change - Feature

Date:

### Added

- ...

### Changed

- ...

### Visual impact

- ...

### Performance impact

- ...

### Compatibility

- ...
```

---

# AI model changelog template

Use this template when changing models.

```markdown
## AI model change - Task

Date:

### Previous model

...

### New model

...

### Reason

...

### Impact

...

### Validation

...
```

---

# Asset changelog template

Use this template when changing asset systems.

```markdown
## Asset change - Asset category

Date:

### Added

- ...

### Changed

- ...

### Removed

- ...

### Licensing impact

- ...

### Renderer impact

- ...
```

---

# Current next changelog entry expected

After Sprint 0B docs are committed, add an entry under Unreleased:

```markdown
### Added

- Completed Sprint 0B project knowledge base.

### Docs

- Added full documentation set for architecture, pipeline, JSON schema, AI, renderer, assets, prompts, coding standards, roadmap, glossary, and sprint planning.
```

After Sprint 1 begins, update Unreleased with actual code changes.

---

# Appendix A - Initial documentation file inventory

Current documentation set:

| File | Purpose | Status |
|---|---|---|
| `AGENTS.md` | AI agent instructions | created |
| `PROJECT_RULES.md` | mandatory project rules | created |
| `README.md` | project overview | created |
| `ROADMAP.md` | sprint roadmap | created |
| `CHANGELOG.md` | change history | current |
| `docs/ProjectVision.md` | product vision | created |
| `docs/Architecture.md` | architecture | created |
| `docs/Pipeline.md` | pipeline design | created |
| `docs/JSONSchema.md` | JSON contracts | created |
| `docs/RendererDesign.md` | renderer design | created |
| `docs/AIDesign.md` | AI design | created |
| `docs/PromptGuide.md` | prompt design | created |
| `docs/AssetGuide.md` | asset design | created |
| `docs/CodingStandard.md` | coding standard | created |
| `docs/DecisionLog.md` | decision history | created |
| `docs/Sprint0.md` | Sprint 0 record | created |
| `docs/Sprint1.md` | Sprint 1 plan | created |
| `docs/Glossary.md` | terminology | created |

---

# Appendix B - Current implementation status

| Component | Status |
|---|---|
| Repository | created |
| GitHub remote | created |
| Initial push | completed |
| Documentation | in progress/completing |
| Audio extraction | not implemented |
| Speech-to-text | not implemented |
| Timeline analyzer | not implemented |
| Visual Director | not implemented |
| Icon selector | not implemented |
| Renderer | not implemented |
| Exporter | not implemented |
| CLI | not implemented |
| UI | not implemented |

---

# Appendix C - Planned Sprint 1 implementation sequence

1. Finalize package layout.
2. Update pyproject.
3. Add common errors.
4. Add JSON IO helpers.
5. Add FFmpeg command builder.
6. Add audio extractor.
7. Add transcript schema.
8. Add Faster Whisper transcriber.
9. Add transcribe script.
10. Add tests.
11. Test on real video.
12. Update changelog.
13. Commit and push.

---

# Appendix D - Changelog final note

This changelog should remain practical.

It should help future maintainers quickly understand the evolution of AI Video Engine.

When in doubt, record meaningful project changes here.

---

# Appendix E - Planned release table

| Version | Focus | Status |
|---|---|---|
| `0.1.0-foundation` | Project foundation and documentation | Planned |
| `0.2.0-transcription` | Speech-to-text pipeline | Planned |
| `0.3.0-timeline` | Timeline analyzer | Planned |
| `0.4.0-director` | Visual Director AI | Planned |
| `0.5.0-icon-selector` | Embedding icon selector | Planned |
| `0.6.0-renderer` | Basic renderer | Planned |
| `0.7.0-exporter` | Final MP4 exporter | Planned |
| `0.8.0-template-system` | Template system | Planned |
| `0.9.0-beta` | End-to-end beta | Planned |
| `1.0.0` | First stable local engine | Planned |

---

# Appendix F - Change categories reference

| Category | Meaning |
|---|---|
| `Added` | New features, files, modules, docs, or capabilities. |
| `Changed` | Changes in behavior, structure, defaults, or workflow. |
| `Deprecated` | Features that still exist but should not be used. |
| `Removed` | Deleted features, files, or dependencies. |
| `Fixed` | Bug fixes. |
| `Security` | Privacy/security-related changes. |
| `Docs` | Documentation-only changes. |
| `Internal` | Internal refactors or development workflow changes. |
| `Breaking` | Changes that require migration or can break existing usage. |
| `Known Issues` | Known limitations at release time. |
| `Next` | Immediate next actions. |

---

# Appendix G - Sprint-to-version mapping

| Sprint | Target version |
|---|---|
| Sprint 0A/0B | `v0.1.0-foundation` |
| Sprint 1 | `v0.2.0-transcription` |
| Sprint 2 | `v0.3.0-timeline` |
| Sprint 3 | `v0.4.0-director` |
| Sprint 4 | `v0.5.0-icon-selector` |
| Sprint 5 | `v0.6.0-renderer` |
| Sprint 6 | `v0.7.0-exporter` |
| Sprint 8 | `v0.8.0-template-system` |
| Sprint 10 | `v0.9.0-beta / v1.0.0-alpha` |

---

# Appendix H - First release checklist

1. All Sprint 0B docs committed.
2. GitHub repository clean.
3. README status updated.
4. DecisionLog populated.
5. Roadmap current.
6. Sprint1.md ready.
7. Changelog updated.
8. No generated output committed.
9. No secrets committed.
10. Next GitHub issue created.
