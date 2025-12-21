# session_logger.py
from datetime import datetime
from pathlib import Path
import json

LOG_PATH = Path("session_log.jsonl")

def log_turn(session_id: str,
             role: str,
             text: str,
             state_vector,
             extras: dict | None = None) -> None:
    record = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "role": role,          # "user" of "pda"
        "text": text,
        "state_vector": state_vector,
    }
    if extras:
        record.update(extras)

    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

