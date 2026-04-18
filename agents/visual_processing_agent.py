import cv2
import mediapipe as mp
import numpy as np
import urllib.request
import os

from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')

_MODEL_URLS = {
    'face':  ('face_landmarker.task',      'https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task'),
    'hands': ('hand_landmarker.task',      'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'),
    'pose':  ('pose_landmarker_lite.task', 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task'),
}

def _ensure_model(name):
    os.makedirs(MODELS_DIR, exist_ok=True)
    filename, url = _MODEL_URLS[name]
    path = os.path.join(MODELS_DIR, filename)
    if not os.path.exists(path):
        print(f"Downloading {name} model...")
        urllib.request.urlretrieve(url, path)
        print(f"Downloaded {name} model.")
    return path


class VisualProcessingAgent:
    def __init__(self):
        face_path  = _ensure_model('face')
        hands_path = _ensure_model('hands')
        pose_path  = _ensure_model('pose')

        self.face_landmarker = vision.FaceLandmarker.create_from_options(
            vision.FaceLandmarkerOptions(
                base_options=mp_python.BaseOptions(model_asset_path=face_path),
                num_faces=1,
                min_face_detection_confidence=0.5,
                min_face_presence_confidence=0.5,
                min_tracking_confidence=0.5,
            )
        )
        self.hand_landmarker = vision.HandLandmarker.create_from_options(
            vision.HandLandmarkerOptions(
                base_options=mp_python.BaseOptions(model_asset_path=hands_path),
                num_hands=2,
                min_hand_detection_confidence=0.5,
                min_hand_presence_confidence=0.5,
                min_tracking_confidence=0.5,
            )
        )
        self.pose_landmarker = vision.PoseLandmarker.create_from_options(
            vision.PoseLandmarkerOptions(
                base_options=mp_python.BaseOptions(model_asset_path=pose_path),
                min_pose_detection_confidence=0.5,
                min_pose_presence_confidence=0.5,
                min_tracking_confidence=0.5,
            )
        )

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        return {
            "face":  self.face_landmarker.detect(mp_image),
            "hands": self.hand_landmarker.detect(mp_image),
            "pose":  self.pose_landmarker.detect(mp_image),
        }

    def draw_landmarks(self, frame, results):
        annotated = frame.copy()
        h, w = frame.shape[:2]

        if results["face"].face_landmarks:
            for landmarks in results["face"].face_landmarks:
                for lm in landmarks:
                    cv2.circle(annotated, (int(lm.x * w), int(lm.y * h)), 1, (0, 255, 0), -1)

        if results["hands"].hand_landmarks:
            for landmarks in results["hands"].hand_landmarks:
                for lm in landmarks:
                    cv2.circle(annotated, (int(lm.x * w), int(lm.y * h)), 4, (255, 0, 0), -1)

        if results["pose"].pose_landmarks:
            for landmarks in results["pose"].pose_landmarks:
                for lm in landmarks:
                    cv2.circle(annotated, (int(lm.x * w), int(lm.y * h)), 5, (0, 0, 255), -1)

        return annotated


if __name__ == "__main__":
    agent = VisualProcessingAgent()
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    res = agent.process_frame(dummy_frame)
    print("Processed dummy frame")
