from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import random
import time

router = APIRouter()

@router.websocket("/ws/clinical-live")
async def clinical_live_ws(websocket: WebSocket):
    await websocket.accept()
    pulse = 0

    try:
        while True:
            payload = {
                "pulse": pulse,
                "heartRate": random.randint(72, 88),
                "spo2": random.randint(96, 100),
                "risk": random.randint(5, 28),
                "ultrasoundFps": random.randint(42, 58),
                "dicomEvents": random.randint(6, 18),
                "monaiConfidence": random.randint(88, 99),
                "agentMessages": random.randint(1800, 2600),
                "timestamp": time.time(),
            }

            await websocket.send_json(payload)
            pulse += 1
            await asyncio.sleep(0.8)

    except WebSocketDisconnect:
        print("Clinical WebSocket disconnected")
