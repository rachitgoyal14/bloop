from fastapi import APIRouter,UploadFile,File
from services.sad_talker_service import run_sadtalker
from core.config import INPUT_IMAGE_DIR,INPUT_AUDIO_DIR
import os
import shutil


router = APIRouter(prefix="/video",tags=["SadTalker Vdeo"])

@router.post("/generate")
async def generate_video(image: UploadFile = File(...), 
                        audio: UploadFile = File(...)
                    ):
    image_path = os.path.join(INPUT_IMAGE_DIR, image.filename)
    audio_path = os.path.join(INPUT_AUDIO_DIR, audio.filename)

    with open(image_path,"wb") as img_file:
        shutil.copyfileobj(image.file,img_file)

    with open(audio_path,"wb") as audio_file:
        shutil.copyfileobj(audio.file,audio_file)

    job_id = run_sadtalker(image_path, audio_path)
    
    return {
        "status": "processing",
        "job_id": job_id
        }
