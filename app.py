"""
VisionBridge AI - Alternative entrypoint for hosting services that look for app.py.
"""
from pathlib import Path

# Run streamlit_app.py
entry_point = Path(__file__).resolve().parent / "streamlit_app.py"
with open(entry_point, "r", encoding="utf-8") as f:
    code = f.read()

exec(compile(code, str(entry_point), "exec"))
