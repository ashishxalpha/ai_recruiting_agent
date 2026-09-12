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
    // If already logged in as a registered recruiter/admin, redirect to app
    if (!loading && user && !isGuest) {
      router.replace("/");
    }
  }, [user, isGuest, loading, router]);

  return (
    <div className="min-h-screen bg-zinc-950 text-foreground flex flex-col justify-between relative overflow-hidden">
      {/* Background ambient lighting */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[350px] bg-gradient-to-b from-blue-600/10 via-purple-600/5 to-transparent rounded-full blur-3xl pointer-events-none" />

      {/* Auth Header */}
      <header className="px-8 py-6 relative z-10 flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold shadow-md shadow-blue-500/20">
            RC
          </div>
          <span className="font-bold text-lg tracking-tight text-white">
            Recruiting Copilot
          </span>
        </Link>
        <div className="flex items-center space-x-2 text-xs text-zinc-400">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span>Platform Online</span>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-4 py-8 relative z-10">
        {children}
      </main>

      {/* Footer */}
      <footer className="px-8 py-6 text-center text-xs text-zinc-500 relative z-10 border-t border-zinc-900">
        <p>Enterprise AI Recruiting Copilot Platform &bull; Protected & Monitored</p>
      </footer>

      <Toaster theme="dark" position="bottom-right" />
    </div>
  );
}
