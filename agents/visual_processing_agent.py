import cv2
import mediapipe as mp
import numpy as np
from mediapipe.python.solutions import face_mesh, hands, pose, drawing_utils, drawing_styles

class VisualProcessingAgent:
    def __init__(self):
        # Using the specific imports requested for reliability
        self.mp_face_mesh = face_mesh
        self.mp_hands = hands
        self.mp_pose = pose
        self.mp_drawing = drawing_utils
        self.mp_drawing_styles = drawing_styles

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.hands_detector = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.pose_detector = self.mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def process_frame(self, frame):
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process face, hands, and pose
        face_results = self.face_mesh.process(rgb_frame)
        hand_results = self.hands_detector.process(rgb_frame)
        pose_results = self.pose_detector.process(rgb_frame)

        return {
            "face": face_results,
            "hands": hand_results,
            "pose": pose_results
        }

    def draw_landmarks(self, frame, results):
        annotated_frame = frame.copy()

        # Draw face mesh
        if results["face"].multi_face_landmarks:
            for face_landmarks in results["face"].multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    image=annotated_frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )

        # Draw hands
        if results["hands"].multi_hand_landmarks:
            for hand_landmarks in results["hands"].multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    annotated_frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )

        # Draw pose
        if results["pose"].pose_landmarks:
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                results["pose"].pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )

        return annotated_frame

if __name__ == "__main__":
    # Basic smoke test
    agent = VisualProcessingAgent()
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    res = agent.process_frame(dummy_frame)
    print("Processed dummy frame")
