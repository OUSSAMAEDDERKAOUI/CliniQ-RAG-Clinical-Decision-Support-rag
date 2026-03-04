// Simple token store backed by localStorage

export const authStore = {
  getToken: (): string | null => localStorage.getItem("access_token"),

  setToken: (token: string): void => {
    localStorage.setItem("access_token", token);
  },

  removeToken: (): void => {
    localStorage.removeItem("access_token");
  },

  isAuthenticated: (): boolean => {
    const token = localStorage.getItem("access_token");
    if (!token) return false;
    // Basic JWT expiry check
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      if (payload.exp && Date.now() / 1000 > payload.exp) {
        localStorage.removeItem("access_token");
        return false;
      }
      return true;
    } catch {
      return true; // If not decodable, assume valid
    }
  },
};
