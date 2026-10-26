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
import time
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
    st.session_state.pending_speech = "Jarvis accessibility neural system online. Voice commands, real-time object tracking, and sign language translation are active."
    st.session_state.last_vcmd = ""
    st.session_state.sign_translation = None
    st.session_state.continuous_live = False

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
    elif "accumulated_sentence" in cmd_res:
        st.session_state.sign_translation = cmd_res
    st.rerun()


# Sidebar Settings & Accessibility Options
with st.sidebar:
    st.markdown("### ⚡ Jarvis Core & Audio Settings")

    browser_voice_enabled = st.checkbox(
        "Browser Voice & Speech Synthesis",
        value=True,
        help="Plays authentic Jarvis vocal feedback and warnings directly through your browser speakers."
    )
    auto_warn = st.checkbox(
        "Proactive Hazard Warnings",
        value=True,
        help="Automatically warns the user when obstacles or acoustic hazards are detected."
    )
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
    - **`[T]`** Translate Sign Language
    - **`[S]`** System Diagnostic Status
    """)

    st.markdown("---")
    st.markdown("### 🤟 Sign Language Vocabulary (ASL)")
    st.markdown("""
    - ✋ **HELLO**: Hand open & spread
    - 🙏 **THANK YOU**: Hand angled toward chest
    - 🆘 **HELP**: Need assistance emergency
    - ✌️ **PEACE / 2**: Index & middle fingers
    - 👍 **GOOD / YES**: Thumb pointing up
    - ✊ **YES / A**: Closed solid fist
    - 🤟 **I LOVE YOU**: Thumb, index & pinky
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
        st.session_state.pending_speech = "Jarvis online. Standing by for voice commands, visual navigation, or sign language translation."
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
    ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4, ctrl_col5 = st.columns([2, 2, 2, 2, 2])

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
                st.session_state.continuous_live = False
                st.session_state.pending_speech = "Visual sensor array deactivated. System in standby mode."
                st.rerun()

    with ctrl_col2:
        if st.button("🔍 Describe [D]", key="btn_describe", use_container_width=True, disabled=not st.session_state.camera_active):
            with st.spinner("Analyzing scene with OpenCV 5..."):
                res = assistant.describe_surroundings()
                if "annotated_frame" in res:
                    st.session_state.last_annotated = res["annotated_frame"]
                if "speech_text" in res:
                    st.session_state.pending_speech = res["speech_text"]
            st.rerun()

    with ctrl_col3:
        if st.button("📖 OCR [R]", key="btn_read_ocr", use_container_width=True, disabled=not st.session_state.camera_active):
            with st.spinner("Extracting text with OpenCV 5 OCR..."):
                res = assistant.read_text()
                if "speech_text" in res:
                    st.session_state.pending_speech = res["speech_text"]
            st.rerun()

    with ctrl_col4:
        if st.button("🤟 Sign Lang [T]", key="btn_sign_lang", use_container_width=True, disabled=not st.session_state.camera_active):
            with st.spinner("Translating sign language gesture..."):
                res = assistant.translate_sign_language()
                if "annotated_frame" in res:
                    st.session_state.last_annotated = res["annotated_frame"]
                if "speech_text" in res:
                    st.session_state.pending_speech = res["speech_text"]
                st.session_state.sign_translation = res
            st.rerun()

    with ctrl_col5:
        if st.button("⚠️ Hazard Scan", key="btn_hazard_check", use_container_width=True):
            with st.spinner("Evaluating hazards & surroundings..."):
                res = assistant.process_command("warn me of hazards")
                if "speech_text" in res:
                    st.session_state.pending_speech = res["speech_text"]
            st.rerun()

    # Real-Time Continuous Live Stream Toggle
    live_col1, live_col2 = st.columns([3, 1])
    with live_col1:
        st.session_state.continuous_live = st.toggle(
            "🔄 Real-Time Live Vision & Gesture Tracking (Continuous Object & Sign Detection)",
            value=st.session_state.continuous_live,
            disabled=not st.session_state.camera_active,
            help="When enabled, streams camera continuously, detecting objects and sign language gestures in real time."
        )
    with live_col2:
        if st.session_state.continuous_live:
            if st.button("⏹️ Pause Tracking", use_container_width=True):
                st.session_state.continuous_live = False
                st.rerun()

    # Video / Image Display Area with Sci-Fi Reticle Overlay
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    video_container = st.empty()

    if st.session_state.camera_active:
        if st.session_state.continuous_live:
            # Real-time continuous detection loop (15-30 FPS)
            for _ in range(25):
                frame = assistant.get_current_frame()
                if frame is not None:
                    # Detect objects in real time
                    det_res = assistant.detector.detect(frame)
                    confirmed = det_res["confirmed_detections"]
                    uncertain = det_res["uncertain_detections"]
                    
                    # Also evaluate sign language hand gestures in real time
                    sign_res = assistant.sign_translator.translate_frame(frame)
                    annotated = sign_res["annotated_frame"]
                    annotated = assistant.vision.draw_accessible_annotations(
                        annotated, confirmed + uncertain, show_labels=True
                    )
                    
                    rgb_live = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                    with video_container.container():
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
                                    <div class="jarvis-hud-badge">REAL-TIME LIVE TRACKING &bull; OPENCV 5 HUD &bull; FOV 78°</div>
                                </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.image(rgb_live, caption="Real-Time Live Vision & Gesture Stream (OpenCV 5)", use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    time.sleep(0.04)
        else:
            frame = assistant.get_current_frame()
            st.session_state.last_frame = frame
            display_img = st.session_state.last_annotated if st.session_state.last_annotated is not None else frame
            if display_img is not None:
                rgb_img = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
                with video_container.container():
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
        with video_container.container():
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
    # Sign Language Live Translation Display (Deaf Communication)
    if st.session_state.sign_translation:
        st_data = st.session_state.sign_translation
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, rgba(0, 230, 118, 0.2), rgba(0, 112, 243, 0.25)); border: 2px solid #00e676; border-radius: 12px; padding: 16px; margin-bottom: 14px; box-shadow: 0 0 20px rgba(0, 230, 118, 0.25);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-family: 'Orbitron', sans-serif; font-size: 1.1rem; color: #00e676; font-weight: bold;">
                        {st_data.get('icon', '🤟')} SIGN TRANSLATION (DEAF ASSIST)
                    </span>
                    <span style="background: rgba(0, 230, 118, 0.3); color: #bbf7d0; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem; font-family: monospace;">
                        CONFIDENCE: {int(st_data.get('confidence', 0.9)*100)}%
                    </span>
                </div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin: 8px 0;">
                    Detected Sign: <span style="color: #00f0ff;">{st_data.get('meaning', 'Hello')}</span>
                </div>
                <div style="font-size: 1.05rem; color: #c5d8f7; background: rgba(0, 0, 0, 0.4); padding: 8px 12px; border-radius: 8px; border-left: 3px solid #00e676;">
                    <b>Translated Saying:</b> "{st_data.get('accumulated_sentence', st_data.get('meaning'))}"
                </div>
                <div style="font-size: 0.85rem; color: #8fa6ca; margin-top: 6px;">
                    🔊 Vocalized aloud through browser speakers for hearing companions.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Deaf Sign Language Gesture Simulator Buttons
    st.markdown("### 🤟 Sign Language Gestures (Simulator & Testing)")
    sig_col1, sig_col2, sig_col3 = st.columns(3)
    with sig_col1:
        if st.button("✋ Hello", use_container_width=True):
            res = assistant.translate_sign_language(hint="HELLO")
            st.session_state.sign_translation = res
            st.session_state.pending_speech = res["speech_text"]
            st.rerun()
        if sig_col2.button("🙏 Thank You", use_container_width=True):
            res = assistant.translate_sign_language(hint="THANK_YOU")
            st.session_state.sign_translation = res
            st.session_state.pending_speech = res["speech_text"]
            st.rerun()
        if sig_col3.button("🆘 Help", use_container_width=True):
            res = assistant.translate_sign_language(hint="HELP")
            st.session_state.sign_translation = res
            st.session_state.pending_speech = res["speech_text"]
            st.rerun()

    sig_col4, sig_col5, sig_col6 = st.columns(3)
    with sig_col4:
        if st.button("✌️ Peace", use_container_width=True):
            res = assistant.translate_sign_language(hint="PEACE")
            st.session_state.sign_translation = res
            st.session_state.pending_speech = res["speech_text"]
            st.rerun()
        if sig_col5.button("👍 Good / Yes", use_container_width=True):
            res = assistant.translate_sign_language(hint="GOOD")
            st.session_state.sign_translation = res
            st.session_state.pending_speech = res["speech_text"]
            st.rerun()
        if sig_col6.button("🧹 Clear Saying", use_container_width=True):
            assistant.sign_translator.clear_sentence()
            st.session_state.sign_translation = None
            st.session_state.pending_speech = "Translated gesture accumulator cleared, sir."
            st.rerun()

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
        "Enter or speak a command (e.g. 'Describe surroundings', 'Read text', 'Translate sign', 'Status')",
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
        elif "accumulated_sentence" in res:
            st.session_state.sign_translation = res
        st.rerun()

    # Live High-Contrast Captions Panel
    st.markdown("### 📜 Live Visual Captions & Telemetry Log")
    captions = assistant.audio.captions_history

    captions_html = "<div class='vb-captions-container'>"
    if not captions:
        captions_html += "<div class='vb-caption-entry' style='color: #6a82a6;'>Jarvis voice & gesture interface initialized. Spoken warnings, captions, and sign translations will log here in real time.</div>"
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
            <b>Safety Notice:</b> VisionBridge AI provides situational perception, sign language translation, and cognitive assistance. Ordinary 2D computer vision does not guarantee detection of all negative ground hazards (e.g. drop-offs or stairwells). Always utilize primary mobility aids.
        </div>
        """,
        unsafe_allow_html=True,
    )
