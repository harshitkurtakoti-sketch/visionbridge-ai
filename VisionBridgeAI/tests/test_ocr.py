"""
Unit tests for OCR engine and error metrics (CER, WER).
"""

import numpy as np
import pytest
from src.ocr import OCREngine


def test_character_error_rate_exact():
    """Verify CER calculation on exact and substituted strings."""
    engine = OCREngine()
    # Exact match -> CER = 0.0
    cer_exact = engine.calculate_character_error_rate("EXIT", "EXIT")
    assert cer_exact == 0.0

    # 1 substitution out of 4 characters -> 1/4 = 0.25
    cer_sub = engine.calculate_character_error_rate("EXIT", "EX1T")
    assert round(cer_sub, 2) == 0.25

    # Completely different -> 1.0 or higher
    cer_diff = engine.calculate_character_error_rate("STOP", "WALK")
    assert cer_diff == 1.0


def test_word_error_rate():
    """Verify WER calculation."""
    engine = OCREngine()
    wer_exact = engine.calculate_word_error_rate("EMERGENCY EXIT AHEAD", "EMERGENCY EXIT AHEAD")
    assert wer_exact == 0.0

    wer_one_err = engine.calculate_word_error_rate("EMERGENCY EXIT AHEAD", "EMERGENCY DOOR AHEAD")
    assert round(wer_one_err, 2) == round(1 / 3, 2)


def test_ocr_preprocessing_and_extraction():
    """Verify preprocessing generates required layers and handles test images."""
    engine = OCREngine()
    test_img = np.ones((100, 300, 3), dtype=np.uint8) * 255
    # Draw simple text
    import cv2
    cv2.putText(test_img, "EXIT", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

    prep = engine.preprocess_for_ocr(test_img)
    assert "gray" in prep
    assert "contrast_boosted" in prep
    assert "binarized" in prep
    assert "deskewed" in prep

    res = engine.extract_text(test_img)
    assert "text" in res
    assert "spoken_script" in res
    assert "confidence" in res
