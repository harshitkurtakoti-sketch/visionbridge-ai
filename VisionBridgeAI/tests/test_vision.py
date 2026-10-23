"""
Unit tests for OpenCV 5 vision pipeline and spatial coordinate mapping.
"""

import numpy as np
import pytest
from src.vision import VisionPipeline, SpatialCoordinateMapper, ImageQualityAssessment


def test_spatial_coordinate_mapper_zones():
    """Verify horizontal zone and proximity categorizations."""
    mapper = SpatialCoordinateMapper(frame_width=640, frame_height=480)

    # Box at far left: x=30, y=200, w=50, h=100 -> cx=55 (55/640 = 0.086)
    far_left_box = (30, 200, 50, 100)
    res_left = mapper.map_box(far_left_box)
    assert res_left["direction"] == "to your far left"

    # Box directly ahead: center_x = 320 -> norm_cx = 0.50
    center_box = (295, 200, 50, 200)
    res_center = mapper.map_box(center_box)
    assert res_center["direction"] == "directly ahead"
    assert "mid-range" in res_center["proximity"]

    # Box at far right: center_x = 580 -> norm_cx = 0.906
    right_box = (560, 200, 40, 80)
    res_right = mapper.map_box(right_box)
    assert res_right["direction"] == "to your far right"


def test_quality_assessment_blur_and_lighting():
    """Verify blur and low-light detection advisories."""
    qa = ImageQualityAssessment(blur_threshold=50.0, low_light_threshold=40.0)

    # Flat black image (severe low-light)
    dark_img = np.zeros((480, 640, 3), dtype=np.uint8)
    res_dark = qa.evaluate(dark_img)
    assert res_dark["is_low_light"] is True
    assert any("dim" in adv.lower() for adv in res_dark["advisories"])

    # High detail image with sharp gradient (not blurry, normal lighting)
    sharp_img = np.zeros((480, 640, 3), dtype=np.uint8)
    sharp_img[:, :320] = 200
    res_sharp = qa.evaluate(sharp_img)
    assert res_sharp["mean_brightness"] > 50


def test_vision_pipeline_preprocessing():
    """Verify CLAHE and edge generation."""
    pipe = VisionPipeline(width=640, height=480)
    frame = np.full((480, 640, 3), 120, dtype=np.uint8)

    views = pipe.preprocess(frame)
    assert "bgr" in views
    assert "gray" in views
    assert "clahe_bgr" in views
    assert "edges" in views
    assert views["clahe_bgr"].shape == (480, 640, 3)
