import os
import uuid
from TTS.api import TTS
from core.config import AUDIO_DIR
import torch 

AUDIO_DIR = AUDIO_DIR
os.makedirs(AUDIO_DIR,exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

def text_to_speech(text:str)->str:
    filename = f"{uuid.uuid4()}.wav"
    path = os.path.join(AUDIO_DIR,filename)

    tts.tts_to_file(text=text,file_path=path)

    return path