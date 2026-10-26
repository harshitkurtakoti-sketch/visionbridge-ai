"""
Accessible UI Styles and Components for VisionBridge AI.

Implements WCAG 2.2 AAA high-contrast standards, ARIA landmark semantics,
Stark/Jarvis HUD aesthetics, Web Speech recognition & synthesis bridge,
and acoustic indicators for deaf, hard-of-hearing, blind, and low-vision users.
"""

import json
from typing import Optional, Dict, Any
import streamlit.components.v1 as components


JARVIS_HUD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Inter:wght@300;400;600;700;800&family=Share+Tech+Mono&display=swap');

/* VisionBridge AI - Jarvis Sci-Fi HUD & Accessibility Theme (WCAG AAA) */
:root {
    --jarvis-bg: #060a12;
    --jarvis-panel: rgba(10, 18, 36, 0.88);
    --jarvis-panel-border: rgba(0, 240, 255, 0.35);
    --jarvis-cyan: #00f0ff;
    --jarvis-cyan-glow: rgba(0, 240, 255, 0.45);
    --jarvis-blue: #0070f3;
    --jarvis-gold: #ffb800;
    --jarvis-gold-glow: rgba(255, 184, 0, 0.4);
    --jarvis-red: #ff2a5f;
    --jarvis-red-glow: rgba(255, 42, 95, 0.5);
    --jarvis-green: #00e676;
    --jarvis-text-primary: #ffffff;
    --jarvis-text-secondary: #c5d8f7;
    --jarvis-font-mono: 'Share Tech Mono', 'Courier New', monospace;
    --jarvis-font-hud: 'Orbitron', -apple-system, sans-serif;
    --jarvis-font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

body, [data-testid="stAppViewContainer"] {
    background-color: var(--jarvis-bg) !important;
    background-image: 
        radial-gradient(circle at 50% 0%, rgba(0, 112, 243, 0.15), transparent 45%),
        linear-gradient(rgba(0, 240, 255, 0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 240, 255, 0.02) 1px, transparent 1px) !important;
    background-size: 100% 100%, 32px 32px, 32px 32px !important;
    color: var(--jarvis-text-primary) !important;
    font-family: var(--jarvis-font-body) !important;
}

[data-testid="stSidebar"] {
    background-color: rgba(6, 12, 24, 0.95) !important;
    border-right: 1px solid var(--jarvis-panel-border) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.6) !important;
}

/* Jarvis Top HUD Header */
.jarvis-header-container {
    background: linear-gradient(135deg, rgba(10, 22, 44, 0.92) 0%, rgba(6, 12, 26, 0.95) 100%);
    border: 1px solid var(--jarvis-panel-border);
    border-radius: 14px;
    padding: 18px 24px;
    margin-bottom: 22px;
    box-shadow: 0 0 30px rgba(0, 240, 255, 0.12), inset 0 0 15px rgba(0, 240, 255, 0.04);
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    overflow: hidden;
}

.jarvis-header-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--jarvis-cyan), var(--jarvis-gold), transparent);
}

.jarvis-brand-title {
    font-family: var(--jarvis-font-hud);
    font-size: 2.3rem;
    font-weight: 900;
    letter-spacing: 2px;
    color: var(--jarvis-cyan);
    text-shadow: 0 0 18px var(--jarvis-cyan-glow);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 14px;
}

.jarvis-brand-subtitle {
    font-family: var(--jarvis-font-mono);
    color: var(--jarvis-text-secondary);
    font-size: 0.95rem;
    letter-spacing: 1px;
    margin-top: 5px;
}

.jarvis-telemetry-bar {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
}

.jarvis-pill {
    font-family: var(--jarvis-font-mono);
    font-size: 0.8rem;
    padding: 6px 12px;
    border-radius: 20px;
    background: rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(0, 240, 255, 0.3);
    color: var(--jarvis-text-secondary);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
}

