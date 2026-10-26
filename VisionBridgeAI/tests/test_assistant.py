"""
Integration and functional tests for VisionBridgeAssistant.
"""

import pytest
from src.assistant import VisionBridgeAssistant
from src.aws_service import PrivacyConsentError


@pytest.fixture
def assistant():
    """Create a headless assistant instance for testing."""
    ast = VisionBridgeAssistant(enable_tts=False)
    ast.start_camera()
    yield ast
    ast.stop_camera()


def test_assistant_describe_surroundings(assistant):
    """Verify end-to-end scene description generation and safety note."""
    result = assistant.describe_surroundings()
    assert "error" not in result
    assert "speech_text" in result
    assert "safety_note" in result
    # Check that safety disclaimer is strictly present
    assert "not guarantee safe obstacle avoidance" in result["safety_note"]
    assert len(result["speech_text"]) > 0


def test_assistant_read_text(assistant):
    """Verify text reading workflow."""
    result = assistant.read_text()
    assert "speech_text" in result
    assert "confidence" in result
    assert "engine" in result


def test_assistant_command_routing(assistant):
    """Verify spoken and typed command parsing."""
    res_describe = assistant.process_command("Jarvis, describe my surroundings.")
    assert "speech_text" in res_describe

    res_help = assistant.process_command("help")
    assert "help_message" in res_help

    res_status = assistant.process_command("status")
    assert "status_message" in res_status

    res_sign = assistant.process_command("Jarvis, translate sign language.")
    assert "sign" in res_sign
    assert "speech_text" in res_sign


def test_assistant_sign_language_translation(assistant):
    """Verify sign language gesture translation for deaf users."""
    result = assistant.translate_sign_language(hint="HELLO")
    assert "error" not in result
    assert result["sign"] == "HELLO"
    assert "meaning" in result
    assert "spoken_translation" in result
    assert "speech_text" in result
    assert "Deaf user signed" in result["speech_text"]


def test_acoustic_alert_differentiation(assistant):
    """Verify clear distinction between sound candidates and confirmed events."""
    # Low amplitude -> Unconfirmed candidate
    cand_res = assistant.detect_environmental_sound("doorbell", peak_db=58.0)
    assert cand_res["status"] == "UNCONFIRMED_CANDIDATE"
    assert cand_res["is_confirmed"] is False

    # High amplitude -> Confirmed event
    conf_res = assistant.detect_environmental_sound("fire_alarm", peak_db=88.5)
    assert conf_res["status"] == "CONFIRMED_EVENT"
    assert conf_res["is_confirmed"] is True


def test_cloud_privacy_safeguard(assistant):
    """Verify that cloud processing is blocked when user consent is not granted."""
    assistant.user_cloud_consent = False
    result = assistant.request_cloud_analysis()
    # Must report privacy block
    assert "error" in result
    assert "PrivacyConsentError" in result["error"] or "privacy safeguard" in result.get("message", "").lower()

    # When user grants explicit consent, cloud service processes successfully
    assistant.user_cloud_consent = True
    consented_res = assistant.request_cloud_analysis()
    assert "error" not in consented_res
    assert consented_res.get("status") == "success"
