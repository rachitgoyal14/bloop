from fastapi import APIRouter
from services.roadmap_service import generate_roadmap

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])

@router.get("/{document_id}")
def get_roadmap(document_id: str):
    return generate_roadmap(document_id)
