import { useEffect, useState, useCallback } from "react";
import { AuthContext } from "./authContextObject";
import { getToken, setToken, login as apiLogin, signup as apiSignup, getMe } from "../lib/api";



export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(() => !!getToken());

  useEffect(() => {
    if (!getToken()) return;

    getMe()
      .then(setUser)
      .catch(() => setToken(null))
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (credentials) => {
    const data = await apiLogin(credentials);
    setToken(data.access_token);
    setUser(data.user);
    return data.user;
  }, []);

  const signup = useCallback(async (details) => {
    const data = await apiSignup(details);
    setToken(data.access_token);
    setUser(data.user);
    return data.user;
  }, []);

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}
