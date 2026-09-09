from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import asyncio

router = APIRouter(tags=["Telemetry"])

@router.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    """
    Bidirectional WebSocket stream for real-time 60 FPS gesture and sculpt telemetry.
    Transfers frame timestamp, gesture state, vertex count, and brush pressure.
    """
    await websocket.accept()
    try:
        while True:
            data_text = await websocket.receive_text()
            data = json.loads(data_text)
            # Echo processed telemetry frame with edge server receipt timestamp
            data["serverAckTimestamp"] = asyncio.get_event_loop().time()
            data["status"] = "synced"
            await websocket.send_text(json.dumps(data))
    except WebSocketDisconnect:
        pass
    except Exception:
        await websocket.close()
