from fastapi import APIRouter
from fastapi.responses import FileResponse
from services.tts_service import text_to_speech

router = APIRouter(prefix="/tts", tags=["TTS"])

@router.post("/answer")
def speak_answer(text: str):
    audio_path = text_to_speech(text)

    return FileResponse(
        audio_path,
        media_type="audio/wav",
        filename="answer.wav"
    )