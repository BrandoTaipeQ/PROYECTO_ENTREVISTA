from agents.capture_agent import CaptureAgent
from agents.visual_processing_agent import VisualProcessingAgent
from agents.behavioral_analysis_agent import BehavioralAnalysisAgent
from agents.visualization_agent import VisualizationAgent
import time

class OrchestratorAgent:
    def __init__(self, source=0):
        self.capture_agent = CaptureAgent(source)
        self.visual_agent = VisualProcessingAgent()
        self.behavioral_agent = BehavioralAnalysisAgent()
        self.viz_agent = VisualizationAgent()
        self.running = False

    def run_cycle(self):
        """
        Executes one cycle of the pipeline.
        Returns the payload to be sent to the dashboard.
        """
        frame = self.capture_agent.get_frame()
        if frame is None:
            return None

        # 1. Process visual landmarks
        landmarks = self.visual_agent.process_frame(frame)

        # 2. Analyze behavior
        analysis = self.behavioral_agent.analyze(landmarks)

        # 3. Draw landmarks on frame for visualization
        annotated_frame = self.visual_agent.draw_landmarks(frame, landmarks)

        # 4. Prepare final payload
        payload = self.viz_agent.prepare_payload(annotated_frame, analysis)

        return payload

    def start_capture(self):
        return self.capture_agent.start()

    def stop_capture(self):
        self.capture_agent.release()

if __name__ == "__main__":
    # Test orchestrator
    orchestrator = OrchestratorAgent()
    if orchestrator.start_capture():
        payload = orchestrator.run_cycle()
        print(f"Cycle run successful: {payload is not None}")
        orchestrator.stop_capture()
