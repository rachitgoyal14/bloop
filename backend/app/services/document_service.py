from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_nomic import NomicEmbeddings
from core.config import VECTOR_DB_DIR
import uuid


def ingest_document(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()


    splitter = RecursiveCharacterTextSplitter(
        chunk_size =700,
        chunk_overlap =150
    )

    chunks = splitter.split_documents(docs)

    embeddings = NomicEmbeddings(
        model = "nomic-embed-text-v1.5"
    )

    doc_id = str(uuid.uuid4())

    vector_db = Chroma(
        collection_name=doc_id,
        embedding_function=embeddings,
        persist_directory=VECTOR_DB_DIR
    )

    vector_db.add_documents(chunks)
    # vector_db.persist()

    return doc_id


