
import time
from fastapi import FastAPI, Request, Response, HTTPException
from prometheus_client import Counter, Histogram, generate_latest
from app.db.init_db import init_db
from app.api.v1 import auth
from app.api.v1.rag_router import router as rag_router
from app.api.v1.rag_router import ask_question


app = FastAPI(title="RAG Biomedical Support")


REQUEST_COUNT = Counter("request_count_total", "Total API requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency in seconds", ["method", "endpoint"])
ERROR_COUNT = Counter("error_count_total", "Total number of errors", ["method", "endpoint", "http_status"])

RAG_RESPONSE_LATENCY = Histogram("rag_response_latency_seconds", "Latency of RAG responses")
RAG_RESPONSE_SUCCESS = Counter("rag_success_total", "Number of successful RAG responses")
RAG_RESPONSE_ERROR = Counter("rag_error_total", "Number of failed RAG responses")


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time

    endpoint = request.url.path
    method = request.method
    status = str(response.status_code)

    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(process_time)

    if response.status_code >= 400:
        ERROR_COUNT.labels(method=method, endpoint=endpoint, http_status=status).inc()

    return response


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")


@app.on_event("startup")
def startup():
    init_db()


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(rag_router, prefix="/api/v1/index", tags=["rag"])
