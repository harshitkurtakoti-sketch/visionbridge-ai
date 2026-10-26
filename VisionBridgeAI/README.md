# VisionBridge AI — Jarvis for Accessibility
**An Intelligent Multimodal Assistant for Blind, Low-Vision, Deaf, and Hard-of-Hearing Users**  
*Submitted to the OpenCV AI Competition 2026 — Powered by Amazon Web Services (AWS)*

[![OpenCV 5](https://img.shields.io/badge/OpenCV-5.0.0.93-blue.svg)](https://opencv.org/)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-green.svg)](https://python.org/)
[![AWS Graviton](https://img.shields.io/badge/AWS-Graviton%20%7C%20COOL-orange.svg)](https://aws.amazon.com/)
[![Tests Passing](https://img.shields.io/badge/pytest-14%2F14%20passed-brightgreen.svg)]()
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

---

## 🌟 Overview

**VisionBridge AI** is an assistive vision and acoustic communication system inspired by Jarvis. Designed with an unwavering focus on real-world utility, user dignity, and privacy, VisionBridge AI bridges sensory gaps through:

1. **Vision Assistance (Blind & Low-Vision Users):**
   - Live camera stream and image analysis using **OpenCV 5**.
   - Spatial object identification with direction (*"to your left"*, *"directly ahead"*) and proximity estimation.
   - Text reading and signage OCR with adaptive CLAHE contrast enhancement and deskew rotation.
   - Offline, privacy-preserving text-to-speech vocalization.
   - Explicit uncertainty signaling when confident identification is not possible.
   - Clear navigation safety disclaimers (does not claim safe obstacle avoidance).

2. **Acoustic & Deaf Assistance (Deaf, Hard-of-Hearing & Non-Verbal Users):**
   - **Real-Time Sign Language Translation**: Translates American Sign Language (ASL) and hand gestures (Hello, Thank you, Help, Peace, Yes, Good) into live text captions and **vocalized speech output** for hearing companions.
   - High-contrast, large-format live captions conforming to WCAG 2.2 AAA.
   - Environmental sound event detection strictly differentiating between **Confirmed Events** ($\ge 75\text{ dB}$) and **Unconfirmed Sound Candidates** ($< 75\text{ dB}$).
   - In-browser microphone voice commands and Web Audio emergency sirens.

3. **Opt-In AWS Cloud Component:**
   - Serverless AWS Lambda on **AWS Graviton (ARM64)** architecture using the **Cloud Optimized OpenCV Library (COOL)**.
   - Strict local-first privacy gate: cloud processing is blocked unless explicit user consent is provided.

---

## 💻 System Prerequisites (Requirements to Run)

| Requirement | Details |
| :--- | :--- |
| **Python** | Python 3.10, 3.11, 3.12, or 3.13 |
| **OS** | Windows 10/11 (64-bit), Ubuntu 20.04+, or macOS 12.0+ |
| **Hardware** | Camera (integrated or USB webcam), Microphone, Speakers / Audio Output |
| **Browser** | Chrome, Edge, Firefox, or Brave (supporting Web Speech & Web Audio APIs) |
| **OCR (Optional)** | Tesseract OCR (`winget install UB-Mannheim.TesseractOCR` on Windows, `apt-get install tesseract-ocr` on Linux) |

---

## 📁 Project Directory Structure

```text
VisionBridgeAI/
├── notebooks/                         # 7 reproducible Jupyter Notebooks
├── src/                               # Core Python Modules
│   ├── __init__.py
│   ├── assistant.py                   # Central Jarvis orchestrator
│   ├── sign_language.py               # ASL Sign Language recognition & translation
│   ├── camera.py                      # Resilient frame capture & synthetic fallback
│   ├── vision.py                      # OpenCV 5 pipeline & spatial mapping
│   ├── object_detection.py            # Object detection, scene describer & uncertainty
│   ├── ocr.py                         # OpenCV 5 OCR preprocessor, CER & WER
│   ├── speech_to_text.py              # Command parser & acoustic event detection
│   ├── text_to_speech.py              # Local pyttsx3 speech synthesis
│   └── aws_service.py                 # AWS Lambda & S3 client with privacy gate
├── app/                               # User Interface
│   ├── main.py                        # Streamlit accessible application & real-time loop
│   └── ui.py                          # Jarvis HUD styles, audio bridge, and reticle
├── tests/                             # 19 Automated Tests
└── README.md                          # Main project guide
```

---

## 🚀 Quick Start & Installation

### 1. Set Up Virtual Environment

```bash
python -m venv .venv

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On Linux/macOS:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Verify OpenCV:
```bash
python -c "import cv2; print('OpenCV Version:', cv2.__version__)"
```

---

## 🧪 Running the Test Suite

Run unit and integration tests across all modules:

```bash
python -m pytest -v
```

**Results:** **19/19 tests passing** across camera, vision, OCR, assistant, AWS, and sign language translation.

---

## 💻 Running the Application

Launch the interactive Jarvis accessibility application:

```bash
streamlit run app/main.py
```
*(or from project root: `streamlit run streamlit_app.py`)*

### Key Controls & Shortcuts:
- **`[V]`**: Push-to-Talk Voice Command Activation.
- **`[C]`**: Toggle live camera stream (or synthetic assistive test feed).
- **`[D]`**: Describe surroundings with spatial direction and proximity.
- **`[R]`**: Read text and signage using OpenCV 5 OCR binarization.
- **`[T]`**: Translate Sign Language hand gestures (Deaf assist).
- **`[S]`**: Query system status and camera lighting/blur quality.
- **`🔄 Real-Time Live Tracking`**: Continuous 15-30 FPS object detection & sign translation.
- **Sound Event Simulator**: Trigger simulated environmental sounds to test deaf visual alerts and sirens.
- **AWS Cloud Toggle**: Opt-in toggle to test AWS Graviton serverless inference.

---

## 📓 Running the Jupyter Notebooks

Launch Jupyter to explore the step-by-step notebooks:

```bash
jupyter notebook notebooks/
```

- `01_environment_dataset.ipynb`: Environment check & dataset verification.
- `02_image_video_processing.ipynb`: OpenCV 5 frame operations, CLAHE, and blur checks.
- `03_object_detection.ipynb`: Object detection & spatial coordinate mapping.
- `04_ocr.ipynb`: OCR binarization, deskewing, and CER/WER calculations.
- `05_speech_accessibility.ipynb`: Voice commands & acoustic event differentiation.
- `06_evaluation.ipynb`: Empirical latency benchmarks & resource analysis.
- `07_integration_demo.ipynb`: Complete Jarvis integration walkthrough.

---

## ☁️ AWS Integration Details

- **Compute Platform:** AWS Lambda on **ARM64 (AWS Graviton)** using the Cloud Optimized OpenCV Library (COOL).
- **Storage:** Amazon S3 with server-side encryption for benchmark reports.
- **Privacy Assurance:** Strict local-first architecture. Any cloud operation without explicit user consent raises a `PrivacyConsentError`.
- **Deployment Template:** See `deploy/aws_template.yaml` for AWS SAM / CloudFormation specification.

---

## ⚖️ Safety & Ethical Statement

VisionBridge AI provides situational awareness and reading assistance. **Ordinary computer vision object detection does not guarantee obstacle avoidance, hazard detection, or safe navigation.** Users must always rely on primary mobility aids (such as white canes or guide dogs).

---

## 📄 License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
