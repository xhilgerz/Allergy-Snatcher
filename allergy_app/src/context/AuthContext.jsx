import { createContext, useCallback, useContext, useEffect, useState } from "react";
import {
  getAuthStatus,
  login as apiLogin,
  logout as apiLogout,
  registerUser,
} from "../api/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getAuthStatus();
      setUser(data.logged_in ? data.user : null);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const login = useCallback(
    async (username, password) => {
      await apiLogin(username, password);
      await refresh();
    },
    [refresh]
  );

  const register = useCallback(
    async (payload) => {
      await registerUser(payload);
      await login(payload.username, payload.password);
    },
    [login]
  );

  const logout = useCallback(async () => {
    await apiLogout();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, register, refresh }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
