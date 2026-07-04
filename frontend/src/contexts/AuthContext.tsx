"use client";

import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from '@/lib/api-client';
import { useRouter, usePathname } from 'next/navigation';

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (data: any) => Promise<void>;
  register: (data: any) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await apiClient.get('/api/v1/auth/me');
        setUser(response as any);
      } catch (err) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };
    
    // Don't fetch user on public routes if not needed, but generally good to know if logged in
    fetchUser();
  }, []);

  const login = async (data: any) => {
    await apiClient.post('/api/v1/auth/login', data);
    const response = await apiClient.get('/api/v1/auth/me');
    setUser(response as any);
    router.push('/');
  };

  const register = async (data: any) => {
    await apiClient.post('/api/v1/auth/register', data);
    // After register, either login or redirect to login
    await login({ email: data.email, password: data.password });
  };

  const logout = async () => {
    await apiClient.post('/api/v1/auth/logout');
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
