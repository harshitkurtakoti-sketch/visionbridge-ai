"""
VisionBridge AI - Interactive Accessibility Assistant Application.
Designed for OpenCV AI Competition 2026.

Run with:
    streamlit run app/main.py
    or:
    streamlit run streamlit_app.py
"""

import sys
import os
from pathlib import Path
import streamlit as st
import numpy as np
import cv2

# Ensure application and project roots are in sys.path
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
for _p in [str(APP_DIR), str(PROJECT_ROOT), str(PROJECT_ROOT.parent)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from src.assistant import VisionBridgeAssistant
except ImportError:
    from VisionBridgeAI.src.assistant import VisionBridgeAssistant

try:
    from app.ui import ACCESSIBLE_CSS, render_header, render_jarvis_audio_bridge
except (ImportError, ModuleNotFoundError):
    try:
        from VisionBridgeAI.app.ui import ACCESSIBLE_CSS, render_header, render_jarvis_audio_bridge
    except (ImportError, ModuleNotFoundError):
        from ui import ACCESSIBLE_CSS, render_header, render_jarvis_audio_bridge


st.set_page_config(
    page_title="VisionBridge AI - Jarvis for Accessibility",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject accessible styling & Jarvis HUD header
st.markdown(ACCESSIBLE_CSS, unsafe_allow_html=True)
st.markdown(render_header(), unsafe_allow_html=True)


# Initialize assistant & session state
if "assistant" not in st.session_state:
    st.session_state.assistant = VisionBridgeAssistant(enable_tts=False)
    st.session_state.camera_active = False
    st.session_state.last_frame = None
    st.session_state.last_annotated = None
    st.session_state.cloud_consent = False
    st.session_state.acoustic_alert = None
    st.session_state.pending_speech = "Jarvis accessibility neural system online. Voice commands and auditory warnings are active."
    st.session_state.last_vcmd = ""

assistant: VisionBridgeAssistant = st.session_state.assistant


# Process incoming browser voice commands (via URL query parameters)
query_vcmd = st.query_params.get("vcmd") or st.query_params.get("voice_cmd")
if query_vcmd and query_vcmd != st.session_state.last_vcmd:
    st.session_state.last_vcmd = query_vcmd
    st.query_params.clear()
    cmd_res = assistant.process_command(query_vcmd)
    if "speech_text" in cmd_res:
        st.session_state.pending_speech = cmd_res["speech_text"]
    if "annotated_frame" in cmd_res:
        st.session_state.last_annotated = cmd_res["annotated_frame"]
    if cmd_res.get("action") == "start_camera":
        st.session_state.camera_active = True
    elif cmd_res.get("action") == "stop_camera":
        st.session_state.camera_active = False
    elif "is_confirmed" in cmd_res:
        st.session_state.acoustic_alert = cmd_res
    st.rerun()


# Sidebar Settings & Accessibility Options
with st.sidebar:
    st.markdown("### ⚡ Jarvis Core & Audio Settings")

    browser_voice_enabled = st.checkbox("Browser Voice & Speech Synthesis", value=True, help="Plays authentic Jarvis vocal feedback and warnings directly through your browser speakers.")
    auto_warn = st.checkbox("Proactive Hazard Warnings", value=True, help="Automatically warns the user when obstacles or acoustic hazards are detected.")
    high_contrast = st.checkbox("WCAG 2.2 AAA Contrast Mode", value=True)
    
    st.markdown("---")
    st.markdown("### 🔒 Privacy Controls")
    st.session_state.cloud_consent = st.toggle(
        "Allow Opt-in Cloud Processing (AWS)",
        value=st.session_state.cloud_consent,
        help="When enabled, allows secure processing on AWS. By default, all processing is strictly local."
    )
    assistant.user_cloud_consent = st.session_state.cloud_consent

    if st.session_state.cloud_consent:
        st.info("🌐 AWS Cloud Component: Enabled (User Consent Granted)")
    else:
        st.success("🛡️ Strict Local-First: Cloud Upload Blocked")

    st.markdown("---")
    st.markdown("### ⌨️ Keyboard Shortcuts")
    st.markdown("""
    - **`[V]`** Voice Command (Push-to-Talk)
    - **`[C]`** Toggle Camera Sensor
    - **`[D]`** Describe Scene
    - **`[R]`** Read Text (OCR)
    - **`[S]`** System Diagnostic Status
    """)

    st.markdown("---")
    st.markdown("### 🔊 Sound Event Simulator (Deaf Assist)")
    sound_col1, sound_col2 = st.columns(2)
    with sound_col1:
        if st.button("Door Knock (62dB)", use_container_width=True):
            alert = assistant.detect_environmental_sound("door_knock", peak_db=62.0)
            st.session_state.acoustic_alert = alert
            st.session_state.pending_speech = alert["speech_text"]
            st.rerun()
    with sound_col2:
        if st.button("🚨 Fire Alarm (88dB)", use_container_width=True):
            alert = assistant.detect_environmental_sound("fire_alarm", peak_db=88.5)
            st.session_state.acoustic_alert = alert
            st.session_state.pending_speech = alert["speech_text"]
            st.rerun()

    if st.button("🔊 Re-vocalize Jarvis Introduction", use_container_width=True):
        st.session_state.pending_speech = "Jarvis online. Standing by for voice commands, visual navigation, or environmental hazard warnings."
        st.rerun()


# Render in-browser Web Speech Recognition, Speech Synthesis, & Web Audio Bridge
render_jarvis_audio_bridge(
    speech_text=st.session_state.pending_speech,
    alert_data=st.session_state.acoustic_alert,
    auto_speak=browser_voice_enabled,
    height=270,
)


# Main Content Layout: Two Columns (Vision Feed vs Assistive Output)
left_col, right_col = st.columns([3, 2], gap="large")

with left_col:
    # Camera Status & Control Bar
    ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([2, 2, 2, 2])

    with ctrl_col1:
        if not st.session_state.camera_active:
            if st.button("▶️ Start Camera [C]", key="btn_start_cam", use_container_width=True):
                assistant.start_camera()
                st.session_state.camera_active = True
                st.session_state.pending_speech = "Visual sensor array online and streaming, sir."
                st.rerun()
        else:
            if st.button("⏹️ Stop Camera [C]", key="btn_stop_cam", use_container_width=True):
                assistant.stop_camera()
                st.session_state.camera_active = False
                st.session_state.pending_speech = "Visual sensor array deactivated. System in standby mode."
                st.rerun()

    with ctrl_col2:
        if st.button("🔍 Describe Scene [D]", key="btn_describe", use_container_width=True, disabled=not st.session_state.camera_active):
            with st.spinner("Analyzing scene with OpenCV 5..."):
                res = assistant.describe_surroundings()
                if "annotated_frame" in res:
                    st.session_state.last_annotated = res["annotated_frame"]
                if "speech_text" in res:
                    st.session_state.pending_speech = res["speech_text"]
            st.rerun()

    with ctrl_col3:
        if st.button("📖 Read Text [R]", key="btn_read_ocr", use_container_width=True, disabled=not st.session_state.camera_active):
            with st.spinner("Extracting text with OpenCV 5 OCR..."):
                res = assistant.read_text()
                if "speech_text" in res:
                    st.session_state.pending_speech = res["speech_text"]
            st.rerun()

    with ctrl_col4:
        if st.button("⚠️ Hazard Check", key="btn_hazard_check", use_container_width=True):
            with st.spinner("Evaluating hazards & surroundings..."):
                res = assistant.process_command("warn me of hazards")
                if "speech_text" in res:
                    st.session_state.pending_speech = res["speech_text"]
            st.rerun()

    # Video / Image Display Area with Sci-Fi Reticle Overlay
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    if st.session_state.camera_active:
        frame = assistant.get_current_frame()
        st.session_state.last_frame = frame

        display_img = st.session_state.last_annotated if st.session_state.last_annotated is not None else frame
        if display_img is not None:
            # Convert BGR to RGB for Streamlit
            rgb_img = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
            
            # Encapsulate image inside HUD Reticle frame
            st.markdown(
                """
                <div class="jarvis-hud-viewport">
                    <div class="jarvis-reticle-overlay">
                        <div class="jarvis-corner-tl"></div>
                        <div class="jarvis-corner-tr"></div>
                        <div class="jarvis-corner-bl"></div>
                        <div class="jarvis-corner-br"></div>
                        <div class="jarvis-center-crosshair"></div>
                        <div class="jarvis-scan-line"></div>
                        <div class="jarvis-hud-badge">JARVIS HUD &bull; TARGET SCAN ARMED &bull; FOV 78°</div>
                    </div>
                """,
                unsafe_allow_html=True,
            )
            st.image(rgb_img, caption="Live Accessible Vision Stream (OpenCV 5 & Jarvis Reticle)", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div style="background: rgba(10, 18, 36, 0.9); border: 2px dashed rgba(0, 240, 255, 0.4); border-radius: 12px; height: 360px; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(0, 0, 0, 0.6);">
                <div style="font-size: 3rem; margin-bottom: 10px; filter: drop-shadow(0 0 12px #00f0ff);">👁️⚡</div>
                <p style="font-size: 1.35rem; color: #00f0ff; margin: 0; font-family: 'Orbitron', sans-serif; font-weight: 700;">VISUAL SENSOR ARRAY STANDBY</p>
                <p style="font-size: 0.95rem; color: #c5d8f7; margin-top: 6px;">Press <b>Start Camera [C]</b> or say <b>"Jarvis, start camera"</b> to activate vision perception.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Cloud Enhancement Trigger (AWS)
    if st.session_state.camera_active and st.session_state.cloud_consent:
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        if st.button("☁️ Run AWS Graviton Cloud Scene Analysis", use_container_width=True):
            with st.spinner("Transmitting frame to AWS Lambda (OpenCV 5 COOL)..."):
                cloud_res = assistant.request_cloud_analysis()
                st.session_state.pending_speech = "AWS Graviton cloud scene analysis received and verified, sir."
                st.json(cloud_res)


with right_col:
    # Acoustic Event Alert Banner (if triggered)
    if st.session_state.acoustic_alert:
        alert = st.session_state.acoustic_alert
        if alert.get("is_confirmed"):
            st.markdown(
                f"<div class='vb-sound-alert-confirmed'>🚨 {alert['guidance_banner']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='vb-sound-alert-candidate'>⚠️ {alert['guidance_banner']}</div>",
                unsafe_allow_html=True,
            )

    # Jarvis Command Interface & Natural Language Input
    st.markdown("### 💬 Jarvis Command Input")
    command_text = st.text_input(
        "Enter or speak a command (e.g. 'Describe surroundings', 'Read text', 'Warn me of hazards', 'Status')",
        key="txt_command",
        placeholder="Type command or click the mic button above...",
    )
    if command_text:
        res = assistant.process_command(command_text)
        if "speech_text" in res:
            st.session_state.pending_speech = res["speech_text"]
        if "annotated_frame" in res:
            st.session_state.last_annotated = res["annotated_frame"]
        if res.get("action") == "start_camera":
            st.session_state.camera_active = True
        elif res.get("action") == "stop_camera":
            st.session_state.camera_active = False
        elif "is_confirmed" in res:
            st.session_state.acoustic_alert = res
        st.rerun()

    # Live High-Contrast Captions Panel
    st.markdown("### 📜 Live Visual Captions & Telemetry Log")
    captions = assistant.audio.captions_history

    captions_html = "<div class='vb-captions-container'>"
    if not captions:
        captions_html += "<div class='vb-caption-entry' style='color: #6a82a6;'>Jarvis voice interface initialized. Spoken warnings, captions, and telemetry will log here in real time.</div>"
    else:
        for cap in reversed(captions[-8:]):
            speaker = cap.get("source", "Jarvis")
            text = cap.get("text", "")
            captions_html += f"<div class='vb-caption-entry'><span class='vb-caption-speaker'>[{speaker}]</span> {text}</div>"
    captions_html += "</div>"

    st.markdown(captions_html, unsafe_allow_html=True)

    # Navigation Safety Notice
    st.markdown(
        """
        <div style="background-color: rgba(30, 20, 0, 0.85); border-left: 4px solid #ffb800; padding: 12px 16px; border-radius: 8px; margin-top: 18px; font-size: 0.95rem; color: #ffe699; box-shadow: 0 2px 10px rgba(0,0,0,0.5);">
            <b>Safety Notice:</b> VisionBridge AI provides situational perception and cognitive assistance. Ordinary 2D computer vision does not guarantee detection of all negative ground hazards (e.g. drop-offs or stairwells). Always utilize primary mobility aids.
        </div>
        """,
        unsafe_allow_html=True,
    )
