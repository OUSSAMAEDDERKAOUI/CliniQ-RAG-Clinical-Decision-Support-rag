import streamlit as st
from components.auth import require_auth, logout_button
from components.api import ask_question

if not require_auth():
    st.stop()

st.title("💬 Assistant RAG Clinique")
logout_button()

if st.session_state.get("user_email"):
    st.caption(f"Connecté en tant que : {st.session_state.user_email}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique de la session
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("evaluation"):
            with st.expander("📊 Métriques d'évaluation"):
                for metric, score in m["evaluation"].items():
                    st.metric(label=metric, value=round(score, 3) if score else "N/A")

prompt = st.chat_input("Pose ta question clinique…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyse en cours…"):
            try:
                res = ask_question(st.session_state.token, prompt)
                answer = res.get("answer", "")
                evaluation = res.get("answer_evaluation")

                st.markdown(answer)

                if evaluation:
                    with st.expander("📊 Métriques d'évaluation"):
                        for metric, score in evaluation.items():
                            st.metric(label=metric, value=round(score, 3) if score else "N/A")

            except Exception as e:
                answer = f"❌ Erreur : {e}"
                evaluation = None
                st.error(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "evaluation": evaluation
    })
