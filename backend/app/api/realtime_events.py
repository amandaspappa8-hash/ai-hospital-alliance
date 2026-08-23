from fastapi import APIRouter, WebSocket
import asyncio

router = APIRouter(tags=["Realtime Clinical Events"])

@router.websocket("/ws/clinical-events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        await websocket.send_json({
            "event": "clinical_alert",
            "severity": "high",
            "message": "Critical potassium detected",
        })
        await asyncio.sleep(10)
