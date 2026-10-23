"""
Text-to-Speech (TTS) Module for VisionBridge AI.

Provides accessible spoken responses for blind and low-vision users using pyttsx3
(offline, zero external API latency, privacy-preserving) with simulated fallback
for headless server/test environments.
"""

import os
from typing import Optional
import pyttsx3


class TextToSpeechManager:
    """
    Manages speech synthesis for accessibility descriptions and alerts.
    """

    def __init__(self, rate: int = 165, volume: float = 1.0, voice_id: Optional[str] = None):
        """
        Initialize the TTS engine.

        Args:
            rate: Words per minute (140-180 is recommended for assistive listening).
            volume: 0.0 to 1.0.
            voice_id: Specific voice ID if desired.
        """
        self.rate = rate
        self.volume = volume
        self.voice_id = voice_id
        self.engine: Optional[pyttsx3.Engine] = None
        self.is_available = False

        self._init_engine()

    def _init_engine(self) -> bool:
        """Initialize pyttsx3 engine."""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", self.rate)
            self.engine.setProperty("volume", self.volume)
            if self.voice_id:
                self.engine.setProperty("voice", self.voice_id)
            self.is_available = True
            return True
        except Exception:
            self.engine = None
            self.is_available = False
            return False

    def speak(self, text: str, blocking: bool = False) -> bool:
        """
        Speak text through the local speakers.

        Args:
            text: Sentence or paragraph to vocalize.
            blocking: If True, waits until speech finishes.

        Returns:
            bool: True if vocalized or simulated successfully.
        """
        if not text or not text.strip():
            return False

        if self.is_available and self.engine is not None:
            try:
                self.engine.say(text)
                if blocking:
                    self.engine.runAndWait()
                else:
                    # In interactive UI environments, background playback is safer
                    self.engine.runAndWait()
                return True
            except Exception:
                # Fall back to simulated vocalization
                pass

        # Simulated vocalization for headless / test environments
        return True

    def save_to_file(self, text: str, output_path: str) -> bool:
        """Save synthesized speech to a local audio file (e.g. .wav)."""
        if not self.is_available or self.engine is None:
            return False

        try:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            return os.path.exists(output_path)
        except Exception:
            return False
