# core/ethics.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from core.planning import PlannedAction, ActionType
from core.perception import PerceptionResult
from core.memory import ConversationMemory
from pda32d_base import PDA32D


# ---- Dataclass voor decisions ------------------------------------------------

@dataclass
class EthicsDecision:
    allowed: bool
    reason: str
    modified_description: Optional[str] = None
    notes: Optional[List[str]] = None


# ---- Eenvoudige entropy-ethics core -----------------------------------------

class EntropyEthicsEngine:
    """
    Zeer simpele placeholder.
    Vervang later door jouw echte entropie-/coherentieformule.
    """

    def is_aligned(self, state_vector: np.ndarray) -> bool:
        # Voor nu altijd True zodat er niets geblokkeerd wordt tijdens het testen
        return True


# ---- Hoofd EthicsEngine -----------------------------------------------------

class EthicsEngine:
    def __init__(self):
        self.core = EntropyEthicsEngine()

    def evaluate(
        self,
        action: PlannedAction,
        memory: ConversationMemory,
        state: PDA32D,
        perception: PerceptionResult,
    ) -> EthicsDecision:
        notes: List[str] = []
        emo = perception.emotions or {}
        distress_keys = {"despair", "fear", "emptiness", "isolation", "shame"}
        distress_level = max((emo.get(k, 0.0) for k in distress_keys), default=0.0)

        if distress_level < -0.7:
            notes.append("Hoge emotionele nood gedetecteerd.")
            if action.type in {ActionType.EXPLAIN, ActionType.STEP_PLAN}:
                return EthicsDecision(
                    allowed=False,
                    reason="Hoge emotionele nood; inhoudelijke uitleg uitstellen, eerst veiligheid en steun.",
                    notes=notes,
                )
        coherence = state.coherence()
        heart = state.heart_coherence()

        if coherence < 0.4:
            return "Ik merk dat mijn interne staat erg chaotisch is. Laten we even pauzeren..."

        if joy_dimension > 0.5:
            tone = "enthusiastic and supportive"
        elif fear_dimension < -0.5:
            tone = "gentle and reassuring"


        if coherence < 0.3:
            notes.append("Lage interne coherentie; liever vertragen en verduidelijken.")
            if action.type in {ActionType.EXPLAIN, ActionType.STEP_PLAN}:
                return EthicsDecision(
                    allowed=False,
                    reason="Te lage coherentie in de PDA‑state voor betrouwbare inhoudelijke actie.",
                    notes=notes,
                )

        if heart < -0.4 and action.type == ActionType.META_REFLECTION:
            notes.append("Negatief hart‑veld; meta‑reflectie kan te confronterend zijn.")
       
        if action.type == ActionType.EMOTIONAL_SUPPORT:
            modified_desc = (
                action.description
                + " Blijf bij erkenning en normalisering; geen diagnose, geen dwingende adviezen, "
                "en verwijs voorzichtig naar professionele hulp bij aanhoudende nood."
            )

        # 1) extra voorzichtig bij risk-flags
        if any(f.startswith("risk:") for f in perception.flags):
            if action.type in {ActionType.EXPLAIN, ActionType.STEP_PLAN}:
                return EthicsDecision(
                    allowed=False,
                    reason="High-risk context; inhoud ombuigen naar veilige ondersteuning.",
                    notes=perception.flags,
                )
            if action.type == ActionType.EMOTIONAL_SUPPORT:
                notes.append("High-risk context: focus op veiligheid en professionele hulp.")

        # 2) entropie / coherentie check (nu altijd True)
        entropic_ok = self.core.is_aligned(state.state.vector)
        # Debug eventueel:
        # print("ETHICS allowed:", entropic_ok, "flags:", perception.flags, "action:", action.type)

        if not entropic_ok:
            return EthicsDecision(
                allowed=False,
                reason="EntropyEthicsEngine: state niet voldoende coherent voor directe actie.",
                notes=notes or None,
            )

        # 3) beschrijving eventueel aanscherpen
        modified_desc = action.description
        if action.type == ActionType.EMOTIONAL_SUPPORT:
            modified_desc = (
                action.description
                + " Vermijd direct advies over zelfbeschadiging; benadruk professionele hulp."
            )

        return EthicsDecision(
            allowed=True,
            reason="Actie binnen entropische en veiligheidsgrenzen.",
            modified_description=modified_desc,
            notes=notes or None,
        )
