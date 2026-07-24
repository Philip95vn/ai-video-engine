"""Faster Whisper speech-to-text engine."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

from ai_video_engine.common.errors import SpeechToTextError
from ai_video_engine.speech.schema import (
    Transcript,
    TranscriptSegment,
    make_segment_id,
)


class FasterWhisperTranscriber:
    """Transcribe audio using Faster Whisper."""

    def __init__(
        self,
        model_name: str = "medium",
        device: str = "cpu",
        compute_type: str = "int8",
    ) -> None:
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self._model: Any | None = None

    def _load_model(self) -> Any:
        """Load and cache the Faster Whisper model."""
        if self._model is not None:
            return self._model

        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise SpeechToTextError(
                "faster-whisper is not installed. "
                "Install it with: pip install faster-whisper"
            ) from exc

        try:
            model = WhisperModel(
                self.model_name,
                device=self.device,
                compute_type=self.compute_type,
            )
        except Exception as exc:
            raise SpeechToTextError(
                f"Failed to load Faster Whisper model: {self.model_name}. "
                "Try a smaller model such as: small."
            ) from exc

        self._model = model
        return model

    def transcribe(
        self,
        audio_path: Path,
        language: str = "vi",
        vad_filter: bool = True,
        beam_size: int = 5,
        source_input: Path | str | None = None,
    ) -> Transcript:
        """Transcribe an audio file into a validated Transcript."""
        if not audio_path.is_file():
            raise SpeechToTextError(f"Audio file not found: {audio_path}")

        model = self._load_model()

        try:
            raw_segments, _ = model.transcribe(
                str(audio_path),
                language=language,
                vad_filter=vad_filter,
                beam_size=beam_size,
            )
            segments = self._convert_segments(raw_segments)
        except Exception as exc:
            raise SpeechToTextError(
                f"Failed to transcribe audio: {audio_path}"
            ) from exc

        metadata: dict[str, Any] = {
            "speech_provider": "faster_whisper",
            "speech_model": self.model_name,
            "language": language,
            "source_audio": str(audio_path),
            "device": self.device,
            "compute_type": self.compute_type,
        }

        if source_input is not None:
            metadata["source_input"] = str(source_input)

        return Transcript(
            metadata=metadata,
            segments=segments,
        )

    @staticmethod
    def _convert_segments(
        raw_segments: Iterable[Any],
    ) -> list[TranscriptSegment]:
        """Convert Faster Whisper segments into transcript segments."""
        segments: list[TranscriptSegment] = []

        for raw_segment in raw_segments:
            text = raw_segment.text.strip()

            if not text:
                continue

            start = round(float(raw_segment.start), 2)
            end = round(float(raw_segment.end), 2)
            duration = round(end - start, 2)

            segments.append(
                TranscriptSegment(
                    id=make_segment_id(len(segments) + 1),
                    start=start,
                    end=end,
                    duration=duration,
                    text=text,
                )
            )

        return segments