from fastapi import APIRouter, FastAPI
import requests
from pydantic import BaseModel
router = APIRouter(prefix="/manim",tags=["Video generation endpoints"])

class ExplainRequest(BaseModel):
    topic: str
    level: str = "school"
    persona: str = "teacher"

@router.post("/explain")
async def explain(request: ExplainRequest):
    request_data = {
        "topic": request.topic,
        "level": request.level,
        "persona": request.persona
    }
    response = requests.post("http://localhost:8001/explain", json=request_data)
    return response.json()
