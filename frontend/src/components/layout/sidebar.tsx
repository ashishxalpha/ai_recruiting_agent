"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  Users, 
  Briefcase, 
  Upload, 
  Activity, 
  BarChart3, 
  MessageSquareHeart, 
  Network,
  LogOut,
  LogIn,
  Lock,
  Compass
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useAuth } from "@/contexts/AuthContext";
import { isRouteAllowedForGuest, GUEST_ACCESS_CONFIG } from "@/config/guest-access";

const NAV_ITEMS = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Candidates", href: "/candidates", icon: Users },
  { name: "Jobs", href: "/jobs", icon: Briefcase },
  { name: "Upload", href: "/upload", icon: Upload },
  { name: "Feedback", href: "/feedback", icon: MessageSquareHeart },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Workflow", href: "/workflow", icon: Network },
  { name: "Activity", href: "/activity", icon: Activity },
  { name: "AI Playground", href: "/playground", icon: Activity },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user, isGuest, logout } = useAuth();

  const initials = isGuest
    ? "GE"
    : user?.first_name && user?.last_name
    ? `${user.first_name[0]}${user.last_name[0]}`.toUpperCase()
    : (user?.email ? user.email.slice(0, 2).toUpperCase() : "RC");

  const displayName = isGuest
    ? "Guest Explorer"
    : user?.first_name && user?.last_name
    ? `${user.first_name} ${user.last_name}`
    : (user?.email ? user.email.split("@")[0] : "Recruiter");

  const displayRole = isGuest
    ? "Guest (Read-Only)"
    : user?.role
    ? user.role.charAt(0).toUpperCase() + user.role.slice(1)
    : "Member";

  return (
    <div className="w-64 border-r bg-card/50 flex flex-col h-screen fixed top-0 left-0">
      <div className="p-6 flex items-center space-x-3">
        <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-primary-foreground font-bold shadow-sm">
          RC
        </div>
        <div className="flex flex-col">
          <span className="font-semibold text-base tracking-tight leading-tight">Recruiting Copilot</span>
          {isGuest && (
            <span className="text-[10px] font-medium text-amber-400 flex items-center gap-1">
              <Compass className="w-2.5 h-2.5" />
              <span>Guest Demo Mode</span>
            </span>
          )}
        </div>
      </div>
      
      <nav className="flex-1 px-4 space-y-1 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
          const isRestricted = isGuest && !isRouteAllowedForGuest(item.href) && GUEST_ACCESS_CONFIG.ui.lockRestrictedNavItems;

          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors group",
                isActive 
                  ? "bg-primary/10 text-primary font-semibold" 
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
                isRestricted && "opacity-75"
              )}
            >
              <item.icon className={cn("w-4 h-4", isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground")} />
              <span className="truncate">{item.name}</span>
              {isRestricted && (
                <span title="Locked in Guest Mode" className="ml-auto flex items-center">
                  <Lock className="w-3.5 h-3.5 text-amber-500/80" />
                </span>
              )}
            </Link>
          );
        })}
      </nav>
      
      <div className="p-4 border-t space-y-2">
        {isGuest ? (
          <div className="space-y-2">
            <div className="flex items-center justify-between px-2.5 py-2 rounded-lg bg-amber-500/10 border border-amber-500/20">
              <div className="flex items-center space-x-2.5 min-w-0">
                <div className="w-7 h-7 rounded-full bg-amber-500/20 text-amber-400 font-bold flex items-center justify-center text-[10px] shrink-0 border border-amber-500/30">
                  GE
                </div>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-semibold text-foreground truncate">Guest Explorer</span>
                  <span className="text-[10px] text-amber-400 font-medium truncate">Read-Only Session</span>
                </div>
              </div>
              <button
                onClick={() => logout()}
                title="Exit Guest Mode"
                className="p-1 rounded text-muted-foreground hover:text-destructive transition-colors"
              >
                <LogOut className="w-3.5 h-3.5" />
              </button>
            </div>
            <Link
              href={`/login?redirect=${encodeURIComponent(pathname)}`}
              className="flex items-center justify-center space-x-2 w-full py-1.5 px-3 text-xs font-semibold rounded-md bg-primary text-primary-foreground hover:bg-primary/90 transition-colors shadow-sm"
            >
              <LogIn className="w-3.5 h-3.5" />
              <span>Sign In Full Account</span>
            </Link>
          </div>
        ) : user ? (
          <div className="flex items-center justify-between px-2 py-1.5 rounded-lg bg-muted/40">
            <div className="flex items-center space-x-2.5 min-w-0">
              <div className="w-8 h-8 rounded-full bg-primary/20 text-primary font-semibold flex items-center justify-center text-xs shrink-0">
                {initials}
              </div>
              <div className="flex flex-col min-w-0">
                <span className="text-xs font-semibold truncate text-foreground">{displayName}</span>
                <span className="text-[10px] text-muted-foreground truncate">{displayRole}</span>
              </div>
            </div>
            <button
              onClick={() => logout()}
              title="Sign out"
              className="p-1.5 rounded-md text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-colors"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <Link
            href="/login"
            className="flex items-center justify-center space-x-2 w-full py-2 px-3 text-xs font-semibold rounded-md bg-primary text-primary-foreground hover:bg-primary/90 transition-colors"
          >
            <LogIn className="w-3.5 h-3.5" />
            <span>Sign In</span>
          </Link>
        )}
      </div>
    </div>
  );
}
