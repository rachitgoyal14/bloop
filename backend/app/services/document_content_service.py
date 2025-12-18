from langchain_chroma import Chroma
from langchain_nomic import NomicEmbeddings

VECTOR_DB_DIR = "vectorstore/chroma_db"



def get_document_chunks(document_id:str,k: int =15)->list [str]:
    vector_db = Chroma(
        collection_name=document_id,
        embedding_function=NomicEmbeddings(
            model="nomic-embed-text-v1.5"
        ),
        persist_directory=VECTOR_DB_DIR
    )
     
    docs = vector_db.similarity_search(
          "core concepts and key ideas of the document",
          k=k
    )

    return [doc.page_content for doc in docs]

