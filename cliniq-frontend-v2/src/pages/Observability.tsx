import React from "react";
import {
  Box,
  Typography,
  Paper,
  Card,
  CardContent,
  CardActionArea,
  Chip,
  Divider,
} from "@mui/material";
import Grid from "@mui/material/Grid";
import {
  BarChart,
  OpenInNew,
  Hub,
  Science,
  Analytics,
  Webhook,
} from "@mui/icons-material";
import Layout from "../components/Layout";

const BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

const tools = [
  {
    title: "MLflow",
    description: "Suivi des expériences RAG, métriques, artefacts et modèles",
    url: `${BASE.replace(":8000", ":5000")}`,
    icon: <Science sx={{ fontSize: 32, color: "primary.main" }} />,
    color: "primary",
    chip: "Experiments",
  },
  {
    title: "Grafana",
    description: "Tableaux de bord de monitoring en temps réel",
    url: `${BASE.replace(":8000", ":3000")}`,
    icon: <Analytics sx={{ fontSize: 32, color: "secondary.main" }} />,
    color: "secondary",
    chip: "Dashboards",
  },
  {
    title: "Prometheus",
    description: "Collecte et stockage des métriques de l'API",
    url: `${BASE.replace(":8000", ":9090")}`,
    icon: <Hub sx={{ fontSize: 32, color: "#e6522c" }} />,
    color: "warning",
    chip: "Metrics",
  },
  {
    title: "API Docs",
    description: "Documentation interactive Swagger / OpenAPI",
    url: `${BASE}/docs`,
    icon: <Webhook sx={{ fontSize: 32, color: "success.main" }} />,
    color: "success",
    chip: "Swagger",
  },
  {
    title: "Adminer",
    description: "Gestionnaire de base de données PostgreSQL",
    url: `${BASE.replace(":8000", ":8080")}`,
    icon: <BarChart sx={{ fontSize: 32, color: "info.main" }} />,
    color: "info",
    chip: "DB Admin",
  },
];

const metricsInfo = [
  {
    label: "Answer Relevancy",
    description: "Mesure si la réponse est pertinente par rapport à la question posée.",
  },
  {
    label: "Faithfulness",
    description: "Vérifie que la réponse est fidèle aux documents sources récupérés.",
  },
  {
    label: "Contextual Precision",
    description: "Évalue si les documents récupérés sont précisément ciblés.",
  },
  {
    label: "Contextual Recall",
    description: "Mesure la capacité à récupérer tous les documents pertinents.",
  },
];

const Observability: React.FC = () => {
  return (
    <Layout>
      <Box sx={{ height: "100vh", overflowY: "auto" }}>
        {/* Header */}
        <Box
          sx={{
            px: 3,
            py: 2,
            borderBottom: 1,
            borderColor: "divider",
            bgcolor: "background.paper",
            display: "flex",
            alignItems: "center",
            gap: 1,
          }}
        >
          <BarChart sx={{ color: "primary.main" }} />
          <Typography variant="h6" fontWeight={700}>
            Observabilité
          </Typography>
        </Box>

        <Box sx={{ p: 3 }}>
          {/* Tools */}
          <Typography variant="subtitle1" fontWeight={700} sx={{ mb: 2 }}>
            Outils de monitoring
          </Typography>
          <Grid container spacing={2} sx={{ mb: 4 }}>
            {tools.map((tool) => (
              <Grid size={{ xs: 12, sm: 6, lg: 4 }} key={tool.title}>
                <Card
                  variant="outlined"
                  sx={{
                    borderRadius: 3,
                    height: "100%",
                    transition: "border-color 0.2s",
                    "&:hover": { borderColor: "primary.main" },
                  }}
                >
                  <CardActionArea
                    href={tool.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    sx={{ height: "100%", p: 2 }}
                  >
                    <CardContent sx={{ p: 0 }}>
                      <Box sx={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", mb: 1.5 }}>
                        {tool.icon}
                        <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
                          <Chip label={tool.chip} size="small" variant="outlined" sx={{ fontSize: "0.65rem" }} />
                          <OpenInNew sx={{ fontSize: 14, color: "text.disabled" }} />
                        </Box>
                      </Box>
                      <Typography variant="subtitle2" fontWeight={700} gutterBottom>
                        {tool.title}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {tool.description}
                      </Typography>
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            ))}
          </Grid>

          <Divider sx={{ mb: 3 }} />

          {/* Eval metrics */}
          <Typography variant="subtitle1" fontWeight={700} sx={{ mb: 2 }}>
            Métriques d'évaluation RAG (DeepEval)
          </Typography>
          <Grid container spacing={2}>
            {metricsInfo.map((m) => (
              <Grid size={{ xs: 12, sm: 6 }} key={m.label}>
                <Paper
                  variant="outlined"
                  sx={{ p: 2.5, borderRadius: 3, height: "100%" }}
                >
                  <Typography variant="subtitle2" fontWeight={700} color="primary" gutterBottom>
                    {m.label}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {m.description}
                  </Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>

          <Divider sx={{ mt: 3, mb: 3 }} />

          {/* Architecture */}
          <Typography variant="subtitle1" fontWeight={700} sx={{ mb: 2 }}>
            Architecture du pipeline
          </Typography>
          <Paper variant="outlined" sx={{ p: 3, borderRadius: 3 }}>
            <Box
              component="pre"
              sx={{
                fontFamily: '"Fira Code", monospace',
                fontSize: "0.75rem",
                color: "text.secondary",
                overflowX: "auto",
                m: 0,
              }}
            >
{`Question utilisateur
       │
       ▼
┌─────────────────┐
│  Hybrid Search  │  BM25 (sparse) + ChromaDB MMR (dense)
└────────┬────────┘
         │  top-k documents
         ▼
┌─────────────────┐
│  Mistral 7B     │  Génération via Ollama
│  (RAG Chain)    │
└────────┬────────┘
         │  réponse + sources
         ▼
┌─────────────────┐
│  DeepEval       │  Évaluation 4 métriques → MLflow
└────────┬────────┘
         │  métriques loggées
         ▼
┌─────────────────┐
│  PostgreSQL     │  Persistance query + réponse
└─────────────────┘`}
            </Box>
          </Paper>
        </Box>
      </Box>
    </Layout>
  );
};

export default Observability;
