"""
Generates standard benchmark evaluation images for VisionBridge AI.
Includes indoor scene, high-contrast sign, blurry label, and low-light scene.
"""

from pathlib import Path
import cv2
import numpy as np

SAMPLE_DIR = Path(__file__).resolve().parent / "sample_images"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)


def create_sample_images():
    # 1. Indoor Scene with person, cup, desk
    indoor = np.zeros((480, 640, 3), dtype=np.uint8)
    indoor[:, :] = (45, 40, 40)
    # Desk
    cv2.rectangle(indoor, (40, 320), (600, 470), (80, 75, 95), -1)
    # Cup
    cv2.rectangle(indoor, (130, 240), (190, 340), (190, 110, 60), -1)
    cv2.putText(indoor, "Cup", (135, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    # Book / Sign
    cv2.rectangle(indoor, (240, 300), (420, 380), (230, 230, 230), -1)
    cv2.putText(indoor, "EXIT SIGN", (260, 345), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (20, 20, 20), 2)
    # Person
    cv2.circle(indoor, (510, 170), 35, (110, 150, 190), -1)
    cv2.rectangle(indoor, (470, 205), (550, 340), (110, 150, 190), -1)
    cv2.imwrite(str(SAMPLE_DIR / "indoor_room.jpg"), indoor)
    print("Created indoor_room.jpg")

    # 2. Emergency Exit Sign (High Contrast)
    exit_sign = np.full((160, 480, 3), (25, 140, 30), dtype=np.uint8)  # Accessible green
    cv2.rectangle(exit_sign, (10, 10), (470, 150), (255, 255, 255), 4)
    cv2.putText(exit_sign, "EMERGENCY EXIT", (35, 95), cv2.FONT_HERSHEY_DUPLEX, 1.2, (255, 255, 255), 3)
    cv2.imwrite(str(SAMPLE_DIR / "emergency_exit_sign.jpg"), exit_sign)
    print("Created emergency_exit_sign.jpg")

    # 3. Blurry medicine label (testing blur detection)
    sharp_label = np.full((180, 400, 3), 245, dtype=np.uint8)
    cv2.putText(sharp_label, "ASPIRIN 500mg", (30, 95), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (15, 15, 15), 2)
    cv2.putText(sharp_label, "Take with water", (40, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 50, 50), 1)
    # Apply severe Gaussian blur
    blurry = cv2.GaussianBlur(sharp_label, (25, 25), 10.0)
    cv2.imwrite(str(SAMPLE_DIR / "blurry_label.jpg"), blurry)
    print("Created blurry_label.jpg")

    # 4. Low-Light Corridor (testing CLAHE and low-light warning)
    low_light = np.zeros((480, 640, 3), dtype=np.uint8)
    low_light[:, :] = (20, 18, 18)
    # Dim silhouette
    cv2.rectangle(low_light, (260, 200), (380, 420), (38, 35, 35), -1)
    cv2.putText(low_light, "RESTROOM", (270, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (55, 55, 55), 1)
    cv2.imwrite(str(SAMPLE_DIR / "low_light_corridor.jpg"), low_light)
    print("Created low_light_corridor.jpg")


if __name__ == "__main__":
    create_sample_images()
