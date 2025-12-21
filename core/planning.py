# planning.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum

from core.perception import PerceptionResult, Intent
from core.memory import ConversationMemory
from pda32d_base import PDA32D


class ActionType(str, Enum):
    EXPLAIN = "explain"
    ASK_CLARIFY = "ask_clarify"
    EMOTIONAL_SUPPORT = "emotional_support"
    META_REFLECTION = "meta_reflection"
    STEP_PLAN = "step_plan"


@dataclass
class PlannedAction:
    type: ActionType
    description: str
    priority: float = 1.0
    payload: Dict[str, Any] = field(default_factory=dict)
    ethics_check_required: bool = True


@dataclass
class Plan:
    actions: List[PlannedAction] = field(default_factory=list)

    def top(self) -> PlannedAction | None:
        if not self.actions:
            return None
        return sorted(self.actions, key=lambda a: a.priority, reverse=True)[0]


class Planner:
    def __init__(self):
        pass

    def make_plan(
        self,
        memory: ConversationMemory,
        state: PDA32D,
        perception: PerceptionResult,
    ) -> Plan:
        actions: List[PlannedAction] = []
        coherence = state.coherence()
        emo = perception.emotions or {}
        distress_keys = {"despair", "fear", "emptiness", "isolation", "shame"}
        distress_level = max((emo.get(k, 0.0) for k in distress_keys), default=0.0)

        if distress_level < -0.5:  # sterke negatieve waarde
            actions.append(
                PlannedAction(
                    type=ActionType.EMOTIONAL_SUPPORT,
                    description="De gebruiker lijkt het zwaar te hebben; reageer vooral steunend en voorzichtig, geen harde adviezen.",
                    priority=1.2,
                )
            )

        # Bij lage coherence: altijd eerst verduidelijken
        if coherence < 0.5:
            actions.append(
                PlannedAction(
                    type=ActionType.ASK_CLARIFY,
                    description="Je klinkt wat versnipperd; kun je iets concreter vertellen wat je nu het meest bezighoudt?",
                    priority=1.1,  # hoger dan de rest
                )
            )
        # basis op intent
        if perception.intent == Intent.HELP_REQUEST:
            actions.append(
                PlannedAction(
                    type=ActionType.EXPLAIN,
                    description="Leg duidelijk het gevraagde concept of probleem uit.",
                    priority=0.9,
                )
            )
            actions.append(
                PlannedAction(
                    type=ActionType.STEP_PLAN,
                    description="Bied een kort stappenplan om het doel te bereiken.",
                    priority=0.7,
                )
            )

        elif perception.intent == Intent.ASK_PDA_SELF:
            actions.append(
                PlannedAction(
                    type=ActionType.EXPLAIN,
                    description="Antwoord in maximaal 3 zinnen in ik‑vorm: wat PDA32D is, "
                                "hoe je de gebruiker helpt, en een korte zin over je beperkingen "
                                "zonder uitgebreide medische disclaimers.",
                    priority=1.0,
                 )
            )

            actions.append(
                PlannedAction(
                    type=ActionType.ASK_CLARIFY,
                    description="Vraag op een zachte manier waar de gebruiker vooral nieuwsgierig naar is over jou of het systeem.",
                    priority=0.6,
                  )
            )


        elif perception.intent == Intent.META_SYSTEM:
            actions.append(
                PlannedAction(
                    type=ActionType.META_REFLECTION,
                    description="Reflecteer op PDA‑architectuur, 32D‑state en designkeuzes.",
                    priority=0.9,
                )
            )

        else:
            actions.append(
                PlannedAction(
                    type=ActionType.ASK_CLARIFY,
                    description="Vraag wat de gebruiker precies wil bereiken.",
                    priority=0.8,
                )
            )

        # context hooks (voorbeeld)
        if len(memory.turns) > 10:
            actions.append(
                PlannedAction(
                    type=ActionType.META_REFLECTION,
                    description="Maak een korte reflectie op de voortgang in dit gesprek.",
                    priority=0.3,
                    ethics_check_required=False,
                )
            )

        return Plan(actions=actions)
