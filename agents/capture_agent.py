import cv2
import logging
import numpy as np

class CaptureAgent:
    def __init__(self, source=0):
        """
        Initializes the Capture Agent.
        :param source: Camera index or path to a video file.
        """
        self.source = source
        self.cap = None
        self.logger = logging.getLogger(__name__)
        self.simulated = False

    def start(self):
        if self.source == "simulated":
            self.simulated = True
            return True

        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            self.logger.error(f"Could not open video source: {self.source}. Falling back to simulated stream.")
            self.simulated = True
            return True
        return True

    def get_frame(self):
        if self.simulated:
            # Create a dummy frame with some noise/content
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Simulated Stream", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            # Add some random circles to simulate movement
            for _ in range(3):
                center = (np.random.randint(0, 640), np.random.randint(0, 480))
                cv2.circle(frame, center, 20, (0, 255, 0), -1)
            return frame

        if self.cap is None or not self.cap.isOpened():
            return None

        ret, frame = self.cap.read()
        if not ret:
            self.logger.warning("Failed to grab frame")
            return None

        return frame

    def release(self):
        if self.cap:
            self.cap.release()

if __name__ == "__main__":
    # Basic test
    capture = CaptureAgent()
    if capture.start():
        frame = capture.get_frame()
        print(f"Frame captured: {frame is not None}")
        capture.release()
    else:
        print("Failed to start capture agent")
