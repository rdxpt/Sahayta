"""
AgentState definition for the MCD 311 Sovereign Voice AI system.
Defines the state schema for the LangGraph workflow.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class CallState(str, Enum):
    """Enumeration of possible call states in the FSM."""

    INITIATED = "initiated"
    LISTENING = "listening"
    PROCESSING = "processing"
    RESPONDING = "responding"
    ESCALATION_CHECK = "escalation_check"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    COMPLETED = "completed"
    WIPED = "wiped"


class GrievanceCategory(str, Enum):
    """Categories of grievances the system can handle."""

    WATER_SUPPLY = "water_supply"
    SEWAGE = "sewage"
    ROAD = "road"
    STREET_LIGHT = "street_light"
    ILLEGAL_CONSTRUCTION = "illegal_construction"
    SANITATION = "sanitation"
    PARKING = "parking"
    NOISE_POLLUTION = "noise_pollution"
    OTHER = "other"


@dataclass
class AgentState:
    """
    Complete state object for a single citizen call session.
    This is the single source of truth for all session data.
    
    Key Privacy Feature:
    - All data stored in Redis with TTL = SESSION_DATA_RETENTION_SECONDS
    - No data persists to disk
    - Programmatically shredded on call completion
    """

    # === SESSION IDENTIFICATION ===
    session_id: str
    call_timestamp: str
    call_duration_seconds: float = 0.0

    # === CITIZEN DATA (ZERO-PERSISTENCE) ===
    citizen_phone: Optional[str] = None
    citizen_name: Optional[str] = None
    citizen_location: Optional[str] = None
    citizen_language: str = "hindi"  # Hindi, English, or Hinglish

    # === GRIEVANCE DETAILS ===
    grievance_category: Optional[GrievanceCategory] = None
    grievance_description: str = ""
    grievance_latitude: Optional[float] = None
    grievance_longitude: Optional[float] = None
    grievance_attachment_count: int = 0

    # === AGENT DECISION MAKING ===
    current_state: CallState = CallState.INITIATED
    confidence_score: float = 0.0
    requires_escalation: bool = False
    escalation_reason: str = ""
    assigned_department: str = ""

    # === INTERACTION TRANSCRIPT ===
    # This is the only "log" - exists only in RAM
    transcript: List[Dict[str, str]] = field(default_factory=list)

    # === REDIS CHECKPOINT ===
    # References to LangGraph checkpoint IDs
    checkpoint_id: Optional[str] = None
    checkpoint_timestamp: Optional[str] = None

    # === METADATA ===
    system_metadata: Dict[str, Any] = field(default_factory=dict)
    error_logs: List[str] = field(default_factory=list)

    def add_transcript_entry(
        self, speaker: str, message: str, timestamp: str, confidence: float = 1.0
    ):
        """Add an entry to the session transcript."""
        self.transcript.append(
            {
                "timestamp": timestamp,
                "speaker": speaker,  # "citizen", "agent", "system"
                "message": message,
                "confidence": confidence,
            }
        )

    def to_redis_dict(self) -> Dict[str, Any]:
        """
        Convert state to dictionary for Redis storage.
        Serializes complex types to JSON-compatible formats.
        """
        return {
            "session_id": self.session_id,
            "call_timestamp": self.call_timestamp,
            "call_duration_seconds": self.call_duration_seconds,
            "citizen_phone": self.citizen_phone or "",
            "citizen_name": self.citizen_name or "",
            "citizen_location": self.citizen_location or "",
            "citizen_language": self.citizen_language,
            "grievance_category": self.grievance_category.value
            if self.grievance_category
            else "",
            "grievance_description": self.grievance_description,
            "grievance_latitude": self.grievance_latitude or 0.0,
            "grievance_longitude": self.grievance_longitude or 0.0,
            "current_state": self.current_state.value,
            "confidence_score": self.confidence_score,
            "requires_escalation": str(self.requires_escalation),
            "assigned_department": self.assigned_department,
            "transcript_count": len(self.transcript),
            "checkpoint_id": self.checkpoint_id or "",
        }

    @staticmethod
    def from_redis_dict(data: Dict[str, str]) -> "AgentState":
        """
        Reconstruct AgentState from Redis dictionary.
        """
        return AgentState(
            session_id=data.get("session_id", ""),
            call_timestamp=data.get("call_timestamp", ""),
            call_duration_seconds=float(data.get("call_duration_seconds", 0)),
            citizen_phone=data.get("citizen_phone") or None,
            citizen_name=data.get("citizen_name") or None,
            citizen_location=data.get("citizen_location") or None,
            citizen_language=data.get("citizen_language", "hindi"),
            grievance_category=GrievanceCategory(data.get("grievance_category"))
            if data.get("grievance_category")
            else None,
            grievance_description=data.get("grievance_description", ""),
            current_state=CallState(data.get("current_state", "initiated")),
            confidence_score=float(data.get("confidence_score", 0)),
            requires_escalation=data.get("requires_escalation") == "True",
            assigned_department=data.get("assigned_department", ""),
        )

    def __repr__(self) -> str:
        """String representation of state for logging."""
        return (
            f"<AgentState session_id={self.session_id} "
            f"state={self.current_state.value} "
            f"escalation={self.requires_escalation}>"
        )
