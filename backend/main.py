from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)

    try:
        while True:
            data = {
                "voltage": 260,
                "current": 12,
                "status": "OVERLOAD"
            }

            message = json.dumps(data)

            for client in clients:
                await client.send_text(message)

            await asyncio.sleep(1)
    except WebSocketDisconnect:
        clients.remove(ws)
        print("Client disconnected")
