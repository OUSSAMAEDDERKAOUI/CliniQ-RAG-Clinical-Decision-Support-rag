# import mlflow
# import os
# from datetime import datetime
# import time

# MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI")
# EXPERIMENT = os.getenv("MLFLOW_EXPERIMENT", "rag_biomedical")

# mlflow.set_tracking_uri(MLFLOW_URI)
# mlflow.set_experiment(EXPERIMENT)


# def start_rag_run():
#     run_name = f"rag_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
#     return mlflow.start_run(run_name=run_name)


# def log_chunking_config(config: dict):
#     for k, v in config.items():
#         mlflow.log_param(k, v)


# def log_retrieval_params(params: dict):
#     for k, v in params.items():
#         mlflow.log_param(k, v)


# def log_llm_params(params: dict):
#     for k, v in params.items():
#         mlflow.log_param(k, v)


# def log_answer(question, answer):
#     mlflow.log_text(question, "question.txt")
#     mlflow.log_text(answer, "answer.txt")


# def end_run():
#     mlflow.end_run()







# def log_retriever_config():

#     mlflow.log_params({

#         # Vector DB
#         "vector_db": "chroma",
#         "collection_name": "biomedical",

#         # Dense retriever
#         "retrieval_type": "hybrid",
#         "dense_search_type": "mmr",
#         "dense_k": 6,
#         "dense_fetch_k": 20,
#         "dense_lambda": 0.8,

#         # Sparse retriever
#         "bm25_k": 1,

#         # Reranker
#         "reranker_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
#         "rerank_top_k": 6
#     })


# def log_retrieval_query(query: str, docs, scores):

#     mlflow.log_param("last_query", query)

#     mlflow.log_metric("num_docs_before_rerank", len(scores))
#     mlflow.log_metric("num_docs_after_rerank", len(docs))

#     for i, score in enumerate(scores):
#         mlflow.log_metric(f"rerank_score_{i}", float(score))

#     context_text = "\n\n----\n\n".join([d.page_content for d in docs])

#     mlflow.log_text(context_text, "retrieved_context.txt")


# def start_retrieval_timer():
#     return time.time()


# def end_retrieval_timer(start):
#     duration = time.time() - start
#     mlflow.log_metric("retrieval_time_sec", duration)

import mlflow
import os
from datetime import datetime
import time


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
    mlflow.log_text(question, "question.txt")
    mlflow.log_text(answer, "answer.txt")


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

        "bm25_k": 1,

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

    mlflow.log_text(context_text, "retrieved_context.txt")


def start_retrieval_timer():
    return time.time()


def end_retrieval_timer(start):
    duration = time.time() - start
    mlflow.log_metric("retrieval_time_sec", duration)
