"use client";

import { useState, Suspense } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { Compass, UserPlus } from 'lucide-react';
import { Button } from '@/components/ui/button';

function RegisterFormContent() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { register, continueAsGuest } = useAuth();
  const searchParams = useSearchParams();
  const redirect = searchParams.get('redirect') || '/';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);
    try {
      await register({ email, password, first_name: firstName, last_name: lastName }, redirect);
    } catch (err: any) {
      setError(err.message || 'Failed to register account');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="w-full max-w-md space-y-6 rounded-2xl bg-zinc-900/90 p-8 shadow-2xl ring-1 ring-white/10 backdrop-blur-xl">
      <div className="text-center space-y-1.5">
        <h2 className="text-2xl font-bold tracking-tight text-white">Create Recruiter Account</h2>
        <p className="text-sm text-zinc-400">Join the Enterprise Cognitive Platform</p>
      </div>

      <form className="space-y-4" onSubmit={handleSubmit}>
        {error && (
          <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-xs">
            {error}
          </div>
        )}

        <div className="space-y-3">
          <div className="flex gap-3">
            <div className="w-1/2">
              <label className="block text-xs font-medium text-zinc-300 mb-1" htmlFor="first-name">
                First name
              </label>
              <input
                id="first-name"
                name="firstName"
                type="text"
                required
                value={firstName}
                onChange={e => setFirstName(e.target.value)}
                className="w-full rounded-lg border-0 bg-zinc-800/80 py-2 text-white ring-1 ring-inset ring-zinc-700 placeholder:text-zinc-500 focus:ring-2 focus:ring-blue-500 text-sm px-3"
                placeholder="Jane"
              />
            </div>
            <div className="w-1/2">
              <label className="block text-xs font-medium text-zinc-300 mb-1" htmlFor="last-name">
                Last name
              </label>
              <input
                id="last-name"
                name="lastName"
                type="text"
                required
                value={lastName}
                onChange={e => setLastName(e.target.value)}
                className="w-full rounded-lg border-0 bg-zinc-800/80 py-2 text-white ring-1 ring-inset ring-zinc-700 placeholder:text-zinc-500 focus:ring-2 focus:ring-blue-500 text-sm px-3"
                placeholder="Doe"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-zinc-300 mb-1" htmlFor="email-address">
              Work email
            </label>
            <input
              id="email-address"
              name="email"
              type="email"
              required
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full rounded-lg border-0 bg-zinc-800/80 py-2 text-white ring-1 ring-inset ring-zinc-700 placeholder:text-zinc-500 focus:ring-2 focus:ring-blue-500 text-sm px-3"
              placeholder="jane.doe@company.com"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-zinc-300 mb-1" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              minLength={8}
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="w-full rounded-lg border-0 bg-zinc-800/80 py-2 text-white ring-1 ring-inset ring-zinc-700 placeholder:text-zinc-500 focus:ring-2 focus:ring-blue-500 text-sm px-3"
              placeholder="At least 8 characters"
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
              Creating account...
            </span>
          ) : (
            <span className="flex items-center gap-1.5">
              <UserPlus className="w-4 h-4" />
              <span>Create Account</span>
            </span>
          )}
        </Button>
      </form>

      <div className="relative flex items-center justify-center">
        <div className="border-t border-zinc-800 w-full" />
        <span className="bg-zinc-900 px-3 text-[11px] font-medium uppercase tracking-wider text-zinc-500 absolute">
          Or
        </span>
      </div>

      <Button
        type="button"
        variant="ghost"
        onClick={() => continueAsGuest(redirect)}
        className="w-full text-xs text-zinc-400 hover:text-white hover:bg-zinc-800/60 h-9"
      >
        <Compass className="w-3.5 h-3.5 mr-1.5 text-blue-400" />
        <span>Skip registration & continue as guest</span>
      </Button>

      <div className="text-center text-xs text-zinc-400">
        Already have an account?{' '}
        <Link href={`/login?redirect=${encodeURIComponent(redirect)}`} className="font-semibold text-blue-400 hover:text-blue-300">
          Sign in
        </Link>
      </div>
    </div>
  );
}

export default function RegisterPage() {
  return (
    <Suspense fallback={
      <div className="w-full max-w-md h-96 rounded-2xl bg-zinc-900/60 animate-pulse" />
    }>
      <RegisterFormContent />
    </Suspense>
  );
}
