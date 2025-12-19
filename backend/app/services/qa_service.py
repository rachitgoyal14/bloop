from langchain_chroma import Chroma
from langchain_nomic import NomicEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from core.config import VECTOR_DB_DIR
from services.vision_service import extract_text_from_image

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    max_tokens=512,
    timeout=30,
    max_retries=2,
)





SUMMARY_KEYWORDS = [
    "summarize",
    "summary",
    "explain",
    "overview",
    "what is this document about",
    "key points",
    "gist",
    "ELI5"
]

def is_summary_question(question: str) -> bool:
    q = question.lower()
    return any(k in q for k in SUMMARY_KEYWORDS)


def extract_question_from_text(ocr_text: str) -> str:
    prompt = f"""
You are an educational assistant.

From the text below, extract the MAIN question being asked.
If multiple questions exist, pick the most relevant one.
If no clear question exists, rewrite the text into a clear question.

Return ONLY the question.

Text:
{ocr_text}

Question:
"""
    response = llm.invoke(prompt)
    return response.content.strip()



def answer_ques(
        question: str, 
        document_id: str | None = None,
        image_path:str|None=None
        ) -> str:
    
    if image_path:
        ocr_text = extract_text_from_image(image_path)

        if not ocr_text.strip():
            return "I could not extract any readable text from the image."

        question = extract_question_from_text(ocr_text)

    if not question or not question.strip():
        return "No valid question could be determined."
    is_summary = is_summary_question(question)

    if document_id:
        vector_db = Chroma(
            collection_name=document_id,
            embedding_function=NomicEmbeddings(
                model="nomic-embed-text-v1.5",
            ),
            persist_directory=VECTOR_DB_DIR,
        )

        retrieval_query = (
            "summary of the document"
            if is_summary
            else question
        )

        docs_with_score = vector_db.similarity_search_with_score(
            retrieval_query,
            k=12
        )

        for _, score in docs_with_score:
            print("Similarity score:", score)

        print("Collection:", document_id)
        print("DB path:", VECTOR_DB_DIR)
        print("Docs retrieved:", len(docs_with_score))



        if is_summary:
            docs = [doc for doc, _ in docs_with_score]
        else:
            docs = [
                doc for doc, score in docs_with_score
                if score < 0.6
            ]

        if not docs:
            return "I don't know."

        context = "\n".join(doc.page_content for doc in docs)

        if is_summary:
            prompt = f"""
You are an educational assistant.
Using ONLY the document content below, answer the user's request.
You may summarize, explain, or reorganize the information,
but do NOT add information not present in the document.

Document:
{context}

Task:
{question}

Answer:
"""
        else:
            prompt = f"""
You are an educational assistant.
Answer the question ONLY using the context below.
If the answer is not present in the context, reply with:
"I don't know."

Context:
{context}

Question:
{question}

Answer:
"""

    else:
        prompt = f"""
Answer the following question clearly and concisely.

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)
    return response.content.strip()
