from fastapi import APIRouter, UploadFile, File ,Depends 
from app.rag.pipeline import build_pipeline
from app.services.rag_service import ask_question
from app.rag.qa_chain import log_pipeline_to_mlflow

from app.rag.retriever import get_vectorstore
from pydantic import BaseModel
import mlflow
from app.monitoring.mlflow_logger import start_rag_run,log_llm_params

from app.monitoring.mlflow_logger import (
    log_retriever_config,
    log_retrieval_query,
    start_retrieval_timer,
    end_retrieval_timer
)
from app.api.deps import get_current_user   
from app.models.user import User 
from app.db.session import get_db
from app.models.query import Query    
from app.schemas.query import QueryCreate        
from sqlalchemy.orm import Session
router = APIRouter()

@router.post("/")
async def index_pdf(file: UploadFile = File(...)):

    path = f"data/raw_pdfs/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    result = build_pipeline(path)

    return result






class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask(data: QuestionRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    with start_rag_run("RetrievalQA_pipeline_RAG", "HybridRetriever_dense_bm25_mistral"):
        question = data.question
        log_retriever_config()
        log_pipeline_to_mlflow()
        run_id = mlflow.active_run().info.run_id
        result = ask_question(question, run_id=run_id, user_id=current_user.id)

        db_query = Query(
            query=question,
            response=result["answer"],
            user_id=current_user.id
        )
        db.add(db_query)
        db.commit()
        db.refresh(db_query)

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

    with start_rag_run("test","testo_testa"):
        if mlflow.active_run():
            log_llm_params({
                "model": "mistral:latest",
                "temperature": 0,
                "top_k": 10,
                "top_p": 0.9
            })
    return {
        "total": len(results),
        "chunks": results
    }

@router.get("/history")
async def get_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    queries = db.query(Query)\
        .filter(Query.user_id == current_user.id)\
        .order_by(Query.created_at.desc())\
        .limit(limit)\
        .all()

    return {
        "items": [
            {
                "id": q.id,
                "question": q.query,
                "answer": q.response,
                "timestamp": q.created_at,
            }
            for q in queries
        ]
    }