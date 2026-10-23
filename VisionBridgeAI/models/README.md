# VisionBridge AI - Models Directory

This directory contains configuration, labels, and documentation for pretrained deep learning models used by VisionBridge AI.

## Supported Model Architectures

1. **MobileNet SSD / YOLO (OpenCV DNN compatible)**
   - Pretrained on the COCO dataset (80 common object classes).
   - Lightweight, real-time inference suitable for CPU/edge devices and accessible assistive devices.
   - Files:
     - `coco_names.txt` - Labels for the 80 COCO classes.
     - `ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt` or equivalent ONNX / TFLite runtime weights.

2. **OpenCV 5 DNN Engine**
   - Leverages OpenCV 5's modernized Deep Neural Network module with native ONNX support and SIMD/hardware acceleration.
   - Graceful fallback: If external model weights are not pre-downloaded, VisionBridge AI operates a robust contour-based geometric and color-spatial saliency detector, ensuring the vision pipeline remains 100% functional without unhandled crashes.

## Downloading Pretrained Weights

To download the standard COCO-trained MobileNet SSD model:
```bash
python -m src.download_models
```
Model files are excluded from Git via `.gitignore` to keep the repository lightweight and compliant with competition guidelines.
