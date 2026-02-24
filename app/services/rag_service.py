# # from app.rag.qa_chain import get_qa_chain
# # from app.monitoring.mlflow_logger import log_answer
# # from app.monitoring.evaluator import evaluate_rag
# # from app.rag.retriever import get_retriever

# # def ask_question(question: str):

# #     qa = get_qa_chain()

# #     result = qa.invoke({"query": question})
# #     log_answer(question, result.get("result", str(result)))
# #     retriever = get_retriever()
# #     contexts = retriever.get_relevant_documents(question)

# #     results = evaluate_rag(question, result, contexts)

# #     return {
# #         "question": question,
# #         "answer": result,
# #         "answer evaluation":results
# #     }

# # def ask_question(question: str):

# #     qa = get_qa_chain()

# #     result = qa.invoke({"query": question})

# #     if isinstance(result, dict):
# #         answer_text = result.get("result", "")
# #     else:
# #         answer_text = str(result)

# #     log_answer(question, answer_text)

# #     retriever = get_retriever()
# #     docs = retriever.get_relevant_documents(question)

# #     contexts = [doc.page_content for doc in docs]

# #     results = evaluate_rag(question, answer_text, contexts)

# #     return {
# #         "question": question,
# #         "answer": answer_text,
# #         "answer_evaluation": results
# #     }




# # from app.rag.qa_chain import get_qa_chain
# # from app.rag.retriever import get_retriever
# # from app.monitoring.evaluator import evaluate_rag, OllamaModel
# # from app.monitoring.mlflow_logger import log_answer
# # from langchain_community.llms import Ollama

# # # Ton LLM local
# # llm = Ollama(model="mistral:latest", base_url="http://ollama:11434")
# # local_llm_model = OllamaModel(llm)

# # def ask_question(question: str):
# #     qa = get_qa_chain()
# #     result = qa.invoke({"query": question})
# #     answer_text = result.get("result", str(result))

# #     log_answer(question, answer_text)

# #     retriever = get_retriever()
# #     contexts = retriever.get_relevant_documents(question)
# #     contexts_text = [doc.page_content for doc in contexts]

# #     # Évaluation avec DeepEval + LLM local
# #     results = evaluate_rag(question, answer_text, contexts_text, llm_model=local_llm_model)

# #     return {
# #         "question": question,
# #         "answer": answer_text,
# #         "answer_evaluation": results
# #     }


# # app/services/rag_service.py
# # from app.rag.qa_chain import get_qa_chain
# # from app.rag.retriever import get_retriever
# # from app.monitoring.evaluator import evaluate_rag 
# # from app.monitoring.mlflow_logger import log_answer
# from langchain_community.llms import Ollama
# from app.core.config import settings

# from deepeval.models.llms.ollama_model import OllamaModel as DeepEvalOllamaModel

# # LLM local Ollama
# llm = Ollama(model="mistral:latest", base_url="http://ollama:11434")
# local_llm_model = DeepEvalOllamaModel(
#     model="mistral:latest",
#     base_url="http://ollama:11434"
# )


# def ask_question(question: str):
#     qa = get_qa_chain()
#     result = qa.invoke({"query": question})
#     answer_text = result.get("result", str(result))

#     # Log question et réponse
#     log_answer(question, answer_text)

#     # Récupérer contextes
#     results = None
#     retriever = get_retriever()
#     contexts = retriever.get_relevant_documents(question)
#     contexts_text = [doc.page_content for doc in contexts]
#     if settings.ENABLE_EVALUATION:
#         results = evaluate_rag(question, answer_text, contexts_text, llm_model=local_llm_model)

#     return {
#         "question": question,
#         "answer": answer_text,
#         "answer_evaluation": results
#     }
