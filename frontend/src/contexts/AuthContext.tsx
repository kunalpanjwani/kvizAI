import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, authAPI, setAuthToken, getAuthToken, setUser, getUser, isAuthenticated } from '../services/api';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isLoggedIn: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUserState] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const initAuth = async () => {
      try {
        if (isAuthenticated()) {
          const currentUser = await authAPI.getCurrentUser();
          setUserState(currentUser);
          setUser(currentUser);
        }
      } catch (error) {
        console.error('Failed to get current user:', error);
        // Clear invalid token
        authAPI.logout();
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      const response = await authAPI.login({ username, password });
      setAuthToken(response.access_token);
      setUserState(response.user);
      setUser(response.user);
    } catch (error) {
      throw error;
    }
  };

  const register = async (email: string, password: string) => {
    try {
      // Use email as username as requested
      const response = await authAPI.register({ 
        username: email, 
        email, 
        password 
      });
      setAuthToken(response.access_token);
      setUserState(response.user);
      setUser(response.user);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    authAPI.logout();
    setUserState(null);
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    isLoggedIn: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};