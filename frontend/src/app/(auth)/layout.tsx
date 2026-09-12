"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import Link from "next/link";
import { Toaster } from "sonner";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, isGuest, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // If already logged in as a registered user, redirect to app
    if (!loading && user && !isGuest) {
      router.replace("/");
    }
  }, [user, isGuest, loading, router]);

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col justify-between">
      {/* Header */}
      <header className="px-6 py-4 flex items-center justify-between border-b border-border/40">
        <Link href="/" className="flex items-center space-x-2.5">
          <div className="w-7 h-7 rounded-md bg-primary flex items-center justify-center text-primary-foreground font-bold text-xs">
            RC
          </div>
          <span className="font-semibold text-sm tracking-tight text-foreground">
            Recruiting Copilot
          </span>
        </Link>
      </header>

      {/* Main Container */}
      <main className="flex-1 flex items-center justify-center px-4 py-12">
        {children}
      </main>

      {/* Footer */}
      <footer className="px-6 py-4 text-center text-xs text-muted-foreground border-t border-border/40">
        <p>&copy; {new Date().getFullYear()} Recruiting Copilot. All rights reserved.</p>
      </footer>

      <Toaster theme="dark" position="bottom-right" />
    </div>
  );
}
