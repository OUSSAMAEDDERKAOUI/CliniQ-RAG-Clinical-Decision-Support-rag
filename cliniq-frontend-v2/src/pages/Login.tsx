import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  InputAdornment,
  IconButton,
  Alert,
  CircularProgress,
  Avatar,
  Divider,
} from "@mui/material";
import {
  Visibility,
  VisibilityOff,
  LocalHospital,
  Person,
  Lock,
} from "@mui/icons-material";
import { useMutation } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { login } from "../api/rag";
import { authStore } from "../store/authStore";
import { useThemeMode } from "../theme/ThemeProvider";
import { LightMode, DarkMode } from "@mui/icons-material";

const Login: React.FC = () => {
  const navigate = useNavigate();
  const { mode, toggleTheme } = useThemeMode();
  const [form, setForm] = useState({ username: "", password: "" });
  const [showPwd, setShowPwd] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: login,
    onSuccess: (data) => {
      authStore.setToken(data.access_token);
      toast.success("Connexion réussie !");
      navigate("/chat");
    },
    onError: (err: unknown) => {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
        "Identifiants incorrects";
      setError(msg);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!form.username || !form.password) {
      setError("Veuillez remplir tous les champs");
      return;
    }
    mutation.mutate(form);
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        bgcolor: "background.default",
        p: 2,
      }}
    >
      {/* Theme toggle */}
      <IconButton
        onClick={toggleTheme}
        sx={{ position: "fixed", top: 16, right: 16 }}
      >
        {mode === "dark" ? <LightMode /> : <DarkMode />}
      </IconButton>

      <Paper
        elevation={0}
        sx={{
          p: { xs: 3, sm: 5 },
          width: "100%",
          maxWidth: 420,
          border: 1,
          borderColor: "divider",
          borderRadius: 3,
        }}
      >
        {/* Header */}
        <Box sx={{ textAlign: "center", mb: 4 }}>
          <Avatar
            sx={{
              bgcolor: "primary.main",
              width: 56,
              height: 56,
              mx: "auto",
              mb: 2,
            }}
          >
            <LocalHospital fontSize="large" />
          </Avatar>
          <Typography variant="h5" fontWeight={700} gutterBottom>
            CliniQ RAG
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Assistant biomédical clinique
          </Typography>
        </Box>

        <Divider sx={{ mb: 3 }}>
          <Typography variant="caption" color="text.disabled">
            Connexion
          </Typography>
        </Divider>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit} sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
          <TextField
            label="Nom d'utilisateur"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            fullWidth
            autoFocus
            autoComplete="username"
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Person fontSize="small" color="action" />
                </InputAdornment>
              ),
            }}
          />

          <TextField
            label="Mot de passe"
            type={showPwd ? "text" : "password"}
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            fullWidth
            autoComplete="current-password"
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Lock fontSize="small" color="action" />
                </InputAdornment>
              ),
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    onClick={() => setShowPwd((v) => !v)}
                    edge="end"
                    size="small"
                  >
                    {showPwd ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          <Button
            type="submit"
            variant="contained"
            size="large"
            fullWidth
            disabled={mutation.isPending}
            sx={{ mt: 1, py: 1.5 }}
          >
            {mutation.isPending ? (
              <CircularProgress size={22} color="inherit" />
            ) : (
              "Se connecter"
            )}
          </Button>
        </Box>

        <Typography
          variant="caption"
          color="text.disabled"
          sx={{ display: "block", textAlign: "center", mt: 3 }}
        >
          © {new Date().getFullYear()} CliniQ — Système d'aide à la décision clinique
        </Typography>
      </Paper>
    </Box>
  );
};

export default Login;
