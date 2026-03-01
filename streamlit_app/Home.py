import streamlit as st
from components.auth import require_auth, logout_button

if not require_auth():
    st.stop()

st.title("🏥 CliniQ — Assistant RAG Clinique")
logout_button()

st.markdown("""
Bienvenue sur **CliniQ**, votre assistant clinique intelligent basé sur RAG.

### 🗂️ Navigation
- **💬 Chat RAG** — Posez vos questions cliniques
- **📊 Historique** — Consultez vos interactions passées

### ℹ️ À propos
- Modèle LLM : `mistral:latest`
- Embeddings : `BAAI/bge-base-en-v1.5`
- Vector DB : `ChromaDB`
- Retriever : `Hybrid (MMR + BM25)`
""")
