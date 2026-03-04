// ─── Auth ───────────────────────────────────────────────────────────────────

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
}

// ─── RAG ────────────────────────────────────────────────────────────────────

export interface Source {
  content: string;
  metadata: Record<string, unknown>;
  score?: number;
}

export interface EvaluationMetrics {
  AnswerRelevancyMetric?: number | null;
  FaithfulnessMetric?: number | null;
  ContextualPrecisionMetric?: number | null;
  ContextualRecallMetric?: number | null;
  [key: string]: number | null | undefined;
}

export interface AskResponse {
  question: string;
  answer: string;
  sources?: Source[];
  answer_evaluation?: EvaluationMetrics;
}

export interface AskRequest {
  question: string;
}

// ─── History ────────────────────────────────────────────────────────────────

export interface HistoryItem {
  id: number;
  question: string;
  answer: string;
  timestamp: string;
}

export interface HistoryResponse {
  items: HistoryItem[];
}

// ─── Chat message (local) ────────────────────────────────────────────────────

export type MessageRole = "user" | "assistant";

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  sources?: Source[];
  evaluation?: EvaluationMetrics;
  timestamp: Date;
  loading?: boolean;
}
