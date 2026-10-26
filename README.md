# VisionBridge AI — Jarvis for Accessibility
### Autonomous Assistive Vision, Acoustic Intelligence & Sign Language Translation
**Submitted for the OpenCV AI Competition 2026**

[![OpenCV 5](https://img.shields.io/badge/OpenCV-5.0.0.93-blue.svg)](https://opencv.org/)
[![Python 3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-green.svg)](https://python.org/)
[![AWS Graviton](https://img.shields.io/badge/AWS-Graviton%20%7C%20COOL-orange.svg)](https://aws.amazon.com/)
[![Tests Passing](https://img.shields.io/badge/pytest-19%2F19%20passed-brightgreen.svg)]()
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

---

## 🌟 Overview

**VisionBridge AI** is an advanced, multimodal accessibility assistant inspired by Iron Man's Jarvis. Engineered with an uncompromising commitment to user dignity, independence, and strict privacy, VisionBridge AI bridges sensory barriers for **blind, low-vision, deaf, hard-of-hearing, and non-verbal users**:

1. **Real-Time Camera & Scene Perception (Blind & Low-Vision)**:
   - Live continuous video object detection with spatial orientation (*"to your left"*, *"directly ahead"*) and proximity estimation.
   - OpenCV 5 signage and document OCR with adaptive CLAHE contrast enhancement and skew angle correction.
   - Proactive auditory hazard collision warnings.

2. **Sign Language Recognition & Translation (Deaf & Non-Verbal Users)**:
   - Real-time American Sign Language (ASL) & universal hand gesture recognition using OpenCV skin contour segmentation and convexity defects.
   - Automatic gesture phrase accumulation and visual subtitles for deaf users.
   - **Speech Vocalization**: Jarvis speaks the translated sign language aloud through browser speakers so hearing companions instantly hear what the deaf person signed.

3. **In-Browser Jarvis Voice Commands & Auditory Warner**:
   - Live microphone voice recognition (`[V]` shortcut & push-to-talk button).
   - Crisp AI speech synthesis output and Web Audio emergency sirens.
   - Acoustic emergency differentiation between **Confirmed Events** ($\ge 75\text{ dB}$, e.g. fire alarms) and **Unconfirmed Candidates** ($< 75\text{ dB}$, e.g. door knocks).

4. **Stark Industries Sci-Fi HUD Interface**:
   - Holographic target reticle overlay on the camera feed with animated sweep lines and telemetry readouts.
   - Dynamic audio waveform visualizer equalizer.
   - WCAG 2.2 AAA high-contrast accessibility compliance.

5. **Opt-In AWS Graviton Cloud Component**:
   - Serverless AWS Lambda on **AWS Graviton (ARM64)** with the **Cloud Optimized OpenCV Library (COOL)**.
   - Strict local-first privacy firewall: cloud upload is blocked by default and requires explicit user consent.

---

## 💻 System Prerequisites (What Must Be Present on Your System)

Before executing VisionBridge AI, verify that your machine meets the following hardware and software requirements:

### 1. Hardware Requirements
| Component | Minimum Requirement | Recommended |
| :--- | :--- | :--- |
| **Processor (CPU)** | Dual-core x86_64 or ARM64 | Quad-core (Intel Core i5+, AMD Ryzen, or Apple Silicon) |
| **RAM** | 4 GB | 8 GB or higher |
| **Webcam / Camera** | Standard integrated webcam or USB camera | 720p / 1080p camera with DirectShow support |
| **Microphone** | Standard built-in or USB microphone | Clear directional microphone for voice commands |
| **Speakers / Headphones** | Any audio output device | Speakers or headphones for Jarvis spoken alerts & warnings |

### 2. Operating System Support
- **Windows**: Windows 10 or Windows 11 (64-bit)
- **Linux**: Ubuntu 20.04+, Debian 11+, Fedora 36+
- **macOS**: macOS Monterey (12.0+), Ventura, Sonoma, or Sequoia (Apple Silicon & Intel)

### 3. Software Dependencies
- **Python**: Version **3.10, 3.11, 3.12, or 3.13** installed.
  - Check with: `python --version`
- **Git**: Installed and on system PATH.
  - Check with: `git --version`
- **Modern Web Browser**: Google Chrome, Microsoft Edge, Brave, or Firefox with Web Speech API and Web Audio API enabled.
- **Tesseract OCR (Optional for Text Reading)**:
  - **Windows**: `winget install UB-Mannheim.TesseractOCR`
  - **Linux (Ubuntu/Debian)**: `sudo apt-get install tesseract-ocr`
  - **macOS (Homebrew)**: `brew install tesseract`

---

## 🚀 How to Execute & Run the Site (Step-by-Step)

Follow these simple instructions to set up and start the website:

### Step 1: Open Terminal / Command Prompt
Open your terminal (PowerShell, Command Prompt, or Bash) and navigate to the project root:
```bash
cd opencv
```

### Step 2: Create & Activate a Python Virtual Environment
Creating a virtual environment ensures dependencies remain isolated and clean:

- **On Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
  *(If execution policies restrict script activation, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first)*

- **On Windows (CMD)**:
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate.bat
  ```

- **On Linux / macOS**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### Step 3: Upgrade pip & Install Required Packages
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify OpenCV Installation
Verify that OpenCV is operational:
```bash
python -c "import cv2; print('OpenCV Version:', cv2.__version__)"
```

### Step 5: Launch the Streamlit Application
Start the interactive VisionBridge AI server:
```bash
streamlit run streamlit_app.py
```
*(Alternative direct launch: `python -m streamlit run VisionBridgeAI/app/main.py`)*

### Step 6: Access in Your Browser
Streamlit will automatically open the site in your default browser. If not, open your browser and navigate to:
```
http://localhost:8501
```

---

## 🎮 How to Use the Jarvis Website & Features

### 1. Activating Real-Time Camera Object Detection
1. Click **▶️ Start Camera [C]** to activate your webcam.
2. Toggle **🔄 Real-Time Live Vision & Gesture Tracking** for continuous 15–30 FPS object detection and gesture classification.
3. Watch the holographic HUD overlay with target brackets, center crosshairs, and live bounding boxes.
4. Click **🔍 Describe [D]** to hear Jarvis describe your surrounding environment, objects, and spatial directions aloud.

### 2. Using Sign Language Translation (Deaf Assist)
1. Point your hand toward the camera.
2. Form standard American Sign Language (ASL) gestures:
   - ✋ **HELLO**: Spread open hand
   - 🙏 **THANK YOU**: Hand angled toward chest
   - 🆘 **HELP**: Fist on palm / Emergency assistance
   - ✌️ **PEACE / 2**: Two fingers upright
   - 👍 **GOOD / YES**: Thumb up
   - ✊ **YES / A**: Solid closed fist
   - 🤟 **I LOVE YOU**: Thumb, index & pinky spread
3. Click **🤟 Sign Lang [T]** or use the quick gesture chips to translate.
4. Jarvis displays the translated sentence banner and **vocalizes it through browser speakers** so hearing companions can understand the deaf user.

### 3. Using In-Browser Voice Commands
1. Click the glowing blue **🎙️ ACTIVATE VOICE COMMAND (SPEAK NOW)** button or press keyboard shortcut **`[V]`**.
2. Speak clearly into your microphone:
   - *"Jarvis, describe surroundings."*
   - *"Jarvis, read this text."*
   - *"Jarvis, translate sign language."*
   - *"Jarvis, warn me of hazards."*
   - *"Jarvis, system status."*
   - *"Fire alarm test."*
3. Jarvis executes the command and answers verbally in real time.

### 4. Acoustic Emergency Alerts & Sound Simulator
1. In the sidebar or sound panel, click **🚨 Fire Alarm (88dB)** or **Door Knock (62dB)**.
2. Confirmed emergencies trigger an immediate **oscillating Web Audio klaxon siren** followed by a high-priority spoken evacuation advisory.

### 5. Keyboard Shortcuts Cheatsheet
| Key | Action |
| :---: | :--- |
| **`[V]`** | Push-to-Talk Voice Command Activation |
| **`[C]`** | Toggle Camera Stream On / Off |
| **`[D]`** | Describe Scene Surroundings & Spatial Objects |
| **`[R]`** | Read Text / OCR Document Extraction |
| **`[T]`** | Translate Sign Language Hand Gesture |
| **`[S]`** | System Diagnostic Status Report |

---

## 🧪 Running the Automated Test Suite

To verify system integrity, run the complete pytest suite:
```powershell
python -m pytest -v
```
**Results:** `19 passed in ~20s` across:
- `tests/test_camera.py`: Hardware camera & synthetic fallback verification
- `tests/test_vision.py`: Spatial mapping, CLAHE, and blur estimation
- `tests/test_ocr.py`: Binarization, character error rate (CER), and deskewing
- `tests/test_assistant.py`: Scene descriptions, voice routing, acoustic alerts, AWS privacy gate, and sign language translation

---

## 📁 Repository Structure

```text
opencv/
├── streamlit_app.py                     # Primary deployment entrypoint (Cloud / Local)
├── requirements.txt                     # Pinned dependencies
├── packages.txt                         # Linux system packages (tesseract-ocr, libgl1)
├── pytest.ini                           # Test configuration
├── Dockerfile                           # Production container specification
├── README.md                            # Main execution guide & documentation
└── VisionBridgeAI/
    ├── app/
    │   ├── main.py                      # Core Streamlit application & live tracking loop
    │   └── ui.py                        # Jarvis HUD styles, audio bridge, and reticle
    ├── src/
    │   ├── assistant.py                 # Central Jarvis orchestrator
    │   ├── sign_language.py             # ASL Sign Language recognition & translation
    │   ├── camera.py                    # Resilient frame capture
    │   ├── vision.py                    # OpenCV 5 image processing & spatial mapper
    │   ├── object_detection.py          # Object detector & scene describer
    │   ├── ocr.py                       # OpenCV 5 OCR preprocessor
    │   ├── speech_to_text.py            # Natural language command parser
    │   ├── text_to_speech.py            # Local offline speech synthesis
    │   └── aws_service.py               # Opt-in AWS Graviton COOL service
    ├── notebooks/                       # 7 reproducible Jupyter research notebooks
    ├── tests/                           # 19 automated unit & integration tests
    ├── reports/                         # Architecture & evaluation reports
    └── README.md                        # VisionBridge AI detailed documentation
```

---

## ⚖️ Safety & Ethical Statement

VisionBridge AI provides situational perception, sign language translation, and accessibility assistance. **Ordinary 2D computer vision object detection does not guarantee detection of all negative ground hazards (e.g. drop-offs or stairwells). Users must always utilize their primary mobility aids (such as white canes or guide dogs).**

---

## 📄 License
This project is licensed under the Apache License 2.0. See [LICENSE](VisionBridgeAI/LICENSE) for details.
