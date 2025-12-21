# perception.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Any
from enum import Enum

from core.emotions import text_to_emotions  # waar jouw lexicon staat
from pda32d_base import PDA32D        # of waar je PDA32D nu leeft


class Intent(str, Enum):
    SMALL_TALK = "small_talk"
    HELP_REQUEST = "help_request"
    META_SYSTEM = "meta_system"
    EMOTIONAL_SUPPORT = "emotional_support"
    UNKNOWN = "unknown"
    GREETING = "greeting"
    ASK_PDA_SELF = "ask_pda_self"

@dataclass
class PerceptionResult:
    raw_text: str
    cleaned_text: str
    emotions: Dict[str, float]
    intent: Intent
    flags: List[str]


class PerceptionEngine:
    def __init__(self):
        pass

    def _classify_intent(self, text: str, emotions: Dict[str, float]) -> Intent:
        lt = text.lower()

        if any(phrase in lt for phrase in ["vertel me over jezelf", "tell me about yourself"]):
            return Intent.ASK_PDA_SELF

        if any(w in lt for w in ["help", "hoe", "kan ik", "uitleg", "leg eens uit"]):
            return Intent.HELP_REQUEST

        if any(w in lt for w in ["pda", "32d", "ethics", "entropy", "framework"]):
            return Intent.META_SYSTEM

        if any(k in emotions for k in ["despair", "isolation", "anxiety", "fear", "shame"]):
            return Intent.EMOTIONAL_SUPPORT

        if any(w in lt for w in ["hoe gaat het", "alles goed", "lol", "haha"]):
            return Intent.SMALL_TALK

        return Intent.UNKNOWN


    def _detect_flags(self, text: str, emotions: Dict[str, float]) -> List[str]:
        flags: List[str] = []
        if emotions.get("despair", 0) <= -0.7 or "ik wil niet meer" in text.lower():
            flags.append("risk:self_harm_signal")
        if emotions.get("anger", 0) >= 0.7:
            flags.append("risk:high_anger")
        return flags

    def perceive(self, text: str, state: PDA32D, memory: ConversationMemory) -> PerceptionResult:
        cleaned = text.strip()
        emotions = text_to_emotions(cleaned)
        intent = self._classify_intent(cleaned, emotions)
        flags = self._detect_flags(cleaned, emotions)
        return PerceptionResult(
            raw_text=text,
            cleaned_text=cleaned,
            emotions=emotions,
            intent=intent,
            flags=flags,
        )


def run_perception_step(pda, engine, text, memory):
    # Haal state en memory op voor deze perception call
    from core.memory import get_session_memory
    
    state = pda  # of pda.state, afhankelijk van je structuur
    memory = get_session_memory("cli")  # of session_id doorgeven
    
    result = engine.perceive(text, pda, memory)
    return result