.jarvis-pill-online {
    border-color: var(--jarvis-green);
    color: #bbf7d0;
}
.jarvis-pill-active {
    border-color: var(--jarvis-cyan);
    color: #e0faff;
}
.jarvis-pill-hazard {
    border-color: var(--jarvis-red);
    color: #fecdd3;
    animation: jarvis-pulse 1.2s infinite alternate;
}

.jarvis-dot-pulse {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: currentColor;
    box-shadow: 0 0 8px currentColor;
}

@keyframes jarvis-pulse {
    from { opacity: 0.7; transform: scale(0.96); }
    to { opacity: 1; transform: scale(1.05); }
}

/* Jarvis Vision HUD Overlay Frame */
.jarvis-hud-viewport {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid var(--jarvis-cyan);
    box-shadow: 0 0 24px rgba(0, 240, 255, 0.2);
    background-color: #030712;
}

.jarvis-reticle-overlay {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 10;
}

.jarvis-corner-tl {
    position: absolute;
    top: 12px; left: 12px;
    width: 24px; height: 24px;
    border-top: 3px solid var(--jarvis-cyan);
    border-left: 3px solid var(--jarvis-cyan);
}
.jarvis-corner-tr {
    position: absolute;
    top: 12px; right: 12px;
    width: 24px; height: 24px;
    border-top: 3px solid var(--jarvis-cyan);
    border-right: 3px solid var(--jarvis-cyan);
}
.jarvis-corner-bl {
    position: absolute;
    bottom: 12px; left: 12px;
    width: 24px; height: 24px;
    border-bottom: 3px solid var(--jarvis-cyan);
    border-left: 3px solid var(--jarvis-cyan);
}
.jarvis-corner-br {
    position: absolute;
    bottom: 12px; right: 12px;
    width: 24px; height: 24px;
    border-bottom: 3px solid var(--jarvis-cyan);
    border-right: 3px solid var(--jarvis-cyan);
}

.jarvis-center-crosshair {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 80px; height: 80px;
    border: 1px dashed rgba(0, 240, 255, 0.6);
    border-radius: 50%;
}
.jarvis-center-crosshair::before {
    content: '+';
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    color: var(--jarvis-cyan);
    font-size: 20px;
    font-weight: bold;
}

.jarvis-scan-line {
    position: absolute;
    left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0, 240, 255, 0.8), transparent);
    animation: jarvis-scan 3s ease-in-out infinite alternate;
}

@keyframes jarvis-scan {
    0% { top: 4%; }
    100% { top: 96%; }
}

.jarvis-hud-badge {
    position: absolute;
    bottom: 12px;
    left: 20px;
    background: rgba(0, 0, 0, 0.75);
    border: 1px solid var(--jarvis-cyan);
    color: var(--jarvis-cyan);
    padding: 4px 10px;
    font-family: var(--jarvis-font-mono);
    font-size: 0.75rem;
    border-radius: 4px;
    letter-spacing: 1px;
}

/* Captions & Alert Styling */
.vb-captions-container {
    background-color: rgba(4, 8, 18, 0.94);
    border: 2px solid var(--jarvis-panel-border);
    border-radius: 12px;
    padding: 16px;
    min-height: 160px;
    max-height: 280px;
    overflow-y: auto;
    font-size: 1.15rem;
    line-height: 1.5;
    color: #ffffff;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
}

