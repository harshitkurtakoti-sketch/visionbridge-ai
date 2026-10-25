"""
VisionBridge AI - Cloud Deployment Entrypoint (streamlit_app.py)

Designed for Streamlit Community Cloud, Hugging Face Spaces, and Docker.
Ensures that all module paths (VisionBridgeAI, src, app) are correctly added
to sys.path and executes the core application seamlessly.
"""

import sys
import os
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent
VISIONBRIDGE_DIR = ROOT_DIR / "VisionBridgeAI"

# Register paths so imports like `from src...` and `from app...` work seamlessly
for p in [str(VISIONBRIDGE_DIR), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Execute main application script
main_script_path = VISIONBRIDGE_DIR / "app" / "main.py"

if not main_script_path.exists():
    raise FileNotFoundError(
        f"VisionBridge AI main application entrypoint was not found at {main_script_path}."
    )

with open(main_script_path, "r", encoding="utf-8") as f:
    app_code = f.read()

# Execute in the context of the main script
exec(compile(app_code, str(main_script_path), "exec"))
