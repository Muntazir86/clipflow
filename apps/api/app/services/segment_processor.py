"""Segment post-processing service."""

from dataclasses import asdict, dataclass
from typing import List, Literal, Optional

from app.config import get_settings

settings = get_settings()


@dataclass
class ProcessedSegment:
    """Represents a processed segment with classification."""

    start_ms: int
    end_ms: int
    type: Literal["speech", "silence", "filler"]
    confidence: float
    text: Optional[str] = None
    filler_word: Optional[str] = None
    classification: Literal["keep", "remove", "suggest_remove"] = "keep"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


class SegmentProcessor:
    """Service for post-processing detected segments."""

    def __init__(
        self,
        min_silence_duration_ms: int = 300,
        min_speech_duration_ms: int = 250,
        merge_threshold_ms: int = 100,
        speech_padding_ms: int = 50,
    ):
        """
        Initialize segment processor.

        Args:
            min_silence_duration_ms: Minimum silence duration to keep
            min_speech_duration_ms: Minimum speech duration to keep
            merge_threshold_ms: Merge segments closer than this
            speech_padding_ms: Padding to add around speech segments
        """
        self.min_silence_duration_ms = min_silence_duration_ms
        self.min_speech_duration_ms = min_speech_duration_ms
        self.merge_threshold_ms = merge_threshold_ms
        self.speech_padding_ms = speech_padding_ms

    def process_segments(
        self,
        segments: List[dict],
        total_duration_ms: Optional[int] = None,
    ) -> List[ProcessedSegment]:
        """
        Process and classify segments.

        Args:
            segments: List of segment dictionaries
            total_duration_ms: Total audio duration in milliseconds

        Returns:
            List of processed segments with classifications
        """
        if not segments:
            return []

        # Convert to ProcessedSegment objects
        processed = [
            ProcessedSegment(
                start_ms=s.get("start_ms", 0),
                end_ms=s.get("end_ms", 0),
                type=s.get("type", "speech"),
                confidence=s.get("confidence", 0.0),
                text=s.get("text"),
                filler_word=s.get("filler_word"),
            )
            for s in segments
        ]

        # Apply minimum duration filters
        processed = self._apply_duration_filters(processed)

        # Merge close segments
        processed = self._merge_close_segments(processed)

        # Add padding to speech segments
        processed = self._add_padding(processed, total_duration_ms)

        # Classify segments
        processed = self._classify_segments(processed)

        return processed

    def _apply_duration_filters(
        self,
        segments: List[ProcessedSegment],
    ) -> List[ProcessedSegment]:
        """Filter out segments that don't meet minimum duration."""
        filtered = []

        for seg in segments:
            duration = seg.end_ms - seg.start_ms

            if seg.type == "silence" and duration < self.min_silence_duration_ms:
                continue
            if seg.type == "speech" and duration < self.min_speech_duration_ms:
                continue

            filtered.append(seg)

        return filtered

    def _merge_close_segments(
        self,
        segments: List[ProcessedSegment],
    ) -> List[ProcessedSegment]:
        """Merge segments of the same type that are close together."""
        if len(segments) < 2:
            return segments

        # Sort by start time
        sorted_segments = sorted(segments, key=lambda x: x.start_ms)
        merged = [sorted_segments[0]]

        for current in sorted_segments[1:]:
            previous = merged[-1]

            # Check if same type and close enough to merge
            if (
                current.type == previous.type
                and current.start_ms - previous.end_ms <= self.merge_threshold_ms
            ):
                # Merge segments
                merged[-1] = ProcessedSegment(
                    start_ms=previous.start_ms,
                    end_ms=current.end_ms,
                    type=previous.type,
                    confidence=(previous.confidence + current.confidence) / 2,
                    text=(
                        f"{previous.text or ''} {current.text or ''}".strip()
                        if previous.text or current.text
                        else None
                    ),
                    filler_word=previous.filler_word or current.filler_word,
                )
            else:
                merged.append(current)

        return merged

    def _add_padding(
        self,
        segments: List[ProcessedSegment],
        total_duration_ms: Optional[int] = None,
    ) -> List[ProcessedSegment]:
        """Add padding around speech segments."""
        if not segments:
            return segments

        padded = []

        for i, seg in enumerate(segments):
            if seg.type == "speech":
                # Calculate padded boundaries
                new_start = max(0, seg.start_ms - self.speech_padding_ms)
                new_end = seg.end_ms + self.speech_padding_ms

                # Constrain to total duration if provided
                if total_duration_ms:
                    new_end = min(new_end, total_duration_ms)

                # Avoid overlap with previous segment
                if padded and new_start < padded[-1].end_ms:
                    new_start = padded[-1].end_ms

                padded.append(
                    ProcessedSegment(
                        start_ms=new_start,
                        end_ms=new_end,
                        type=seg.type,
                        confidence=seg.confidence,
                        text=seg.text,
                        filler_word=seg.filler_word,
                    )
                )
            else:
                # Adjust silence/filler to not overlap with padded speech
                if padded and seg.start_ms < padded[-1].end_ms:
                    seg = ProcessedSegment(
                        start_ms=padded[-1].end_ms,
                        end_ms=seg.end_ms,
                        type=seg.type,
                        confidence=seg.confidence,
                        text=seg.text,
                        filler_word=seg.filler_word,
                    )

                if seg.end_ms > seg.start_ms:
                    padded.append(seg)

        return padded

    def _classify_segments(
        self,
        segments: List[ProcessedSegment],
    ) -> List[ProcessedSegment]:
        """Classify segments as keep, remove, or suggest_remove."""
        classified = []

        for seg in segments:
            if seg.type == "speech":
                classification = "keep"
            elif seg.type == "silence":
                classification = "remove"
            elif seg.type == "filler":
                classification = "suggest_remove"
            else:
                classification = "keep"

            classified.append(
                ProcessedSegment(
                    start_ms=seg.start_ms,
                    end_ms=seg.end_ms,
                    type=seg.type,
                    confidence=seg.confidence,
                    text=seg.text,
                    filler_word=seg.filler_word,
                    classification=classification,
                )
            )

        return classified

    def generate_edl(
        self,
        segments: List[ProcessedSegment],
        fps: float = 30.0,
    ) -> str:
        """
        Generate Edit Decision List (EDL) format output.

        Args:
            segments: List of processed segments
            fps: Frames per second for timecode conversion

        Returns:
            EDL formatted string
        """
        lines = ["TITLE: ClipFlow Export", "FCM: NON-DROP FRAME", ""]

        edit_num = 1
        for seg in segments:
            if seg.classification == "keep":
                # Convert milliseconds to timecode
                start_tc = self._ms_to_timecode(seg.start_ms, fps)
                end_tc = self._ms_to_timecode(seg.end_ms, fps)

                line = f"{edit_num:03d}  001      V     C        {start_tc} {end_tc} {start_tc} {end_tc}"
                lines.append(line)
                edit_num += 1

        return "\n".join(lines)

    def _ms_to_timecode(self, ms: int, fps: float) -> str:
        """Convert milliseconds to timecode format (HH:MM:SS:FF)."""
        total_seconds = ms / 1000
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        frames = int((total_seconds % 1) * fps)

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frames:02d}"


def get_segment_processor(
    min_silence_duration_ms: Optional[int] = None,
    min_speech_duration_ms: Optional[int] = None,
) -> SegmentProcessor:
    """Get segment processor instance."""
    return SegmentProcessor(
        min_silence_duration_ms=min_silence_duration_ms
        or settings.min_silence_duration_ms,
        min_speech_duration_ms=min_speech_duration_ms or settings.min_speech_duration_ms,
    )
