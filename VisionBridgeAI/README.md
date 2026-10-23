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

2. **Acoustic Assistance (Deaf & Hard-of-Hearing Users):**
   - High-contrast, large-format live captions conforming to WCAG 2.2 AAA.
   - Environmental sound event detection strictly differentiating between **Confirmed Events** ($\ge 75\text{ dB}$) and **Unconfirmed Sound Candidates** ($< 75\text{ dB}$).
   - Full text-based conversational interaction with the assistant.

3. **Opt-In AWS Cloud Component:**
   - Serverless AWS Lambda on **AWS Graviton (ARM64)** architecture using the **Cloud Optimized OpenCV Library (COOL)**.
   - Strict local-first privacy gate: cloud processing is blocked unless explicit user consent is provided.

---

## 📁 Project Directory Structure

```text
VisionBridgeAI/
├── notebooks/                         # 7 reproducible Jupyter Notebooks
│   ├── 01_environment_dataset.ipynb
│   ├── 02_image_video_processing.ipynb
│   ├── 03_object_detection.ipynb
│   ├── 04_ocr.ipynb
│   ├── 05_speech_accessibility.ipynb
│   ├── 06_evaluation.ipynb
│   └── 07_integration_demo.ipynb
├── src/                               # Core Python Modules
│   ├── __init__.py
│   ├── camera.py                      # Resilient frame capture & synthetic fallback
│   ├── vision.py                      # OpenCV 5 pipeline & spatial mapping
│   ├── object_detection.py            # Object detection, scene describer & uncertainty
│   ├── ocr.py                         # OpenCV 5 OCR preprocessor, CER & WER
│   ├── speech_to_text.py              # Command parser & acoustic event detection
│   ├── text_to_speech.py              # Local pyttsx3 speech synthesis
│   ├── assistant.py                   # Central Jarvis orchestrator
│   └── aws_service.py                 # AWS Lambda & S3 client with privacy gate
├── app/                               # User Interface
│   ├── main.py                        # Streamlit accessible application
│   └── ui.py                          # WCAG AAA styles & accessible components
├── deploy/                            # AWS CloudFormation / SAM deployment
│   ├── lambda_function.py             # OpenCV 5 COOL handler on Graviton
│   └── aws_template.yaml              # Least-privilege IAM, S3 & Lambda template
├── tests/                             # Test Suite
│   ├── test_camera.py
│   ├── test_vision.py
│   ├── test_ocr.py
│   └── test_assistant.py
├── models/
│   └── README.md                      # Model documentation & weights handling
├── data/
│   └── README.md                      # Data guidelines & privacy policy
├── reports/
│   ├── architecture.md                # System architecture document
│   └── evaluation_report.md           # Benchmark and evaluation results
├── requirements.txt                   # Pinned project dependencies
├── .env.example                       # Environment configuration template
├── .gitignore                         # Excludes models, weights, keys & cache
├── LICENSE                            # Apache 2.0 License
└── README.md                          # Main project guide
```

---

## 🚀 Quick Start & Installation

### 1. Clone & Set Up Virtual Environment

```bash
cd VisionBridgeAI
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Verify OpenCV 5 is active:
```bash
python -c "import cv2; print('OpenCV Version:', cv2.__version__)"
# Output: OpenCV Version: 5.0.0.93
```

---

## 🧪 Running the Test Suite

Run unit and integration tests across all modules:

```bash
# Set PYTHONPATH to project root:
# On Windows (PowerShell):
$env:PYTHONPATH="." ; pytest -p no:cacheprovider -v

# On Linux / macOS:
PYTHONPATH=. pytest -v
```

**Results:** 14/14 tests passing (`tests/test_camera.py`, `tests/test_vision.py`, `tests/test_ocr.py`, `tests/test_assistant.py`).

---

## 💻 Running the Application

Launch the interactive accessibility application:

```bash
streamlit run app/main.py
```

### Key Controls & Shortcuts:
- **`[C]`**: Toggle live camera stream (or synthetic assistive test feed).
- **`[D]`**: Describe surroundings with spatial direction and proximity.
- **`[R]`**: Read text and signage using OpenCV 5 OCR binarization.
- **`[S]`**: Query system status and camera lighting/blur quality.
- **Sound Event Simulator**: Trigger simulated environmental sounds to test deaf visual alerts.
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
