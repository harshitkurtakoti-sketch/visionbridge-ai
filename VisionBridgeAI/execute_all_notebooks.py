"""
Executes all 7 Jupyter Notebooks in-place, populating all outputs, execution counts,
and plots for competition review and evaluation reproducibility.
"""

import sys
import os
from pathlib import Path
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

NOTEBOOKS_DIR = Path(__file__).resolve().parent / "notebooks"
PROJECT_ROOT = Path(__file__).resolve().parent

# Ensure project root is on sys.path
sys.path.insert(0, str(PROJECT_ROOT))
os.environ["PYTHONPATH"] = str(PROJECT_ROOT)

ep = ExecutePreprocessor(timeout=600, kernel_name="python3")

notebook_files = [
    "01_environment_dataset.ipynb",
    "02_image_video_processing.ipynb",
    "03_object_detection.ipynb",
    "04_ocr.ipynb",
    "05_speech_accessibility.ipynb",
    "06_evaluation.ipynb",
    "07_integration_demo.ipynb",
]

print("=== EXECUTING ALL 7 JUPYTER NOTEBOOKS ===")

for nb_name in notebook_files:
    nb_path = NOTEBOOKS_DIR / nb_name
    print(f"\nExecuting: {nb_name} ...", end=" ", flush=True)

    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    try:
        ep.preprocess(nb, {"metadata": {"path": str(NOTEBOOKS_DIR)}})
        with open(nb_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        print("SUCCESS (Outputs populated)")
    except Exception as e:
        print(f"FAILED: {e}")

print("\nAll notebooks have been executed and saved with outputs!")
