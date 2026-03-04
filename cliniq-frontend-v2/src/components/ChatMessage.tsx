import React from "react";
import { Box, Paper, Typography, Chip, Skeleton, Avatar } from "@mui/material";
import { Person, SmartToy, ExpandMore, ExpandLess } from "@mui/icons-material";
import type { ChatMessage as ChatMessageType } from "../types";
import SourcesPanel from "./SourcesPanel";

interface Props {
  message: ChatMessageType;
}

const MetricChip: React.FC<{ label: string; value: number | null | undefined }> = ({ label, value }) => {
  if (value === null || value === undefined) return null;
  const pct = Math.round(value * 100);
  const color = pct >= 70 ? "success" : pct >= 40 ? "warning" : "error";
  return (
    <Chip
      label={`${label.replace("Metric", "")}: ${pct}%`}
      color={color}
      size="small"
      variant="outlined"
      sx={{ fontSize: "0.7rem", height: 22 }}
    />
  );
};

const ChatMessage: React.FC<Props> = ({ message }) => {
  const [showSources, setShowSources] = React.useState(false);
  const isUser = message.role === "user";

  if (message.loading) {
    return (
      <Box sx={{ display: "flex", gap: 1.5, mb: 2 }}>
        <Avatar sx={{ bgcolor: "primary.main", width: 32, height: 32 }}>
          <SmartToy fontSize="small" />
        </Avatar>
        <Paper sx={{ p: 2, maxWidth: "75%", borderRadius: "4px 16px 16px 16px" }}>
          <Skeleton width={240} height={16} />
          <Skeleton width={180} height={16} sx={{ mt: 0.5 }} />
          <Skeleton width={120} height={16} sx={{ mt: 0.5 }} />
        </Paper>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: isUser ? "row-reverse" : "row",
        gap: 1.5,
        mb: 2,
        alignItems: "flex-start",
      }}
    >
      <Avatar
        sx={{
          bgcolor: isUser ? "secondary.main" : "primary.main",
          width: 32,
          height: 32,
          flexShrink: 0,
        }}
      >
        {isUser ? <Person fontSize="small" /> : <SmartToy fontSize="small" />}
      </Avatar>

      <Box sx={{ maxWidth: "75%", display: "flex", flexDirection: "column", gap: 0.75 }}>
        <Paper
          elevation={0}
          sx={{
            p: 2,
            borderRadius: isUser ? "16px 4px 16px 16px" : "4px 16px 16px 16px",
            bgcolor: isUser ? "primary.main" : "background.paper",
            color: isUser ? "primary.contrastText" : "text.primary",
            border: 1,
            borderColor: isUser ? "primary.main" : "divider",
          }}
        >
          <Typography variant="body2" sx={{ whiteSpace: "pre-wrap", lineHeight: 1.7 }}>
            {message.content}
          </Typography>
        </Paper>

        {/* Evaluation metrics */}
        {message.evaluation && (
          <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5, px: 0.5 }}>
            {Object.entries(message.evaluation).map(([key, val]) => (
              <MetricChip key={key} label={key} value={val} />
            ))}
          </Box>
        )}

        {/* Sources toggle */}
        {message.sources && message.sources.length > 0 && (
          <Box>
            <Chip
              icon={showSources ? <ExpandLess fontSize="small" /> : <ExpandMore fontSize="small" />}
              label={`${message.sources.length} source${message.sources.length > 1 ? "s" : ""}`}
              size="small"
              variant="outlined"
              onClick={() => setShowSources((v) => !v)}
              sx={{ cursor: "pointer", fontSize: "0.7rem" }}
            />
            {showSources && <SourcesPanel sources={message.sources} />}
          </Box>
        )}

        <Typography variant="caption" color="text.disabled" sx={{ px: 0.5 }}>
          {message.timestamp.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })}
        </Typography>
      </Box>
    </Box>
  );
};

export default ChatMessage;
