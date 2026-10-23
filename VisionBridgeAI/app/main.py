"""
VisionBridge AI - Interactive Accessibility Assistant Application.
Designed for OpenCV AI Competition 2026.

Run with:
    streamlit run app/main.py
"""

import sys
import os
from pathlib import Path
import streamlit as st
import numpy as np
import cv2

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.assistant import VisionBridgeAssistant
from app.ui import ACCESSIBLE_CSS, render_header


st.set_page_config(
    page_title="VisionBridge AI - Jarvis for Accessibility",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject accessible styling
st.markdown(ACCESSIBLE_CSS, unsafe_allow_html=True)
st.markdown(render_header(), unsafe_allow_html=True)


# Initialize assistant in session state
if "assistant" not in st.session_state:
    st.session_state.assistant = VisionBridgeAssistant(enable_tts=False)
    st.session_state.camera_active = False
    st.session_state.last_frame = None
    st.session_state.last_annotated = None
    st.session_state.cloud_consent = False
    st.session_state.acoustic_alert = None

assistant: VisionBridgeAssistant = st.session_state.assistant


# Sidebar Settings & Accessibility Options
with st.sidebar:
    st.markdown("### ⚙️ Accessibility & Privacy Settings")

    high_contrast = st.checkbox("High-Contrast Mode (WCAG AAA)", value=True)
    voice_feedback = st.checkbox("Vocal Spoken Feedback", value=False)
    assistant.enable_tts = voice_feedback

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
    - **`[C]`** Toggle Camera
    - **`[D]`** Describe Scene
    - **`[R]`** Read Text (OCR)
    - **`[S]`** System Status
    """)

    st.markdown("---")
    st.markdown("### 🔊 Sound Event Simulator (Deaf Assist)")
    sound_col1, sound_col2 = st.columns(2)
    with sound_col1:
        if st.button("Door Knock (62dB)"):
            st.session_state.acoustic_alert = assistant.detect_environmental_sound("door_knock", peak_db=62.0)
    with sound_col2:
        if st.button("Fire Alarm (88dB)"):
            st.session_state.acoustic_alert = assistant.detect_environmental_sound("fire_alarm", peak_db=88.5)


# Main Content Layout: Two Columns (Vision Feed vs Assistive Output)
left_col, right_col = st.columns([3, 2], gap="large")

with left_col:
    # Camera Status & Control Bar
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 2, 2])

    with ctrl_col1:
        if not st.session_state.camera_active:
            if st.button("▶️ Start Camera [C]", key="btn_start_cam", use_container_width=True):
                assistant.start_camera()
                st.session_state.camera_active = True
                st.rerun()
        else:
            if st.button("⏹️ Stop Camera [C]", key="btn_stop_cam", use_container_width=True):
                assistant.stop_camera()
                st.session_state.camera_active = False
                st.rerun()

    with ctrl_col2:
        if st.button("🔍 Describe Scene [D]", key="btn_describe", use_container_width=True, disabled=not st.session_state.camera_active):
            with st.spinner("Analyzing scene..."):
                res = assistant.describe_surroundings()
                if "annotated_frame" in res:
                    st.session_state.last_annotated = res["annotated_frame"]
            st.rerun()

    with ctrl_col3:
        if st.button("📖 Read Text [R]", key="btn_read_ocr", use_container_width=True, disabled=not st.session_state.camera_active):
            with st.spinner("Extracting text with OpenCV 5..."):
                assistant.read_text()
            st.rerun()

    # Video / Image Display Area
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    if st.session_state.camera_active:
        frame = assistant.get_current_frame()
        st.session_state.last_frame = frame

        display_img = st.session_state.last_annotated if st.session_state.last_annotated is not None else frame
        if display_img is not None:
            # Convert BGR to RGB for Streamlit
            rgb_img = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
            st.image(rgb_img, caption="Live Accessible Vision Stream (OpenCV 5)", use_container_width=True)
    else:
        st.markdown(
            """
            <div style="background-color: #151d30; border: 2px dashed #283655; border-radius: 12px; height: 360px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <p style="font-size: 1.4rem; color: #c5d1eb; margin: 0;">Camera is currently paused.</p>
                <p style="font-size: 1.0rem; color: #7f93b5;">Press <b>Start Camera</b> to begin live vision streaming or synthetic testing.</p>
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
                st.json(cloud_res)


with right_col:
    # Acoustic Event Alert Banner (if triggered)
    if st.session_state.acoustic_alert:
        alert = st.session_state.acoustic_alert
        if alert["is_confirmed"]:
            st.markdown(
                f"<div class='vb-sound-alert-confirmed'>🚨 {alert['guidance_banner']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='vb-sound-alert-candidate'>⚠️ {alert['guidance_banner']}</div>",
                unsafe_allow_html=True,
            )

    # Spoken Commands & Natural Language Input
    st.markdown("### 💬 Jarvis Command Interface")
    command_text = st.text_input(
        "Enter or speak a command (e.g. 'Describe surroundings', 'Read text', 'Status')",
        key="txt_command",
        placeholder="Type command here and press Enter...",
    )
    if command_text:
        assistant.process_command(command_text)
        st.rerun()

    # Live High-Contrast Captions Panel
    st.markdown("### 📜 Live Visual Captions")
    captions = assistant.audio.captions_history

    captions_html = "<div class='vb-captions-container'>"
    if not captions:
        captions_html += "<div class='vb-caption-entry' style='color: #888;'>No interactions yet. Captions will appear here in real time.</div>"
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
        <div style="background-color: #2b1f00; border-left: 4px solid #ffb800; padding: 10px 14px; border-radius: 6px; margin-top: 20px; font-size: 0.95rem; color: #ffe699;">
            <b>Safety Notice:</b> VisionBridge AI provides situational perception assistance. Ordinary object detection does not guarantee detection of all ground hazards or replace human mobility aids.
        </div>
        """,
        unsafe_allow_html=True,
    )
