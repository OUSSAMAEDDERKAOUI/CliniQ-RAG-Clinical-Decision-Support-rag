# # endpoint :
# from fastapi import APIRouter,Depends
# from app.db.session import get_db
# from app.api.deps import get_current_user
# from sqlalchemy.orm import Session
# from app.models.query import Query

# router = APIRouter(prefix="/test-route")


# @router.get("/query")
# def get_all(db:Session =Depends(get_db),user=Depends(get_current_user)):
#     queries=db.query(Query).filter(Query.user_id == user.id ).all()
#     return {
#         "all_query":queries,
#         "status":"success"
#     }





# # test 


# import pytest
# from fastapi.testclient import TestClient
# from app.main import app

# client=TestClient(app)

# def test_end_point():
#     response= client.get("/query")
#     res=response.json()
#     assert response.status_code==200
#     assert res["status"]=="success"
    



# from sqlalchemy.orm import relationship 
# from sqlalchemy import Column, Integer, String, ForeignKey
# from app.modeles.user import User
# class Query:


#     __tablename__ = "Queries"
#     id=Column(Integer,primary_key=True,index=True)
#     query=Column(String, Nullable=False)
#     response=Column(String,nullable=False)
#     user_id=Column(Integer,ForeignKey="users.id")
#     user = relationship("User",back_populates="queries")



# class QueryCreate(BaseModel):
#     query : str
#     response : str
# class QueryResponse(QueryCreate):
#     id:int 
#     user_id :int 
#     class Config :
#         from_attributes= True














# import mlflow 
# with mlflow.start_run(run_name="test_run"):
#     mlflow.log_param("test",acc)
#     mlflow/log_metric("accuracy",acc)






# # docker file 


# # FROM "test"
# # # Base image    
# # FROM python:3.11-slim
# # WORKDIR /app

# # copy ./requirement.txt .
 
# # run ./requirement
# # # Install dependencies

# # RUN pip install --no-cache-dir -r ./requirement
# # COPY . .
# # EXPOSE 1818
# # CMD [""]





# # mlflow

# import mlflow

# with mlflow.start_run(run_name="rag_evaluation"):
#     mlflow.log_metric("answer_relevance", answer_relevance)
#     mlflow.log_metric("recall", recall)
#     mlflow.log_metric("precision", precision)
    

# # pydantic schemas 



# # class 

# from pydantic import BaseModel

# class QueryCreate(BaseModel):
#     query: str
#     response: str

# class QueryResponse(QueryCreate):
#     id: int
#     created_at: datetime

#     class Config:
#         from_attributes = True






# # tests/test_rag_service.py
# from unittest.mock import Mock
# from app.rag_service import rag_answer

# def test_rag_answer():
#     fake_chain = Mock()
#     fake_chain.invoke.return_value = {"answer": "Réponse mockée"}

#     out = rag_answer(fake_chain, "Douleur thoracique ?")

#     assert out == "Réponse mockée"
#     fake_chain.invoke.assert_called_once()




# from unittest.mock import MagicMock

# def test_generate_answer():
#     fake_llm = MagicMock()
#     fake_llm.invoke.return_value = "Réponse mockée"

#     result = generate_answer(fake_llm, "Test")

#     assert result == "Réponse mockée"





# from unittest.mock import MagicMock

# def test_methode():
#     fake_llm=MagicMock()
#     fake_llm.invoke().return_value("response")

#     res=ask_question(fake_llm,Query)
    


#     assert res=="response"



from pydantic import BaseModel


class QueryCreate(BaseModel):
    query : str 
    response: str 


class QueryResponse(QueryCreate):
    id : int 
    user_id : int 

    class config:
        from_attributes:True


