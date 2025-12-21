from __future__ import annotations
from core.llm_client import generate_text
from typing import Dict, Any
from session_logger import log_turn
from core.memory import get_session_memory
from core.utils import to_list

from pda32d_base import PDA32D
from core.perception import PerceptionEngine, run_perception_step, PerceptionResult
from core.planning import Planner, PlannedAction, ActionType
from core.memory import MemoryStore
from ethics import EthicsEngine, EthicsDecision

import numpy as np

def to_list(vec):
    """Convert any vector format to Python list"""
    if isinstance(vec, np.ndarray):
        return vec.tolist()
    if isinstance(vec, list):
        return vec
    return list(vec)




# Session state store
_session_states = {}

_pda_instance = PDA32D()
pda = PDA32D()
perception_engine = PerceptionEngine()
planner = Planner()
ethics = EthicsEngine()
memory_store = MemoryStore()

def get_session_state(session_id: str) -> PDA32D:
    """Haal of creëer PDA state voor deze sessie"""
    if session_id not in _session_states:
        _session_states[session_id] = PDA32D()
    return _session_states[session_id]

def handle_turn(session_id: str, user_text: str) -> Dict[str, Any]:
    from core.memory import get_session_memory
    from core.llm_client import generate_text
    from core.utils import to_list
    import numpy as np
    
    # 1. Get PDA and memory
    pda = _pda_instance
    memory = get_session_memory(session_id)
    
    # 2. Run perception
    perception = run_perception_step(pda, perception_engine, user_text, memory)
    
    # 3. Debug emotions
    print(f"[DEBUG] Detected emotions: {perception.emotions}")
    
    # 4. Update state if emotions detected
    if perception.emotions:
        print(f"[DEBUG] Updating state with: {perception.emotions}")
        pda.state.update_from_emotions(perception.emotions)
    else:
        print(f"[DEBUG] No emotions detected, state not updated")
    
    # 5. GET STATE VECTOR HERE ← moet na state update!
    state_vector = pda.state.vector if hasattr(pda.state, 'vector') else np.zeros(32)
    state_list = to_list(state_vector)  # ✅ Nu bestaat state_vector al
    coherence = pda.state.coherence() if hasattr(pda.state, 'coherence') else 1.0
    
    # 6. Build memory context
    recent_turns = memory.get_recent(n=5) if hasattr(memory, 'get_recent') else []
    memory_context = "\n".join([
        f"{'User' if turn.role == 'user' else 'PDA'}: {turn.text}"
        for turn in recent_turns
    ])
    user_prompt = f"""
Current emotional state: coherence={coherence:.2f}, joy={state_vector[0]:.2f}
User: {user_text}
"""

    # 7. Build prompts
    system_prompt = """Je bent een ethische AI assistent voor persoonlijke ontwikkeling.
Je onthoudt de context van het gesprek en gebruikt eerdere informatie om gepersonaliseerde hulp te bieden."""
    
    # ✨ Enhanced user prompt with state info
    user_prompt = f"""Gesprek geschiedenis:
    {memory_context}

    Jouw huidige interne staat:
    - Coherence: {coherence:.3f} (1.0 = neutraal, <0.5 = complex/chaotisch)
    - Joy dimensie: {state_vector[0]:.3f}
    - Fear dimensie: {state_vector[6]:.3f}
    - Sadness dimensie: {state_vector[12]:.3f}

    Huidige bericht van user: {user_text}
    Detected intent: {perception.intent}
    Detected emotions: {perception.emotions}

    Geef een empathisch, contextbewust antwoord dat past bij je interne staat.
    Als je coherence laag is (<0.5), erken dat je de complexiteit van de situatie voelt."""

    print("\n" + "="*50)
    print("PROMPT SENT TO MISTRAL:")
    print("="*50)
    print(f"SYSTEM: {system_prompt[:100]}...")
    print(f"\nUSER PROMPT:\n{user_prompt}")
    print("="*50 + "\n")
    # 8. Generate response
    assistant_text = generate_text(system_prompt, user_prompt)
    
    # 9. Log to memory
    memory.append_turn(
        role="user",
        text=user_text,
        emotions=perception.emotions or {},
        state_vector=state_list
    )
    memory.append_turn(
        role="pda",
        text=assistant_text,
        emotions={},
        state_vector=state_list
    )
    
    # 10. Return result
    return {
        "assistant_text": assistant_text,
        "state_vector": state_list,
        "coherence": float(coherence),
    }




# In engine.py na handle_turn
import json
from pathlib import Path

LOG_PATH = Path("session_log.jsonl")

def log_turn(session_id, user_text, assistant_text, perception):
    with LOG_PATH.open("a", encoding="utf-8") as f:
        json.dump({
            "session_id": session_id,
            "user": user_text,
            "assistant": assistant_text,
            "intent": str(perception.intent),
            "emotions": perception.emotions,
        }, f)
        f.write("\n")



def generate_response(
    action: PlannedAction,
    perception: PerceptionResult,
    decision: EthicsDecision,
) -> str:
    hint = decision.modified_description or action.description

    # 1) vaste, niet‑LLM antwoorden
    if action.type == ActionType.ASK_CLARIFY:
        return "Je klinkt positief. Kun je vertellen wat je precies wilt bereiken?"

    if action.type == ActionType.EMOTIONAL_SUPPORT:
        return (
            "Ik hoor dat dit veel met je doet. "
            "Je hoeft hier niet alleen doorheen te gaan; het is oké om steun te vragen. "
            "Wil je delen wat er nu het meest op de voorgrond staat, "
            "of is er iemand in je omgeving bij wie je terecht kunt?"
        )

    # 2) voor EXPLAIN / STEP_PLAN / META_REFLECTION de LLM gebruiken
    if action.type in {ActionType.EXPLAIN, ActionType.STEP_PLAN, ActionType.META_REFLECTION}:
        # TODO: échte memory‑samenvatting maken; voor nu leeg
        memory_summary = ""
        return generate_text(action, perception, decision, memory_summary)

    # fallback
    return hint
