
# import requests
# import os

# API_BASE = os.getenv("API_BASE", "http://rag_CliniQ_api:8000")

# def login(username: str, password: str) -> str:  # ✅ username pas email
#     r = requests.post(
#         f"{API_BASE}/api/v1/auth/login",
#         json={"username": username, "password": password},  # ✅ username
#         timeout=30
#     )
#     r.raise_for_status()
#     return r.json()["access_token"]

# def ask_question(token: str, question: str) -> dict:
#     headers = {"Authorization": f"Bearer {token}"}
#     r = requests.post(
#         f"{API_BASE}/api/v1/index/ask",
#         json={"question": question},
#         headers=headers,
#         timeout=120
#     )
#     r.raise_for_status()
#     return r.json()

# def get_history(token: str, limit: int = 50) -> list:
#     headers = {"Authorization": f"Bearer {token}"}
#     r = requests.get(
#         f"{API_BASE}/api/v1/rag/history",
#         params={"limit": limit},
#         headers=headers,
#         timeout=30
#     )
#     r.raise_for_status()
#     return r.json()["items"]


import requests
import os

API_BASE = os.getenv("API_BASE", "http://rag_CliniQ_api:8000")

def login(username: str, password: str) -> str:
    r = requests.post(
        f"{API_BASE}/api/v1/auth/login",
        json={"username": username, "password": password},
        timeout=30
    )
    r.raise_for_status()
    return r.json()["access_token"]

def ask_question(token: str, question: str) -> dict:
    r = requests.post(
        f"{API_BASE}/api/v1/index/ask",
        params={"token": token},         # ✅ token en query param
        json={"question": question},
        timeout=120
    )
    r.raise_for_status()
    return r.json()

def get_history(token: str, limit: int = 50) -> list:
    r = requests.get(
        f"{API_BASE}/api/v1/rag/history",
        params={"token": token, "limit": limit},  # ✅ token en query param
        timeout=30
    )
    r.raise_for_status()
    return r.json()["items"]