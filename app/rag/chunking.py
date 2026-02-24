

from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.monitoring.mlflow_logger import  log_chunking_config


EMBEDDINGS = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)

SEMANTIC_SPLITTER = SemanticChunker(EMBEDDINGS)

RECURSIVE_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=120
)


def clean_text(text: str) -> str:
    text = text.strip()
    text = " ".join(text.split())
    return text


def hybrid_chunking(docs):

    chunks = []

    for i, d in enumerate(docs):

        text = clean_text(d["text"])

        if len(text) < 80:
            continue

        semantic_splits = SEMANTIC_SPLITTER.split_text(text)

        for j, part in enumerate(semantic_splits):

            part = clean_text(part)

            if len(part) > 900:
                sub_chunks = RECURSIVE_SPLITTER.split_text(part)
            else:
                sub_chunks = [part]

            for k, s in enumerate(sub_chunks):

                if len(s) < 80:
                    continue

                chunks.append({
                    "text": s,
                    "metadata": {
                        **d["metadata"],
                        "doc_id": i,
                        "semantic_part": j,
                        "sub_part": k,
                        "length": len(s)
                    }
                })

    print(f"[CHUNKING] Total chunks générés : {len(chunks)}")


    
    log_chunking_config({
    "chunking_strategy": "hybrid",
    "semantic_chunker": SEMANTIC_SPLITTER.__class__.__name__,
    "embedding_model_chunking": EMBEDDINGS.model_name,

    "recursive_chunk_size": RECURSIVE_SPLITTER._chunk_size,
    "recursive_overlap": RECURSIVE_SPLITTER._chunk_overlap,

    "min_chunk_length": 80,
    "max_semantic_length": 900,

    "text_cleaning": True,
    })





    return chunks
