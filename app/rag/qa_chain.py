
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from app.rag.retriever import get_retriever
import os
from langchain.prompts import PromptTemplate
from app.monitoring.mlflow_logger import log_llm_params,log_rag_pipeline_artifacts
import mlflow
from functools import lru_cache
from app.rag.prompt import RESPONSE_GENERATION_PROMPT


@lru_cache(maxsize=1)
def get_qa_chain():

    llm = Ollama(
        model="mistral:latest",
        temperature=0,
        top_k=10,
        top_p=0.9,
        base_url="http://ollama:11434"
    )

    prompt = PromptTemplate(
        template=RESPONSE_GENERATION_PROMPT,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=get_retriever(),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True  
    )

    if mlflow.active_run():
        log_llm_params({
            "model": "mistral:latest",
            "temperature": 0,
            "top_k": 10,
            "top_p": 0.9
        })

        log_rag_pipeline_artifacts(
            prompt_template=RESPONSE_GENERATION_PROMPT,
            indexing_hybrid_chunking_config={
                "chunking_strategy": "hybrid",
                "semantic_chunker": "SemanticChunker",
                "embedding_model_chunking": "BAAI/bge-base-en-v1.5",

                "recursive_chunk_size": 600,
                "recursive_overlap": 120,

                "min_chunk_length": 80,
                "max_semantic_length": 900,

                "text_cleaning": True,
            },
            retriever_config={
                "vector_db": "chroma",
                "collection_name": "CliniQ _rag",
                "dense": {"type": "mmr", "k": 6, "fetch_k": 20, "lambda_mult": 0.8},
                "bm25_k": 2,
                "reranker_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
                "top_k": 6,
            },
            llm_config={
                "model": "mistral:latest",
                "temperature": 0,
                "top_k": 10,
                "top_p": 0.9
            }
            


        )



    return qa_chain
