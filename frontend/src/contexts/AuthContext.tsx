"use client";

import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from '@/lib/api-client';
import { useRouter } from 'next/navigation';

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  isGuest?: boolean;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isGuest: boolean;
  login: (data: any, redirectPath?: string) => Promise<void>;
  register: (data: any, redirectPath?: string) => Promise<void>;
  continueAsGuest: (redirectPath?: string) => void;
  logout: () => Promise<void>;
}

const GUEST_USER: User = {
  id: "guest-user",
  email: "guest@recruitingcopilot.local",
  first_name: "Guest",
  last_name: "Explorer",
  role: "guest",
  isGuest: true,
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isGuest, setIsGuest] = useState(false);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const fetchUser = async () => {
      const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
      const isGuestStored = typeof window !== 'undefined' ? localStorage.getItem('copilot_guest_mode') === 'true' : false;

      if (token) {
        try {
          const response = await apiClient.get('/api/v1/auth/me');
          setUser({ ...(response as any), isGuest: false });
          setIsGuest(false);
        } catch (err) {
          if (typeof window !== 'undefined') {
            localStorage.removeItem('token');
          }
          if (isGuestStored) {
            setUser(GUEST_USER);
            setIsGuest(true);
          } else {
            setUser(null);
            setIsGuest(false);
          }
        } finally {
          setLoading(false);
        }
      } else if (isGuestStored) {
        setUser(GUEST_USER);
        setIsGuest(true);
        setLoading(false);
      } else {
        setUser(null);
        setIsGuest(false);
        setLoading(false);
      }
    };
    
    fetchUser();
  }, []);

  const login = async (data: any, redirectPath?: string) => {
    const res: any = await apiClient.post('/api/v1/auth/login', data);
    if (res?.access_token && typeof window !== 'undefined') {
      localStorage.setItem('token', res.access_token);
      localStorage.removeItem('copilot_guest_mode');
    }
    const response = await apiClient.get('/api/v1/auth/me');
    setUser({ ...(response as any), isGuest: false });
    setIsGuest(false);
    router.push(redirectPath || '/');
  };

  const register = async (data: any, redirectPath?: string) => {
    const res: any = await apiClient.post('/api/v1/auth/register', data);
    if (res?.access_token && typeof window !== 'undefined') {
      localStorage.setItem('token', res.access_token);
      localStorage.removeItem('copilot_guest_mode');
    }
    const response = await apiClient.get('/api/v1/auth/me');
    setUser({ ...(response as any), isGuest: false });
    setIsGuest(false);
    router.push(redirectPath || '/');
  };

  const continueAsGuest = (redirectPath?: string) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('copilot_guest_mode', 'true');
      localStorage.removeItem('token');
    }
    setUser(GUEST_USER);
    setIsGuest(true);
    router.push(redirectPath || '/');
  };

  const logout = async () => {
    try {
      if (typeof window !== 'undefined' && localStorage.getItem('token')) {
        await apiClient.post('/api/v1/auth/logout');
      }
    } catch (e) {
      // ignore network errors on logout
    } finally {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        localStorage.removeItem('copilot_guest_mode');
      }
      setUser(null);
      setIsGuest(false);
      router.push('/login');
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, isGuest, login, register, continueAsGuest, logout }}>
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
