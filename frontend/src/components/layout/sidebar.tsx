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
  Network
} from "lucide-react";
import { cn } from "@/lib/utils";

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

  return (
    <div className="w-64 border-r bg-card/50 flex flex-col h-screen fixed top-0 left-0">
      <div className="p-6 flex items-center space-x-3">
        <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-primary-foreground font-bold">
          RC
        </div>
        <span className="font-semibold text-lg tracking-tight">Recruiting Copilot</span>
      </div>
      
      <nav className="flex-1 px-4 space-y-1">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center space-x-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors",
                isActive 
                  ? "bg-primary/10 text-primary" 
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              )}
            >
              <item.icon className="w-4 h-4" />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>
      
      <div className="p-4 border-t">
        <div className="flex items-center space-x-3 px-3 py-2">
          <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center text-xs">
            AK
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-medium">Ashish K.</span>
            <span className="text-xs text-muted-foreground">Lead Recruiter</span>
          </div>
        </div>
      </div>
    </div>
  );
}
