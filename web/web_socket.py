from fastapi import WebSocket,WebSocketDisconnect,WebSocketException

class ConnectionManager:
    def __init__(self):
        self.active_connections:list[WebSocket]=[]
    #Conexion al WebSocket
    async def connect(self,websocket:WebSocket):
        await websocket.accept()
    #Desconexion al WebSocket
    def disconnect(self,websocket:WebSocket):
        self.active_connections.remove(websocket)
    #Envío del evento
    async def broadcast(self,message:dict):
        for connection in self.active_connections:
            await connection.send_json(message)
            
manager=ConnectionManager()