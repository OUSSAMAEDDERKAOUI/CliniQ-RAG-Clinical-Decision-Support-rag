

from app.rag.qa_chain import get_qa_chain
from app.rag.retriever import get_retriever
from app.monitoring.evaluator import evaluate_rag 
from app.monitoring.mlflow_logger import log_answer
from langchain_community.llms import Ollama
from app.core.config import settings

from deepeval.models.llms.ollama_model import OllamaModel as DeepEvalOllamaModel

llm = Ollama(model="mistral:latest", base_url="http://ollama:11434")
local_llm_model = DeepEvalOllamaModel(
    model="mistral:latest",
    base_url="http://ollama:11434"
)







def ask_question(question: str, run_id: str = None,user_id:int=None):
    qa = get_qa_chain()

    result = qa.invoke({"query": question})

    answer_text = result["result"]

    source_docs = result["source_documents"]
    contexts_text = [doc.page_content for doc in source_docs]

    log_answer(question, answer_text)

    results = None
    if settings.ENABLE_EVALUATION:
        results = evaluate_rag(
            question,
            answer_text,
            contexts_text,
            llm_model=local_llm_model,
            run_id=run_id
        )  

    return {
        "question": question,
        "answer": answer_text,
        "answer_evaluation": results
    }
