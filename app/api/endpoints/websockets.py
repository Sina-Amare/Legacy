from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.ws.manager import manager

router = APIRouter()

@router.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int):
    """
    Handles the WebSocket lifecycle for a specific game session.
    """
    await manager.connect(websocket, game_id)
    try:
        while True:
            # Keep the connection alive. The client does not need to send data.
            # The server will push updates when they are ready.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(game_id)
        print(f"WebSocket connection closed for game_id: {game_id}")