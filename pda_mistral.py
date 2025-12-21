# pda_mistral.py

from mistralai import Mistral
import os

# GitHub injects this automatically
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise RuntimeError("MISTRAL_API_KEY not found in environment. Add it to GitHub Codespaces Secrets.")


def chat(
    system_prompt: str, 
    user_prompt: str, 
    temperature: float = 0.7,
    max_tokens: int = 200,        # ✅ ADD
    top_p: float = 0.95,          # ✅ ADD
    frequency_penalty: float = 0.3,  # ✅ ADD (optioneel voor Mistral)
    presence_penalty: float = 0.2    # ✅ ADD (optioneel voor Mistral)
) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    
    return resp.choices[0].message.content


_api_key = os.getenv("MISTRAL_API_KEY")
if not _api_key:
    raise RuntimeError("MISTRAL_API_KEY ontbreekt of is leeg")

client = Mistral(api_key=_api_key)
MODEL_NAME = "mistral-small-latest"  # begin met small, goedkoper/stabiel [web:539]


def chat(system_prompt: str, user_prompt: str, temperature: float = 0.4) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",  "content": user_prompt},
    ]
    try:
        resp = client.chat.complete(
            model=MODEL_NAME,
            messages=messages,
            temperature=temperature,
        )
        return resp.choices[0].message.content
    except Exception as e:
        print("Mistral error:", repr(e))
        raise