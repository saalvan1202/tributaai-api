from fastapi import APIRouter,Depends,FastAPI, WebSocket, WebSocketDisconnect
from database import get_db
from schemas.agente_schema import AgenteSchema
from sqlalchemy.orm import Session
from services.agentes_service import get_agentes,create_agente,delete_agente
from fastapi.responses import HTMLResponse
from datetime import datetime
import json


router=APIRouter(prefix="/api/v1/agente",tags=["Agentes"])

@router.get("/")
def llamar(db:Session=Depends(get_db)):
    return get_agentes(db)

@router.post("/")
def create(data:AgenteSchema,db:Session=Depends(get_db)):
    return create_agente(db,data)

@router.delete("/{id}")
def destroy(id:int,db:Session=Depends(get_db)):
    return delete_agente(db,id)

HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8"/>
    <title>FastAPI Chat - Demo</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 20px; }
      #chat { border: 1px solid #ccc; height: 400px; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
      .msg { margin: 6px 0; }
      .me { font-weight: bold; }
      #controls { display:flex; gap:8px; }
      input[type="text"] { flex: 1; padding: 8px; }
      button { padding: 8px 12px; }
    </style>
  </head>
  <body>
    <h2>Chat en tiempo real (FastAPI + WebSocket)</h2>
    <div>
      <label>Nombre: <input id="name" type="text" placeholder="Tu nombre" value="Usuario"/></label>
    </div>
    <div id="chat"></div>
    <div id="controls">
      <input id="msg" type="text" placeholder="Escribe un mensaje..."/>
      <button id="send">Enviar</button>
    </div>

    <script>
      const chat = document.getElementById('chat');
      const msgInput = document.getElementById('msg');
      const sendBtn = document.getElementById('send');
      const nameInput = document.getElementById('name');

      // Conectar al WS (si usas https o deploy, cambia ws:// por wss://)
      const ws = new WebSocket("ws://127.0.0.1:8000/api/v1/agente/ws");

      ws.onopen = () => {
        appendSystem("Conectado al servidor");
      };

      ws.onmessage = (evt) => {
        try {
          const data = JSON.parse(evt.data);
          const when = new Date(data.time).toLocaleTimeString();
          const me = data.user === nameInput.value;
          const el = document.createElement('div');
          el.className = 'msg';
          el.innerHTML = `<span class="${me ? 'me' : ''}">${data.user}</span> [${when}]: ${escapeHtml(data.message)}`;
          chat.appendChild(el);
          chat.scrollTop = chat.scrollHeight;
        } catch (e){
          console.error("Mensaje no JSON:", evt.data);
        }
      };

      ws.onclose = () => appendSystem("Desconectado del servidor");

      sendBtn.onclick = sendMessage;
      msgInput.addEventListener('keydown', (e) => { if(e.key === 'Enter') sendMessage(); });

      function sendMessage(){
        const text = msgInput.value.trim();
        const user = nameInput.value || "Anon";
        if (!text) return;
        const payload = { user, message: text };
        ws.send(JSON.stringify(payload));
        msgInput.value = "";
      }

      function appendSystem(text){
        const el = document.createElement('div');
        el.style.color = '#666';
        el.style.fontStyle = 'italic';
        el.textContent = text;
        chat.appendChild(el);
      }

      // seguridad mínima: escapar HTML
      function escapeHtml(str) {
        return str.replace(/[&<>"']/g, function(m) { return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[m]; });
      }
    </script>
  </body>
</html>
"""

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # intenta enviar a todos; si falla, los elimina
        disconnects = []
        for conn in list(self.active_connections):
            try:
                await conn.send_text(message)
            except Exception:
                disconnects.append(conn)
        for d in disconnects:
            self.disconnect(d)

manager = ConnectionManager()

@router.get("/ejemplo")
async def get():
    return HTMLResponse(HTML)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # esperamos JSON desde el cliente { user, message }
            try:
                payload = json.loads(data)
                user = payload.get("user", "Anon")
                message = payload.get("message", "")
            except Exception:
                user = "Anon"
                message = str(data)
            now_iso = datetime.utcnow().isoformat() + "Z"
            out = json.dumps({
                "user": user,
                "message": message,
                "time": now_iso
            })
            await manager.broadcast(out)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
