"use client";

import { useState, Suspense } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { Compass, KeyRound, ArrowRight, ShieldCheck, Sparkles, UserCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';

function LoginFormContent() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login, continueAsGuest } = useAuth();
  const searchParams = useSearchParams();
  const redirect = searchParams.get('redirect') || '/';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);
    try {
      await login({ email, password }, redirect);
    } catch (err: any) {
      setError(err.message || 'Invalid credentials or failed to login');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGuest = () => {
    continueAsGuest(redirect);
  };

  const setDemoAccount = (demoEmail: string, demoPass: string) => {
    setEmail(demoEmail);
    setPassword(demoPass);
    setError('');
  };

  return (
    <div className="w-full max-w-md space-y-6 rounded-2xl bg-zinc-900/90 p-8 shadow-2xl ring-1 ring-white/10 backdrop-blur-xl">
      <div className="text-center space-y-1.5">
        <h2 className="text-2xl font-bold tracking-tight text-white">Sign in to Copilot</h2>
        <p className="text-sm text-zinc-400">
          Enter your recruiter credentials to access the cognitive platform
        </p>
      </div>

      {/* Guest Mode Card Option */}
      <div className="p-4 rounded-xl bg-gradient-to-r from-blue-950/40 via-indigo-950/40 to-zinc-900 border border-blue-500/20 space-y-3">
        <div className="flex items-start justify-between">
          <div className="space-y-0.5">
            <div className="flex items-center gap-1.5 text-xs font-semibold text-blue-400">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Instant Access</span>
            </div>
            <h3 className="text-sm font-bold text-white">Explore as Guest</h3>
            <p className="text-xs text-zinc-400">
              Browse candidate vectors, job matches & dashboards without signing up.
            </p>
          </div>
        </div>
        <Button
          type="button"
          onClick={handleGuest}
          variant="outline"
          className="w-full bg-blue-600/10 hover:bg-blue-600/20 text-blue-300 border-blue-500/30 hover:border-blue-500/50 text-xs font-semibold h-9"
        >
          <Compass className="w-3.5 h-3.5 mr-1.5 text-blue-400" />
          <span>Continue as Guest</span>
          <ArrowRight className="w-3 h-3 ml-auto opacity-70" />
        </Button>
      </div>

      <div className="relative flex items-center justify-center">
        <div className="border-t border-zinc-800 w-full" />
        <span className="bg-zinc-900 px-3 text-[11px] font-medium uppercase tracking-wider text-zinc-500 absolute">
          Or sign in with account
        </span>
      </div>

      {/* Standard Credentials Form */}
      <form className="space-y-4" onSubmit={handleSubmit}>
        {error && (
          <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-xs">
            {error}
          </div>
        )}

        <div className="space-y-3">
          <div>
            <label className="block text-xs font-medium text-zinc-300 mb-1" htmlFor="email-address">
              Email address
            </label>
            <input
              id="email-address"
              name="email"
              type="email"
              required
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full rounded-lg border-0 bg-zinc-800/80 py-2 text-white ring-1 ring-inset ring-zinc-700 placeholder:text-zinc-500 focus:ring-2 focus:ring-blue-500 text-sm px-3 transition-all"
              placeholder="name@company.com"
            />
          </div>
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs font-medium text-zinc-300" htmlFor="password">
                Password
              </label>
            </div>
            <input
              id="password"
              name="password"
              type="password"
              required
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="w-full rounded-lg border-0 bg-zinc-800/80 py-2 text-white ring-1 ring-inset ring-zinc-700 placeholder:text-zinc-500 focus:ring-2 focus:ring-blue-500 text-sm px-3 transition-all"
              placeholder="••••••••••••"
            />
          </div>
        </div>

        <Button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold text-sm h-10 shadow-md shadow-blue-600/20"
        >
          {isSubmitting ? (
            <span className="flex items-center gap-2">
              <span className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Signing in...
            </span>
          ) : (
            <span className="flex items-center gap-1.5">
              <KeyRound className="w-4 h-4" />
              <span>Sign In</span>
            </span>
          )}
        </Button>
      </form>

      {/* Demo Credentials Helper */}
      <div className="p-3 rounded-xl bg-zinc-800/40 border border-zinc-800 text-xs space-y-2">
        <div className="flex items-center justify-between text-zinc-400">
          <span className="font-semibold text-zinc-300 flex items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Demo Test Accounts</span>
          </span>
          <span className="text-[10px] text-zinc-500">1-Click autofill</span>
        </div>
        <div className="grid grid-cols-2 gap-2 pt-1">
          <button
            type="button"
            onClick={() => setDemoAccount('ashish@example.com', 'Recruiter123!')}
            className="px-2.5 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-750 border border-zinc-700/60 text-left transition-colors group"
          >
            <div className="text-[11px] font-semibold text-zinc-200 group-hover:text-blue-400 flex items-center justify-between">
              <span>Recruiter</span>
              <UserCheck className="w-3 h-3 text-zinc-500 group-hover:text-blue-400" />
            </div>
            <div className="text-[10px] text-zinc-400 truncate">ashish@example.com</div>
          </button>
          <button
            type="button"
            onClick={() => setDemoAccount('admin@example.com', 'Admin123!')}
            className="px-2.5 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-750 border border-zinc-700/60 text-left transition-colors group"
          >
            <div className="text-[11px] font-semibold text-zinc-200 group-hover:text-blue-400 flex items-center justify-between">
              <span>Admin</span>
              <UserCheck className="w-3 h-3 text-zinc-500 group-hover:text-blue-400" />
            </div>
            <div className="text-[10px] text-zinc-400 truncate">admin@example.com</div>
          </button>
        </div>
      </div>

      <div className="text-center text-xs text-zinc-400">
        Don&apos;t have an account?{' '}
        <Link href={`/register?redirect=${encodeURIComponent(redirect)}`} className="font-semibold text-blue-400 hover:text-blue-300">
          Register new recruiter
        </Link>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={
      <div className="w-full max-w-md h-96 rounded-2xl bg-zinc-900/60 animate-pulse" />
    }>
      <LoginFormContent />
    </Suspense>
  );
}
