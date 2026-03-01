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
df = df.sort_values("timestamp", ascending=False)

st.subheader("❓ Questions fréquentes")

for _, row in df.iterrows():
    with st.expander(f"🔹 {row['question']}"):
        st.markdown(f"**🕒 Date :** {row['timestamp']}")
        st.markdown("**💬 Réponse :**")
        st.markdown(row["answer"])