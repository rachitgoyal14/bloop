import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

SADTALKER_DIR = os.path.join(BASE_DIR, "ai_models", "SadTalker")
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCUMENT_UPLOAD_DIR = os.path.join(DATA_DIR, "documents")
AUDIO_DIR = os.path.join(DATA_DIR,"audio/answers")

VECTOR_DB_DIR = os.path.join(BASE_DIR, "backend", "app", "vectorstore", "chroma_db")

INPUT_IMAGE_DIR = os.path.join(DATA_DIR, "input_images")
INPUT_AUDIO_DIR = os.path.join(DATA_DIR, "input_audio")
OUTPUT_VIDEO_DIR = os.path.join(DATA_DIR, "generated_videos")

os.makedirs(INPUT_IMAGE_DIR, exist_ok=True)
os.makedirs(INPUT_AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_VIDEO_DIR, exist_ok=True)
os.makedirs(DOCUMENT_UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)

# ==============================
# API KEYS (ENVIRONMENT VARIABLES)
# ==============================


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set in environment variables")

if not ASSEMBLYAI_API_KEY:
    raise RuntimeError("ASSEMBLYAI_API_KEY not set in environment variables")