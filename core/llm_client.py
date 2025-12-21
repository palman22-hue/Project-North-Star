# core/llm_client.py
from __future__ import annotations
from typing import Any, Dict

import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral:latest"  # jij gebruikt deze tag

# placeholder: hier kun je later Mistral / OpenAI / lokaal model inprikken


def build_prompt(
    action_type: str,
    hint: str,
    perception: Any,
    decision: Any,
    memory_summary: str,
) -> str:
    """Zet alle context om in één duidelijke NL‑prompt voor de LLM."""
    emotions = perception.emotions or {}
    flags = perception.flags or []

    return f"""Je bent een zorgzame, nuchtere Personal Digital Assistant (PDA), 
    niet de psychische aandoening PTSS. Je helpt de gebruiker vanuit een 32-dimensionale 
    innerlijke staat (emoties, waarden, intenties).

Doel van deze beurt:
- Actietype: {action_type}
- Beschrijving: {hint}

Context:
- Intent: {perception.intent.value}
- Emoties (ruw): {emotions}
- Veiligheidsflags: {flags}
- Gesprekssamenvatting: {memory_summary}

Richtlijnen:
- Volg de beschrijving en ethische grenzen hierboven.
- Schrijf in het Nederlands, warm maar helder.
- Geen diagnoses, geen medische claims, geen beloftes.
- Maximaal één alinea + eventueel een vervolgvraag.
- Gebruik "PDA" altijd als Personal Digital Assistant, nooit als psychische stoornis.
- Spreek in ik vorm
- Geen herhalingen van disclaimers
- Als de intentie ASK_PDA_SELF is, antwoord in maximaal 3 zinnen
- Leg kort uit: wat PDA32D is, 
- Wat je voor de gebruiker doet,
- 1 zin over je grenzen
- Vermijd lange medische disclaimers, noem alleen dat je geen diagnoses of behandelingen biedt
- Antwoord bij intent ASK_PDA_SELF in maximaal 2 zinnen
- Noem één korte zin over beperkingen,
- vermijd details zoals ‘raadpleeg altijd een menselijk gesprek’ tenzij er expliciet naar risico/nood wordt gevraagd  
  Geef nu alleen de tekst van je antwoord:"""



def call_llm(prompt: str) -> str:
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", "").strip()


def generate_text(system_prompt: str, user_prompt: str) -> str:
    from pda_mistral import chat
    
    # Roep alleen aan met de parameters die chat() accepteert
    return chat(system_prompt, user_prompt)


