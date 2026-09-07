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
      const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }
      try {
        const response = await apiClient.get('/api/v1/auth/me');
        setUser(response as any);
      } catch (err) {
        if (typeof window !== 'undefined') {
          localStorage.removeItem('token');
        }
        setUser(null);
      } finally {
        setLoading(false);
      }
    };
    
    fetchUser();
  }, []);

  const login = async (data: any) => {
    const res: any = await apiClient.post('/api/v1/auth/login', data);
    if (res?.access_token && typeof window !== 'undefined') {
      localStorage.setItem('token', res.access_token);
    }
    const response = await apiClient.get('/api/v1/auth/me');
    setUser(response as any);
    router.push('/');
  };

  const register = async (data: any) => {
    const res: any = await apiClient.post('/api/v1/auth/register', data);
    if (res?.access_token && typeof window !== 'undefined') {
      localStorage.setItem('token', res.access_token);
    }
    const response = await apiClient.get('/api/v1/auth/me');
    setUser(response as any);
    router.push('/');
  };

  const logout = async () => {
    try {
      await apiClient.post('/api/v1/auth/logout');
    } catch (e) {
      // ignore network errors on logout
    } finally {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
      }
      setUser(null);
      router.push('/login');
    }
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
