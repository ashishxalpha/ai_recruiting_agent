"use client";

import { useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { usePathname, useRouter } from "next/navigation";
import { isRouteAllowedForGuest } from "@/config/guest-access";
import { Lock } from "lucide-react";
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

  // Clean, minimal loading indicator matching dashboard widgets
  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!user) {
    return null;
  }

  // Intercept restricted routes for guests with a clean, minimal card
  if (isGuest && !isRouteAllowedForGuest(pathname)) {
    return (
      <div className="max-w-md mx-auto my-16 p-6 rounded-xl border border-border bg-card text-center space-y-4 shadow-sm">
        <div className="w-10 h-10 mx-auto rounded-full bg-muted flex items-center justify-center text-muted-foreground">
          <Lock className="w-5 h-5" />
        </div>

        <div className="space-y-1">
          <h2 className="text-base font-semibold text-foreground">Sign in required</h2>
          <p className="text-xs text-muted-foreground">
            This section is restricted in guest mode. Sign in with a recruiter account to access it.
          </p>
        </div>

        <div className="flex items-center justify-center gap-2 pt-2">
          <Link
            href={`/login?redirect=${encodeURIComponent(pathname)}`}
            className={cn(buttonVariants({ variant: "default" }), "h-8 px-3 text-xs font-medium")}
          >
            Sign in
          </Link>
          <Link
            href="/"
            className={cn(buttonVariants({ variant: "outline" }), "h-8 px-3 text-xs font-medium")}
          >
            Back to dashboard
          </Link>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
