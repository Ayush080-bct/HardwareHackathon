from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json

# ---------- DB ----------
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///tokens.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class DeviceToken(Base):
    __tablename__ = "device_tokens"
    device_id = Column(String, primary_key=True, index=True)
    token = Column(String)

Base.metadata.create_all(bind=engine)

# ---------- Firebase ----------
import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# ---------- App ----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = set()

# ---------- Models ----------
class TokenData(BaseModel):
    deviceId: str
    token: str

# ---------- Save Token ----------
@app.post("/save-token")
def save_token(data: TokenData):
    db = SessionLocal()
    obj = db.get(DeviceToken, data.deviceId)

    if obj:
        obj.token = data.token
    else:
        obj = DeviceToken(device_id=data.deviceId, token=data.token)
        db.add(obj)

    db.commit()
    db.close()

    return {"status": "saved"}

# ---------- Show DB (for teacher demo) ----------
@app.get("/tokens")
def show_tokens():
    db = SessionLocal()
    rows = db.query(DeviceToken).all()
    db.close()
    return [{"deviceId": r.device_id, "token": r.token[:25]+"..."} for r in rows]

# ---------- Push Sender ----------
def send_push(token, title, body):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )
        messaging.send(message)
        print("✅ Push sent")
    except Exception as e:
        print("❌ Push failed:", e)


def broadcast_push(title, body):
    db = SessionLocal()
    rows = db.query(DeviceToken).all()

    if not rows:
        db.close()
        return

    for r in rows:
        try:
            send_push(r.token, title, body)
        except Exception as e:
            print("❌ Push failed:", e)

    db.close()

# ---------- WebSocket ----------
async def send_data_to_clients():
    while True:
        data = {
            "voltage": 260,
            "current": 12,
            "status": "OVERLOAD"
        }

        message = json.dumps(data)

        dead = []
        for ws in clients:
            try:
                await ws.send_text(message)
            except:
                dead.append(ws)

        for ws in dead:
            clients.remove(ws)

        # 🔔 trigger push on overload
        if data["status"] == "OVERLOAD":
            broadcast_push(
                "⚡ Power Alert",
                "Overload detected!"
            )

        await asyncio.sleep(5)

@app.on_event("startup")
async def startup():
    asyncio.create_task(send_data_to_clients())

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.remove(ws)
@app.get("/test-push")
def test_push():
    broadcast_push("⚡ Demo Alert", "Manual trigger")
    return {"sent": True}

