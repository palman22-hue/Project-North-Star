from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from engine import handle_turn
import uvicorn

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

class TurnRequest(BaseModel):
    session_id: str
    user_text: str

class TurnResponse(BaseModel):
    assistant_text: str
    state_vector: list = []
    coherence: float = 1.0

@app.get("/")
async def root():
    """Serve de HTML UI"""
    return FileResponse("static/index.html")

@app.post("/turn")
async def turn(request: TurnRequest) -> TurnResponse:
    result = handle_turn(request.session_id, request.user_text)
    
    print(f"[API DEBUG] Coherence: {result.get('coherence')}")  # ✨ debug
    print(f"[API DEBUG] State sum: {sum(result.get('state_vector', []))}")  # ✨ debug
    
    return TurnResponse(
        assistant_text=result["assistant_text"],
        state_vector=result.get("state_vector", [0.0] * 32),
        coherence=result.get("coherence", 1.0)
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)