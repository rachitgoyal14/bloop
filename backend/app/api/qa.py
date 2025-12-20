from fastapi import UploadFile,APIRouter,File
from services.document_service import ingest_document
from services.qa_service import answer_ques
from services.sad_talker_service import run_sadtalker
from services.tts_service import text_to_speech
from utils.file_utils import save_file
from core.config import DOCUMENT_UPLOAD_DIR
import uuid
import requests

router = APIRouter(prefix="/qa",tags=["Document Ask Endpoints"])

MANIM_SERVICE_URL = "http://127.0.0.1:8001/explain"

@router.post("/upload-doc")
async def upload_file(file:UploadFile= File(...)):
    file_path = save_file(file,DOCUMENT_UPLOAD_DIR)
    doc_id = ingest_document(file_path)
    return {
        "document_id": doc_id,
        "status": "uploaded"
    }

@router.post("/ask")
async def ask_question(
    question: str,
    document_id: str | None = None,
    video_enabled: bool = False,
    face_enabled: bool = False
):
    answer = answer_ques(question, document_id)

    response = {
        "answer": answer,
        "video_enabled": video_enabled,
        "face_enabled": face_enabled
    }

    # 🎬 Delegate to Manim backend
    if video_enabled:
        manim_payload = {
            "topic": answer,            # IMPORTANT: use ANSWER, not raw question
            "level": "school",
            "persona": "teacher",
            "face_enabled": face_enabled
        }

        manim_response = requests.post(
            MANIM_SERVICE_URL,
            params=manim_payload,
            timeout=300
        )

        if manim_response.status_code != 200:
            return {
                "answer": answer,
                "error": "Manim generation failed"
            }

        response.update({
            "video_status": "processing",
            "manim_pipeline": True
        })

    return response

@router.post("/ask-from-image")
def ask_from_image(
    image: UploadFile = File(...),
    document_id: str | None = None,     
    video_enabled: bool = False,
    image_path: str = "D:/bloop/data/avatars/sir-isaac-newton.webp"

):
    job_id = str(uuid.uuid4())
    path = save_file(image, "data/uploads/images")

    answer = answer_ques(
        question=None,
        document_id=document_id,
        image_path=path
    )
    response = {
        "answer": answer,
        "video_enabled": video_enabled
    }
    if video_enabled:
        audio_path = text_to_speech(answer, job_id)
        run_sadtalker(image_path, audio_path, job_id)

        response.update({
            "job_id": job_id,
            "video_status": "processing",
            "audio_available": True
        })



    return {"answer": answer}

