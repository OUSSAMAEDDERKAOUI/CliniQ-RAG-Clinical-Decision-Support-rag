from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    embedding_model: str = "all-MiniLM-L6-v2"
    vector_db: str = "chroma"
    persist_directory: str = "./vectorstore"

    CHROMA_HOST: str
    OLLAMA_URL: str
    DATA_DIR: str
    ENABLE_EVALUATION: bool = True   

    class Config:
        env_file = ".env"
        extra = "allow"   


settings = Settings()
