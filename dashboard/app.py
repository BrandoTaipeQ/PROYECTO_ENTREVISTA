import streamlit as st
import asyncio
import websockets
import json
import base64
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="AI Interview Orchestra Dashboard", layout="wide")

st.title("🎭 Orquesta de Agentes IA - Entrevistas en Vivo")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("📹 Video en Vivo")
    image_placeholder = st.empty()

with col2:
    st.header("📊 Análisis de Comportamiento")
    emotion_placeholder = st.empty()
    stress_placeholder = st.empty()
    confidence_placeholder = st.empty()
    nervousness_placeholder = st.empty()

async def connect_to_stream():
    uri = "ws://localhost:8000/ws/stream"
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)

                if "heartbeat" in data:
                    continue

                # Process image
                img_data = base64.b64decode(data["image"])
                nparr = np.frombuffer(img_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Update UI
                image_placeholder.image(img, channels="RGB", use_column_width=True)

                analysis = data["analysis"]
                emotion_placeholder.metric("Emoción Detectada", analysis["emotion"])

                metrics = analysis["metrics"]
                stress_placeholder.write(f"Estrés: {metrics['stress']:.2f}")
                stress_placeholder.progress(metrics['stress'])

                confidence_placeholder.write(f"Confianza: {metrics['confidence']:.2f}")
                confidence_placeholder.progress(metrics['confidence'])

                nervousness_placeholder.write(f"Nerviosismo: {metrics['nervousness']:.2f}")
                nervousness_placeholder.progress(metrics['nervousness'])

            except Exception as e:
                st.error(f"Error recibiendo datos: {e}")
                break

if st.button("Iniciar Streaming"):
    asyncio.run(connect_to_stream())
else:
    st.info("Haz clic en 'Iniciar Streaming' para conectar con el servidor.")
