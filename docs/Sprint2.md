@'
# AI Video Engine - Sprint 2: Timeline Analyzer

## 0. Purpose

Sprint 2 converts a validated transcript into a normalized renderable timeline.

Input:

```text
output/transcript.json

Output:

output/timeline.normalized.json

Sprint 2 is deterministic.

It does not use LLM.
It does not select keywords.
It does not select icons.
It does not render video.

1. Sprint 2 summary

Sprint name:

Timeline Analyzer

Main command:

python scripts/analyze_timeline.py output/transcript.json

Main output:

output/timeline.normalized.json

Main modules:

src/ai_video_engine/timeline/schema.py
src/ai_video_engine/timeline/analyzer.py
scripts/analyze_timeline.py
2. Pipeline
output/transcript.json
â†“
Load transcript JSON
â†“
Validate transcript schema
â†“
Clean transcript text
â†“
Merge short segments
â†“
Split long segments
â†“
Generate scene IDs
â†“
Validate normalized timeline
â†“
output/timeline.normalized.json
3. Normalized timeline schema

Example:

{
  "schema_version": "0.1.0",
  "metadata": {
    "source": "timeline_analyzer",
    "source_schema_version": "0.1.0"
  },
  "scenes": [
    {
      "id": "scene_0001",
      "source_segment_ids": ["seg_0001"],
      "start": 0.0,
      "end": 3.14,
      "duration": 3.14,
      "speaker": {
        "id": "SPEAKER_00",
        "source": "unknown"
      },
      "text": "Xin chÃ o Viá»‡t Nam."
    }
  ]
}
4. Implemented behavior

Sprint 2 currently supports:

Loading transcript.json
Validating transcript data with Pydantic
Normalizing whitespace
Preserving Vietnamese UTF-8 text
Creating deterministic scene IDs
Preserving source_segment_ids
Preserving scene timing
Computing scene duration
Adding speaker placeholder data
Merging very short adjacent segments
Splitting long segments by duration
Splitting long segments by text length
Writing formatted UTF-8 JSON
CLI execution through scripts/analyze_timeline.py
5. Validation

Validated with:

python -m pytest -q

Current result:

50 passed

Manual test:

python scripts/analyze_timeline.py output/transcript.json

Manual output:

[timeline] analyzing output/transcript.json
[timeline] scenes: 11
[timeline] wrote output/timeline.normalized.json
6. Definition of Done

Sprint 2 is done when:

output/transcript.json can be read.
Invalid transcript data fails clearly.
output/timeline.normalized.json is created.
Every scene has id, source_segment_ids, start, end, duration, speaker, and text.
Scene IDs are deterministic.
Scene timing is valid.
Vietnamese text is preserved.
Short segments are handled.
Long segments are handled.
Unit tests pass.
No LLM is called.
No renderer code is added.
7. Next sprint

After Sprint 2:

Sprint 3 - Visual Director

'@ | Set-Content docs\Sprint2.md -Encoding UTF8
