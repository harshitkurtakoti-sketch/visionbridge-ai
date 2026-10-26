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
from .sign_language import SignLanguageTranslator


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
        self.sign_translator = SignLanguageTranslator()

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

    def translate_sign_language(self, frame: Optional[np.ndarray] = None, hint: Optional[str] = None) -> Dict[str, Any]:
        """
        Translate American Sign Language (ASL) and hand gestures for deaf communication.
        Provides both visual captions and vocalized speech for hearing companions.
        """
        if frame is None:
            frame = self.get_current_frame()
            if frame is None:
                err_msg = "Camera is not active. Please start camera first for sign language recognition."
                self.audio.add_caption(err_msg, source="System")
                return {"error": err_msg}

        res = self.sign_translator.translate_frame(frame, synthetic_hint=hint)
        spoken_script = res["spoken_translation"]

        self.audio.add_caption(
            f"{res['icon']} Sign: {res['meaning']} - Saying: \"{res['accumulated_sentence']}\"",
            source="Deaf Assist (Sign Language)",
        )

        if self.enable_tts and self.tts:
            self.tts.speak(spoken_script)

        res["speech_text"] = spoken_script
        return res

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
        elif intent == CommandIntent.TRANSLATE_SIGN_LANGUAGE:
            return self.translate_sign_language()
        elif intent == CommandIntent.START_CAMERA:
            self.start_camera()
            msg = "Visual sensor array online and streaming, sir."
            self.audio.add_caption(msg, source="Jarvis")
            if self.enable_tts and self.tts:
                self.tts.speak(msg)
            return {"action": "start_camera", "speech_text": msg, "status_message": msg}
        elif intent == CommandIntent.STOP_CAMERA:
            self.stop_camera()
            msg = "Visual sensor array deactivated. System standby."
            self.audio.add_caption(msg, source="Jarvis")
            if self.enable_tts and self.tts:
                self.tts.speak(msg)
            return {"action": "stop_camera", "speech_text": msg, "status_message": msg}
        elif intent == CommandIntent.HAZARD_WARNING:
            frame = self.get_current_frame()
            if frame is not None:
                q = self.vision.assess_frame(frame)
                det = self.detector.detect(frame)
                hazards = [d for d in det["confirmed_detections"] if d.get("distance_estimate") == "immediate"]
                if hazards:
                    labels = ", ".join(h["label"] for h in hazards)
                    msg = f"Caution! Immediate proximity hazard detected: {labels}. Please proceed with vigilance."
                elif q["advisories"]:
                    msg = f"Warning: Visual environment degraded. {q['advisories'][0]}. Proceed with caution."
                else:
                    msg = "Diagnostic hazard scan completed. Forward path is clear. No immediate collision vectors detected."
            else:
                msg = "Acoustic and situational alert sensors are active. No active hazards reported in immediate sector."
            self.audio.add_caption(msg, source="Jarvis (Hazard Guard)")
            if self.enable_tts and self.tts:
                self.tts.speak(msg)
            return {"speech_text": msg, "status_message": msg, "hazard_checked": True}
        elif intent == CommandIntent.FIRE_ALARM:
            return self.detect_environmental_sound("fire_alarm", peak_db=88.5)
        elif intent == CommandIntent.DOOR_KNOCK:
            return self.detect_environmental_sound("door_knock", peak_db=62.0)
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
            return {"status_message": msg, "speech_text": msg}
        elif intent == CommandIntent.HELP:
            help_msg = (
                "Jarvis Voice commands: 'Describe surroundings', 'Read text', "
                "'Warn me of hazards', 'Check status', 'Fire alarm test', or 'Toggle camera'. "
                "Keyboard shortcuts: V for Voice, C for Camera, D for Describe, R for OCR."
            )
            self.audio.add_caption(help_msg, source="Jarvis")
            if self.enable_tts and self.tts:
                self.tts.speak(help_msg)
            return {"help_message": help_msg, "speech_text": help_msg}
        else:
            fallback = "I heard you, but did not recognize that specific command. Try saying 'Describe surroundings', 'Read text', or 'Warn me of hazards'."
            self.audio.add_caption(fallback, source="Jarvis")
            if self.enable_tts and self.tts:
                self.tts.speak(fallback)
            return {"unrecognized": True, "message": fallback, "speech_text": fallback}

    def detect_environmental_sound(self, sound_type: str, peak_db: float) -> Dict[str, Any]:
        """
        Acoustic alert for deaf and hard-of-hearing users with spoken warning voice.
        """
        result = self.audio.evaluate_environmental_sound(sound_type, peak_db)
        if result["is_confirmed"]:
            speech_text = f"Warning! High amplitude {sound_type.replace('_', ' ')} emergency signal confirmed at {result['amplitude_db']} decibels. Please verify immediate surroundings."
        else:
            speech_text = f"Notice. Acoustic activity candidate detected: {sound_type.replace('_', ' ')} at {result['amplitude_db']} decibels. Unconfirmed candidate."

        result["speech_text"] = speech_text
        self.audio.add_caption(result["guidance_banner"], source="Sound Alert", visual_alert=result["status"])

        if self.enable_tts and self.tts:
            self.tts.speak(speech_text)

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
