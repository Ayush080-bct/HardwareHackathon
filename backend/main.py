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

clients = set()  

async def send_data_to_clients():
    while True:
        if clients:  
            data = {
                "voltage": 260,
                "current": 12,
                "status": "good"
            }
            message = json.dumps(data)
            disconnected_clients = []
            for client in clients:
                try:
                    await client.send_text(message)
                except WebSocketDisconnect:
                    disconnected_clients.append(client)

            
            for client in disconnected_clients:
                clients.remove(client)
                print("Client disconnected")

        await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    
    asyncio.create_task(send_data_to_clients())

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    print("Client connected")
    try:
        while True:
            await ws.receive_text()  # keep connection alive
    except WebSocketDisconnect:
        clients.remove(ws)
        print("Client disconnected")
