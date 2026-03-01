
# from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
# from deepeval.test_case import LLMTestCase
# from deepeval.models.llms.ollama_model import OllamaModel as DeepEvalOllamaModel
# import mlflow

# def evaluate_rag(question, answer, context, llm_model):
  
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

#     active_run = mlflow.active_run()
#     print(f"MLflow active run : {active_run}")

#     if active_run:
#         for k, v in results.items():
#             mlflow.log_metric(k, v)
#             print(f"Logged metric: {k} = {v}")
#     else:
#         logger.warning("Aucun run MLflow actif — les métriques ne seront pas loguées")
#         print("Aucun run MLflow actif !")

#     return results
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric
)
from deepeval.test_case import LLMTestCase
import mlflow
import json
import os
import logging

logger = logging.getLogger(__name__)

EVAL_DATASET_PATH = os.path.join(os.path.dirname(__file__), "eval_dataset.json")

def normalize(text: str) -> str:
    return text.strip().lower()

def load_eval_dataset() -> dict:
    if not os.path.exists(EVAL_DATASET_PATH):
        logger.warning(f"⚠️ Dataset introuvable : {EVAL_DATASET_PATH}")
        return {}
    with open(EVAL_DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {normalize(item["question"]): item["expected_answer"] for item in data}


def evaluate_rag(question: str, answer: str, context: list, llm_model, run_id: str = None):

    eval_dataset = load_eval_dataset()
    expected_answer = eval_dataset.get(normalize(question), None)

    print(f">>> Question         : {question}")
    print(f">>> Expected answer  : {expected_answer is not None}")
    print(f">>> Context length   : {len(context)}")

    # ✅ Valider le context
    if not context or not all(isinstance(c, str) and c.strip() for c in context):
        logger.error("❌ context invalide")
        return {}

    # ✅ Construire le test case
    test_case = LLMTestCase(
        input=question,
        actual_output=str(answer),
        retrieval_context=[str(c).strip() for c in context],
        expected_output=expected_answer
    )

    # ✅ Métriques de base (toujours actives)
    metrics = [
        AnswerRelevancyMetric(model=llm_model),
        FaithfulnessMetric(model=llm_model),
    ]

    # ✅ Métriques contextuelles — SANS paramètre k
    if expected_answer:
        metrics += [
            ContextualPrecisionMetric(model=llm_model),  # ✅ pas de k
            ContextualRecallMetric(model=llm_model),     # ✅ pas de k
        ]
        print(f">>> ✅ Métriques contextuelles activées")
    else:
        print(f">>> ⚠️ Pas d'expected_answer → métriques contextuelles ignorées")

    # ✅ Mesurer
    results = {}
    for metric in metrics:
        try:
            metric.measure(test_case)
            results[metric.__class__.__name__] = metric.score
            print(f">>> {metric.__class__.__name__} = {metric.score}")
        except Exception as e:
            logger.error(f"❌ Erreur {metric.__class__.__name__} : {e}", exc_info=True)
            results[metric.__class__.__name__] = None

    
    if run_id:
        with mlflow.start_run(run_id=run_id, nested=True):
            for k_metric, v in results.items():
                if v is not None:
                    mlflow.log_metric(k_metric, v)
                    print(f">>> ✅ MLflow logged: {k_metric} = {v}")
    else:
        logger.warning("⚠️ Aucun run_id fourni — métriques non loguées")

    return results

    return results