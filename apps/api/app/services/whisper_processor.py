"""Whisper API processor for transcription and filler word detection."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Optional

from openai import OpenAI

from app.config import get_settings
from app.services.vad_processor import Segment, get_vad_processor

settings = get_settings()


@dataclass
class FillerWord:
    """Represents a detected filler word."""

    word: str
    start_ms: int
    end_ms: int
    confidence: float


@dataclass
class WhisperSegment(Segment):
    """Extended segment with transcription data."""

    text: Optional[str] = None
    filler_word: Optional[str] = None


class WhisperProcessor:
    """Processor for OpenAI Whisper API transcription and filler detection."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        detect_filler_words: bool = True,
        filler_words: Optional[List[str]] = None,
        filler_word_padding_ms: int = 100,
    ):
        """
        Initialize Whisper processor.

        Args:
            api_key: OpenAI API key
            detect_filler_words: Whether to detect filler words
            filler_words: List of filler words to detect
            filler_word_padding_ms: Padding around detected filler words
        """
        self.api_key = api_key or settings.openai_api_key
        self.detect_filler_words = detect_filler_words
        self.filler_words = filler_words or settings.filler_words_list
        self.filler_word_padding_ms = filler_word_padding_ms

        if not self.api_key:
            raise ValueError("OpenAI API key is required for Whisper processing")

        self.client = OpenAI(api_key=self.api_key)

    def process_audio(
        self,
        audio_path: Path,
        vad_aggressiveness: int = 3,
        min_silence_duration_ms: int = 300,
        min_speech_duration_ms: int = 250,
    ) -> tuple[List[WhisperSegment], str, List[FillerWord]]:
        """
        Process audio file with Whisper API and VAD.

        Args:
            audio_path: Path to audio file
            vad_aggressiveness: VAD aggressiveness level
            min_silence_duration_ms: Minimum silence duration
            min_speech_duration_ms: Minimum speech duration

        Returns:
            Tuple of (segments, full_transcription, filler_words)
        """
        # Get transcription from Whisper API
        transcription_data = self._transcribe(audio_path)

        # Run VAD in parallel for silence detection
        vad = get_vad_processor(
            aggressiveness=vad_aggressiveness,
            min_silence_duration_ms=min_silence_duration_ms,
            min_speech_duration_ms=min_speech_duration_ms,
        )
        vad_segments = vad.process_audio(audio_path)

        # Detect filler words
        filler_words = []
        if self.detect_filler_words:
            filler_words = self._detect_filler_words(transcription_data)

        # Merge VAD segments with transcription
        segments = self._merge_segments(
            vad_segments,
            transcription_data,
            filler_words,
        )

        # Get full transcription text
        full_text = transcription_data.get("text", "")

        return segments, full_text, filler_words

    def _transcribe(self, audio_path: Path) -> dict:
        """Transcribe audio using Whisper API."""
        with open(audio_path, "rb") as audio_file:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["word", "segment"],
            )

        return response.model_dump()

    def _detect_filler_words(self, transcription_data: dict) -> List[FillerWord]:
        """Detect filler words in transcription."""
        filler_words = []
        words = transcription_data.get("words", [])

        for word_data in words:
            word = word_data.get("word", "").lower().strip()

            # Check single word fillers
            if word in self.filler_words:
                filler_words.append(
                    FillerWord(
                        word=word,
                        start_ms=int(word_data.get("start", 0) * 1000),
                        end_ms=int(word_data.get("end", 0) * 1000),
                        confidence=0.9,
                    )
                )

        # Check multi-word fillers (e.g., "you know", "I mean")
        multi_word_fillers = [f for f in self.filler_words if " " in f]
        if multi_word_fillers and words:
            text_lower = transcription_data.get("text", "").lower()
            for filler in multi_word_fillers:
                if filler in text_lower:
                    # Find approximate position
                    filler_words_list = filler.split()
                    for i, word_data in enumerate(words):
                        if (
                            word_data.get("word", "").lower().strip()
                            == filler_words_list[0]
                        ):
                            # Check if subsequent words match
                            matches = True
                            for j, fw in enumerate(filler_words_list[1:], 1):
                                if i + j >= len(words):
                                    matches = False
                                    break
                                if words[i + j].get("word", "").lower().strip() != fw:
                                    matches = False
                                    break

                            if matches:
                                end_idx = i + len(filler_words_list) - 1
                                filler_words.append(
                                    FillerWord(
                                        word=filler,
                                        start_ms=int(word_data.get("start", 0) * 1000),
                                        end_ms=int(words[end_idx].get("end", 0) * 1000),
                                        confidence=0.85,
                                    )
                                )

        return filler_words

    def _merge_segments(
        self,
        vad_segments: List[Segment],
        transcription_data: dict,
        filler_words: List[FillerWord],
    ) -> List[WhisperSegment]:
        """Merge VAD segments with transcription and filler word data."""
        segments = []
        whisper_segments = transcription_data.get("segments", [])

        for vad_seg in vad_segments:
            if vad_seg.type == "silence":
                segments.append(
                    WhisperSegment(
                        start_ms=vad_seg.start_ms,
                        end_ms=vad_seg.end_ms,
                        type="silence",
                        confidence=vad_seg.confidence,
                    )
                )
            else:
                # Find matching transcription text
                text = self._get_text_for_segment(
                    vad_seg.start_ms,
                    vad_seg.end_ms,
                    whisper_segments,
                )

                # Check if this segment contains filler words
                segment_fillers = [
                    fw
                    for fw in filler_words
                    if fw.start_ms >= vad_seg.start_ms and fw.end_ms <= vad_seg.end_ms
                ]

                if segment_fillers:
                    # Split segment around filler words
                    current_start = vad_seg.start_ms

                    for filler in sorted(segment_fillers, key=lambda x: x.start_ms):
                        # Add speech before filler
                        if filler.start_ms > current_start:
                            segments.append(
                                WhisperSegment(
                                    start_ms=current_start,
                                    end_ms=filler.start_ms - self.filler_word_padding_ms,
                                    type="speech",
                                    confidence=vad_seg.confidence,
                                    text=self._get_text_for_segment(
                                        current_start,
                                        filler.start_ms,
                                        whisper_segments,
                                    ),
                                )
                            )

                        # Add filler segment
                        segments.append(
                            WhisperSegment(
                                start_ms=max(
                                    0, filler.start_ms - self.filler_word_padding_ms
                                ),
                                end_ms=filler.end_ms + self.filler_word_padding_ms,
                                type="filler",
                                confidence=filler.confidence,
                                text=filler.word,
                                filler_word=filler.word,
                            )
                        )

                        current_start = filler.end_ms + self.filler_word_padding_ms

                    # Add remaining speech after last filler
                    if current_start < vad_seg.end_ms:
                        segments.append(
                            WhisperSegment(
                                start_ms=current_start,
                                end_ms=vad_seg.end_ms,
                                type="speech",
                                confidence=vad_seg.confidence,
                                text=self._get_text_for_segment(
                                    current_start,
                                    vad_seg.end_ms,
                                    whisper_segments,
                                ),
                            )
                        )
                else:
                    segments.append(
                        WhisperSegment(
                            start_ms=vad_seg.start_ms,
                            end_ms=vad_seg.end_ms,
                            type="speech",
                            confidence=vad_seg.confidence,
                            text=text,
                        )
                    )

        return segments

    def _get_text_for_segment(
        self,
        start_ms: int,
        end_ms: int,
        whisper_segments: List[dict],
    ) -> str:
        """Get transcription text for a time range."""
        texts = []
        for seg in whisper_segments:
            seg_start = int(seg.get("start", 0) * 1000)
            seg_end = int(seg.get("end", 0) * 1000)

            # Check for overlap
            if seg_start < end_ms and seg_end > start_ms:
                texts.append(seg.get("text", "").strip())

        return " ".join(texts)


def get_whisper_processor(
    detect_filler_words: Optional[bool] = None,
    custom_filler_words: Optional[List[str]] = None,
) -> WhisperProcessor:
    """Get Whisper processor instance."""
    if not settings.ai_features_enabled or not settings.whisper_api_enabled:
        raise ValueError("Whisper API is not enabled")

    filler_words = settings.filler_words_list
    if custom_filler_words:
        filler_words = list(set(filler_words + custom_filler_words))

    return WhisperProcessor(
        detect_filler_words=detect_filler_words
        if detect_filler_words is not None
        else settings.detect_filler_words,
        filler_words=filler_words,
        filler_word_padding_ms=settings.filler_word_padding_ms,
    )
