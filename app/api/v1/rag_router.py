from fastapi import APIRouter, UploadFile, File
from app.rag.pipeline import build_pipeline
from app.services.rag_service import ask_question
from app.rag.retriever import get_vectorstore
from pydantic import BaseModel
import mlflow
from app.monitoring.mlflow_logger import start_rag_run

from app.monitoring.mlflow_logger import (
    log_retriever_config,
    log_retrieval_query,
    start_retrieval_timer,
    end_retrieval_timer
)


router = APIRouter()

@router.post("/")
async def index_pdf(file: UploadFile = File(...)):

    path = f"data/raw_pdfs/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    result = build_pipeline(path)

    return result



# @router.post("/ask")
# async def ask(data:str):

#     question = data.get("question")

#     result = ask_question(question)

#     return result


class QuestionRequest(BaseModel):
    question: str



@router.post("/ask")
async def ask(data: QuestionRequest):
    with start_rag_run("RetrievalQA","HybridRetriever_dense_bm25_mistral"):

        question = data.question
        result = ask_question(question)

    return result








@router.get("/chunks")
def get_all_chunks():

    vectorstore = get_vectorstore()

    data = vectorstore._collection.get()

    results = []

    for i, text in enumerate(data["documents"]):
        results.append({
            "id": data["ids"][i],
            "text": text,
            "metadata": data["metadatas"][i]
        })

    return {
        "total": len(results),
        "chunks": results
    }
