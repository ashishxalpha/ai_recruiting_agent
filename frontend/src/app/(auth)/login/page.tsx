"use client";

import { useState, Suspense } from "react";
import { useAuth } from "@/contexts/AuthContext";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Button } from "@/components/ui/button";

function LoginFormContent() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login, continueAsGuest } = useAuth();
  const searchParams = useSearchParams();
  const redirect = searchParams.get("redirect") || "/";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);
    try {
      await login({ email, password }, redirect);
    } catch (err: any) {
      setError(err.message || "Invalid email or password");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGuest = () => {
    continueAsGuest(redirect);
  };

  const fillCredentials = (demoEmail: string, demoPass: string) => {
    setEmail(demoEmail);
    setPassword(demoPass);
    setError("");
  };

  return (
    <div className="w-full max-w-sm space-y-5">
      <div className="space-y-1 text-center">
        <h1 className="text-xl font-semibold tracking-tight text-foreground">Sign in</h1>
        <p className="text-xs text-muted-foreground">
          Enter your email and password to access the platform
        </p>
      </div>

      <div className="rounded-xl border border-border bg-card p-6 shadow-sm space-y-4">
        <form onSubmit={handleSubmit} className="space-y-3.5">
          {error && (
            <div className="p-2.5 rounded-md bg-destructive/10 border border-destructive/20 text-destructive text-xs">
              {error}
            </div>
          )}

          <div className="space-y-1.5">
            <label className="text-xs font-medium text-foreground" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@example.com"
              className="w-full rounded-md border border-input bg-background px-3 py-1.5 text-sm text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring transition-colors"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-medium text-foreground" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••••••"
              className="w-full rounded-md border border-input bg-background px-3 py-1.5 text-sm text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring transition-colors"
            />
          </div>

          <Button
            type="submit"
            disabled={isSubmitting}
            className="w-full h-9 text-sm font-medium mt-1"
          >
            {isSubmitting ? "Signing in..." : "Sign in"}
          </Button>
        </form>

        <div className="relative flex items-center justify-center my-3">
          <div className="border-t border-border w-full" />
          <span className="bg-card px-2 text-[11px] uppercase tracking-wider text-muted-foreground absolute">
            or
          </span>
        </div>

        <Button
          type="button"
          variant="outline"
          onClick={handleGuest}
          className="w-full h-9 text-sm font-medium"
        >
          Continue as guest
        </Button>
      </div>

      <div className="flex items-center justify-between px-1 text-xs text-muted-foreground">
        <span>Demo:</span>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => fillCredentials("ashish@example.com", "Recruiter123!")}
            className="hover:text-foreground underline underline-offset-2 transition-colors cursor-pointer"
          >
            Recruiter
          </button>
          <span>&bull;</span>
          <button
            type="button"
            onClick={() => fillCredentials("admin@example.com", "Admin123!")}
            className="hover:text-foreground underline underline-offset-2 transition-colors cursor-pointer"
          >
            Admin
          </button>
        </div>
      </div>

      <p className="text-center text-xs text-muted-foreground">
        Don&apos;t have an account?{" "}
        <Link
          href={`/register?redirect=${encodeURIComponent(redirect)}`}
          className="text-foreground font-medium hover:underline underline-offset-2"
        >
          Sign up
        </Link>
      </p>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <div className="w-full max-w-sm h-80 rounded-xl border border-border bg-card/50 animate-pulse" />
      }
    >
      <LoginFormContent />
    </Suspense>
  );
}
