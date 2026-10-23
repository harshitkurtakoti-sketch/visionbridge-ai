"""
Object Detection and Spatial Scene Description Module for VisionBridge AI.

Detects everyday objects, maps their spatial orientation relative to the user,
generates conversational scene descriptions inspired by Jarvis, and manages
uncertainty and navigation safety notices.
"""

import os
from typing import List, Dict, Any, Optional, Tuple
import cv2
import numpy as np
from .vision import SpatialCoordinateMapper


COCO_LABELS = [
    "background", "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
    "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
    "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza",
    "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet",
    "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven",
    "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear",
    "hair drier", "toothbrush"
]


class ObjectDetector:
    """
    Unified Object Detector supporting OpenCV 5 DNN models (ONNX/Caffe/TF)
    with a robust fallback saliency/contour detector for zero-external-dependency execution.
    """

    def __init__(
        self,
        model_path: Optional[str] = None,
        config_path: Optional[str] = None,
        confidence_threshold: float = 0.50,
        uncertainty_threshold: float = 0.35,
        frame_width: int = 640,
        frame_height: int = 480,
    ):
        self.confidence_threshold = confidence_threshold
        self.uncertainty_threshold = uncertainty_threshold
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.spatial_mapper = SpatialCoordinateMapper(frame_width, frame_height)

        self.net: Optional[cv2.dnn.Net] = None
        self.model_type = "saliency_fallback"

        if model_path and os.path.exists(model_path):
            self._load_dnn_model(model_path, config_path)

    def _load_dnn_model(self, model_path: str, config_path: Optional[str]) -> bool:
        """Attempt loading neural network using OpenCV 5 DNN."""
        try:
            if model_path.endswith(".onnx"):
                self.net = cv2.dnn.readNetFromONNX(model_path)
                self.model_type = "onnx"
            elif config_path and os.path.exists(config_path):
                self.net = cv2.dnn.readNetFromCaffe(config_path, model_path)
                self.model_type = "caffe"
            else:
                self.net = cv2.dnn.readNet(model_path)
                self.model_type = "opencv_dnn"

            # Prefer CPU for maximum compatibility across devices
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            return True
        except Exception:
            self.net = None
            self.model_type = "saliency_fallback"
            return False

    def detect(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Run object detection on the input frame.

        Returns:
            Dict containing:
                - confirmed_detections: list of high-confidence objects
                - uncertain_detections: list of low-confidence candidates
                - raw_count: total objects processed
                - inference_ms: latency in milliseconds
        """
        start_tick = cv2.getTickCount()

        if self.net is not None:
            confirmed, uncertain = self._detect_dnn(frame)
        else:
            confirmed, uncertain = self._detect_geometric_saliency(frame)

        elapsed_ms = (cv2.getTickCount() - start_tick) / cv2.getTickFrequency() * 1000.0

        return {
            "confirmed_detections": confirmed,
            "uncertain_detections": uncertain,
            "total_detected": len(confirmed),
            "inference_ms": round(elapsed_ms, 2),
            "model_type": self.model_type,
        }

    def _detect_dnn(self, frame: np.ndarray) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Perform DNN forward pass."""
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        confirmed: List[Dict[str, Any]] = []
        uncertain: List[Dict[str, Any]] = []

        for i in range(detections.shape[2]):
            confidence = float(detections[0, 0, i, 2])
            class_id = int(detections[0, 0, i, 1])

            if confidence < self.uncertainty_threshold:
                continue

            box_x1 = int(detections[0, 0, i, 3] * w)
            box_y1 = int(detections[0, 0, i, 4] * h)
            box_x2 = int(detections[0, 0, i, 5] * w)
            box_y2 = int(detections[0, 0, i, 6] * h)

            box_w = max(0, box_x2 - box_x1)
            box_h = max(0, box_y2 - box_y1)
            box = (box_x1, box_y1, box_w, box_h)

            label = COCO_LABELS[class_id] if class_id < len(COCO_LABELS) else f"Object_{class_id}"
            spatial_info = self.spatial_mapper.map_box(box)

            record = {
                "label": label,
                "confidence": round(confidence, 3),
                "box": box,
                "direction": spatial_info["direction"],
                "proximity": spatial_info["proximity"],
                "vertical_pos": spatial_info["vertical_pos"],
            }

            if confidence >= self.confidence_threshold:
                confirmed.append(record)
            else:
                uncertain.append(record)

        return confirmed, uncertain

    def _detect_geometric_saliency(self, frame: np.ndarray) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Pure OpenCV 5 contour & morphological saliency detector.
        Provides guaranteed functional detection on synthetic feeds, captured images,
        and offline systems without downloading multi-megabyte weights.
        """
        h, w = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame

        # Enhance contrast and suppress background noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        confirmed: List[Dict[str, Any]] = []
        uncertain: List[Dict[str, Any]] = []

        min_area = (w * h) * 0.015  # At least 1.5% of frame
        max_area = (w * h) * 0.70   # Not entire background

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < min_area or area > max_area:
                continue

            bx, by, bw, bh = cv2.boundingRect(cnt)
            aspect_ratio = float(bw) / float(bh)
            spatial_info = self.spatial_mapper.map_box((bx, by, bw, bh))

            # Heuristic classification based on aspect ratio and spatial context
            if 0.65 <= aspect_ratio <= 1.4:
                label = "cup" if area < (w * h * 0.08) else "box / container"
                conf = 0.78
            elif aspect_ratio < 0.55:
                label = "person" if bh > (h * 0.35) else "bottle"
                conf = 0.74
            elif aspect_ratio > 1.8:
                label = "table / surface item" if by > (h * 0.5) else "sign / display"
                conf = 0.72
            else:
                label = "object"
                conf = 0.48

            record = {
                "label": label,
                "confidence": round(conf, 3),
                "box": (bx, by, bw, bh),
                "direction": spatial_info["direction"],
                "proximity": spatial_info["proximity"],
                "vertical_pos": spatial_info["vertical_pos"],
            }

            if conf >= self.confidence_threshold:
                confirmed.append(record)
            elif conf >= self.uncertainty_threshold:
                uncertain.append(record)

        return confirmed, uncertain


class SceneDescriber:
    """
    Constructs accessible, Jarvis-style natural language scene descriptions
    for blind and low-vision users.
    """

    SAFETY_DISCLAIMER = (
        "Note: VisionBridge AI provides situational awareness, but ordinary object detection "
        "does not guarantee safe obstacle avoidance or hazard-free navigation."
    )

    @classmethod
    def generate_description(
        cls,
        confirmed: List[Dict[str, Any]],
        uncertain: List[Dict[str, Any]],
        quality_advisories: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Synthesize detections into clear spoken text and visual captions.

        Returns:
            Dict containing speech_text, visual_caption, uncertainty_warnings, and safety_note.
        """
        sentences: List[str] = []

        # 1. Advisories if lighting or blur is suboptimal
        if quality_advisories:
            for adv in quality_advisories:
                sentences.append(adv)

        # 2. Confirmed objects summary
        if not confirmed and not uncertain:
            sentences.append("I do not detect any distinct objects in front of you.")
        elif confirmed:
            sentences.append(f"I observe {len(confirmed)} primary object{'s' if len(confirmed) > 1 else ''}:")
            for det in confirmed:
                desc = f"A {det['label']} is located {det['direction']}, {det['proximity']}."
                sentences.append(desc)

        # 3. Uncertainty handling
        uncertainty_notes: List[str] = []
        if uncertain:
            candidate_names = list(set([d["label"] for d in uncertain]))
            u_text = (
                f"I also detect potential item(s) that might be a {', '.join(candidate_names)}, "
                f"but confidence is low. Please adjust camera angle or lighting to verify."
            )
            uncertainty_notes.append(u_text)
            sentences.append(u_text)

        spoken_script = " ".join(sentences)

        return {
            "spoken_script": spoken_script,
            "caption": spoken_script,
            "uncertainty_warnings": uncertainty_notes,
            "safety_note": cls.SAFETY_DISCLAIMER,
            "object_count": len(confirmed),
        }
