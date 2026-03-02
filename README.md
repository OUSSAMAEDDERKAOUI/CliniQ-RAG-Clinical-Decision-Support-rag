# 🏥 CliniQ — Clinical Decision Support System

> Système de support à la décision clinique basé sur **RAG (Retrieval-Augmented Generation)**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-green)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange)

---

## 📋 Table des matières

- [Problématique](#-problématique)
- [Architecture](#-architecture)
- [Pipeline RAG](#-pipeline-rag)
- [Stack Technique](#-stack-technique)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Évaluation RAG](#-évaluation-rag)
- [Monitoring](#-monitoring)

---

## ❓ Problématique

- ❌ Les médecins perdent du temps à chercher dans des documents volumineux
- ❌ Les LLMs classiques **hallucinent** sur des données médicales
- ✅ CliniQ propose un assistant RAG **ancré sur des documents médicaux fiables**

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Streamlit  │────▶│   FastAPI    │────▶│   Ollama    │
│   (Front)   │     │   (Backend)  │     │  Mistral 7B │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ ChromaDB │ │PostgreSQL│ │  MLflow  │
        │(Vectors) │ │  (Users) │ │(Tracking)│
        └──────────┘ └──────────┘ └──────────┘
```

---

## 🔄 Pipeline RAG

```
📄 Documents PDF
        │
        ▼
🔪 Chunking Hybride
   ├── SemanticChunker (BAAI/bge-base-en-v1.5)
   └── RecursiveTextSplitter (600 tokens / overlap 120)
        │
        ▼
🔍 Retriever Hybride
   ├── Dense MMR (ChromaDB) — k=6
   └── BM25 — k=2
        │
        ▼
🏆 Reranker
   └── cross-encoder/ms-marco-MiniLM-L-6-v2
        │
        ▼
🤖 LLM Mistral 7B (Ollama)
        │
        ▼
✅ Réponse Clinique
```

---

## 🛠️ Stack Technique

| Composant | Technologie |
|---|---|
| **Backend** | FastAPI + SQLAlchemy |
| **Frontend** | Streamlit |
| **LLM** | Mistral 7B (Ollama) |
| **Embeddings** | BAAI/bge-base-en-v1.5 |
| **Vector DB** | ChromaDB |
| **Base de données** | PostgreSQL |
| **Monitoring** | MLflow + Prometheus + Grafana |
| **Évaluation RAG** | DeepEval |
| **Conteneurisation** | Docker Compose |

---

## ✅ Fonctionnalités

- 📄 Indexation de documents PDF médicaux
- 🔪 Chunking hybride (sémantique + récursif)
- 🔍 Retrieval hybride (dense + BM25 + reranking)
- 🔐 Authentification JWT (register/login)
- 📊 Historique des requêtes par utilisateur
- 📈 Évaluation automatique RAG (DeepEval)
- 🖥️ Monitoring complet (MLflow + Grafana)

---

## 🚀 Installation

### Prérequis

- Docker & Docker Compose
- GPU recommandé (CPU possible)

### Lancer le projet

```bash
# Cloner le repo
git clone https://github.com/OUSSAMAEDDERKAOUI/CliniQ-RAG-Clinical-Decision-Support-rag/
cd CliniQ

# Configurer les variables d'environnement
cp .env.example .env

# Lancer tous les services
docker compose up --build
```

### Pull le modèle Mistral

```bash
docker exec -it rag_CliniQ_ollama ollama pull mistral:7b-instruct-q4_0
```

---

## 💻 Utilisation

| Service | URL |
|---|---|
| **Streamlit** (Frontend) | http://localhost:8501 |
| **FastAPI** (Swagger) | http://localhost:8000/docs |
| **MLflow** | http://localhost:5000 |
| **Grafana** | http://localhost:3000 |
| **Adminer** (DB) | http://localhost:8080 |

### Workflow

```
1️⃣  Register / Login sur Streamlit
2️⃣  Poser une question clinique
3️⃣  Obtenir une réponse RAG ancrée
4️⃣  Consulter l'historique
5️⃣  Voir les métriques sur MLflow / Grafana
```

---

## 📊 Évaluation RAG

CliniQ utilise **DeepEval** pour évaluer automatiquement la qualité des réponses :

| Métrique | Description |
|---|---|
| **AnswerRelevancy** | La réponse est-elle pertinente à la question ? |
| **Faithfulness** | La réponse est-elle fidèle au contexte ? |
| **ContextualPrecision** | Le contexte récupéré est-il précis ? |
| **ContextualRecall** | Tout le contexte nécessaire est-il récupéré ? |

```json
{
  "AnswerRelevancyMetric": 1.0,
  "FaithfulnessMetric": 0.5,
  "ContextualPrecisionMetric": 0.86,
  "ContextualRecallMetric": 1.0
}
```

---

## 📈 Monitoring

```
📊 MLflow
   ├── Paramètres LLM (model, temperature, top_k)
   ├── Configuration Retriever
   ├── Métriques DeepEval
   └── Artifacts (prompt, config)

📈 Grafana + Prometheus
   ├── Latence des requêtes
   ├── Nombre de requêtes
   └── Taux d'erreurs
```

---

## 📁 Structure du projet

```
CliniQ/
├── app/
│   ├── api/v1/          ← Endpoints FastAPI
│   ├── rag/             ← Pipeline RAG
│   ├── monitoring/      ← MLflow + DeepEval
│   ├── models/          ← SQLAlchemy models
│   └── services/        ← Business logic
├── streamlit_app/       ← Frontend Streamlit
├── data/                ← Documents PDF
├── monitoring/          ← Prometheus + Grafana config
└── docker-compose.yml
```

---

## 👨‍💻 Auteur

Projet développé dans le cadre d'un système de support à la décision clinique basé sur l'IA.