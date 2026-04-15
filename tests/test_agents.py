import pytest
import numpy as np
from agents.capture_agent import CaptureAgent
from agents.visual_processing_agent import VisualProcessingAgent
from agents.behavioral_analysis_agent import BehavioralAnalysisAgent

def test_capture_agent_init():
    agent = CaptureAgent(source=0)
    assert agent.source == 0

def test_visual_agent_processing():
    agent = VisualProcessingAgent()
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    results = agent.process_frame(dummy_frame)
    assert "face" in results
    assert "hands" in results
    assert "pose" in results

def test_behavioral_agent_analysis():
    agent = BehavioralAnalysisAgent()
    results = agent.analyze({})
    assert "emotion" in results
    assert "metrics" in results
    assert "stress" in results["metrics"]
