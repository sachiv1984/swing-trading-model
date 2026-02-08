import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState({
    id: 'default-user',
    email: 'trader@example.com',
    name: 'Portfolio Manager',
    role: 'admin'
  });
  const [isAuthenticated, setIsAuthenticated] = useState(true);
  const [isLoadingAuth, setIsLoadingAuth] = useState(false);
  const [isLoadingPublicSettings, setIsLoadingPublicSettings] = useState(false);
  const [authError, setAuthError] = useState(null);
  const [appPublicSettings, setAppPublicSettings] = useState({ 
    id: 'trading-app', 
    public_settings: {} 
  });

  useEffect(() => {
    // Log once on mount
    console.log('🔓 Auth: Single-user mode active (no authentication required)');
  }, []);

  const logout = () => {
    console.warn('Logout called but auth is disabled');
  };

  const navigateToLogin = () => {
    console.warn('Login called but auth is disabled');
  };

  const checkAppState = () => {
    console.log('App state check skipped');
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      isAuthenticated, 
      isLoadingAuth,
      isLoadingPublicSettings,
      authError,
      appPublicSettings,
      logo
