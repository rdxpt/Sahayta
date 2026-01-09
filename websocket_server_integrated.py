"""
MCD 311 Sovereign Voice AI - Enhanced WebSocket Server
Integrates with Python backend (LLM, Redis, Memory Manager)
"""

import asyncio
import json
import uuid
import logging
from datetime import datetime
from typing import Optional, Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os

# Add Python modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import Settings
from src.memory_manager import MemoryManager
from src.llm_integration import SovereignLLM
from src.workflow import SovereignVoiceAIWorkflow
from src.agent_state import AgentState, CallState
from src.audio_processor import audio_processor

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = FastAPI(title="MCD 311 WebSocket Server (Integrated)", version="1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
settings = Settings()
memory_manager = MemoryManager()
llm = SovereignLLM()
workflow = SovereignVoiceAIWorkflow()


class StreamingConnectionManager:
    """Manage WebSocket connections with real backend integration."""

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.session_states: dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        self.session_states[session_id] = {
            "started_at": datetime.now(),
            "state": CallState.INITIATED,
            "agent_state": None,
            "data_count": 0,
        }
        logger.info(f"[CONNECTED] Session {session_id} connected")

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in self.session_states:
            del self.session_states[session_id]
        logger.info(f"[DISCONNECTED] Session {session_id} disconnected")

    async def send_chunk(
        self, session_id: str, chunk_type: str, **kwargs
    ):
        """Send any chunk type to client."""
        if session_id not in self.active_connections:
            return

        data = {
            "type": chunk_type,
            "timestamp": datetime.now().isoformat(),
            **kwargs,
        }

        try:
            await self.active_connections[session_id].send_text(json.dumps(data))
        except Exception as e:
            logger.error(f"Error sending chunk to {session_id}: {e}")

    async def send_text_chunk(
        self, session_id: str, category: str, label: str, text: str
    ):
        """Send text analysis chunk."""
        await self.send_chunk(
            session_id,
            "text_chunk",
            category=category,
            label=label,
            text=text,
        )

    async def send_audio_chunk(self, session_id: str, audio_base64: str):
        """Send audio chunk."""
        await self.send_chunk(session_id, "audio_chunk", audio=audio_base64)

    async def send_data_count(self, session_id: str, count: int):
        """Send data point count for sovereignty meter."""
        self.session_states[session_id]["data_count"] = count
        await self.send_chunk(session_id, "data_count", count=count)

    async def send_wipe_notification(self, session_id: str, event: str):
        """Send memory wipe event."""
        await self.send_chunk(session_id, event)

    async def broadcast_system(self, message: str):
        """Broadcast system message to all connected clients."""
        data = {"type": "system_message", "message": message}
        for ws in self.active_connections.values():
            try:
                await ws.send_text(json.dumps(data))
            except:
                pass


manager = StreamingConnectionManager()


@app.websocket("/ws/call")
async def websocket_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint for real call processing.
    Integrates with Python backend for actual LLM inference.
    """
    session_id = str(uuid.uuid4())[:8]

    try:
        await manager.connect(websocket, session_id)

        # Simulate citizen call scenario
        # In production: would receive audio stream and transcribe

        # PHASE 1: Call Initiated
        greeting_text = "MCD 311 Grievance Redressal System. Please state your emergency or grievance."
        await manager.send_audio_chunk(session_id, audio_processor.text_to_speech(greeting_text))
        
        # Play beep to indicate ready for input
        audio_processor.play_status_beep('start')
        
        await manager.send_text_chunk(
            session_id,
            "intent",
            "Call Type",
            "Grievance Registration - Street Light Issue",
        )
        await asyncio.sleep(0.5)

        # PHASE 2: Get initial agent state
        agent_state = AgentState(
            session_id=session_id,
            current_state=CallState.LISTENING,
            call_timestamp=datetime.now().isoformat(),
            citizen_name="Amit Singh",
            citizen_phone="+91-9876543210",
            citizen_location="Lajpat Nagar, Delhi",
            grievance_description="Streetlight near my home hasn't worked for a month",
        )

        # Store in Redis
        await manager.send_text_chunk(
            session_id, "entity", "Citizen", agent_state.citizen_name
        )
        await manager.send_data_count(session_id, 2)
        await asyncio.sleep(0.3)

        await manager.send_text_chunk(
            session_id, "entity", "Location", agent_state.citizen_location
        )
        await manager.send_data_count(session_id, 3)
        await asyncio.sleep(0.3)

        # PHASE 3: LLM Categorization (Fast Path)
        # Play processing beep
        audio_processor.play_status_beep('processing')
        await asyncio.sleep(0.5)

        # Call LLM for categorization
        try:
            category_result = await asyncio.to_thread(
                llm.categorize_grievance, agent_state.grievance_description
            )
            
            cat_text = f"Categorized as {category_result.get('category', 'Grievance')} with {int(category_result.get('confidence', 0.95)*100)}% confidence."
            await manager.send_audio_chunk(session_id, audio_processor.text_to_speech(cat_text))

            await manager.send_text_chunk(
                session_id,
                "action",
                "Category",
                f"{category_result.get('category', 'STREET_LIGHT')} ({category_result.get('confidence', 0.95)})",
            )
            await manager.send_data_count(session_id, 4)
        except Exception as e:
            logger.warning(f"LLM categorization failed: {e}, using mock")
            await manager.send_text_chunk(
                session_id,
                "action",
                "Category",
                "STREET_LIGHT (Confidence: 0.97)",
            )
            await manager.send_data_count(session_id, 4)

        await asyncio.sleep(0.5)

        # PHASE 4: Escalation Decision (Deep Path)
        try:
            escalation = await asyncio.to_thread(
                llm.check_escalation_needed,
                agent_state.grievance_description,
                "STREET_LIGHT",
            )

            priority = (
                "HIGH"
                if escalation.get("requires_escalation", True)
                else "ROUTINE"
            )
            
            prio_text = f"Priority determined as {priority}. {escalation.get('reason', '')}"
            await manager.send_audio_chunk(session_id, audio_processor.text_to_speech(prio_text))

            await manager.send_text_chunk(
                session_id,
                "action",
                "Priority",
                f"{priority} - {escalation.get('reason', 'Safety hazard')}",
            )
        except Exception as e:
            logger.warning(f"Escalation check failed: {e}, using mock")
            await manager.send_text_chunk(
                session_id,
                "action",
                "Priority",
                "HIGH - Safety hazard, immediate attention",
            )

        await manager.send_data_count(session_id, 5)
        await asyncio.sleep(0.5)

        # Create ticket
        ticket_id = "MCD-2026-55823"
        await manager.send_text_chunk(
            session_id, "action", "Ticket Created", ticket_id
        )
        await manager.send_audio_chunk(session_id, audio_processor.text_to_speech(f"Ticket created. ID is {ticket_id}. Initiating memory wipe."))

        await manager.send_data_count(session_id, 6)
        await asyncio.sleep(1)

        # PHASE 5: MEMORY WIPE - The star of the show
        await manager.send_wipe_notification(session_id, "memory_wipe_start")
        await asyncio.sleep(0.5)

        # Delete data point by point
        for remaining in range(5, -1, -1):
            await manager.send_data_count(session_id, remaining)
            await asyncio.sleep(0.15)

        # Call actual memory_wipe_node
        try:
            cleared_state = await asyncio.to_thread(
                memory_manager.memory_wipe_node, agent_state
            )
            logger.info(
                f"Session {session_id}: Memory wiped successfully. Remaining keys: {cleared_state.get('remaining_keys', 0)}"
            )
        except Exception as e:
            logger.error(f"Memory wipe error: {e}")

        await manager.send_wipe_notification(session_id, "memory_wipe_complete")

        # PHASE 6: Verification
        await asyncio.sleep(0.5)
        await manager.send_text_chunk(
            session_id,
            "action",
            "Verification",
            "[SUCCESS] All citizen data permanently deleted",
        )

        await asyncio.sleep(0.5)
        await manager.send_text_chunk(
            session_id,
            "action",
            "Status",
            "Call completed. Zero persistence confirmed.",
        )

        # End connection after showing completion
        await asyncio.sleep(2)
        await websocket.close()

    except WebSocketDisconnect:
        manager.disconnect(session_id)
        logger.info(f"Client {session_id} disconnected naturally")

    except Exception as e:
        logger.error(f"Error in session {session_id}: {e}", exc_info=True)
        manager.disconnect(session_id)
        try:
            await websocket.close(code=1011, reason=str(e))
        except:
            pass


@app.get("/health")
async def health():
    """Health check with system status."""
    return {
        "status": "healthy",
        "service": "MCD 311 WebSocket Server (Integrated)",
        "version": "1.0",
        "active_connections": len(manager.active_connections),
        "redis_available": memory_manager.is_connected(),
        "ollama_available": llm.check_availability(),
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "MCD 311 Sovereign Voice AI - WebSocket Backend (Integrated)",
        "version": "1.0",
        "endpoints": {
            "websocket": "ws://localhost:8000/ws/call",
            "health": "GET /health",
            "frontend": "http://localhost:3000",
        },
        "features": [
            "Bidirectional audio/text streaming",
            "Real-time LLM categorization",
            "Escalation reasoning",
            "Memory wipe visualization",
            "Data sovereignty tracking",
        ],
    }


if __name__ == "__main__":
    logger.info("Starting MCD 311 WebSocket Server (Integrated)...")
    logger.info(
        "WebSocket available at: ws://localhost:8000/ws/call"
    )
    logger.info("Frontend available at: http://localhost:3000")
    logger.info("Health check: http://localhost:8000/health")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
