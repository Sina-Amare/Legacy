from fastapi import WebSocket

class ConnectionManager:
    """
    Manages active WebSocket connections for game sessions.
    
    This simple in-memory manager is suitable for a single-process server.
    For a production, multi-worker setup, a more robust solution like
    a Redis Pub/Sub broadcast system would be required.
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

    async def send_personal_message(self, message: str, game_id: int):
        """Sends a message to a specific game session's WebSocket."""
        if game_id in self.active_connections:
            websocket = self.active_connections[game_id]
            await websocket.send_text(message)

# Create a single, global instance of the manager
manager = ConnectionManager()