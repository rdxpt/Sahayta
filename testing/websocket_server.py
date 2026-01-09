"""
FastAPI WebSocket Server for MCD 311 Sovereign Voice AI
Handles bidirectional streaming with audio/text chunks
"""

import asyncio
import json
import base64
import uuid
import logging
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MCD 311 WebSocket Server", version="1.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost", "127.0.0.1", "0.0.0.0"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    """Manage WebSocket connections and streaming."""

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.session_data: dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        self.session_data[session_id] = {
            "started_at": datetime.now(),
            "data_points": 0,
            "messages": [],
        }
        logger.info(f"Client {session_id} connected")

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in self.session_data:
            del self.session_data[session_id]
        logger.info(f"Client {session_id} disconnected")

    async def send_text_chunk(self, session_id: str, category: str, label: str, text: str):
        """Send text chunk to client."""
        if session_id in self.active_connections:
            data = {
                "type": "text_chunk",
                "category": category,
                "label": label,
                "text": text,
                "timestamp": datetime.now().isoformat(),
            }
            await self.active_connections[session_id].send_text(json.dumps(data))
            self.session_data[session_id]["messages"].append(data)

    async def send_audio_chunk(self, session_id: str, audio_base64: str):
        """Send audio chunk to client."""
        if session_id in self.active_connections:
            data = {
                "type": "audio_chunk",
                "audio": audio_base64,
                "timestamp": datetime.now().isoformat(),
            }
            await self.active_connections[session_id].send_text(json.dumps(data))

    async def send_data_count(self, session_id: str, count: int):
        """Send current data point count."""
        if session_id in self.active_connections:
            self.session_data[session_id]["data_points"] = count
            data = {"type": "data_count", "count": count}
            await self.active_connections[session_id].send_text(json.dumps(data))

    async def send_wipe_notification(self, session_id: str, event_type: str):
        """Send memory wipe notifications."""
        if session_id in self.active_connections:
            data = {"type": event_type, "timestamp": datetime.now().isoformat()}
            await self.active_connections[session_id].send_text(json.dumps(data))


manager = ConnectionManager()


@app.websocket("/ws/call")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for bidirectional streaming.
    Receives audio chunks, processes them, streams back text + audio.
    """
    session_id = str(uuid.uuid4())[:8]

    try:
        await manager.connect(websocket, session_id)
        logger.info(f"Session {session_id} initiated")

        # Simulate receiving citizen data
        await asyncio.sleep(1)
        await manager.send_text_chunk(
            session_id, "intent", "Call Type", "Grievance Registration"
        )

        while True:
            # Receive audio chunk from client
            data = await websocket.receive_text()
            received = json.loads(data)

            if received.get("type") == "audio_chunk":
                # Simulate speech-to-text processing
                await asyncio.sleep(0.2)

                # Mock categorization (in real: would use LLM)
                if "light" in str(received).lower() or random_grievance():
                    await manager.send_text_chunk(
                        session_id,
                        "entity",
                        "Category",
                        "STREET_LIGHT (Confidence: 0.97)",
                    )
                    await manager.send_data_count(session_id, 6)

                    await asyncio.sleep(0.5)
                    await manager.send_text_chunk(
                        session_id,
                        "entity",
                        "Location",
                        "Lajpat Nagar, Delhi",
                    )

                    await asyncio.sleep(0.5)
                    await manager.send_text_chunk(
                        session_id,
                        "action",
                        "Priority",
                        "HIGH - Assigned to Electrical Team",
                    )

                    await asyncio.sleep(1)
                    await manager.send_wipe_notification(session_id, "memory_wipe_start")

                    # Simulate data deletion
                    for i in range(6, 0, -1):
                        await asyncio.sleep(0.1)
                        await manager.send_data_count(session_id, i - 1)

                    await manager.send_wipe_notification(session_id, "memory_wipe_complete")
                    await manager.send_text_chunk(
                        session_id,
                        "action",
                        "Status",
                        "✓ All citizen data wiped",
                    )

    except WebSocketDisconnect:
        manager.disconnect(session_id)
        logger.info(f"Client {session_id} disconnected")
    except Exception as e:
        logger.error(f"Error in session {session_id}: {e}")
        manager.disconnect(session_id)


def random_grievance():
    """Simulate random grievance detection."""
    import random

    return random.random() > 0.5


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "MCD 311 WebSocket Server",
        "active_connections": len(manager.active_connections),
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "MCD 311 Sovereign Voice AI - WebSocket Backend",
        "version": "1.0",
        "endpoints": {
            "websocket": "ws://localhost:8000/ws/call",
            "health": "GET /health",
        },
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
