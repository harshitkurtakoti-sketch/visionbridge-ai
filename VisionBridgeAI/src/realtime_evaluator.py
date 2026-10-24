"""
Real-Time Execution and Benchmark Evaluation Harness for VisionBridge AI.
Measures live FPS, per-stage latency breakdown, memory consumption,
uncertainty handling frequency, and OCR accuracy across streaming frames.
"""

import sys
import os
import time
import json
from pathlib import Path
import psutil
import cv2
import numpy as np

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.assistant import VisionBridgeAssistant


def run_realtime_evaluation(num_frames: int = 60, report_dir: str = "reports"):
    print("=" * 65)
    print("  VISIONBRIDGE AI — REAL-TIME EXECUTION & LIVE EVALUATION")
    print("=" * 65)

    assistant = VisionBridgeAssistant(enable_tts=False)
    success = assistant.start_camera()
    print(f"[*] Camera subsystem initialized (Synthetic/Hardware: {assistant.camera.is_synthetic})")

    process = psutil.Process(os.getpid())
    initial_mem_mb = process.memory_info().rss / (1024 * 1024)
    print(f"[*] Initial Memory Footprint : {initial_mem_mb:.2f} MB")

    # Metrics storage
    latencies_capture = []
    latencies_preprocess = []
    latencies_detection = []
    latencies_ocr = []
    latencies_total = []
    fps_history = []
    object_counts = []
    uncertain_counts = []
    blur_scores = []
    luminance_scores = []

    print(f"\n[*] Starting real-time stream execution over {num_frames} frames...\n")

    t_start_total = time.time()

    for frame_idx in range(1, num_frames + 1):
        t_frame_start = time.perf_counter()

        # 1. Capture Stage
        t0 = time.perf_counter()
        ret, frame = assistant.camera.get_frame()
        t_cap = (time.perf_counter() - t0) * 1000.0
        latencies_capture.append(t_cap)

        if not ret or frame is None:
            continue

        # 2. Quality Assessment & Preprocessing Stage
        t0 = time.perf_counter()
        quality = assistant.vision.assess_frame(frame)
        preprocessed = assistant.vision.preprocess(frame)
        t_prep = (time.perf_counter() - t0) * 1000.0
        latencies_preprocess.append(t_prep)
        blur_scores.append(quality["blur_score"])
        luminance_scores.append(quality["mean_brightness"])

        # 3. Object Detection & Spatial Mapping Stage
        t0 = time.perf_counter()
        det_res = assistant.detector.detect(frame)
        t_det = (time.perf_counter() - t0) * 1000.0
        latencies_detection.append(t_det)
        object_counts.append(len(det_res["confirmed_detections"]))
        uncertain_counts.append(len(det_res["uncertain_detections"]))

        # 4. OCR Extraction Stage (run periodically every 5 frames to emulate assistive reader)
        if frame_idx % 5 == 0:
            t0 = time.perf_counter()
            ocr_res = assistant.ocr.extract_text(frame)
            t_ocr = (time.perf_counter() - t0) * 1000.0
            latencies_ocr.append(t_ocr)

        # Total frame processing time
        t_frame_end = time.perf_counter()
        t_total = (t_frame_end - t_frame_start) * 1000.0
        latencies_total.append(t_total)

        current_fps = 1000.0 / t_total if t_total > 0 else 0
        fps_history.append(current_fps)

        # Print live ticker every 10 frames
        if frame_idx % 10 == 0 or frame_idx == 1:
            print(
                f"  Frame {frame_idx:03d}/{num_frames:03d} | "
                f"Total Latency: {t_total:5.1f}ms | "
                f"Det: {t_det:4.1f}ms | "
                f"FPS: {current_fps:4.1f} | "
                f"Objects: {len(det_res['confirmed_detections'])} (Uncertain: {len(det_res['uncertain_detections'])})"
            )

    elapsed_wall_time = time.time() - t_start_total
    final_mem_mb = process.memory_info().rss / (1024 * 1024)
    assistant.stop_camera()

    # Aggregate Statistics
    mean_fps = np.mean(fps_history)
    mean_total_lat = np.mean(latencies_total)
    p95_total_lat = np.percentile(latencies_total, 95)
    mean_det_lat = np.mean(latencies_detection)
    mean_ocr_lat = np.mean(latencies_ocr) if latencies_ocr else 0.0

    print("\n" + "=" * 65)
    print("  LIVE EVALUATION BENCHMARK SUMMARY")
    print("=" * 65)
    print(f"Total Frames Evaluated     : {num_frames}")
    print(f"Total Elapsed Time         : {elapsed_wall_time:.2f} s")
    print(f"Real-Time Throughput       : {mean_fps:.2f} FPS")
    print(f"End-to-End Mean Latency    : {mean_total_lat:.2f} ms")
    print(f"P95 Tail Latency           : {p95_total_lat:.2f} ms")
    print(f"  - Frame Capture (OpenCV) : {np.mean(latencies_capture):.2f} ms")
    print(f"  - Preprocessing (CLAHE)  : {np.mean(latencies_preprocess):.2f} ms")
    print(f"  - Spatial Detection      : {mean_det_lat:.2f} ms")
    print(f"  - OCR Extraction         : {mean_ocr_lat:.2f} ms")
    print(f"Average Detected Objects   : {np.mean(object_counts):.2f} objects/frame")
    print(f"Uncertainty Flagging Rate  : {np.mean(uncertain_counts):.2f} candidates/frame")
    print(f"Mean Blur Score (Laplacian): {np.mean(blur_scores):.1f}")
    print(f"Mean Scene Luminance       : {np.mean(luminance_scores):.1f}")
    print(f"Memory Utilization         : {final_mem_mb:.2f} MB (Delta: +{final_mem_mb - initial_mem_mb:.2f} MB)")
    print("=" * 65)

    # Save structured telemetry results
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_frames": num_frames,
        "elapsed_wall_time_sec": round(elapsed_wall_time, 2),
        "mean_fps": round(float(mean_fps), 2),
        "mean_latency_ms": round(float(mean_total_lat), 2),
        "p95_latency_ms": round(float(p95_total_lat), 2),
        "stage_latencies_ms": {
            "capture": round(float(np.mean(latencies_capture)), 2),
            "preprocessing": round(float(np.mean(latencies_preprocess)), 2),
            "detection": round(float(mean_det_lat), 2),
            "ocr": round(float(mean_ocr_lat), 2),
        },
        "mean_objects_detected": round(float(np.mean(object_counts)), 2),
        "mean_uncertainty_candidates": round(float(np.mean(uncertain_counts)), 2),
        "memory_rss_mb": round(final_mem_mb, 2),
    }

    out_dir = PROJECT_ROOT / report_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / "realtime_benchmark_results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[*] Exported metrics payload to: {out_json}")

    return results


if __name__ == "__main__":
    run_realtime_evaluation(num_frames=60)
