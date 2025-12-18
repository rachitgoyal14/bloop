from services.document_content_service import get_document_chunks
from langchain_groq import ChatGroq


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2
)

def generate_quiz(document_id: str, count: int = 5):
    chunks = get_document_chunks(document_id)

    context = "\n".join(chunks)

    prompt = f"""
You are an educational assistant.

Generate {count} multiple-choice questions (MCQs) from the document.

Rules:
- Each question must be answerable from the document
- Provide 4 options
- Exactly ONE option must be correct
- Do NOT add external knowledge
- Output ONLY valid JSON in the format:

[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "B"
  }}
]

Document content:
{context}
"""

    response = llm.invoke(prompt)
    return response.content