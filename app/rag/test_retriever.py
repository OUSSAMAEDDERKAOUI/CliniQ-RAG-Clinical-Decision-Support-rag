from app.rag.retriever import get_retriever
from app.monitoring.mlflow_logger import start_rag_run
import mlflow

print(" Initialisation du retriever...")
with start_rag_run("retrieval","HybridRetriever_dense_bm25"):
    retriever = get_retriever()

print(" Retriever prêt")

query = "Qu'est-ce que  Outils utilisés en CI/CD  ?"

print(f"\n Recherche pour : {query}\n")

docs = retriever.get_relevant_documents(query)

print(f" Nombre de résultats : {len(docs)}\n")

for i, d in enumerate(docs):
    print(f"----- CHUNK {i+1} -----")
    print(d.page_content)
    print("\nMETADATA :", d.metadata)
    print("\n")
