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
  Lock
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
    ? "G"
    : user?.first_name && user?.last_name
    ? `${user.first_name[0]}${user.last_name[0]}`.toUpperCase()
    : (user?.email ? user.email.slice(0, 2).toUpperCase() : "RC");

  const displayName = isGuest
    ? "Guest User"
    : user?.first_name && user?.last_name
    ? `${user.first_name} ${user.last_name}`
    : (user?.email ? user.email.split("@")[0] : "Recruiter");

  const displayRole = isGuest
    ? "Read-only"
    : user?.role
    ? user.role.charAt(0).toUpperCase() + user.role.slice(1)
    : "Member";

  return (
    <div className="w-64 border-r bg-card/50 flex flex-col h-screen fixed top-0 left-0">
      <div className="p-6 flex items-center space-x-3">
        <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-primary-foreground font-bold">
          RC
        </div>
        <span className="font-semibold text-lg tracking-tight">Recruiting Copilot</span>
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
                "flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                isActive 
                  ? "bg-primary/10 text-primary" 
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              )}
            >
              <item.icon className="w-4 h-4" />
              <span>{item.name}</span>
              {isRestricted && (
                <Lock className="w-3.5 h-3.5 ml-auto text-muted-foreground/50" />
              )}
            </Link>
          );
        })}
      </nav>
      
      <div className="p-4 border-t">
        {isGuest ? (
          <div className="space-y-2">
            <div className="flex items-center justify-between px-2 py-1.5 rounded-lg bg-muted/40">
              <div className="flex items-center space-x-2.5 min-w-0">
                <div className="w-8 h-8 rounded-full bg-muted text-muted-foreground font-medium flex items-center justify-center text-xs shrink-0">
                  G
                </div>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-semibold truncate text-foreground">Guest User</span>
                  <span className="text-[10px] text-muted-foreground truncate">Read-only</span>
                </div>
              </div>
              <button
                onClick={() => logout()}
                title="Exit Guest Mode"
                className="p-1.5 rounded-md text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
            <Link
              href={`/login?redirect=${encodeURIComponent(pathname)}`}
              className="flex items-center justify-center space-x-1.5 w-full py-1.5 px-3 text-xs font-medium rounded-md border border-border bg-background hover:bg-muted text-foreground transition-colors"
            >
              <LogIn className="w-3.5 h-3.5" />
              <span>Sign in</span>
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
