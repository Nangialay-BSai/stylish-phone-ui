from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services import realtime


router = APIRouter()


@router.websocket("/ws/echo")
async def ws_echo(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(data)
    except WebSocketDisconnect:
        return


@router.websocket("/ws/channel/{name}")
async def ws_channel(ws: WebSocket, name: str):
    await ws.accept()
    async for msg in realtime.subscribe(name):
        await ws.send_text(msg)
