import React, { useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  TextField,
  InputAdornment,
  CircularProgress,
  Alert,
  Button,
} from "@mui/material";
import {
  ExpandMore,
  History as HistoryIcon,
  Search,
  Refresh,
  QuestionAnswer,
} from "@mui/icons-material";
import { useQuery } from "@tanstack/react-query";
import Layout from "../components/Layout";
import { getHistory } from "../api/rag";

const History: React.FC = () => {
  const [search, setSearch] = useState("");
  const [limit, setLimit] = useState(50);

  const { data, isLoading, isError, refetch, isFetching } = useQuery({
    queryKey: ["history", limit],
    queryFn: () => getHistory(limit),
    staleTime: 30_000,
  });

  const filtered = (data?.items ?? []).filter(
    (item) =>
      item.question.toLowerCase().includes(search.toLowerCase()) ||
      item.answer.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <Layout>
      <Box sx={{ display: "flex", flexDirection: "column", height: "100vh" }}>
        {/* Header */}
        <Box
          sx={{
            px: 3,
            py: 2,
            borderBottom: 1,
            borderColor: "divider",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            bgcolor: "background.paper",
          }}
        >
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <HistoryIcon sx={{ color: "primary.main" }} />
            <Typography variant="h6" fontWeight={700}>
              Historique
            </Typography>
            {data && (
              <Chip
                label={`${data.items.length} requête${data.items.length > 1 ? "s" : ""}`}
                size="small"
                color="primary"
                variant="outlined"
              />
            )}
          </Box>
          <Button
            startIcon={isFetching ? <CircularProgress size={14} /> : <Refresh />}
            onClick={() => refetch()}
            size="small"
            disabled={isFetching}
          >
            Actualiser
          </Button>
        </Box>

        {/* Search */}
        <Box sx={{ px: 3, py: 2, bgcolor: "background.paper", borderBottom: 1, borderColor: "divider" }}>
          <TextField
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Rechercher dans l'historique…"
            size="small"
            fullWidth
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search fontSize="small" color="action" />
                </InputAdornment>
              ),
            }}
            sx={{ "& .MuiOutlinedInput-root": { borderRadius: 3 } }}
          />
        </Box>

        {/* Content */}
        <Box sx={{ flex: 1, overflowY: "auto", px: 3, py: 2 }}>
          {isLoading && (
            <Box sx={{ display: "flex", justifyContent: "center", mt: 6 }}>
              <CircularProgress />
            </Box>
          )}

          {isError && (
            <Alert severity="error" sx={{ mt: 2 }}>
              Impossible de charger l'historique. Vérifiez votre connexion.
            </Alert>
          )}

          {!isLoading && !isError && filtered.length === 0 && (
            <Box sx={{ textAlign: "center", mt: 8, color: "text.secondary" }}>
              <QuestionAnswer sx={{ fontSize: 56, opacity: 0.3, mb: 2 }} />
              <Typography>
                {search ? "Aucun résultat pour cette recherche" : "Aucune requête dans l'historique"}
              </Typography>
            </Box>
          )}

          {filtered.map((item) => (
            <Accordion
              key={item.id}
              disableGutters
              elevation={0}
              sx={{
                mb: 1.5,
                border: 1,
                borderColor: "divider",
                borderRadius: "12px !important",
                "&:before": { display: "none" },
                "&.Mui-expanded": { borderColor: "primary.main" },
              }}
            >
              <AccordionSummary
                expandIcon={<ExpandMore />}
                sx={{ borderRadius: 2, px: 2 }}
              >
                <Box sx={{ display: "flex", flexDirection: "column", gap: 0.5, width: "100%", pr: 1 }}>
                  <Typography variant="body2" fontWeight={600} noWrap>
                    {item.question}
                  </Typography>
                  <Typography variant="caption" color="text.disabled">
                    {new Date(item.timestamp).toLocaleString("fr-FR", {
                      day: "2-digit",
                      month: "long",
                      year: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </Typography>
                </Box>
              </AccordionSummary>
              <AccordionDetails sx={{ px: 2, pb: 2 }}>
                <Paper
                  variant="outlined"
                  sx={{ p: 2, borderRadius: 2, bgcolor: "action.hover" }}
                >
                  <Typography variant="body2" sx={{ whiteSpace: "pre-wrap", lineHeight: 1.8 }}>
                    {item.answer}
                  </Typography>
                </Paper>
              </AccordionDetails>
            </Accordion>
          ))}

          {/* Load more */}
          {data && data.items.length >= limit && (
            <Box sx={{ textAlign: "center", mt: 2 }}>
              <Button onClick={() => setLimit((l) => l + 50)} variant="outlined" size="small">
                Charger plus
              </Button>
            </Box>
          )}
        </Box>
      </Box>
    </Layout>
  );
};

export default History;
