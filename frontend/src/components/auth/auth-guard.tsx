"use client";

import { useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { usePathname, useRouter } from "next/navigation";
import { isRouteAllowedForGuest, getGuestRestrictionDetails } from "@/config/guest-access";
import { Lock, ShieldAlert, ArrowRight, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { user, loading, isGuest } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      const redirectUrl = pathname ? `/login?redirect=${encodeURIComponent(pathname)}` : "/login";
      router.replace(redirectUrl);
    }
  }, [user, loading, pathname, router]);

  // Render high-fidelity loading state while checking session token
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center text-primary font-bold text-xl animate-pulse">
            RC
          </div>
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            <span>Verifying session security...</span>
          </div>
        </div>
      </div>
    );
  }

  // If unauthenticated, prevent any content flash during redirect
  if (!user) {
    return null;
  }

  // If in guest mode, enforce configurable route restrictions
  if (isGuest && !isRouteAllowedForGuest(pathname)) {
    const restriction = getGuestRestrictionDetails(pathname);

    return (
      <div className="max-w-2xl mx-auto my-12 p-8 rounded-2xl bg-card border border-border shadow-xl space-y-6 text-center">
        <div className="w-14 h-14 mx-auto rounded-2xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
          <Lock className="w-7 h-7" />
        </div>

        <div className="space-y-2">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <ShieldAlert className="w-3.5 h-3.5" />
            Guest Access Restricted
          </span>
          <h2 className="text-2xl font-bold tracking-tight text-foreground">{restriction.title}</h2>
          <p className="text-sm text-muted-foreground max-w-md mx-auto">
            {restriction.description}
          </p>
        </div>

        <div className="p-4 rounded-xl bg-muted/30 border border-border/50 text-left text-xs text-muted-foreground space-y-1.5">
          <p className="font-semibold text-foreground">Why am I seeing this?</p>
          <p>
            You are browsing in <strong>Guest Mode</strong>. Candidate uploads, real-time workflow mutations, and recruiter evaluations are restricted to authenticated sessions to maintain data integrity.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
          <Link
            href={`/login?redirect=${encodeURIComponent(pathname)}`}
            className={cn(buttonVariants({ variant: "default" }), "w-full sm:w-auto h-9 px-4")}
          >
            <span>Sign In with Recruiter Account</span>
            <ArrowRight className="w-4 h-4 ml-2" />
          </Link>
          <Link
            href="/"
            className={cn(buttonVariants({ variant: "outline" }), "w-full sm:w-auto h-9 px-4")}
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            <span>Return to Dashboard</span>
          </Link>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
