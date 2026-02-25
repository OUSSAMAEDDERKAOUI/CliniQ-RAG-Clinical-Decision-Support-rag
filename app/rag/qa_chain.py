# from langchain.chains import RetrievalQA
# from langchain_community.llms import Ollama
# from app.rag.retriever import get_retriever

# def get_qa_chain():

#     llm = Ollama(model="mistral")   

#     retriever = get_retriever()

#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=retriever,
#         chain_type="stuff"
#     )

#     return qa_chain
# from langchain.chains import RetrievalQA
# from langchain_community.llms import Ollama
# from app.rag.retriever import get_retriever

# def get_qa_chain():

#     llm = Ollama(
#       model="mistral",
#       temperature=0.3,
#       top_k=10,
#       top_p=0.9
#      )


#     retriever = get_retriever()

#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=retriever,
#         chain_type="stuff"
#     )

#     return qa_chain
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from app.rag.retriever import get_retriever
import os
from langchain.prompts import PromptTemplate
from app.monitoring.mlflow_logger import log_llm_params
import mlflow
# def get_qa_chain():
#     # ollama_url = os.getenv("OLLAMA_URL", "http://ollama:11434/api/chat")
    
#     llm = Ollama(
#         model="mistral:latest",
#         temperature=0.3,
#         top_k=10,
#         top_p=0.9,
#         base_url="http://ollama:11434"
#     )

#     retriever = get_retriever()

#     template =     """
#             Tu es un assistant technique spécialisé dans la maintenance d'équipements biomédicaux. 
#             Ton unique mission est d'extraire des informations précises à partir des MANUELS fournis.

#             ### CONTEXTE DES MANUELS :
#             {context}

#             ### RÈGLES STRICTES :
            
# Zéro Hallucination : Si l'information n'est pas explicitement écrite dans le texte ci-dessus, réponds exactement : "Je ne trouve pas l'information dans les manuels disponibles".
# Fidélité Technique : Ne reformule pas les codes d'erreur ou les valeurs de pression/température. Utilise le langage exact du manuel.
# Isolation de Connaissance : Ne réponds pas en utilisant tes propres connaissances générales sur le sujet. Si le manuel est silencieux, tu es silencieux.
# Priorité au Contexte : Si l'utilisateur demande une procédure non décrite ici, refuse d'y répondre.

#             ### QUESTION DE L'UTILISATEUR :
#             {question}

#             RÉPONSE (en français) :
#             """

#     prompt = PromptTemplate(
#         template=template,
#         input_variables=["context", "question"]
#     )





#     qa_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     retriever=retriever,
#     chain_type="stuff",
#     chain_type_kwargs={"prompt": prompt}
#     )


#     log_llm_params({
#     "model": "mistral:latest",
#     "temperature": 0.3,
#     "top_k": 10,
#     "top_p": 0.9
#      })

#     mlflow.langchain.log_model(
#             qa_chain,
#             artifact_path="rag_chain"
#     )



#     return qa_chain
def get_qa_chain():

    llm = Ollama(
        model="mistral:latest",
        temperature=0.3,
        top_k=10,
        top_p=0.9,
        base_url="http://ollama:11434"
    )

    retriever = get_retriever()

   
    template =     """
            Tu es un assistant technique spécialisé dans la maintenance d'équipements biomédicaux. 
            Ton unique mission est d'extraire des informations précises à partir des MANUELS fournis.

            ### CONTEXTE DES MANUELS :
            {context}

            ### RÈGLES STRICTES :
            
Zéro Hallucination : Si l'information n'est pas explicitement écrite dans le texte ci-dessus, réponds exactement : "Je ne trouve pas l'information dans les manuels disponibles".
Fidélité Technique : Ne reformule pas les codes d'erreur ou les valeurs de pression/température. Utilise le langage exact du manuel.
Isolation de Connaissance : Ne réponds pas en utilisant tes propres connaissances générales sur le sujet. Si le manuel est silencieux, tu es silencieux.
Priorité au Contexte : Si l'utilisateur demande une procédure non décrite ici, refuse d'y répondre.

            ### QUESTION DE L'UTILISATEUR :
            {question}

            RÉPONSE (en français) :
            """

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    # Juste log params si run actif
    if mlflow.active_run():
        log_llm_params({
            "model": "mistral:latest",
            "temperature": 0.3,
            "top_k": 10,
            "top_p": 0.9
        })

    return qa_chain
