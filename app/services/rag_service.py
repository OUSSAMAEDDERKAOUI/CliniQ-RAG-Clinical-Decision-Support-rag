
from langchain_community.llms import Ollama
from app.core.config import settings

from deepeval.models.llms.ollama_model import OllamaModel as DeepEvalOllamaModel

# LLM local Ollama
llm = Ollama(model="mistral:latest", base_url="http://ollama:11434")
local_llm_model = DeepEvalOllamaModel(
    model="mistral:latest",
    base_url="http://ollama:11434"
)


def ask_question(question: str):
    qa = get_qa_chain()
    result = qa.invoke({"query": question})
    answer_text = result.get("result", str(result))

    # Log question et réponse
    log_answer(question, answer_text)

    # Récupérer contextes
    results = None
    retriever = get_retriever()
    contexts = retriever.get_relevant_documents(question)
    contexts_text = [doc.page_content for doc in contexts]
    if settings.ENABLE_EVALUATION:
        results = evaluate_rag(question, answer_text, contexts_text, llm_model=local_llm_model)

    return {
        "question": question,
        "answer": answer_text,
        "answer_evaluation": results
    }
