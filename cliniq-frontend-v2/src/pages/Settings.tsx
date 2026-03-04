import React, { useState } from "react";
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Divider,
  Alert,
  Switch,
  FormControlLabel,
  Slider,
  Stack,
  Chip,
} from "@mui/material";
import { Settings as SettingsIcon, Save } from "@mui/icons-material";
import toast from "react-hot-toast";
import Layout from "../components/Layout";
import { useThemeMode } from "../theme/ThemeProvider";

const Settings: React.FC = () => {
  const { mode, toggleTheme } = useThemeMode();

  const [apiBase, setApiBase] = useState(
    import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"
  );
  const [historyLimit, setHistoryLimit] = useState(50);
  const [evaluationEnabled, setEvaluationEnabled] = useState(
    localStorage.getItem("evaluation_enabled") !== "false"
  );

  const handleSave = () => {
    localStorage.setItem("history_limit", String(historyLimit));
    localStorage.setItem("evaluation_enabled", String(evaluationEnabled));
    toast.success("Paramètres sauvegardés");
  };

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
          <SettingsIcon sx={{ color: "primary.main" }} />
          <Typography variant="h6" fontWeight={700}>
            Paramètres
          </Typography>
        </Box>

        <Box sx={{ p: 3, maxWidth: 640 }}>
          {/* Appearance */}
          <Paper variant="outlined" sx={{ p: 3, borderRadius: 3, mb: 3 }}>
            <Typography variant="subtitle1" fontWeight={700} gutterBottom>
              Apparence
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <FormControlLabel
              control={
                <Switch
                  checked={mode === "dark"}
                  onChange={toggleTheme}
                  color="primary"
                />
              }
              label={
                <Stack direction="row" alignItems="center" gap={1}>
                  <Typography variant="body2">Mode sombre</Typography>
                  <Chip
                    label={mode === "dark" ? "Activé" : "Désactivé"}
                    size="small"
                    color={mode === "dark" ? "primary" : "default"}
                    variant="outlined"
                    sx={{ fontSize: "0.65rem" }}
                  />
                </Stack>
              }
            />
          </Paper>

          {/* API */}
          <Paper variant="outlined" sx={{ p: 3, borderRadius: 3, mb: 3 }}>
            <Typography variant="subtitle1" fontWeight={700} gutterBottom>
              Configuration API
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Alert severity="info" sx={{ mb: 2, fontSize: "0.8rem" }}>
              Cette URL est définie au build via <code>VITE_API_BASE_URL</code>. Les modifications
              ici n'affectent pas les appels API actuels.
            </Alert>
            <TextField
              label="URL de base de l'API"
              value={apiBase}
              onChange={(e) => setApiBase(e.target.value)}
              fullWidth
              size="small"
              disabled
              helperText="Modifiable uniquement dans le fichier .env"
            />
          </Paper>

          {/* History */}
          <Paper variant="outlined" sx={{ p: 3, borderRadius: 3, mb: 3 }}>
            <Typography variant="subtitle1" fontWeight={700} gutterBottom>
              Historique
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Nombre de requêtes à charger : <strong>{historyLimit}</strong>
            </Typography>
            <Slider
              value={historyLimit}
              onChange={(_, v) => setHistoryLimit(v as number)}
              min={10}
              max={200}
              step={10}
              marks={[
                { value: 10, label: "10" },
                { value: 50, label: "50" },
                { value: 100, label: "100" },
                { value: 200, label: "200" },
              ]}
              valueLabelDisplay="auto"
              color="primary"
            />
          </Paper>

          {/* Evaluation */}
          <Paper variant="outlined" sx={{ p: 3, borderRadius: 3, mb: 3 }}>
            <Typography variant="subtitle1" fontWeight={700} gutterBottom>
              Évaluation RAG
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <FormControlLabel
              control={
                <Switch
                  checked={evaluationEnabled}
                  onChange={(e) => setEvaluationEnabled(e.target.checked)}
                  color="primary"
                />
              }
              label={
                <Box>
                  <Typography variant="body2">Afficher les métriques DeepEval</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Affiche les scores de pertinence et fidélité sous chaque réponse
                  </Typography>
                </Box>
              }
            />
          </Paper>

          {/* Stack info */}
          <Paper variant="outlined" sx={{ p: 3, borderRadius: 3, mb: 3 }}>
            <Typography variant="subtitle1" fontWeight={700} gutterBottom>
              Stack technique
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
              {[
                "FastAPI",
                "Mistral 7B",
                "Ollama",
                "ChromaDB",
                "BM25",
                "MLflow",
                "DeepEval",
                "PostgreSQL",
                "Prometheus",
                "Grafana",
                "React",
                "TypeScript",
              ].map((t) => (
                <Chip key={t} label={t} size="small" variant="outlined" />
              ))}
            </Box>
          </Paper>

          <Button
            variant="contained"
            startIcon={<Save />}
            onClick={handleSave}
            size="large"
          >
            Sauvegarder les paramètres
          </Button>
        </Box>
      </Box>
    </Layout>
  );
};

export default Settings;
