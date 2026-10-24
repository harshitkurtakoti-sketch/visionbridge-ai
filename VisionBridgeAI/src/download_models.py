"""
Model Downloader Utility for VisionBridge AI.
Downloads lightweight pretrained OpenCV-compatible MobileNet-SSD COCO models
and label sets for offline inference.
"""

import os
from pathlib import Path
import urllib.request

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

COCO_LABELS_URL = "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names"
MODEL_CONFIG_URL = "https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"


def download_coco_labels():
    """Download standard 80-class COCO labels file if missing."""
    target_path = MODELS_DIR / "coco_names.txt"
    if target_path.exists():
        print(f"[OK] Labels already present: {target_path}")
        return True

    print(f"[*] Downloading COCO class labels to {target_path} ...", end=" ")
    try:
        urllib.request.urlretrieve(COCO_LABELS_URL, str(target_path))
        print("DONE")
        return True
    except Exception as e:
        print(f"FAILED ({e})")
        # Write bundled fallback labels
        from src.object_detection import COCO_LABELS
        with open(target_path, "w", encoding="utf-8") as f:
            for label in COCO_LABELS[1:]:  # skip background
                f.write(label + "\n")
        print(f"[OK] Created bundled labels fallback at: {target_path}")
        return True


def ensure_models():
    """Verify and initialize model weights directory."""
    print("=" * 60)
    print("  VISIONBRIDGE AI - MODEL ASSETS INITIALIZATION")
    print("=" * 60)
    download_coco_labels()
    print(f"[OK] Models directory ready at: {MODELS_DIR.resolve()}\n")


if __name__ == "__main__":
    ensure_models()
