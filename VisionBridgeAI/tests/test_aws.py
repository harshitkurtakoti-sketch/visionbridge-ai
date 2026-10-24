"""
Unit and integration tests for AWS Cloud integration and privacy guard.
"""

import json
import base64
import numpy as np
import cv2
import pytest
from src.aws_service import AWSAccessibilityService, PrivacyConsentError
from deploy.lambda_function import lambda_handler


def test_lambda_handler_scene_analysis():
    """Verify Lambda handler processes scene analysis requests."""
    frame = np.zeros((240, 320, 3), dtype=np.uint8)
    _, buf = cv2.imencode(".jpg", frame)
    b64_img = base64.b64encode(buf).decode("utf-8")

    event = {"body": json.dumps({"task": "scene_analysis", "image_base64": b64_img})}
    res = lambda_handler(event, None)
    assert res["statusCode"] == 200
    body = json.loads(res["body"])
    assert body["status"] == "success"
    assert "detected_objects" in body


def test_lambda_handler_ocr_enhancement():
    """Verify Lambda handler processes OCR requests."""
    frame = np.ones((100, 200, 3), dtype=np.uint8) * 255
    _, buf = cv2.imencode(".jpg", frame)
    b64_img = base64.b64encode(buf).decode("utf-8")

    event = {"body": json.dumps({"task": "ocr_enhancement", "image_base64": b64_img})}
    res = lambda_handler(event, None)
    assert res["statusCode"] == 200
    body = json.loads(res["body"])
    assert body["status"] == "success"
    assert "text" in body


def test_aws_service_unconsented_blocked():
    """Verify that cloud upload strictly blocks without consent."""
    service = AWSAccessibilityService(use_mock=True)
    frame = np.zeros((100, 100, 3), dtype=np.uint8)

    with pytest.raises(PrivacyConsentError):
        service.process_frame_cloud(frame, user_consented=False)


def test_aws_service_consented_execution():
    """Verify that cloud upload succeeds when user consent is provided."""
    service = AWSAccessibilityService(use_mock=True)
    frame = np.zeros((100, 100, 3), dtype=np.uint8)

    res = service.process_frame_cloud(frame, user_consented=True)
    assert res["status"] == "success"
    assert "cloud_provider" in res
    assert "compute_target" in res
