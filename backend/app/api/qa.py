from fastapi import UploadFile,APIRouter,File
from services.document_service import ingest_document
from services.qa_service import answer_ques
from utils.file_utils import save_file
from core.config import DOCUMENT_UPLOAD_DIR

router = APIRouter(prefix="/qa",tags=["Docuemt ask enpoitns"])

@router.post("/upload-doc")
async def upload_file(file:UploadFile= File(...)):
    file_path = save_file(file,DOCUMENT_UPLOAD_DIR)
    doc_id = ingest_document(file_path)
    return {
        "document_id": doc_id,
        "status": "uploaded"
    }

@router.post("/ask")
async def ask_question (question:str,document_id:str |None = None):
    answer = answer_ques(question,document_id)
    return {"answer":answer}
