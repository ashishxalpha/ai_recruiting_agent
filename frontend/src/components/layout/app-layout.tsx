"use client";

import { Sidebar } from "./sidebar";
import { Topbar } from "./topbar";
import { Toaster } from "sonner";
import { CommandPalette } from "./command-palette";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export function AppLayout({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [user, loading, router]);

  if (loading || !user) {
    return <div className="min-h-screen bg-background flex items-center justify-center"><div className="text-white">Loading...</div></div>;
  }

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <div className="pl-64 flex flex-col min-h-screen">
        <Topbar />
        <main className="flex-1 p-8 overflow-y-auto">
          {children}
        </main>
      </div>
      <Toaster theme="dark" position="bottom-right" />
      <CommandPalette />
    </div>
  );
}
