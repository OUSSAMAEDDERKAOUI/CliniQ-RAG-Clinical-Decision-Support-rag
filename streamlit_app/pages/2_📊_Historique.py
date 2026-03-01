import streamlit as st
import pandas as pd
from components.auth import require_auth, logout_button
from components.api import get_history

if not require_auth():
    st.stop()

st.title("📊 Historique des requêtes")
logout_button()

limit = st.slider("Nombre d'entrées", 10, 200, 50, 10)

try:
    items = get_history(st.session_state.token, limit=limit)
except Exception as e:
    st.error(f"❌ Erreur chargement historique : {e}")
    st.stop()

if not items:
    st.info("Aucune interaction pour l'instant.")
    st.stop()

df = pd.DataFrame(items)

# Renommer les colonnes selon le modèle Query
if "created_at" in df.columns:
    df = df.sort_values("created_at", ascending=False)

st.dataframe(
    df[["created_at", "query", "response"]].rename(columns={
        "created_at": "Date",
        "query": "Question",
        "response": "Réponse"
    }),
    use_container_width=True
)

with st.expander("🔍 Voir le détail d'une entrée"):
    idx = st.number_input("Index ligne (0..)", 0, len(df) - 1, 0)
    row = df.iloc[int(idx)]
    st.write("**📅 Date**")
    st.write(row.get("created_at", "N/A"))
    st.write("**❓ Question**")
    st.write(row.get("query", "N/A"))
    st.write("**💬 Réponse**")
    st.write(row.get("response", "N/A"))
