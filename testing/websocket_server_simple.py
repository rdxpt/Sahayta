"""
MCD 311 - Simple WebSocket Server
Minimal version for testing
"""

import asyncio
import json
import uuid
import logging
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MCD 311 WebSocket Server (Simple)", version="1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"[CONNECTED] Session {session_id}")

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        logger.info(f"[DISCONNECTED] Session {session_id}")

    async def send_message(self, session_id: str, message_type: str, **data):
        if session_id not in self.active_connections:
            return
        
        payload = {
            "type": message_type,
            "timestamp": datetime.now().isoformat(),
            **data,
        }
        
        try:
            await self.active_connections[session_id].send_text(json.dumps(payload))
        except Exception as e:
            logger.error(f"Error sending message: {e}")


manager = ConnectionManager()


@app.websocket("/ws/call")
async def websocket_endpoint(websocket: WebSocket):
    session_id = str(uuid.uuid4())[:8]
    
    try:
        await manager.connect(websocket, session_id)
        
        # Demo workflow: send items with delays
        items = [
            ("intent", "Call Type", "Grievance Registration - Street Light"),
            ("entity", "Citizen", "Amit Singh"),
            ("entity", "Location", "Lajpat Nagar, Delhi"),
            ("action", "Category", "STREET_LIGHT (Confidence: 0.97)"),
            ("action", "Priority", "HIGH - Safety hazard"),
            ("action", "Ticket Created", "MCD-2026-55823"),
        ]
        
        # Send items
        for i, (category, label, value) in enumerate(items):
            await manager.send_message(
                session_id,
                "text_chunk",
                category=category,
                label=label,
                text=value,
            )
            await manager.send_message(session_id, "data_count", count=i + 1)
            await asyncio.sleep(0.5)
        
        # Wipe phase
        await manager.send_message(session_id, "memory_wipe_start")
        await asyncio.sleep(0.3)
        
        for remaining in range(5, -1, -1):
            await manager.send_message(session_id, "data_count", count=remaining)
            await asyncio.sleep(0.15)
        
        await manager.send_message(session_id, "memory_wipe_complete")
        await asyncio.sleep(1)
        
        # Complete
        await manager.send_message(
            session_id,
            "text_chunk",
            category="action",
            label="Status",
            text="Call completed. Zero persistence confirmed.",
        )
        
        await asyncio.sleep(2)
        await websocket.close()
        
    except WebSocketDisconnect:
        manager.disconnect(session_id)
        logger.info(f"Client {session_id} disconnected")
    except Exception as e:
        logger.error(f"Error: {e}")
        manager.disconnect(session_id)
        try:
            await websocket.close()
        except:
            pass


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "MCD 311 WebSocket Server",
        "version": "1.0",
    }


if __name__ == "__main__":
    logger.info("Starting MCD 311 WebSocket Server...")
    logger.info("WebSocket: ws://localhost:8000/ws/call")
    logger.info("Health: http://localhost:8000/health")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
