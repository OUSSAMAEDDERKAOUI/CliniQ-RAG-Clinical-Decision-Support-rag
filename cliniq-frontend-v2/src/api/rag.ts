import client from "./client";
import type {
  LoginRequest,
  LoginResponse,
  AskRequest,
  AskResponse,
  HistoryResponse,
} from "../types";

// ─── Auth ────────────────────────────────────────────────────────────────────

export const login = async (data: LoginRequest): Promise<LoginResponse> => {
  // API expects JSON body (not form data)
  const res = await client.post<LoginResponse>("/api/v1/auth/login", {
    username: data.username,
    password: data.password,
  });
  return res.data;
};

// ─── RAG ────────────────────────────────────────────────────────────────────

export const askQuestion = async (data: AskRequest): Promise<AskResponse> => {
  const res = await client.post<AskResponse>("/api/v1/index/ask", data);
  return res.data;
};

// ─── History ────────────────────────────────────────────────────────────────

export const getHistory = async (limit = 50): Promise<HistoryResponse> => {
  const res = await client.get<HistoryResponse>("/api/v1/index/history", {
    params: { limit },
  });
  return res.data;
};

// ─── Health ─────────────────────────────────────────────────────────────────

export const healthCheck = async (): Promise<{ status: string }> => {
  const res = await client.get<{ status: string }>("/health");
  return res.data;
};
