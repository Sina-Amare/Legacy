import json
from typing import Any
from fastapi import WebSocket

class ConnectionManager:
    """
    Manages active WebSocket connections for game sessions.
    """
    def __init__(self):
        # A dictionary to store active connections, mapping game_id to WebSocket object.
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, game_id: int):
        """Accepts a new WebSocket connection and stores it."""
        await websocket.accept()
        self.active_connections[game_id] = websocket

    def disconnect(self, game_id: int):
        """Removes a WebSocket connection from the active pool."""
        if game_id in self.active_connections:
            del self.active_connections[game_id]

    async def send_json_message(self, data: dict[str, Any], game_id: int):
        """Sends a dictionary as a JSON string to a specific game session's WebSocket."""
        if game_id in self.active_connections:
            websocket = self.active_connections[game_id]
            await websocket.send_text(json.dumps(data, ensure_ascii=False))

# Create a single, global instance of the manager
manager = ConnectionManager()