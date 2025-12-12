from fastapi import APIRouter,WebSocket,WebSocketDisconnect
from web.web_socket import manager

router=APIRouter(prefix="/api/v1/ws",tags=['WebSocket'])

@router.websocket("/")
async def web_socket_enpoint(websocket:WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)