from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
import time

# Métriques RAG
rag_requests_total = Counter('rag_requests_total', 'Total RAG requests', ['endpoint', 'status'])
rag_response_time = Histogram('rag_response_time_seconds', 'RAG response time')
rag_errors_total = Counter('rag_errors_total', 'Total RAG errors', ['error_type'])
rag_quality_score = Histogram('rag_quality_score', 'RAG response quality score')

async def metrics_middleware(request: Request, call_next):
    """Middleware pour collecter les métriques"""
    start_time = time.time()
    
    response = await call_next(request)
    
    # Mesurer le temps de réponse
    duration = time.time() - start_time
    rag_response_time.observe(duration)
    
    # Compter les requêtes
    rag_requests_total.labels(
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    return response

async def metrics_endpoint():
    """Endpoint pour exposer les métriques Prometheus"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)