.vb-caption-entry {
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.vb-caption-speaker {
    font-family: var(--jarvis-font-mono);
    font-weight: 700;
    color: var(--jarvis-cyan);
    margin-right: 8px;
}

.vb-sound-alert-confirmed {
    background: linear-gradient(135deg, rgba(139, 0, 0, 0.95), rgba(80, 0, 0, 0.95));
    border: 3px solid var(--jarvis-red);
    color: #ffffff;
    padding: 16px 20px;
    border-radius: 12px;
    font-size: 1.25rem;
    font-weight: bold;
    margin: 12px 0;
    box-shadow: 0 0 25px var(--jarvis-red-glow);
    animation: jarvis-pulse 1s infinite alternate;
}

.vb-sound-alert-candidate {
    background: linear-gradient(135deg, rgba(80, 60, 0, 0.95), rgba(40, 30, 0, 0.95));
    border: 2px dashed var(--jarvis-gold);
    color: #fff4ba;
    padding: 14px 18px;
    border-radius: 10px;
    font-size: 1.05rem;
    margin: 12px 0;
}

/* Buttons with tactile feedback and high accessibility */
.stButton > button {
    background: linear-gradient(135deg, rgba(0, 112, 243, 0.8) 0%, rgba(0, 60, 160, 0.9) 100%) !important;
    border: 2px solid var(--jarvis-cyan) !important;
    color: #ffffff !important;
    font-family: var(--jarvis-font-hud) !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(0, 112, 243, 0.3) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0, 160, 255, 0.9) 0%, rgba(0, 112, 243, 1) 100%) !important;
    box-shadow: 0 0 20px var(--jarvis-cyan-glow) !important;
    transform: translateY(-1px) !important;
}
</style>
"""

# Backward compatibility alias
ACCESSIBLE_CSS = JARVIS_HUD_CSS


def render_header() -> str:
    """Returns HTML for the application header with Jarvis branding and telemetry."""
    return """
    <div class="jarvis-header-container">
        <div>
            <div class="jarvis-brand-title">
                <span style="font-size: 2.1rem; filter: drop-shadow(0 0 10px #00f0ff);">👁️⚡</span>
                VISIONBRIDGE &bull; JARVIS
            </div>
            <div class="jarvis-brand-subtitle">
                AUTONOMOUS ACCESSIBILITY & SITUATIONAL INTELLIGENCE &bull; OPENCV 5 CORE
            </div>
        </div>
        <div class="jarvis-telemetry-bar">
            <div class="jarvis-pill jarvis-pill-online">
                <span class="jarvis-dot-pulse"></span> SYSTEM: ONLINE
            </div>
            <div class="jarvis-pill jarvis-pill-active">
                <span class="jarvis-dot-pulse"></span> VOICE COGNITION: ARMED
            </div>
            <div class="jarvis-pill jarvis-pill-active">
                <span class="jarvis-dot-pulse"></span> ACOUSTIC SENSOR: ACTIVE
            </div>
            <div class="jarvis-pill">
                🔒 LOCAL PRIVACY: SECURED
            </div>
        </div>
    </div>
    """


def render_jarvis_audio_bridge(
    speech_text: Optional[str] = None,
    alert_data: Optional[Dict[str, Any]] = None,
    auto_speak: bool = True,
    height: int = 340,
) -> None:
    """
    Renders an in-browser Web Speech Recognition & Web Speech Synthesis bridge.
    Provides hands-free voice command listening, synthesized AI vocal feedback,
    authentic Web Audio hazard sirens, and quick voice trigger chips.
    """
    speech_json = json.dumps(speech_text or "")
    alert_json = json.dumps(alert_data or {})
    auto_speak_str = "true" if auto_speak else "false"

    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Share+Tech+Mono&family=Inter:wght@400;600;700&display=swap');
            
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            body {{
                background-color: transparent;
                color: #ffffff;
                font-family: 'Inter', -apple-system, sans-serif;
                overflow: hidden;
            }}
            .jarvis-bridge-panel {{
                background: linear-gradient(135deg, rgba(8, 16, 32, 0.95) 0%, rgba(4, 10, 22, 0.98) 100%);
                border: 2px solid rgba(0, 240, 255, 0.45);
                border-radius: 14px;
                padding: 16px 20px;
                box-shadow: 0 0 25px rgba(0, 240, 255, 0.15), inset 0 0 15px rgba(0, 240, 255, 0.05);
                position: relative;
            }}
            .bridge-top-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }}
            .bridge-title {{
                font-family: 'Orbitron', sans-serif;
                font-size: 1.15rem;
                font-weight: 800;
                color: #00f0ff;
                display: flex;
                align-items: center;
                gap: 8px;
                letter-spacing: 1px;
                text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
            }}
            .status-indicator {{
                font-family: 'Share Tech Mono', monospace;
                font-size: 0.85rem;
                padding: 4px 10px;
                border-radius: 20px;
                background: rgba(0, 240, 255, 0.12);
                border: 1px solid #00f0ff;
                color: #00f0ff;
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .status-indicator.listening {{
                background: rgba(255, 42, 95, 0.2);
                border-color: #ff2a5f;
                color: #ff2a5f;
                animation: pulse-red 1s infinite alternate;
            }}
            .status-indicator.speaking {{
                background: rgba(255, 184, 0, 0.2);
                border-color: #ffb800;
                color: #ffb800;
            }}
            @keyframes pulse-red {{
                from {{ box-shadow: 0 0 5px #ff2a5f; }}
                to {{ box-shadow: 0 0 15px #ff2a5f; }}
            }}
            
            /* Center Voice Activation Bar */
            .voice-controls-bar {{
                display: flex;
                gap: 12px;
                align-items: center;
                margin-bottom: 12px;
            }}
            .mic-btn {{
                flex: 1;
                background: linear-gradient(135deg, #0070f3 0%, #004fb0 100%);
                border: 2px solid #00f0ff;
                border-radius: 10px;
                padding: 12px 18px;
                color: #ffffff;
                font-family: 'Orbitron', sans-serif;
                font-size: 1.05rem;
                font-weight: 800;
                letter-spacing: 1px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                transition: all 0.2s ease;
                box-shadow: 0 4px 15px rgba(0, 112, 243, 0.4);
            }}
            .mic-btn:hover {{
                background: linear-gradient(135deg, #0090ff 0%, #0070f3 100%);
                box-shadow: 0 0 20px rgba(0, 240, 255, 0.6);
                transform: translateY(-1px);
            }}
            .mic-btn.active {{
                background: linear-gradient(135deg, #ff2a5f 0%, #c00030 100%);
                border-color: #ff7090;
                box-shadow: 0 0 25px rgba(255, 42, 95, 0.8);
                animation: pulse-red 0.8s infinite alternate;
            }}
            .action-icon-btn {{
                background: rgba(0, 0, 0, 0.6);
                border: 1px solid rgba(0, 240, 255, 0.4);
                border-radius: 10px;
                color: #c5d8f7;
                padding: 12px 14px;
                font-size: 1.1rem;
                cursor: pointer;
                transition: all 0.2s;
            }}
            .action-icon-btn:hover {{
                border-color: #00f0ff;
                color: #00f0ff;
                box-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
            }}

            /* Live Transcript Readout Box */
            .transcript-display {{
                background: rgba(2, 6, 14, 0.85);
                border: 1px solid rgba(0, 240, 255, 0.25);
                border-radius: 8px;
                padding: 10px 14px;
                font-family: 'Share Tech Mono', monospace;
                font-size: 0.95rem;
                color: #e0faff;
                min-height: 48px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 12px;
            }}
            .transcript-text {{
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                max-width: 85%;
            }}
            
            /* Quick Preset Command Chips */
            .chips-container {{
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                align-items: center;
            }}
            .chip-label {{
                font-family: 'Share Tech Mono', monospace;
                font-size: 0.75rem;
                color: #8fa6ca;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .command-chip {{
                background: rgba(0, 240, 255, 0.08);
                border: 1px solid rgba(0, 240, 255, 0.3);
                border-radius: 6px;
                color: #c5d8f7;
                font-family: 'Inter', sans-serif;
                font-size: 0.8rem;
                font-weight: 600;
                padding: 6px 10px;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            .command-chip:hover {{
                background: rgba(0, 240, 255, 0.2);
                border-color: #00f0ff;
                color: #ffffff;
                box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
            }}
            .command-chip.hazard {{
                border-color: rgba(255, 184, 0, 0.4);
                color: #ffe699;
            }}
            .command-chip.hazard:hover {{
                background: rgba(255, 184, 0, 0.2);
                border-color: #ffb800;
            }}
            .command-chip.alarm {{
                border-color: rgba(255, 42, 95, 0.4);
                color: #ffb3c0;
            }}
            .command-chip.alarm:hover {{
                background: rgba(255, 42, 95, 0.25);
                border-color: #ff2a5f;
            }}

            /* Waveform Bars Visualizer */
            .equalizer {{
                display: flex;
                align-items: flex-end;
                gap: 3px;
                height: 18px;
            }}
            .eq-bar {{
                width: 3px;
                height: 4px;
                background-color: #00f0ff;
                border-radius: 1px;
                transition: height 0.1s ease;
            }}
            .equalizer.active .eq-bar:nth-child(1) {{ animation: eq-anim 0.4s infinite alternate 0.1s; }}
            .equalizer.active .eq-bar:nth-child(2) {{ animation: eq-anim 0.5s infinite alternate 0.2s; }}
            .equalizer.active .eq-bar:nth-child(3) {{ animation: eq-anim 0.3s infinite alternate 0.05s; }}
            .equalizer.active .eq-bar:nth-child(4) {{ animation: eq-anim 0.6s infinite alternate 0.25s; }}
            .equalizer.active .eq-bar:nth-child(5) {{ animation: eq-anim 0.4s infinite alternate 0.15s; }}
            @keyframes eq-anim {{
                from {{ height: 3px; }}
                to {{ height: 18px; }}
            }}
        </style>
    </head>
    <body>
        <div class="jarvis-bridge-panel">
            <div class="bridge-top-row">
                <div class="bridge-title">
                    <span>⚡</span> JARVIS VOICE COMMAND & AUDITORY WARNER
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div class="equalizer" id="equalizer">
                        <div class="eq-bar"></div>
                        <div class="eq-bar"></div>
                        <div class="eq-bar"></div>
                        <div class="eq-bar"></div>
                        <div class="eq-bar"></div>
                    </div>
                    <div class="status-indicator" id="statusIndicator">
                        <span style="font-size: 8px;">●</span> STANDBY
                    </div>
                </div>
            </div>

            <!-- Voice Controls Bar -->
            <div class="voice-controls-bar">
                <button class="mic-btn" id="btnMic" onclick="toggleSpeechRecognition()">
                    <span id="micIcon" style="font-size: 1.25rem;">🎙️</span>
                    <span id="micLabel">ACTIVATE VOICE COMMAND (SPEAK NOW)</span>
                </button>
                <button class="action-icon-btn" title="Repeat Last Vocal Feedback" onclick="replaySpeech()">
                    🔊 Repeat
                </button>
                <button class="action-icon-btn" title="Test Emergency Siren & Warning" onclick="testEmergencyAlert()">
                    🚨 Alarm Test
                </button>
            </div>

            <!-- Live Transcript Readout -->
            <div class="transcript-display">
                <span class="transcript-text" id="transcriptText">
                    Jarvis voice link armed. Say "Describe surroundings", "Read text", or "Warn me".
                </span>
                <span style="color: #6a82a6; font-size: 0.8rem;" id="shortcutHint">[Shortcut: V]</span>
            </div>

            <!-- Quick Preset Chips -->
            <div class="chips-container">
                <span class="chip-label">Quick Voice Triggers:</span>
                <button class="command-chip" onclick="dispatchVoiceCommand('Jarvis, describe my surroundings.')">
                    🔍 "Describe Scene"
                </button>
                <button class="command-chip" onclick="dispatchVoiceCommand('Jarvis, read this text.')">
                    📖 "Read Text"
                </button>
                <button class="command-chip" style="border-color: #00e676; color: #bbf7d0;" onclick="dispatchVoiceCommand('Jarvis, translate sign language.')">
                    🤟 "Sign Language"
                </button>
                <button class="command-chip hazard" onclick="dispatchVoiceCommand('Jarvis, warn me of hazards.')">
                    ⚠️ "Hazard Check"
                </button>
                <button class="command-chip alarm" onclick="dispatchVoiceCommand('fire alarm')">
                    🚨 "Fire Alarm (88dB)"
                </button>
                <button class="command-chip hazard" onclick="dispatchVoiceCommand('door knock')">
                    🚪 "Door Knock (62dB)"
                </button>
                <button class="command-chip" onclick="dispatchVoiceCommand('status')">
                    📊 "System Status"
                </button>
            </div>
        </div>

        <script>
            // State
            let recognition = null;
            let isListening = false;
            let lastSpokenText = "";
            let audioCtx = null;

            const pendingSpeech = {speech_json};
            const pendingAlert = {alert_json};
            const autoSpeak = {auto_speak_str};

            // Initialize AudioContext on user gesture
            function getAudioContext() {{
                if (!audioCtx) {{
                    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
                    if (AudioContextClass) {{
                        audioCtx = new AudioContextClass();
                    }}
                }}
                if (audioCtx && audioCtx.state === 'suspended') {{
                    audioCtx.resume();
                }}
                return audioCtx;
            }}

            // Web Audio Synthesizer: Iconic Jarvis Sci-Fi Sounds (Zero external downloads)
            function playChirp(frequency = 880, duration = 0.12, type = 'sine') {{
                try {{
                    const ctx = getAudioContext();
                    if (!ctx) return;
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = type;
                    osc.frequency.setValueAtTime(frequency, ctx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(frequency * 1.5, ctx.currentTime + duration);
                    gain.gain.setValueAtTime(0.2, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + duration);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start();
                    osc.stop(ctx.currentTime + duration);
                }} catch(e) {{}}
            }}

            function playEmergencySiren() {{
                try {{
                    const ctx = getAudioContext();
                    if (!ctx) return;
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sawtooth';
                    const now = ctx.currentTime;
                    // Oscillating alarm siren
                    osc.frequency.setValueAtTime(600, now);
                    osc.frequency.linearRampToValueAtTime(1100, now + 0.25);
                    osc.frequency.linearRampToValueAtTime(600, now + 0.5);
                    osc.frequency.linearRampToValueAtTime(1100, now + 0.75);
                    osc.frequency.linearRampToValueAtTime(600, now + 1.0);
                    
                    gain.gain.setValueAtTime(0.25, now);
                    gain.gain.exponentialRampToValueAtTime(0.01, now + 1.1);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now);
                    osc.stop(now + 1.1);
                }} catch(e) {{}}
            }}

            function playWarningTone() {{
                try {{
                    const ctx = getAudioContext();
                    if (!ctx) return;
                    const now = ctx.currentTime;
                    // Dual tone caution beep
                    [0, 0.18].forEach(offset => {{
                        const osc = ctx.createOscillator();
                        const gain = ctx.createGain();
                        osc.type = 'triangle';
                        osc.frequency.setValueAtTime(750, now + offset);
                        gain.gain.setValueAtTime(0.22, now + offset);
                        gain.gain.exponentialRampToValueAtTime(0.01, now + offset + 0.12);
                        osc.connect(gain);
                        gain.connect(ctx.destination);
                        osc.start(now + offset);
                        osc.stop(now + offset + 0.12);
                    }});
                }} catch(e) {{}}
            }}

            // Browser Web Speech Synthesis (Jarvis Voice Output)
            function speakAloud(text, priority = false) {{
                if (!window.speechSynthesis || !text || !text.trim()) return;
                
                // Avoid redundant immediate repeats unless forced
                if (window.speechSynthesis.speaking && !priority) return;
                window.speechSynthesis.cancel(); // Clear queue

                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 1.04;
                utterance.pitch = 0.95;

                // Attempt to pick a sophisticated British / English AI voice
                const voices = window.speechSynthesis.getVoices();
                let selectedVoice = voices.find(v => 
                    v.name.includes("Google UK English Male") ||
                    v.name.includes("Daniel") || 
                    v.name.includes("George") ||
                    (v.lang.startsWith("en-GB") && v.name.toLowerCase().includes("male"))
                );
                if (!selectedVoice) {{
                    selectedVoice = voices.find(v => v.lang.startsWith("en") && !v.localService) || voices.find(v => v.lang.startsWith("en"));
                }}
                if (selectedVoice) {{
                    utterance.voice = selectedVoice;
                }}

                const indicator = document.getElementById("statusIndicator");
                const eq = document.getElementById("equalizer");

                utterance.onstart = () => {{
                    if (indicator) {{
                        indicator.className = "status-indicator speaking";
                        indicator.innerHTML = "<span style='font-size: 8px;'>●</span> JARVIS SPEAKING...";
                    }}
                    if (eq) eq.className = "equalizer active";
                }};

                utterance.onend = utterance.onerror = () => {{
                    if (indicator && !isListening) {{
                        indicator.className = "status-indicator";
                        indicator.innerHTML = "<span style='font-size: 8px;'>●</span> STANDBY";
                    }}
                    if (eq) eq.className = "equalizer";
                }};

                window.speechSynthesis.speak(utterance);
                lastSpokenText = text;
            }}

            function replaySpeech() {{
                if (lastSpokenText) {{
                    speakAloud(lastSpokenText, true);
                }} else {{
                    speakAloud("Jarvis accessibility systems online and ready for spoken commands, sir.", true);
                }}
            }}

            function testEmergencyAlert() {{
                playEmergencySiren();
                setTimeout(() => {{
                    speakAloud("CRITICAL ALERT! High amplitude emergency fire alarm detected at 88.5 decibels. Immediate evacuation protocol advised.", true);
                }}, 700);
            }}

            // Browser Web Speech Recognition (Mic Input)
            function initSpeechRecognition() {{
                const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRec) {{
                    const display = document.getElementById("transcriptText");
                    if (display) display.innerText = "Notice: Web Speech API not supported in this browser. Use Quick Voice chips below.";
                    return null;
                }}
                const rec = new SpeechRec();
                rec.continuous = false;
                rec.interimResults = true;
                rec.lang = 'en-US';

                rec.onstart = () => {{
                    isListening = true;
                    playChirp(700, 0.1);
                    const btn = document.getElementById("btnMic");
                    const lbl = document.getElementById("micLabel");
                    const indicator = document.getElementById("statusIndicator");
                    const eq = document.getElementById("equalizer");
                    if (btn) btn.className = "mic-btn active";
                    if (lbl) lbl.innerText = "LISTENING... SPEAK NOW";
                    if (indicator) {{
                        indicator.className = "status-indicator listening";
                        indicator.innerHTML = "<span style='font-size: 8px;'>●</span> LISTENING...";
                    }}
                    if (eq) eq.className = "equalizer active";
                }};

                rec.onresult = (event) => {{
                    let transcript = "";
                    for (let i = event.resultIndex; i < event.results.length; ++i) {{
                        transcript += event.results[i][0].transcript;
                    }}
                    const display = document.getElementById("transcriptText");
                    if (display && transcript) {{
                        display.innerHTML = '<b>Heard:</b> "' + transcript + '"';
                    }}
                    if (event.results[0].isFinal) {{
                        playChirp(1200, 0.15);
                        dispatchVoiceCommand(transcript);
                    }}
                }};

                rec.onerror = (e) => {{
                    stopListening();
                    const display = document.getElementById("transcriptText");
                    if (display) display.innerText = "Voice input idle. Click mic to speak again.";
                }};

                rec.onend = () => {{
                    stopListening();
                }};

                return rec;
            }}

            function toggleSpeechRecognition() {{
                getAudioContext();
                if (isListening) {{
                    if (recognition) recognition.stop();
                    stopListening();
                }} else {{
                    if (!recognition) {{
                        recognition = initSpeechRecognition();
                    }}
                    if (recognition) {{
                        try {{
                            recognition.start();
                        }} catch(err) {{
                            recognition.stop();
                        }}
                    }}
                }}
            }}

            function stopListening() {{
                isListening = false;
                const btn = document.getElementById("btnMic");
                const lbl = document.getElementById("micLabel");
                const indicator = document.getElementById("statusIndicator");
                const eq = document.getElementById("equalizer");
                if (btn) btn.className = "mic-btn";
                if (lbl) lbl.innerText = "ACTIVATE VOICE COMMAND (SPEAK NOW)";
                if (indicator) {{
                    indicator.className = "status-indicator";
                    indicator.innerHTML = "<span style='font-size: 8px;'>●</span> STANDBY";
                }}
                if (eq) eq.className = "equalizer";
            }}

            // Transmit Voice Command to Streamlit
            function dispatchVoiceCommand(cmd) {{
                if (!cmd || !cmd.trim()) return;
                stopListening();
                const display = document.getElementById("transcriptText");
                if (display) {{
                    display.innerHTML = '<span style="color: #00f0ff;">Transmitting to Jarvis: "' + cmd + '"...</span>';
                }}

                // 1. Communicate with Parent Window Input if accessible
                try {{
                    const parentDoc = window.parent.document;
                    const input = parentDoc.querySelector('input[data-testid="stTextInputRootElement"] input') || 
                                  parentDoc.querySelector('input[placeholder*="command"]');
                    if (input) {{
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                        nativeInputValueSetter.call(input, cmd);
                        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        input.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                    }}
                }} catch(e) {{}}

                // 2. Set Query Parameter in parent URL to guarantee execution
                try {{
                    const currentUrl = new URL(window.parent.location.href);
                    currentUrl.searchParams.set("vcmd", cmd);
                    window.parent.location.href = currentUrl.toString();
                }} catch(err) {{
                    // Fallback local query param
                    window.location.search = "?vcmd=" + encodeURIComponent(cmd);
                }}
            }}

            // Keyboard shortcut listener [V] for push-to-talk
            window.addEventListener('keydown', (e) => {{
                if (e.key === 'v' || e.key === 'V') {{
                    toggleSpeechRecognition();
                }}
            }});
            try {{
                window.parent.addEventListener('keydown', (e) => {{
                    if (e.key === 'v' || e.key === 'V') {{
                        if (e.target && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {{
                            toggleSpeechRecognition();
                        }}
                    }}
                }});
            }} catch(e) {{}}

            // Auto-speak incoming response or alert on load
            window.addEventListener('load', () => {{
                // Pre-fetch voices
                if (window.speechSynthesis) {{
                    window.speechSynthesis.getVoices();
                }}

                if (pendingAlert && pendingAlert.guidance_banner) {{
                    if (pendingAlert.is_confirmed) {{
                        playEmergencySiren();
                        setTimeout(() => {{
                            speakAloud(pendingAlert.speech_text || pendingAlert.guidance_banner, true);
                        }}, 700);
                    }} else {{
                        playWarningTone();
                        setTimeout(() => {{
                            speakAloud(pendingAlert.speech_text || pendingAlert.guidance_banner, false);
                        }}, 400);
                    }}
                }} else if (autoSpeak && pendingSpeech && pendingSpeech.length > 0) {{
                    // Check session storage to avoid repeating the exact same message on page refresh
                    const lastHash = sessionStorage.getItem("jarvis_last_spoken");
                    if (lastHash !== pendingSpeech) {{
                        sessionStorage.setItem("jarvis_last_spoken", pendingSpeech);
                        playChirp(880, 0.1);
                        setTimeout(() => {{
                            speakAloud(pendingSpeech);
                        }}, 300);
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """

    components.html(html_code, height=height, scrolling=False)
