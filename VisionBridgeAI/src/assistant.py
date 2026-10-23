"""
Central Assistant Orchestrator for VisionBridge AI.

Inspired by Jarvis, unites OpenCV 5 vision, object detection, OCR, text-to-speech,
audio captions, sound event alerts, privacy indicators, and AWS integration.
"""

from typing import Dict, Any, Optional
import numpy as np

from .camera import CameraManager
from .vision import VisionPipeline
from .object_detection import ObjectDetector, SceneDescriber
from .ocr import OCREngine
from .text_to_speech import TextToSpeechManager
from .speech_to_text import AudioAccessibilityManager, CommandIntent
from .aws_service import AWSAccessibilityService, PrivacyConsentError


class VisionBridgeAssistant:
    """
    Main controller for VisionBridge AI accessibility assistant.
    """

    def __init__(
        self,
        camera_index: int = 0,
        enable_tts: bool = True,
        speech_rate: int = 165,
        confidence_threshold: float = 0.50,
        uncertainty_threshold: float = 0.35,
    ):
        self.camera = CameraManager(camera_index=camera_index)
        self.vision = VisionPipeline()
        self.detector = ObjectDetector(
            confidence_threshold=confidence_threshold,
            uncertainty_threshold=uncertainty_threshold,
        )
        self.ocr = OCREngine()
        self.tts = TextToSpeechManager(rate=speech_rate) if enable_tts else None
        self.audio = AudioAccessibilityManager()
        self.aws = AWSAccessibilityService()

        self.enable_tts = enable_tts
        self.user_cloud_consent = False

    def start_camera(self) -> bool:
        """Activate camera stream or synthetic fallback."""
        success = self.camera.start()
        if success:
            self.audio.add_caption("Camera stream initiated.", source="System")
        return success

    def stop_camera(self) -> None:
        """Deactivate camera stream."""
        self.camera.stop()
        self.audio.add_caption("Camera stream stopped.", source="System")

    def get_current_frame(self) -> Optional[np.ndarray]:
        """Obtain latest frame from camera."""
        ret, frame = self.camera.get_frame()
        return frame if ret else None

    def describe_surroundings(self, frame: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Synthesize scene understanding:
        1. Grab frame.
        2. Evaluate blur and lighting quality.
        3. Detect objects and map spatial positions.
        4. Generate Jarvis-style spoken description.
        5. Provide captions and uncertainty warnings.
        """
        if frame is None:
            frame = self.get_current_frame()
            if frame is None:
                err_msg = "Camera is not currently active. Please start camera first."
                self.audio.add_caption(err_msg, source="System")
                return {"error": err_msg}

        # Quality check
        quality = self.vision.assess_frame(frame)

        # Object detection
        det_res = self.detector.detect(frame)
        confirmed = det_res["confirmed_detections"]
        uncertain = det_res["uncertain_detections"]

        # Scene description
        desc_res = SceneDescriber.generate_description(
            confirmed, uncertain, quality_advisories=quality["advisories"]
        )

        spoken_script = desc_res["spoken_script"]
        self.audio.add_caption(spoken_script, source="Jarvis")

        if self.enable_tts and self.tts:
            self.tts.speak(spoken_script)

        # Generate annotated frame
        annotated_frame = self.vision.draw_accessible_annotations(
            frame, confirmed + uncertain, show_labels=True
        )

        return {
            "speech_text": spoken_script,
            "quality": quality,
            "confirmed_detections": confirmed,
            "uncertain_detections": uncertain,
            "annotated_frame": annotated_frame,
            "latency_ms": det_res["inference_ms"],
            "safety_note": desc_res["safety_note"],
        }

    def read_text(self, frame: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Read text from signs, labels, or documents using OpenCV 5 + OCR.
        """
        if frame is None:
            frame = self.get_current_frame()
            if frame is None:
                err_msg = "Camera is not active. Please start camera first."
                self.audio.add_caption(err_msg, source="System")
                return {"error": err_msg}

        quality = self.vision.assess_frame(frame)
        ocr_res = self.ocr.extract_text(frame)

        spoken_script = ocr_res["spoken_script"]
        self.audio.add_caption(spoken_script, source="Jarvis (Reading)")

        if self.enable_tts and self.tts:
            self.tts.speak(spoken_script)

        return {
            "text": ocr_res["text"],
            "speech_text": spoken_script,
            "confidence": ocr_res["confidence"],
            "skew_angle": ocr_res["skew_angle"],
            "quality": quality,
            "engine": ocr_res["engine"],
        }

    def process_command(self, command_text: str) -> Dict[str, Any]:
        """
        Process user request (spoken or typed).
        """
        self.audio.add_caption(command_text, source="User")
        parsed = self.audio.parse_command(command_text)
        intent = parsed["intent"]

        if intent == CommandIntent.DESCRIBE_SURROUNDINGS:
            return self.describe_surroundings()
        elif intent == CommandIntent.READ_TEXT:
            return self.read_text()
        elif intent == CommandIntent.DETECT_OBJECTS:
            return self.describe_surroundings()
        elif intent == CommandIntent.SYSTEM_STATUS:
            frame = self.get_current_frame()
            if frame is not None:
                q = self.vision.assess_frame(frame)
                msg = f"System operational. Blur score: {q['blur_score']}, Mean lighting: {q['mean_brightness']}."
            else:
                msg = "System operational. Camera currently paused."
            self.audio.add_caption(msg, source="Jarvis")
            if self.enable_tts and self.tts:
                self.tts.speak(msg)
            return {"status_message": msg}
        elif intent == CommandIntent.HELP:
            help_msg = (
                "Commands available: 'Describe my surroundings', 'Read this text', "
                "'What objects can you see?', or 'Status'. Press keyboard shortcuts: "
                "C to toggle camera, D to describe, R to read text."
            )
            self.audio.add_caption(help_msg, source="Jarvis")
            if self.enable_tts and self.tts:
                self.tts.speak(help_msg)
            return {"help_message": help_msg}
        else:
            fallback = "I heard you, but did not recognize that specific command. Try saying 'Describe surroundings' or 'Read text'."
            self.audio.add_caption(fallback, source="Jarvis")
            if self.enable_tts and self.tts:
                self.tts.speak(fallback)
            return {"unrecognized": True, "message": fallback}

    def detect_environmental_sound(self, sound_type: str, peak_db: float) -> Dict[str, Any]:
        """
        Acoustic alert for deaf and hard-of-hearing users.
        """
        result = self.audio.evaluate_environmental_sound(sound_type, peak_db)
        self.audio.add_caption(result["guidance_banner"], source="Sound Alert", visual_alert=result["status"])
        return result

    def request_cloud_analysis(self, frame: Optional[np.ndarray] = None, task: str = "scene_analysis") -> Dict[str, Any]:
        """
        Invoke AWS cloud component. Strictly requires user consent.
        """
        if frame is None:
            frame = self.get_current_frame()
            if frame is None:
                return {"error": "No active frame to transmit."}

        try:
            return self.aws.process_frame_cloud(
                frame, user_consented=self.user_cloud_consent, task=task
            )
        except PrivacyConsentError as e:
            err_msg = str(e)
            self.audio.add_caption(err_msg, source="Privacy Guard")
            return {"error": "PrivacyConsentError", "message": err_msg}
