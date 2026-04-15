from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from agents.orchestrator_agent import OrchestratorAgent
import asyncio
import json
import logging

app = FastAPI(title="AI Interview Orchestra API")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    return {"message": "AI Interview Orchestra API is running"}

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected to stream")

    # Initialize orchestrator (using 0 for camera or a video path)
    # Note: In a real environment without a camera, we might want a simulated source
    orchestrator = OrchestratorAgent(source=0)

    if not orchestrator.start_capture():
        # If camera fails, let's try to simulate or just send an error
        logger.warning("Failed to start camera, streaming will be unavailable or use dummy data.")
        # For demonstration purposes, we'll continue but the run_cycle will return None

    try:
        while True:
            payload = orchestrator.run_cycle()

            if payload:
                await websocket.send_json(payload)
            else:
                # If no frame, send a heartbeat or wait
                await websocket.send_json({"heartbeat": True})

            # Control frame rate (~20 FPS)
            await asyncio.sleep(0.05)

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error in stream: {e}")
    finally:
        orchestrator.stop_capture()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
