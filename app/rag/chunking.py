# from langchain_experimental.text_splitter import SemanticChunker
# from langchain_community.embeddings import HuggingFaceEmbeddings

# def semantic_chunking(docs):

#     embeddings = HuggingFaceEmbeddings(
#         model_name="all-MiniLM-L6-v2"
#     )

#     splitter = SemanticChunker(embeddings)

#     chunks = []

#     for d in docs:
#         split = splitter.split_text(d["text"])

#         for s in split:
#             chunks.append({
#                 "text": s,
#                 "metadata": d["metadata"]
#             })

#     return chunks


# def semantic_chunking(docs):
#     embeddings = HuggingFaceEmbeddings(
#         model_name="all-MiniLM-L6-v2"
#     )

#     splitter = SemanticChunker(embeddings)

#     chunks = []

#     for d in docs:
#         split_texts = splitter.split_text(d["text"])
#         for s in split_texts:
#             chunks.append({
#                 "text": s,
#                 "metadata": d["metadata"]
#             })

#     return chunks

# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_experimental.text_splitter import SemanticChunker
# from langchain_community.embeddings import HuggingFaceEmbeddings

# def hybrid_chunking(docs):

#     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#     semantic = SemanticChunker(embeddings)

#     recursive = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=100
#     )

#     chunks = []

#     for d in docs:
#         text = d["text"]

#         # 1) Découpage sémantique
#         semantic_splits = semantic.split_text(text)

#         for part in semantic_splits:

#             # 2) Redécouper si trop grand
#             if len(part) > 700:
#                 sub = recursive.split_text(part)
#             else:
#                 sub = [part]

#             for s in sub:
#                 chunks.append({
#                     "text": s,
#                     "metadata": d["metadata"]
#                 })

#     return chunks

from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.monitoring.mlflow_logger import  log_chunking_config

# Charger une seule fois
# EMBEDDINGS = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
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



    # log_chunking_config({
    #     "chunking_strategy": "hybrid",
    #     "semantic_chunker": "SemanticChunker",
    #     "embedding_model_chunking": "all-MiniLM-L6-v2",

    #     "recursive_chunk_size": 600,
    #     "recursive_overlap": 120,

    #     "min_chunk_length": 80,
    #     "max_semantic_length": 900,

    #     "text_cleaning": True,

    #     # === EMBEDDING ===
    #     "embedding_model": "all-MiniLM-L6-v2",
    #     "embedding_dimension": 384
    # })
    
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
