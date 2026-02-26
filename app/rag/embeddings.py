# from langchain_community.embeddings import HuggingFaceEmbeddings

# def get_embeddings():
#     print("🔥 get_retriever called")
#     return  HuggingFaceEmbeddings(
#     model_name="BAAI/bge-base-en-v1.5"
#     )

from functools import lru_cache
from langchain_community.embeddings import HuggingFaceEmbeddings

@lru_cache(maxsize=1)
def get_embeddings():
    print(" Loading embeddings ONCE")
    return HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")