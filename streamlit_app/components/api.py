import requests
import os

API_BASE = os.getenv("API_BASE", "http://rag_cliniq_api:8000")  # ✅ tout minuscules

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
        params={"token": token},
        json={"question": question},
        timeout=None
    )
    r.raise_for_status()
    return r.json()

def get_history(token: str, limit: int = 50) -> list:
    r = requests.get(
        f"{API_BASE}/api/v1/index/history",
        params={"token": token, "limit": limit},
        timeout=30
    )
    r.raise_for_status()
    return r.json()["items"]