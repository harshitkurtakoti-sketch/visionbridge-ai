"""
Accessible UI Styles and Components for VisionBridge AI.

Implements WCAG 2.2 AAA high-contrast standards, ARIA landmark semantics,
large-target controls, live visual captions, and acoustic indicators
for deaf, hard-of-hearing, blind, and low-vision users.
"""

ACCESSIBLE_CSS = """
<style>
/* VisionBridge AI - High-Contrast Accessibility Theme (WCAG AAA) */
:root {
    --vb-bg: #0b0f19;
    --vb-panel: #151d30;
    --vb-panel-border: #283655;
    --vb-text-primary: #ffffff;
    --vb-text-secondary: #c5d1eb;
    --vb-accent: #00d2ff;
    --vb-accent-hover: #33dcff;
    --vb-warning: #ffb800;
    --vb-danger: #ff3b30;
    --vb-success: #00e676;
    --vb-font-size-base: 18px;
}

body {
    background-color: var(--vb-bg) !important;
    color: var(--vb-text-primary) !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    font-size: var(--vb-font-size-base) !important;
}

/* Accessible Large Action Buttons */
.vb-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 60px;
    padding: 14px 28px;
    font-size: 1.25rem;
    font-weight: 700;
    border-radius: 12px;
    border: 3px solid transparent;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    text-decoration: none;
    outline: none;
}

.vb-btn:focus-visible {
    border-color: #ffffff !important;
    box-shadow: 0 0 0 4px var(--vb-accent) !important;
}

.vb-btn-primary {
    background-color: #0070f3;
    color: #ffffff;
}
.vb-btn-primary:hover {
    background-color: #1a82ff;
}

.vb-btn-action {
    background-color: #00b4d8;
    color: #0b0f19;
}
.vb-btn-action:hover {
    background-color: #48cae4;
}

.vb-btn-danger {
    background-color: #d90429;
    color: #ffffff;
}

/* Privacy Indicator Badge */
.vb-privacy-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.95rem;
    font-weight: 600;
}
.vb-privacy-active {
    background-color: rgba(0, 230, 118, 0.2);
    border: 1px solid var(--vb-success);
    color: var(--vb-success);
}
.vb-privacy-idle {
    background-color: rgba(255, 59, 48, 0.2);
    border: 1px solid var(--vb-danger);
    color: #ff8a80;
}
.vb-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
}
.vb-dot-green {
    background-color: var(--vb-success);
    box-shadow: 0 0 8px var(--vb-success);
}
.vb-dot-red {
    background-color: var(--vb-danger);
}

/* Large Captions Panel for Deaf & Hard-of-Hearing Users */
.vb-captions-container {
    background-color: #000000;
    border: 3px solid var(--vb-accent);
    border-radius: 14px;
    padding: 20px;
    min-height: 160px;
    max-height: 320px;
    overflow-y: auto;
    font-size: 1.4rem;
    line-height: 1.6;
    color: #ffffff;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
}

.vb-caption-entry {
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid #333333;
}
.vb-caption-speaker {
    font-weight: bold;
    color: var(--vb-warning);
    margin-right: 8px;
}

/* Acoustic Alert Banner */
.vb-sound-alert-confirmed {
    background-color: #8b0000;
    border: 3px solid #ff2d55;
    color: #ffffff;
    padding: 16px;
    border-radius: 10px;
    font-size: 1.3rem;
    font-weight: bold;
    margin: 12px 0;
    animation: pulse-alert 1.2s infinite alternate;
}
.vb-sound-alert-candidate {
    background-color: #4a3b00;
    border: 2px dashed #ffcc00;
    color: #fff2a3;
    padding: 12px;
    border-radius: 8px;
    font-size: 1.1rem;
    margin: 12px 0;
}

@keyframes pulse-alert {
    from { box-shadow: 0 0 10px #ff2d55; }
    to { box-shadow: 0 0 25px #ff2d55; }
}

/* Keyboard Shortcut Helper */
.vb-shortcut-tag {
    background: #2a3b5c;
    color: #ffffff;
    padding: 2px 8px;
    border-radius: 6px;
    font-family: monospace;
    font-weight: bold;
    margin-left: 6px;
    border: 1px solid #4a6fa5;
}
</style>
"""


def render_header():
    """Returns HTML for the application header with privacy indicator."""
    return """
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #283655; padding-bottom: 15px; margin-bottom: 20px;">
        <div>
            <h1 style="color: #00d2ff; margin: 0; font-size: 2.2rem; font-weight: 800;">
                VisionBridge AI <span style="font-size: 1.1rem; color: #ffb800; font-weight: 400;">| Jarvis for Accessibility</span>
            </h1>
            <p style="color: #c5d1eb; margin: 4px 0 0 0; font-size: 1.05rem;">
                OpenCV AI Competition 2026 &bull; Assistive Vision & Audio System
            </p>
        </div>
    </div>
    """
