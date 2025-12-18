from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional

from services.play.teach_ai_service import TeachAIService
from services.stt_service import STTService
from services.tts_service import text_to_speech  

router = APIRouter(prefix="/play/teach-ai", tags=["Play | Teach AI"])

teach_ai_service = TeachAIService()
stt_service = STTService()


# -------------------------------
# Schemas
# -------------------------------

class TeachAIEvaluationResponse(BaseModel):
    scores: dict
    feedback: list[str]
    follow_up_question: Optional[str]
    passed: bool


# -------------------------------
# MAIN ENDPOINT (TEXT FIRST)
# -------------------------------

@router.post("/evaluate", response_model=TeachAIEvaluationResponse)
async def evaluate_teach_ai(
    concept_id: str = Form(...),
    level: str = Form("beginner"),
    explanation: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None)
):
    """
    Teach-the-AI evaluation.

    Priority:
    1. Use text explanation if provided
    2. Else use backend STT if audio is provided
    3. Else throw error
    """

    final_explanation: Optional[str] = None

    # 1️⃣ Text-first
    if explanation and explanation.strip():
        final_explanation = explanation.strip()

    # 2️⃣ Audio fallback
    elif audio:
        final_explanation = stt_service.transcribe(audio)

        if not final_explanation:
            raise HTTPException(
                status_code=400,
                detail="STT failed to produce transcript"
            )

    # 3️⃣ Nothing provided
    else:
        raise HTTPException(
            status_code=400,
            detail="Either explanation text or audio file must be provided"
        )

    # -------------------------------
    # Evaluate explanation
    # -------------------------------

    return teach_ai_service.evaluate(
        concept_id=concept_id,
        explanation=final_explanation,
        level=level
    )


# -------------------------------
# AI FEEDBACK → TTS (UNCHANGED)
# -------------------------------

@router.post("/feedback-tts")
async def teach_ai_feedback_tts(text: str = Form(...)):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    audio_path = text_to_speech(text)

    return {
        "audio_path": audio_path
    }
