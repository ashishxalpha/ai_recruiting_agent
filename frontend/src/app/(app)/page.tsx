"use client";

import { DashboardOverviewWidget } from "./components/DashboardOverviewWidget";
import { DashboardHealthWidget } from "./components/DashboardHealthWidget";
import { DashboardActivityWidget } from "./components/DashboardActivityWidget";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">AI Platform Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Unified operational command center for the Autonomous Recruiting AI.
        </p>
      </div>

      <div className="space-y-6">
        <DashboardOverviewWidget />
        
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
          <div className="col-span-4 h-[500px]">
             <DashboardActivityWidget />
          </div>
          <div className="col-span-3 h-[500px]">
             <DashboardHealthWidget />
          </div>
        </div>
      </div>
    </div>
  );
}
