import React from "react";
import { Box, Paper, Typography, Chip } from "@mui/material";
import { Description } from "@mui/icons-material";
import type { Source } from "../types";

interface Props {
  sources: Source[];
}

const SourcesPanel: React.FC<Props> = ({ sources }) => {
  return (
    <Box sx={{ mt: 1, display: "flex", flexDirection: "column", gap: 1 }}>
      {sources.map((src, idx) => (
        <Paper
          key={idx}
          variant="outlined"
          sx={{ p: 1.5, borderRadius: 2, bgcolor: "action.hover" }}
        >
          <Box sx={{ display: "flex", alignItems: "center", gap: 0.75, mb: 0.75 }}>
            <Description sx={{ fontSize: 14, color: "primary.main" }} />
            <Typography variant="caption" fontWeight={600} color="primary.main">
              Source {idx + 1}
            </Typography>
            {src.score !== undefined && (
              <Chip
                label={`score: ${src.score.toFixed(3)}`}
                size="small"
                sx={{ fontSize: "0.65rem", height: 18, ml: "auto" }}
              />
            )}
          </Box>
          <Typography
            variant="caption"
            color="text.secondary"
            sx={{
              display: "-webkit-box",
              WebkitLineClamp: 4,
              WebkitBoxOrient: "vertical",
              overflow: "hidden",
              lineHeight: 1.6,
            }}
          >
            {src.content}
          </Typography>
          {src.metadata?.source != null && (
            <Typography variant="caption" color="text.disabled" sx={{ mt: 0.5, display: "block" }}>
              📄 {String(src.metadata.source as string)}
            </Typography>
          )}
        </Paper>
      ))}
    </Box>
  );
};

export default SourcesPanel;
