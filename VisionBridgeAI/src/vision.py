"""
Vision Processing Pipeline for VisionBridge AI.

Uses OpenCV 5 to preprocess camera frames, assess image quality (blur and lighting),
enhance contrast for assistive perception, and compute spatial coordinates
relative to the user's field of view.
"""

from typing import Dict, Any, List, Tuple
import cv2
import numpy as np


class ImageQualityAssessment:
    """Evaluates frame quality to provide guidance to visually impaired users."""

    def __init__(self, blur_threshold: float = 80.0, low_light_threshold: float = 50.0, high_glare_threshold: float = 215.0):
        self.blur_threshold = blur_threshold
        self.low_light_threshold = low_light_threshold
        self.high_glare_threshold = high_glare_threshold

    def evaluate(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Assess frame clarity and illumination.

        Returns:
            Dict containing scores, flags, and spoken guidance recommendations.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame

        # Blur metric: Variance of Laplacian
        laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        is_blurry = laplacian_var < self.blur_threshold

        # Illumination metric: Mean luminance
        mean_brightness = float(np.mean(gray))
        is_low_light = mean_brightness < self.low_light_threshold
        is_glare = mean_brightness > self.high_glare_threshold

        advisories: List[str] = []
        if is_blurry:
            advisories.append("Image appears blurry. Please hold the camera steady.")
        if is_low_light:
            advisories.append("Lighting is very dim. Please turn on a light or move to a brighter area.")
        elif is_glare:
            advisories.append("Strong glare detected. Please angle the camera away from direct lights.")

        return {
            "blur_score": round(laplacian_var, 2),
            "is_blurry": is_blurry,
            "mean_brightness": round(mean_brightness, 2),
            "is_low_light": is_low_light,
            "is_glare": is_glare,
            "is_usable": (not is_blurry) and (not is_low_light),
            "advisories": advisories,
        }


class SpatialCoordinateMapper:
    """
    Translates 2D bounding boxes into natural language spatial descriptions
    suited for blind and low-vision guidance.
    """

    def __init__(self, frame_width: int = 640, frame_height: int = 480):
        self.frame_width = frame_width
        self.frame_height = frame_height

    def map_box(self, box: Tuple[int, int, int, int]) -> Dict[str, Any]:
        """
        Map bounding box (x, y, w, h) to spatial orientation and estimated proximity.

        Returns:
            Dict with normalized coords, direction zone, vertical zone, and proximity category.
        """
        x, y, w, h = box
        center_x = x + (w / 2.0)
        center_y = y + (h / 2.0)

        norm_cx = center_x / self.frame_width
        norm_cy = center_y / self.frame_height
        norm_height = h / self.frame_height

        # Horizontal direction partition
        if norm_cx < 0.22:
            direction = "to your far left"
        elif norm_cx < 0.40:
            direction = "to your left"
        elif norm_cx < 0.60:
            direction = "directly ahead"
        elif norm_cx < 0.78:
            direction = "to your right"
        else:
            direction = "to your far right"

        # Vertical orientation
        if norm_cy < 0.35:
            vertical_pos = "high / overhead"
        elif norm_cy > 0.65:
            vertical_pos = "low / on surface"
        else:
            vertical_pos = "at chest / table level"

        # Estimated relative proximity (based on normalized vertical extent)
        if norm_height > 0.55:
            proximity = "very close (immediate proximity)"
        elif norm_height > 0.25:
            proximity = "mid-range (about 1 to 2 meters)"
        else:
            proximity = "distant (background)"

        return {
            "center": (round(norm_cx, 3), round(norm_cy, 3)),
            "box_dims": (w, h),
            "direction": direction,
            "vertical_pos": vertical_pos,
            "proximity": proximity,
            "norm_height": round(norm_height, 3),
        }


class VisionPipeline:
    """
    Core OpenCV 5 processing pipeline. Performs contrast enhancement,
    filtering, quality checks, and spatial annotation.
    """

    def __init__(self, width: int = 640, height: int = 480):
        self.width = width
        self.height = height
        self.quality_checker = ImageQualityAssessment()
        self.spatial_mapper = SpatialCoordinateMapper(width, height)

        # CLAHE (Contrast Limited Adaptive Histogram Equalization) for low-light enhancement
        self.clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))

    def preprocess(self, frame: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Produce key transformed views of the frame:
        - resized BGR
        - grayscale
        - contrast-enhanced CLAHE
        - edge map (Canny)
        """
        if frame.shape[1] != self.width or frame.shape[0] != self.height:
            frame = cv2.resize(frame, (self.width, self.height))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply CLAHE on luminance channel for better assistive viewing in uneven lighting
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        enhanced_l = self.clahe.apply(l)
        enhanced_lab = cv2.merge((enhanced_l, a, b))
        enhanced_bgr = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

        # Edge representation for tactile/high-contrast viewing
        edges = cv2.Canny(gray, 70, 150)

        return {
            "bgr": frame,
            "gray": gray,
            "clahe_bgr": enhanced_bgr,
            "edges": edges,
        }

    def assess_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """Assess blur and lighting condition of the frame."""
        return self.quality_checker.evaluate(frame)

    def draw_accessible_annotations(
        self,
        frame: np.ndarray,
        detections: List[Dict[str, Any]],
        show_labels: bool = True,
    ) -> np.ndarray:
        """
        Draw high-contrast, bold bounding boxes and spatial tags suitable
        for low-vision users and demonstrations.
        """
        annotated = frame.copy()

        # High-contrast color palette: Accessible Yellow, Cyan, Magenta, Green
        palette = [
            (0, 230, 255),   # Yellow/Amber (BGR)
            (255, 200, 0),   # Cyan (BGR)
            (200, 50, 255),  # Magenta (BGR)
            (50, 230, 50),   # Lime Green (BGR)
        ]

        for i, det in enumerate(detections):
            x, y, w, h = det["box"]
            color = palette[i % len(palette)]
            conf = det.get("confidence", 0.0)
            label = det.get("label", "Object")
            direction = det.get("direction", "")

            # Draw outer dark border + inner bright border for visibility on any background
            cv2.rectangle(annotated, (x - 1, y - 1), (x + w + 1, y + h + 1), (0, 0, 0), 3)
            cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 2)

            if show_labels:
                text_tag = f"{label} ({int(conf * 100)}%) - {direction}"
                (tw, th), baseline = cv2.getTextSize(text_tag, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                # High-contrast background badge
                badge_y1 = max(0, y - th - 8)
                badge_y2 = y
                cv2.rectangle(annotated, (x, badge_y1), (x + tw + 10, badge_y2), (0, 0, 0), -1)
                cv2.putText(
                    annotated,
                    text_tag,
                    (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    1,
                    cv2.LINE_AA,
                )

        return annotated
