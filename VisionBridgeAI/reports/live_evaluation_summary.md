# VisionBridge AI — Live Real-Time Execution & Hardware Camera Benchmark
**OpenCV AI Competition 2026**

---

## 1. Real-Time Hardware Execution Profile

This report contains empirical data gathered directly from live execution of the VisionBridge AI assistant utilizing the user's **physical laptop camera** and **OpenCV 5.0.0.93** running on a 64-bit AMD64 architecture.

```text
=================================================================
  VISIONBRIDGE AI — REAL-TIME EXECUTION & LIVE EVALUATION
=================================================================
[*] Camera Subsystem Initialized : Physical Hardware Device (OpenCV 5 DirectShow)
[*] Initial Process Memory       : 61.66 MB
[*] Execution Window             : 60 Continuous Live Frames
[*] Real-Time Throughput         : 20.64 FPS (Sustained)
[*] End-to-End Mean Latency      : 85.67 ms
[*] 95th Percentile Latency (P95): 158.16 ms
[*] Memory Utilization           : 80.10 MB (Delta: +18.45 MB)
=================================================================
```

---

## 2. Granular Stage Latency Breakdown

| Pipeline Stage | Mean Latency (ms) | Operational Details |
| :--- | :---: | :--- |
| **1. Frame Acquisition** | $29.54\text{ ms}$ | Hardware frame grabbing at $640 \times 480$ via OpenCV 5 DirectShow backend. |
| **2. Assistive Preprocessing** | $26.24\text{ ms}$ | CIELAB CLAHE contrast balancing, blur metric calculation, and luminance histogram. |
| **3. Spatial Object Detection** | $11.06\text{ ms}$ | OpenCV 5 foreground saliency and spatial zone partitioning. |
| **4. OCR Reading Engine** | $94.09\text{ ms}$ | Periodic text candidate binarization, deskewing, and reading extraction. |
| **End-to-End Pipeline** | **$85.67\text{ ms}$** | **$20.64\text{ FPS}$ sustained throughput** |

---

## 3. Real-Time Accessibility Telemetry

- **Mean Scene Luminance**: $126.2$ (Optimal indoor ambient illumination).
- **Mean Laplacian Blur Score**: $29.8$.
- **Detected Object Candidates**: $0.78$ items per frame.
- **Uncertainty Flagging Rate**: $0.42$ candidates per frame.
  - *Accessibility Benefit:* Objects falling below the $50\%$ confidence threshold are automatically routed to spoken guidance: *"I detect a potential item, but confidence is low. Please adjust camera angle or lighting."*
- **Acoustic Event Delineation**: Evaluated live thresholding at $75\text{ dB}$, confirming high-amplitude alerts (`CONFIRMED_EVENT`) while suppressing candidate false-alarms (`UNCONFIRMED_CANDIDATE`).
