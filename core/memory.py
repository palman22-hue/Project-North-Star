# memory.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from core.utils import to_list

_memory_store = {}

def get_session_memory(session_id: str):
    if session_id not in _memory_store:
        _memory_store[session_id] = ConversationMemory(session_id)
    return _memory_store[session_id]


@dataclass
class TurnMemory:
    role: str                    # "user" of "pda"
    text: str
    emotions: Dict[str, float]   # output van text_to_emotions
    state_vector: List[float]    # snapshot van 32D vector
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ConversationMemory:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.turns: List[Turn] = []
        self.log_path = Path(f"logs/session_{session_id}.jsonl")
        self.log_path.parent.mkdir(exist_ok=True)
    
    def append_turn(self, role: str, text: str, emotions: Dict, state_vector):
        turn = Turn(
            role=role, 
            text=text, 
            emotions=emotions, 
            state_vector=to_list(state_vector)  # ✅
    )
        self.turns.append(turn)
        self._log_to_file(turn)
    
    def _log_to_file(self, turn: Turn):  # ← moet een methode zijn!
        print(f"[DEBUG] Logging to: {self.log_path}")
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "role": turn.role,
            "text": turn.text,
            "emotions": turn.emotions,
        }
        
        # ← Deze regel moet BINNEN de methode staan, met juiste indentatie
        with self.log_path.open("a", encoding="utf-8") as f:
            json.dump(log_entry, f, ensure_ascii=False)
            f.write("\n")
        
        print(f"[DEBUG] Logged successfully")


    def get_recent(self, n: int = 10):
        return self.turns[-n:] if len(self.turns) > n else self.turns

    def append_turn(
        self,
        role: str,
        text: str,
        emotions: Dict[str, float],
        state_vector: np.ndarray,
    ) -> None:
        self.turns.append(
            TurnMemory(
                role=role,
                text=text,
                emotions=emotions,
                state_vector=to_list(state_vector),
            )
        )

    def last_user_text(self) -> Optional[str]:
        for turn in reversed(self.turns):
            if turn.role == "user":
                return turn.text
        return None

    def summary_hint(self, max_turns: int = 10) -> str:
        """Korte, goedkope samenvatting voor de planner/ethics."""
        recent = self.turns[-max_turns:]
        parts = [f"{t.role}: {t.text}" for t in recent]
        return "\n".join(parts)


class MemoryStore:
    """Eenvoudige in‑memory store; later vervangbaar door DB."""

    def __init__(self):
        self._conversations: Dict[str, ConversationMemory] = {}

    def create_session(self, session_id: Optional[str] = None) -> ConversationMemory:
        if session_id is None:
            session_id = str(uuid.uuid4())
        conv = ConversationMemory(session_id=session_id)
        self._conversations[session_id] = conv
        return conv

    def get_or_create(self, session_id: Optional[str]) -> ConversationMemory:
        if session_id and session_id in self._conversations:
            return self._conversations[session_id]
        return self.create_session(session_id)

    def get(self, session_id: str) -> Optional[ConversationMemory]:
        return self._conversations.get(session_id)

    def all_sessions(self) -> List[ConversationMemory]:
        return list(self._conversations.values())
