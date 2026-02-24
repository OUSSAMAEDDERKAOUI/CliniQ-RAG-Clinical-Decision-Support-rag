# from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
# from deepeval.test_case import LLMTestCase
# import mlflow


# def evaluate_rag(question, answer, context):

#     test_case = LLMTestCase(
#         input=question,
#         actual_output=answer,
#         retrieval_context=context
#     )

#     metrics = [
#         AnswerRelevancyMetric(),
#         FaithfulnessMetric()
#     ]

#     results = {}

#     for metric in metrics:
#         metric.measure(test_case)
#         results[metric.__class__.__name__] = metric.score

#     for k, v in results.items():
#         mlflow.log_metric(k, v)

#     return results


# from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
# from deepeval.test_case import LLMTestCase
# import mlflow

# # Wrapper pour utiliser ton LLM Ollama local
# class OllamaModel:
#     def __init__(self, llm):
#         self.llm = llm

#     def __call__(self, prompt: str) -> str:
#         result = self.llm.invoke({"prompt": prompt})
#         return result.get("result", str(result))


# def evaluate_rag(question, answer, context, llm_model):
#     """
#     Évalue la réponse d'un RAG avec DeepEval en utilisant un LLM local.
#     """
#     test_case = LLMTestCase(
#         input=question,
#         actual_output=str(answer),  # toujours string
#         retrieval_context=context,
#         model=llm_model  # passer ton OllamaModel ici
#     )

#     metrics = [
#         AnswerRelevancyMetric(model=llm_model),
#         FaithfulnessMetric(model=llm_model)
#     ]

#     results = {}
#     for metric in metrics:
#         metric.measure(test_case)
#         results[metric.__class__.__name__] = metric.score

#     # Log dans MLflow
#     for k, v in results.items():
#         mlflow.log_metric(k, v)

#     return results


# # app/monitoring/evaluator.py
# from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
# from deepeval.test_case import LLMTestCase
# import mlflow

# class OllamaModel:
#     """
#     Wrapper pour utiliser un LLM Ollama local avec DeepEval
#     """
#     def __init__(self, llm):
#         self.llm = llm

#     def __call__(self, prompt: str) -> str:
#         result = self.llm.invoke({"prompt": prompt})
#         return result.get("result", str(result))

# def evaluate_rag(question, answer, context, llm_model):
#     """
#     Évalue la réponse d'un RAG avec DeepEval en utilisant un LLM local.
#     """
#     # DeepEval exige actual_output en string et retrieval_context en liste de strings
#     test_case = LLMTestCase(
#         input=question,
#         actual_output=str(answer),
#         retrieval_context=context,
#         model=llm_model
#     )

#     metrics = [
#         AnswerRelevancyMetric(model=llm_model),
#         FaithfulnessMetric(model=llm_model)
#     ]

#     results = {}
#     for metric in metrics:
#         metric.measure(test_case)
#         results[metric.__class__.__name__] = metric.score

#     # Log des métriques dans MLflow
#     for k, v in results.items():
#         mlflow.log_metric(k, v)

#     return results
# app/monitoring/evaluator.py
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from deepeval.models.llms.ollama_model import OllamaModel as DeepEvalOllamaModel
import mlflow

def evaluate_rag(question, answer, context, llm_model):
    """
    Évalue la réponse d'un RAG avec DeepEval en utilisant un LLM local.
    """
    # DeepEval exige actual_output en string et retrieval_context en liste de strings
    test_case = LLMTestCase(
        input=question,
        actual_output=str(answer),
        retrieval_context=context,
        model=llm_model
    )

    metrics = [
        AnswerRelevancyMetric(model=llm_model),
        FaithfulnessMetric(model=llm_model)
    ]

    results = {}
    for metric in metrics:
        metric.measure(test_case)
        results[metric.__class__.__name__] = metric.score

    # Log des métriques dans MLflow
    for k, v in results.items():
        mlflow.log_metric(k, v)

    return results
