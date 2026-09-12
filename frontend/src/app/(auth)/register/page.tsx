"use client";

import { useState, Suspense } from "react";
import { useAuth } from "@/contexts/AuthContext";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Button } from "@/components/ui/button";

function RegisterFormContent() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { register, continueAsGuest } = useAuth();
  const searchParams = useSearchParams();
  const redirect = searchParams.get("redirect") || "/";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);
    try {
      await register({ email, password, first_name: firstName, last_name: lastName }, redirect);
    } catch (err: any) {
      setError(err.message || "Failed to create account");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="w-full max-w-sm space-y-5">
      <div className="space-y-1 text-center">
        <h1 className="text-xl font-semibold tracking-tight text-foreground">Create an account</h1>
        <p className="text-xs text-muted-foreground">
          Enter your details to register as a recruiter
        </p>
      </div>

      <div className="rounded-xl border border-border bg-card p-6 shadow-sm space-y-4">
        <form onSubmit={handleSubmit} className="space-y-3.5">
          {error && (
            <div className="p-2.5 rounded-md bg-destructive/10 border border-destructive/20 text-destructive text-xs">
              {error}
            </div>
          )}

          <div className="grid grid-cols-2 gap-2.5">
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-foreground" htmlFor="first-name">
                First name
              </label>
              <input
                id="first-name"
                type="text"
                required
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                placeholder="Jane"
                className="w-full rounded-md border border-input bg-background px-3 py-1.5 text-sm text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring transition-colors"
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-foreground" htmlFor="last-name">
                Last name
              </label>
              <input
                id="last-name"
                type="text"
                required
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                placeholder="Doe"
                className="w-full rounded-md border border-input bg-background px-3 py-1.5 text-sm text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring transition-colors"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-medium text-foreground" htmlFor="email">
              Work email
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
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="At least 8 characters"
              className="w-full rounded-md border border-input bg-background px-3 py-1.5 text-sm text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring transition-colors"
            />
          </div>

          <Button
            type="submit"
            disabled={isSubmitting}
            className="w-full h-9 text-sm font-medium mt-1"
          >
            {isSubmitting ? "Creating account..." : "Create account"}
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
          onClick={() => continueAsGuest(redirect)}
          className="w-full h-9 text-sm font-medium"
        >
          Continue as guest
        </Button>
      </div>

      <p className="text-center text-xs text-muted-foreground">
        Already have an account?{" "}
        <Link
          href={`/login?redirect=${encodeURIComponent(redirect)}`}
          className="text-foreground font-medium hover:underline underline-offset-2"
        >
          Sign in
        </Link>
      </p>
    </div>
  );
}

export default function RegisterPage() {
  return (
    <Suspense
      fallback={
        <div className="w-full max-w-sm h-96 rounded-xl border border-border bg-card/50 animate-pulse" />
      }
    >
      <RegisterFormContent />
    </Suspense>
  );
}
