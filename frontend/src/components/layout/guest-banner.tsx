"use client";

import { useAuth } from "@/contexts/AuthContext";
import { GUEST_ACCESS_CONFIG } from "@/config/guest-access";
import { X } from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { usePathname } from "next/navigation";

export function GuestBanner() {
  const { isGuest } = useAuth();
  const [dismissed, setDismissed] = useState(false);
  const pathname = usePathname();

  if (!isGuest || !GUEST_ACCESS_CONFIG.ui.showGuestBanner || dismissed) {
    return null;
  }

  return (
    <div className="bg-muted/40 border-b border-border text-muted-foreground px-4 py-1.5 text-xs flex items-center justify-between sticky top-16 z-30 backdrop-blur-sm">
      <div className="flex items-center space-x-2">
        <span className="px-1.5 py-0.2 rounded bg-foreground/10 text-foreground text-[10px] font-medium tracking-wide">
          Guest session
        </span>
        <span>Viewing demo data in read-only mode.</span>
      </div>
      <div className="flex items-center space-x-3 shrink-0 ml-4">
        <Link
          href={`/login?redirect=${encodeURIComponent(pathname)}`}
          className="text-foreground hover:underline font-medium"
        >
          Sign in for full access
        </Link>
        <button
          onClick={() => setDismissed(true)}
          title="Dismiss banner"
          className="p-0.5 text-muted-foreground hover:text-foreground rounded transition-colors"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
