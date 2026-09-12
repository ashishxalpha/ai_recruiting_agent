"use client";

import { useAuth } from "@/contexts/AuthContext";
import { GUEST_ACCESS_CONFIG } from "@/config/guest-access";
import { Eye, ArrowRight, X } from "lucide-react";
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
    <div className="bg-amber-500/10 border-b border-amber-500/20 text-amber-300 px-4 py-2 text-xs flex items-center justify-between transition-all sticky top-16 z-30 backdrop-blur-md">
      <div className="flex items-center space-x-2">
        <Eye className="w-3.5 h-3.5 text-amber-400 shrink-0" />
        <span className="font-medium">
          {GUEST_ACCESS_CONFIG.ui.bannerMessage}
        </span>
      </div>
      <div className="flex items-center space-x-3 shrink-0 ml-4">
        <Link
          href={`/login?redirect=${encodeURIComponent(pathname)}`}
          className="inline-flex items-center gap-1 font-semibold text-amber-200 hover:text-white underline underline-offset-2 transition-colors"
        >
          <span>Sign In</span>
          <ArrowRight className="w-3 h-3" />
        </Link>
        <button
          onClick={() => setDismissed(true)}
          title="Dismiss banner"
          className="p-1 text-amber-400/80 hover:text-amber-200 rounded transition-colors"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
