import React from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "react-hot-toast";
import { ThemeProvider } from "./theme/ThemeProvider";
import { authStore } from "./store/authStore";
import Login from "./pages/Login";
import Chat from "./pages/Chat";
import History from "./pages/History";
import Observability from "./pages/Observability";
import Settings from "./pages/Settings";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 30_000,
    },
  },
});

// Protected route wrapper
const ProtectedRoute: React.FC<{ element: React.ReactElement }> = ({
  element,
}) => {
  return authStore.isAuthenticated() ? element : <Navigate to="/login" replace />;
};

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/chat"
              element={<ProtectedRoute element={<Chat />} />}
            />
            <Route
              path="/history"
              element={<ProtectedRoute element={<History />} />}
            />
            <Route
              path="/observability"
              element={<ProtectedRoute element={<Observability />} />}
            />
            <Route
              path="/settings"
              element={<ProtectedRoute element={<Settings />} />}
            />
            {/* Default redirect */}
            <Route
              path="/"
              element={
                authStore.isAuthenticated() ? (
                  <Navigate to="/chat" replace />
                ) : (
                  <Navigate to="/login" replace />
                )
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              borderRadius: "12px",
              fontSize: "0.875rem",
            },
          }}
        />
      </ThemeProvider>
    </QueryClientProvider>
  );
};

export default App;
