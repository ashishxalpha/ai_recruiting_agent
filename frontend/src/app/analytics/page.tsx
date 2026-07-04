"use client";

import { FunnelWidget } from "./components/FunnelWidget";
import { MatchingWidget } from "./components/MatchingWidget";
import { PlatformHealthWidget } from "./components/PlatformHealthWidget";
import { WorkflowWidget } from "./components/WorkflowWidget";
import { MemoryWidget } from "./components/MemoryWidget";
import { AgentWidget } from "./components/AgentWidget";
import { ToolWidget } from "./components/ToolWidget";
import { OrganizationWidget } from "./components/OrganizationWidget";

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Analytics</h1>
        <p className="text-muted-foreground mt-2">
          Monitor recruiting performance and platform observability.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Row 1: Core Recruiting */}
        <div className="col-span-1 lg:col-span-2">
          <FunnelWidget />
        </div>
        <div className="col-span-1">
          <MatchingWidget />
        </div>

        {/* Row 2: Underlying Engines */}
        <div className="col-span-1">
          <WorkflowWidget />
        </div>
        <div className="col-span-1">
          <MemoryWidget />
        </div>
        <div className="col-span-1">
          <PlatformHealthWidget />
        </div>

        {/* Row 3: Platform & Organization */}
        <div className="col-span-1">
          <AgentWidget />
        </div>
        <div className="col-span-1">
          <ToolWidget />
        </div>
        <div className="col-span-1">
          <OrganizationWidget />
        </div>
      </div>
    </div>
  );
}
