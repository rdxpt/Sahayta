"""
LLM Integration Module for MCD 311 Sovereign Voice AI
Uses local Ollama models for "Fast Path" and "Deep Reasoning"
Completely offline - no cloud dependencies, ensuring data sovereignty.
"""

import logging
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import ollama
from config.settings import settings

logger = logging.getLogger(__name__)


class SovereignLLM:
    """
    Local LLM integration using Ollama.
    Provides two paths:
    1. FAST_PATH: Quick response using lightweight model (Mistral)
    2. DEEP_PATH: Detailed reasoning using more capable model (Neural-Chat)
    """

    def __init__(self):
        """Initialize Ollama client."""
        try:
            self.client = ollama.Client(host=settings.OLLAMA_BASE_URL)
            # Test connection
            self.client.list()
            logger.info(f"[OK] Ollama connected at {settings.OLLAMA_BASE_URL}")
        except Exception as e:
            logger.error(f"[ERROR] Failed to connect to Ollama: {e}")
            logger.warning("Ensure Ollama is running: ollama serve")
            raise

        self.fast_model = settings.OLLAMA_MODEL_FAST  # Default: mistral
        self.deep_model = settings.OLLAMA_MODEL_DEEP  # Default: neural-chat
        
        # Use available models if defaults not present
        try:
            models_response = self.client.list()
            # Handle different response formats (obj or dict)
            available_models = []
            for m in models_response.get('models', []):
                # Try dict access then attribute access
                name = m.get('name') if isinstance(m, dict) else getattr(m, 'name', None)
                if not name:
                    # Fallback for 'model' key
                    name = m.get('model') if isinstance(m, dict) else getattr(m, 'model', None)
                
                if name:
                    available_models.append(name.split(':')[0])
            
            logger.info(f"Available models: {available_models}")

            if 'mistral' not in available_models and 'phi3' in available_models:
                self.fast_model = 'phi3:mini'
            if 'neural-chat' not in available_models and 'llama3.2' in available_models:
                self.deep_model = 'llama3.2:latest'
        except Exception as e:
            logger.warning(f"Error listing models: {e}. Using defaults.")

    def fast_path_response(self, citizen_input: str, context: Dict[str, Any] = None, max_tokens: int = 100) -> str:
        """
        Fast Path: Lightweight, quick response for simple queries.
        Used for: Grievance categorization, basic FAQ, simple routing.
        
        Args:
            citizen_input: User's input text
            context: Optional context dict
            max_tokens: Maximum tokens to generate (default: 100 for speed)

        Returns:
            Quick response from the model
        """
        prompt = self._build_fast_prompt(citizen_input, context)

        try:
            response = self.client.generate(
                model=self.fast_model,
                prompt=prompt,
                stream=False,
                options={
                    "temperature": 0.3, 
                    "top_p": 0.8,
                    "num_predict": max_tokens
                },
            )

            result = response["response"].strip()
            logger.info(f"Fast Path: {citizen_input[:50]}... → {result[:50]}...")
            return result

        except Exception as e:
            logger.error(f"Fast Path error: {e}")
            return "I'm having trouble understanding. Could you please rephrase?"

    def deep_path_reasoning(
        self, citizen_input: str, context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Deep Path: Detailed reasoning for complex decisions.
        Used for: Escalation determination, complex categorization, resolution planning.

        Args:
            citizen_input: Citizen's detailed grievance
            context: Full context (category, location, previous interactions)

        Returns:
            Dict with 'reasoning', 'decision', 'confidence', etc.
        """
        prompt = self._build_deep_prompt(citizen_input, context)

        try:
            response = self.client.generate(
                model=self.deep_model,
                prompt=prompt,
                stream=False,
                options={
                    "temperature": 0.5, 
                    "top_p": 0.9,
                    "num_predict": 200  # Allow more tokens for reasoning
                },
            )

            raw_response = response["response"].strip()

            # Try to parse JSON response
            try:
                decision = json.loads(raw_response)
            except json.JSONDecodeError:
                # If not JSON, create structured response
                decision = {
                    "reasoning": raw_response,
                    "decision": "ESCALATE",
                    "confidence": 0.7,
                    "requires_human": True,
                }

            logger.info(
                f"Deep Path: Decision={decision.get('decision')}, "
                f"Confidence={decision.get('confidence', 0)}"
            )
            return decision

        except Exception as e:
            logger.error(f"Deep Path error: {e}")
            return {
                "reasoning": "System error in deep reasoning",
                "decision": "ESCALATE",
                "confidence": 0.0,
                "requires_human": True,
            }

    def categorize_grievance(
        self, grievance_description: str, location: str = ""
    ) -> Dict[str, Any]:
        """
        Determine the category of grievance using Fast Path.

        Args:
            grievance_description: What the citizen is complaining about
            location: Location of the grievance

        Returns:
            Dict with category, confidence, and rationale
        """
        context = {"location": location}
        prompt = f"""You are an MCD (Municipal Corporation of Delhi) grievance classification expert.
Classify this citizen complaint into ONE of these categories:
- WATER_SUPPLY: Water availability, quality, leakage, meter issues
- SEWAGE: Overflow, blockage, smell, maintenance
- ROAD: Pothole, damage, maintenance, safety
- STREET_LIGHT: Non-functional lights, darkness
- ILLEGAL_CONSTRUCTION: Unauthorized structures
- SANITATION: Waste collection, cleanliness, pest control
- PARKING: Illegal parking, space issues
- NOISE_POLLUTION: Loud noise, disturbance
- OTHER: Doesn't fit above categories

Complaint: {grievance_description}
Location: {location if location else 'Not provided'}

Respond in JSON format:
{{"category": "CATEGORY_NAME", "confidence": 0.95, "rationale": "Brief explanation"}}
"""

        try:
            response = self.client.generate(
                model=self.fast_model,
                prompt=prompt,
                stream=False,
                options={"temperature": 0.2},
            )

            raw = response["response"].strip()
            try:
                result = json.loads(raw)
            except json.JSONDecodeError:
                result = {
                    "category": "OTHER",
                    "confidence": 0.5,
                    "rationale": "Unable to classify",
                }

            logger.info(
                f"Categorized as: {result.get('category')} "
                f"(confidence: {result.get('confidence')})"
            )
            return result

        except Exception as e:
            logger.error(f"Categorization error: {e}")
            return {
                "category": "OTHER",
                "confidence": 0.0,
                "rationale": "System error",
            }

    def generate_response(
        self, state_summary: str, next_action: str, language: str = "hindi"
    ) -> str:
        """
        Generate a natural language response to the citizen.

        Args:
            state_summary: Current state of the grievance
            next_action: What should happen next
            language: Response language (hindi, english, hinglish)

        Returns:
            Natural language response
        """
        prompt = f"""You are a helpful MCD 311 grievance redressal agent.
Generate a brief, professional response in {language} (if hindi, use Hinglish mix).

Current Status: {state_summary}
Next Action: {next_action}

Keep it under 2 sentences. Be empathetic but professional."""

        try:
            response = self.client.generate(
                model=self.fast_model,
                prompt=prompt,
                stream=False,
                options={"temperature": 0.7},
            )

            return response["response"].strip()

        except Exception as e:
            logger.error(f"Response generation error: {e}")
            return "Thank you for reporting this. We will look into it."

    def check_escalation_needed(self, state_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Deep Path to determine if escalation is needed.

        Args:
            state_data: Complete state information

        Returns:
            Dict with escalation decision and reasoning
        """
        prompt = f"""You are an MCD grievance escalation decision engine.
Based on the following information, decide if human escalation is needed.

Grievance Category: {state_data.get('category', 'Unknown')}
Description: {state_data.get('description', '')}
Urgency: {state_data.get('urgency', 'Normal')}
Previous Attempts: {state_data.get('previous_attempts', 0)}

Respond with JSON:
{{
    "requires_escalation": true/false,
    "escalation_reason": "Brief reason if escalating",
    "assigned_department": "Department to escalate to",
    "priority": "HIGH/MEDIUM/LOW",
    "confidence": 0.0-1.0
}}
"""

        return self.deep_path_reasoning(prompt, state_data)

    # ===== PRIVATE METHODS =====

    def _build_fast_prompt(
        self, citizen_input: str, context: Dict[str, Any] = None
    ) -> str:
        """Build a prompt for fast path inference."""
        base = f"""You are MCD 311 Grievance Redressal Agent.
Respond helpfully and concisely.

Citizen Input: {citizen_input}
"""
        if context:
            base += f"Context: {json.dumps(context)}\n"

        return base

    def _build_deep_prompt(
        self, citizen_input: str, context: Dict[str, Any] = None
    ) -> str:
        """Build a prompt for deep reasoning path."""
        base = f"""You are an expert MCD grievance resolution specialist.
Analyze this situation carefully and provide structured reasoning.

Citizen Input: {citizen_input}
"""
        if context:
            base += f"Context: {json.dumps(context)}\n"

        return base


# Global LLM instance
sovereign_llm = SovereignLLM()

if __name__ == "__main__":
    logger.info("Testing SovereignLLM...")
    llm = SovereignLLM()

    # Test fast path
    response = llm.fast_path_response("There is a big pothole on my street")
    logger.info(f"Fast response: {response}")

    # Test categorization
    result = llm.categorize_grievance(
        "Pothole outside my home for 3 months", location="Connaught Place"
    )
    logger.info(f"Categorization: {result}")
