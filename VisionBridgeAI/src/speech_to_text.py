"""
Speech-to-Text and Audio Accessibility Module for VisionBridge AI.

Supports voice commands, text commands, live captions generation for deaf and
hard-of-hearing users, and environmental sound event detection with clear
distinction between detected sound candidates and confirmed events.
"""

from enum import Enum
from typing import Dict, Any, Optional, List
import re


class CommandIntent(str, Enum):
    DESCRIBE_SURROUNDINGS = "describe_surroundings"
    READ_TEXT = "read_text"
    DETECT_OBJECTS = "detect_objects"
    ENVIRONMENTAL_SOUND_ALERT = "sound_alert"
    SYSTEM_STATUS = "system_status"
    HELP = "help"
    UNKNOWN = "unknown"


class AudioAccessibilityManager:
    """
    Manages speech-to-text, command parsing, large-text captioning,
    and environmental sound notifications.
    """

    def __init__(self):
        self.captions_history: List[Dict[str, Any]] = []

    def parse_command(self, raw_input: str) -> Dict[str, Any]:
        """
        Parse spoken or typed natural language into structured assistant intent.

        Matches commands such as:
        - "Jarvis, describe my surroundings."
        - "Read this text."
        - "What objects can you see?"
        - "Describe the image."
        """
        text = raw_input.strip().lower()
        # Remove wake word if present
        text_clean = re.sub(r"^(hey\s+)?jarvis[,.]?\s*", "", text)

        intent = CommandIntent.UNKNOWN
        confidence = 0.5

        if any(phrase in text_clean for phrase in ["describe", "surroundings", "describe the image", "scene"]):
            intent = CommandIntent.DESCRIBE_SURROUNDINGS
            confidence = 0.95
        elif any(phrase in text_clean for phrase in ["read", "read text", "read this", "read sign", "ocr", "words"]):
            intent = CommandIntent.READ_TEXT
            confidence = 0.95
        elif any(phrase in text_clean for phrase in ["what objects", "objects", "detect objects", "can you see", "find"]):
            intent = CommandIntent.DETECT_OBJECTS
            confidence = 0.90
        elif any(phrase in text_clean for phrase in ["status", "quality", "lighting", "blur", "camera"]):
            intent = CommandIntent.SYSTEM_STATUS
            confidence = 0.85
        elif any(phrase in text_clean for phrase in ["help", "commands", "what can you do"]):
            intent = CommandIntent.HELP
            confidence = 0.95

        return {
            "raw_input": raw_input,
            "cleaned_input": text_clean,
            "intent": intent,
            "confidence": confidence,
        }

    def add_caption(self, text: str, source: str = "Assistant", visual_alert: Optional[str] = None) -> Dict[str, Any]:
        """
        Add a high-visibility caption entry for deaf and hard-of-hearing display.
        """
        entry = {
            "source": source,
            "text": text,
            "visual_alert": visual_alert,
            "timestamp": None,  # Can be populated at runtime
        }
        self.captions_history.append(entry)
        # Keep recent 50 entries
        if len(self.captions_history) > 50:
            self.captions_history.pop(0)
        return entry

    def evaluate_environmental_sound(self, sound_event_type: str, peak_db: float, threshold_db: float = 75.0) -> Dict[str, Any]:
        """
        Evaluate acoustic events (e.g. door knock, doorbell, fire alarm, siren, horn).
        Strictly distinguishes 'Unconfirmed Sound Candidate' from 'Confirmed Event'
        as mandated by competition accessibility guidelines.
        """
        is_above_threshold = peak_db >= threshold_db

        # Clear distinction between detected candidate vs confirmed event
        status = "CONFIRMED_EVENT" if is_above_threshold else "UNCONFIRMED_CANDIDATE"

        guidance = ""
        if status == "CONFIRMED_EVENT":
            guidance = f"ALERT: High-amplitude {sound_event_type.upper()} confirmed ({round(peak_db, 1)} dB). Check surroundings."
        else:
            guidance = f"Low-confidence acoustic activity detected ({sound_event_type.lower()}, {round(peak_db, 1)} dB). Not verified as confirmed emergency."

        return {
            "sound_type": sound_event_type,
            "amplitude_db": round(peak_db, 1),
            "status": status,
            "is_confirmed": is_above_threshold,
            "guidance_banner": guidance,
            "visual_indicator_color": "#FF2D55" if is_above_threshold else "#FFCC00",
        }
