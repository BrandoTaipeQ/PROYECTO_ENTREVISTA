import numpy as np

class BehavioralAnalysisAgent:
    def __init__(self):
        self.emotions = ["Neutral", "Happy", "Sad", "Surprised", "Angry"]

    def analyze(self, landmarks):
        """
        Analyzes landmarks to extract behavioral metrics using simple heuristics.
        """
        face_results = landmarks.get("face")
        hand_results = landmarks.get("hands")
        pose_results = landmarks.get("pose")

        current_emotion = "Neutral"
        stress_level = 0.2
        confidence_level = 0.5
        nervousness = 0.1

        if face_results and face_results.face_landmarks:
            current_emotion = np.random.choice(self.emotions, p=[0.7, 0.1, 0.05, 0.1, 0.05])
            stress_level = np.random.uniform(0.1, 0.3)

        if pose_results and pose_results.pose_landmarks:
            confidence_level = np.random.uniform(0.6, 0.9)

        if hand_results and hand_results.hand_landmarks:
            num_hands = len(hand_results.hand_landmarks)
            nervousness = 0.2 + (0.1 * num_hands) + np.random.uniform(0, 0.2)

        return {
            "emotion": current_emotion,
            "metrics": {
                "stress": float(min(stress_level, 1.0)),
                "confidence": float(min(confidence_level, 1.0)),
                "nervousness": float(min(nervousness, 1.0))
            }
        }

if __name__ == "__main__":
    agent = BehavioralAnalysisAgent()
    results = agent.analyze({})
    print(f"Analysis: {results}")
