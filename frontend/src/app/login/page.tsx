"use client";

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import Link from 'next/link';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await login({ email, password });
    } catch (err: any) {
      setError(err.message || 'Failed to login');
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-950 px-4">
      <div className="w-full max-w-md space-y-8 rounded-xl bg-zinc-900 p-8 shadow-lg ring-1 ring-white/10">
        <div className="text-center">
          <h2 className="text-3xl font-bold tracking-tight text-white">Sign in to Copilot</h2>
          <p className="mt-2 text-sm text-zinc-400">Welcome back to the Enterprise Cognitive Platform</p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && <div className="text-red-500 text-sm text-center">{error}</div>}
          <div className="space-y-4 rounded-md shadow-sm">
            <div>
              <label className="sr-only" htmlFor="email-address">Email address</label>
              <input
                id="email-address"
                name="email"
                type="email"
                required
                value={email}
                onChange={e => setEmail(e.target.value)}
                className="relative block w-full rounded-md border-0 bg-zinc-800 py-1.5 text-white ring-1 ring-inset ring-zinc-700 placeholder:text-zinc-400 focus:z-10 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm sm:leading-6 px-3"
                placeholder="Email address"
              />
            </div>
            <div>
              <label className="sr-only" htmlFor="password">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={password}
                onChange={e => setPassword(e.target.value)}
                className="relative block w-full rounded-md border-0 bg-zinc-800 py-1.5 text-white ring-1 ring-inset ring-zinc-700 placeholder:text-zinc-400 focus:z-10 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm sm:leading-6 px-3"
                placeholder="Password"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="group relative flex w-full justify-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
            >
              Sign in
            </button>
          </div>
        </form>
        <div className="text-center text-sm text-zinc-400">
          Don't have an account?{' '}
          <Link href="/register" className="font-semibold text-blue-500 hover:text-blue-400">
            Sign up
          </Link>
        </div>
      </div>
    </div>
  );
}
