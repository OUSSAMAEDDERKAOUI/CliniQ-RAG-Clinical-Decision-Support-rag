from langchain_community.vectorstores import Chroma
from app.rag.embeddings import get_embeddings
import chromadb
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from sentence_transformers import CrossEncoder
from langchain.schema import BaseRetriever, Document
from typing import List
import hashlib
import mlflow
from app.monitoring.mlflow_logger import (
    log_retriever_config,
    log_retrieval_query,
    start_retrieval_timer,
    end_retrieval_timer
)
from functools import lru_cache
from langchain.schema import BaseRetriever, Document
from typing import List
from pydantic import Field
import hashlib

from langchain.schema import BaseRetriever, Document
from typing import List

class EmptyRetriever(BaseRetriever):
    def _get_relevant_documents(self, query: str) -> List[Document]:
        return []


@lru_cache(maxsize=1)
def get_vectorstore():
    emb = get_embeddings()  
    client = chromadb.HttpClient(host="chroma", port=8000)
    client.get_or_create_collection(name="biomedical")

    return Chroma(
        client=client,
        collection_name="biomedical",
        embedding_function=emb
    )





@lru_cache(maxsize=1)
def load_chunks_from_chroma():


    vectorstore = get_vectorstore()

    all_data = vectorstore.get()

    docs = []

    for text, metadata in zip(all_data["documents"], all_data["metadatas"]):
        docs.append({
            "text": text,
            "metadata": metadata
        })

    return docs




class HybridRetriever(BaseRetriever):
    dense_retriever: BaseRetriever = Field(...)
    bm25_retriever: BaseRetriever = Field(...)
    reranker: object = Field(...)
    top_k: int = 4

    def _deduplicate(self, docs: List[Document]) -> List[Document]:
        seen = set()
        unique = []

        for d in docs:
            h = hashlib.md5(d.page_content.encode()).hexdigest()
            if h not in seen:
                seen.add(h)
                unique.append(d)

        return unique

    
    def _rerank(self, query: str, docs: List[Document]) -> List[Document]:

        pairs = [(query, d.page_content) for d in docs]
        scores = self.reranker.predict(pairs)
    
        ranked = sorted(
            zip(docs, scores),
            key=lambda x: x[1],
            reverse=True
        )
    
        final_docs = [doc for doc, _ in ranked[: self.top_k]]
        final_scores = [score for _, score in ranked[: self.top_k]]
    
        if mlflow.active_run():
            log_retrieval_query(query, final_docs, final_scores)
    
        return final_docs




    def _get_relevant_documents(self, query: str) -> List[Document]:

        start = start_retrieval_timer()
    
        dense_docs = self.dense_retriever.invoke(query)
        sparse_docs = self.bm25_retriever.invoke(query)
    
        merged = dense_docs + sparse_docs
        deduped = self._deduplicate(merged)
    
        results = self._rerank(query, deduped)
    
        end_retrieval_timer(start)
    
        return results


@lru_cache(maxsize=1)
def get_reranker():
    return CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


@lru_cache(maxsize=1)
def get_retriever():
    
    vectorstore = get_vectorstore()

    dense_retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 6,
            "fetch_k": 20,
            "lambda_mult": 0.8
        }
    )

    docs = load_chunks_from_chroma()
    documents = [
        Document(page_content=d["text"], metadata=d["metadata"])
        for d in docs
    ]
    docs = load_chunks_from_chroma()
    if not docs:
        bm25_retriever = EmptyRetriever()
    else:
        bm25_retriever = BM25Retriever.from_documents(documents)
        bm25_retriever.k = 3



    reranker=get_reranker()


    retriever = HybridRetriever(
    dense_retriever=dense_retriever,
    bm25_retriever=bm25_retriever,
    reranker=reranker,
    top_k=6
    )

    if mlflow.active_run():
        log_retriever_config()

    return retriever


