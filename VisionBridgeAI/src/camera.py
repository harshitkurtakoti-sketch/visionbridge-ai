"""
Camera and Frame Capture Module for VisionBridge AI.

Provides resilient camera stream acquisition, image loading, synthetic frame
generation for testing/headless execution, and camera status monitoring
using OpenCV 5.
"""

import time
from typing import Optional, Tuple, Union
import cv2
import numpy as np


class CameraManager:
    """
    Manages camera acquisition, image feeding, and frame preprocessing
    for VisionBridge AI.
    """

    def __init__(
        self,
        camera_index: int = 0,
        width: int = 640,
        height: int = 480,
        fps_target: int = 30,
        use_synthetic_fallback: bool = True,
    ):
        """
        Initialize the camera manager.

        Args:
            camera_index: Index of the physical webcam (typically 0).
            width: Target capture width in pixels.
            height: Target capture height in pixels.
            fps_target: Desired target frame rate.
            use_synthetic_fallback: If True, falls back to synthetic frames if hardware camera is unavailable.
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps_target = fps_target
        self.use_synthetic_fallback = use_synthetic_fallback

        self.cap: Optional[cv2.VideoCapture] = None
        self.is_active = False
        self.is_synthetic = False
        self._last_frame_time = time.time()
        self._current_fps = 0.0
        self._frame_counter = 0

    def start(self) -> bool:
        """
        Attempt to open the physical camera. If unavailable and synthetic fallback
        is permitted, initialize synthetic streaming mode.

        Returns:
            bool: True if either camera or synthetic fallback is initialized.
        """
        # Try DirectShow first on Windows for faster initialization, then default
        try:
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                self.cap.release()
                self.cap = cv2.VideoCapture(self.camera_index)
        except Exception:
            self.cap = cv2.VideoCapture(self.camera_index)

        if self.cap is not None and self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps_target)
            self.is_active = True
            self.is_synthetic = False
            return True

        if self.use_synthetic_fallback:
            self.is_active = True
            self.is_synthetic = True
            return True

        self.is_active = False
        return False

    def stop(self) -> None:
        """Release the camera and reset state."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.is_active = False

    def get_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read the next frame from the camera stream or synthetic generator.

        Returns:
            Tuple of (success: bool, frame: Optional[np.ndarray in BGR format])
        """
        if not self.is_active:
            return False, None

        frame = None
        if not self.is_synthetic and self.cap is not None and self.cap.isOpened():
            ret, raw_frame = self.cap.read()
            if ret and raw_frame is not None:
                frame = cv2.resize(raw_frame, (self.width, self.height))
            else:
                # If camera dropped, fall back to synthetic if permitted
                if self.use_synthetic_fallback:
                    self.is_synthetic = True
                    frame = self._generate_synthetic_frame()
                else:
                    return False, None
        else:
            frame = self._generate_synthetic_frame()

        # Update FPS calculation
        now = time.time()
        dt = now - self._last_frame_time
        if dt > 0:
            instant_fps = 1.0 / dt
            self._current_fps = 0.9 * self._current_fps + 0.1 * instant_fps
        self._last_frame_time = now
        self._frame_counter += 1

        return True, frame

    def load_image(self, file_path_or_bytes: Union[str, bytes]) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Load a static image from file path or raw bytes, resizing to standard resolution.

        Args:
            file_path_or_bytes: Local file path or raw byte payload.

        Returns:
            Tuple of (success: bool, frame: Optional[np.ndarray])
        """
        try:
            if isinstance(file_path_or_bytes, bytes):
                nparr = np.frombuffer(file_path_or_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            else:
                frame = cv2.imread(file_path_or_bytes, cv2.IMREAD_COLOR)

            if frame is None:
                return False, None

            frame = cv2.resize(frame, (self.width, self.height))
            return True, frame
        except Exception:
            return False, None

    def _generate_synthetic_frame(self) -> np.ndarray:
        """
        Generate an accessible test pattern frame with geometric objects,
        text banner, and timestamp for evaluation/testing without physical webcam.
        """
        # Create subtle gradient background (dark theme for assistive UI)
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        frame[:, :] = (35, 30, 30)

        # Draw simulated indoor scene elements:
        # A table surface
        cv2.rectangle(frame, (50, 320), (590, 470), (70, 70, 90), -1)

        # A cup / bottle (standing on table, mid-left)
        cv2.rectangle(frame, (120, 220), (180, 340), (180, 100, 50), -1)
        cv2.putText(frame, "Cup", (125, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # A book / reading text sample (on table, center)
        cv2.rectangle(frame, (230, 290), (410, 370), (220, 220, 220), -1)
        cv2.putText(frame, "EXIT SIGN", (250, 335), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (20, 20, 20), 2)

        # A person silhouette (in background, right)
        cv2.circle(frame, (500, 160), 35, (100, 140, 180), -1)
        cv2.rectangle(frame, (460, 195), (540, 320), (100, 140, 180), -1)
        cv2.putText(frame, "Person", (475, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Header status banner
        banner_text = f"VisionBridge AI [Synthetic Feed] #{self._frame_counter}"
        cv2.putText(frame, banner_text, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 220, 255), 2)

        return frame

    @property
    def fps(self) -> float:
        """Return the current rolling FPS."""
        return round(self._current_fps, 1)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
