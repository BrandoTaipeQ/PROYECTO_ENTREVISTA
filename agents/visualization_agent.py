import cv2
import base64
import json

class VisualizationAgent:
    def __init__(self):
        pass

    def prepare_payload(self, frame, analysis_results):
        """
        Encodes the frame and merges it with analysis results for transmission.
        """
        # Encode frame to base64
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')

        payload = {
            "image": frame_base64,
            "analysis": analysis_results
        }

        return payload

if __name__ == "__main__":
    import numpy as np
    agent = VisualizationAgent()
    dummy_frame = np.zeros((100, 100, 3), dtype=np.uint8)
    payload = agent.prepare_payload(dummy_frame, {"emotion": "Neutral"})
    print(f"Payload keys: {payload.keys()}")
    print(f"Image length: {len(payload['image'])}")
