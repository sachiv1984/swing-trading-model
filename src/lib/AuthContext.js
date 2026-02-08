import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState({
    id: 'default-user',
    email: 'trader@example.com',
    name: 'Trader',
  });
  const [isAuthenticated, setIsAuthenticated] = useState(true);
  const [isLoadingAuth, setIsLoadingAuth] = useState(false);
  const [isLoadingPublicSettings, setIsLoadingPublicSettings] = useState(false);
  const [authError, setAuthError] = useState(null);
  const [appPublicSettings, setAppPublicSettings] = useState({ id: 'app', public_settings: {} });

  // No auth checks - just mark as ready immediately
  useEffect(() => {
    console.log('Auth: Using single-user mode (no authentication)');
  }, []);

  const logout = () => {
    console.log('Logout not implemented (single-user app)');
  };

  const navigateToLogin = () => {
    console.log('Login not implemented (single-user app)');
  };

  const checkAppState = () => {
    console.log('App state check skipped (single-user app)');
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      isAuthenticated, 
      isLoadingAuth,
      isLoadingPublicSettings,
      authError,
      appPublicSettings,
      logout,
      navigateToLogin,
      checkAppState
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
