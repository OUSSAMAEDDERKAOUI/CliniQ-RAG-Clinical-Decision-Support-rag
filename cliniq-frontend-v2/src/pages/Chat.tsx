import React, { useState, useRef, useEffect, useCallback } from "react";
import {
  Box,
  TextField,
  IconButton,
  Typography,
  Paper,
  Tooltip,
  Chip,
  CircularProgress,
} from "@mui/material";
import { Send, Delete, AutoAwesome } from "@mui/icons-material";
import { useMutation } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { v4 as uuidv4 } from "uuid";
import Layout from "../components/Layout";
import ChatMessageComponent from "../components/ChatMessage";
import { askQuestion } from "../api/rag";
import type { ChatMessage } from "../types";

const SUGGESTIONS = [
  "Quel est le traitement de première intention pour l'HTA ?",
  "Quels sont les critères diagnostiques du diabète de type 2 ?",
  "Comment gérer une réaction anaphylactique en urgence ?",
  "Quelles sont les contre-indications de l'amoxicilline ?",
];

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const mutation = useMutation({
    mutationFn: askQuestion,
    onMutate: (vars) => {
      const userMsg: ChatMessage = {
        id: uuidv4(),
        role: "user",
        content: vars.question,
        timestamp: new Date(),
      };
      const loadingMsg: ChatMessage = {
        id: "loading",
        role: "assistant",
        content: "",
        timestamp: new Date(),
        loading: true,
      };
      setMessages((prev) => [...prev, userMsg, loadingMsg]);
    },
    onSuccess: (data) => {
      const assistantMsg: ChatMessage = {
        id: uuidv4(),
        role: "assistant",
        content: data.answer,
        sources: data.sources,
        evaluation: data.answer_evaluation,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev.filter((m) => m.id !== "loading"), assistantMsg]);
    },
    onError: (err: unknown) => {
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
        "Erreur lors de la requête";
      toast.error(detail);
      setMessages((prev) => prev.filter((m) => m.id !== "loading"));
    },
  });

  const handleSend = useCallback(() => {
    const q = input.trim();
    if (!q || mutation.isPending) return;
    setInput("");
    mutation.mutate({ question: q });
  }, [input, mutation]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

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
            <AutoAwesome sx={{ color: "primary.main" }} />
            <Typography variant="h6" fontWeight={700}>
              Chat RAG
            </Typography>
            <Chip label="Mistral 7B" size="small" variant="outlined" sx={{ fontSize: "0.7rem" }} />
          </Box>
          {messages.length > 0 && (
            <Tooltip title="Effacer la conversation">
              <IconButton onClick={clearChat} size="small" color="error">
                <Delete fontSize="small" />
              </IconButton>
            </Tooltip>
          )}
        </Box>

        {/* Messages */}
        <Box
          sx={{
            flex: 1,
            overflowY: "auto",
            px: { xs: 2, md: 4 },
            py: 3,
            display: "flex",
            flexDirection: "column",
          }}
        >
          {messages.length === 0 ? (
            <Box
              sx={{
                flex: 1,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: 3,
              }}
            >
              <AutoAwesome sx={{ fontSize: 56, color: "primary.main", opacity: 0.6 }} />
              <Typography variant="h6" color="text.secondary" textAlign="center">
                Posez votre question clinique
              </Typography>
              <Typography variant="body2" color="text.disabled" textAlign="center" maxWidth={400}>
                Je suis votre assistant biomédical basé sur la documentation clinique. Je recherche les
                informations pertinentes pour répondre à vos questions.
              </Typography>
              {/* Suggestion chips */}
              <Box
                sx={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: 1,
                  justifyContent: "center",
                  maxWidth: 600,
                }}
              >
                {SUGGESTIONS.map((s) => (
                  <Chip
                    key={s}
                    label={s}
                    onClick={() => setInput(s)}
                    variant="outlined"
                    sx={{
                      cursor: "pointer",
                      fontSize: "0.78rem",
                      "&:hover": { bgcolor: "action.hover" },
                    }}
                  />
                ))}
              </Box>
            </Box>
          ) : (
            messages.map((msg) => (
              <ChatMessageComponent key={msg.id} message={msg} />
            ))
          )}
          <div ref={bottomRef} />
        </Box>

        {/* Input */}
        <Paper
          elevation={0}
          sx={{
            px: { xs: 2, md: 4 },
            py: 2,
            borderTop: 1,
            borderColor: "divider",
            bgcolor: "background.paper",
          }}
        >
          <Box sx={{ display: "flex", gap: 1, alignItems: "flex-end" }}>
            <TextField
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              multiline
              maxRows={5}
              fullWidth
              placeholder="Posez votre question clinique… (Entrée pour envoyer)"
              variant="outlined"
              size="small"
              disabled={mutation.isPending}
              sx={{ "& .MuiOutlinedInput-root": { borderRadius: 3 } }}
            />
            <IconButton
              onClick={handleSend}
              disabled={!input.trim() || mutation.isPending}
              color="primary"
              sx={{
                bgcolor: "primary.main",
                color: "primary.contrastText",
                width: 44,
                height: 44,
                "&:hover": { bgcolor: "primary.dark" },
                "&:disabled": { bgcolor: "action.disabledBackground" },
                flexShrink: 0,
              }}
            >
              {mutation.isPending ? (
                <CircularProgress size={18} color="inherit" />
              ) : (
                <Send fontSize="small" />
              )}
            </IconButton>
          </Box>
          <Typography variant="caption" color="text.disabled" sx={{ mt: 0.5, display: "block" }}>
            Les réponses sont basées sur la documentation clinique et peuvent nécessiter une validation médicale.
          </Typography>
        </Paper>
      </Box>
    </Layout>
  );
};

export default Chat;
