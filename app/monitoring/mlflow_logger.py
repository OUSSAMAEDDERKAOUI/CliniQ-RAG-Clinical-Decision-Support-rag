import mlflow
import os
from datetime import datetime
import time
import json
from pathlib import Path

EXPERIMENT = os.getenv("MLFLOW_EXPERIMENT", "rag_biomedical")


def init_mlflow():
    
    uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")

    mlflow.set_tracking_uri(uri)
    mlflow.set_experiment(EXPERIMENT)



def start_rag_run(run_type: str, suffix: str = ""):
    init_mlflow()

    if mlflow.active_run():
        mlflow.end_run()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    run_name = f"{run_type}_{suffix}_{timestamp}" if suffix else f"{run_type}_{timestamp}"

    return mlflow.start_run(run_name=run_name)




def log_chunking_config(config: dict):
    for k, v in config.items():
        mlflow.log_param(k, v)


def log_retrieval_params(params: dict):
    for k, v in params.items():
        mlflow.log_param(k, v)


def log_llm_params(params: dict):
    for k, v in params.items():
        mlflow.log_param(k, v)


def log_answer(question, answer):
    mlflow.log_text(question, "réponses & contextes/question.txt")
    mlflow.log_text(answer, "réponses & contextes/answer.txt")


def end_run():
    mlflow.end_run()


def log_retriever_config():

    mlflow.log_params({

        "vector_db": "chroma",
        "collection_name": "biomedical",

        "retrieval_type": "hybrid",
        "dense_search_type": "mmr",
        "dense_k": 6,
        "dense_fetch_k": 20,
        "dense_lambda": 0.8,

        "bm25_k": 2,

        "reranker_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
        "rerank_top_k": 6
    })


def log_retrieval_query(query: str, docs, scores):

    mlflow.log_param("last_query", query)

    mlflow.log_metric("num_docs_before_rerank", len(scores))
    mlflow.log_metric("num_docs_after_rerank", len(docs))

    for i, score in enumerate(scores):
        mlflow.log_metric(f"rerank_score_{i}", float(score))

    context_text = "\n\n----\n\n".join([d.page_content for d in docs])

    mlflow.log_text(context_text, "réponses & contextes/retrieved_context.txt")


def start_retrieval_timer():
    return time.time()


def end_retrieval_timer(start):
    duration = time.time() - start
    mlflow.log_metric("retrieval_time_sec", duration)




def log_rag_pipeline_artifacts(
    prompt_template: str,
    indexing_hybrid_chunking_config: dict,
    retriever_config: dict,
    chunking_config: dict | None = None,
    llm_config: dict | None = None,
    extra: dict | None = None,
):
    mlflow.log_text(prompt_template, "pipeline RAG/prompt_template.txt")
    mlflow.log_dict(indexing_hybrid_chunking_config, "pipeline RAG/indexing_hybrid_chunking_config.json")
    mlflow.log_dict(retriever_config, "pipeline RAG/retriever_config.json")

    if chunking_config:
        mlflow.log_dict(chunking_config, "pipeline RAG/chunking_config.json")

    if llm_config:
        mlflow.log_dict(llm_config, "pipeline RAG/llm_config.json")

    if extra:
        mlflow.log_dict(extra, "pipeline RAG/extra.json")