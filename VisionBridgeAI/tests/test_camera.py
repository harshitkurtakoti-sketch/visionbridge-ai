"""
Unit tests for CameraManager and frame acquisition in VisionBridge AI.
"""

import numpy as np
import pytest
from src.camera import CameraManager


def test_camera_synthetic_fallback():
    """Verify camera initializes cleanly in synthetic mode when physical device is absent."""
    cam = CameraManager(camera_index=99, use_synthetic_fallback=True)
    success = cam.start()
    assert success is True
    assert cam.is_active is True

    ret, frame = cam.get_frame()
    assert ret is True
    assert frame is not None
    assert frame.shape == (480, 640, 3)
    assert isinstance(frame, np.ndarray)

    cam.stop()
    assert cam.is_active is False


def test_camera_load_image_from_bytes():
    """Verify loading and decoding image bytes."""
    cam = CameraManager()
    dummy = np.zeros((100, 100, 3), dtype=np.uint8)
    import cv2
    _, encoded = cv2.imencode(".jpg", dummy)

    ret, frame = cam.load_image(encoded.tobytes())
    assert ret is True
    assert frame is not None
    assert frame.shape == (480, 640, 3)


def test_camera_context_manager():
    """Verify context manager interface starts and stops camera cleanly."""
    with CameraManager(camera_index=99, use_synthetic_fallback=True) as cam:
        assert cam.is_active is True
        ret, frame = cam.get_frame()
        assert ret is True
        assert frame is not None
    assert cam.is_active is False
