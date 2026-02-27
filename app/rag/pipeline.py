from app.rag.loader import load_pdf
from app.rag.chunking import hybrid_chunking
from app.rag.vector_store import store_chunks,reset_chroma
import json
import os
from app.monitoring.mlflow_logger import start_rag_run
import mlflow




def save_chunks_debug(chunks):

    os.makedirs("data/processed_chunks", exist_ok=True)

    with open("data/processed_chunks/chunks_debug.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)

def build_pipeline(pdf_path):

   
    with start_rag_run("indexing ","hybrid_chunking"):

        reset_chroma()
        docs = load_pdf(pdf_path)
        # grouped_docs = group_docs_by_page(docs)

        chunks = hybrid_chunking(docs)

        save_chunks_debug(chunks)
        store_chunks(chunks)

        mlflow.log_param("nb_documents", len(docs))
        mlflow.log_param("nb_chunks", len(chunks))

    return {
        "documents": len(docs),
        "nb_chunks": len(chunks),
        "chunks": chunks[:10]
    }


