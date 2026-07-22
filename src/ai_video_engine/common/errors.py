"""Project-specific exceptions for AI Video Engine."""


class AIVideoEngineError(Exception):
    """Base error for AI Video Engine."""


class InputFileError(AIVideoEngineError):
    """Raised when an input media file is invalid."""


class MissingFFmpegError(AIVideoEngineError):
    """Raised when FFmpeg is not available."""


class AudioExtractionError(AIVideoEngineError):
    """Raised when audio extraction fails."""


class SpeechToTextError(AIVideoEngineError):
    """Raised when speech-to-text fails."""


class InvalidTranscriptError(AIVideoEngineError):
    """Raised when transcript validation fails."""