"use client";

import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { WorkflowOverviewWidget } from "./components/WorkflowOverviewWidget";
import { WorkflowTimelineWidget } from "./components/WorkflowTimelineWidget";
import { WorkflowGraphWidget } from "./components/WorkflowGraphWidget";
import { WorkflowNodesWidget } from "./components/WorkflowNodesWidget";
import { WorkflowEventsWidget } from "./components/WorkflowEventsWidget";
import { WorkflowCheckpointsWidget } from "./components/WorkflowCheckpointsWidget";
import { WorkflowStatisticsWidget } from "./components/WorkflowStatisticsWidget";

import { useSearchParams } from 'next/navigation';
import { EmptyState } from "@/components/ui/empty-state";
import { AlertCircle } from "lucide-react";

export default function WorkflowWorkspace() {
  const [activeTab, setActiveTab] = useState("overview");
  const searchParams = useSearchParams();
  const workflowId = searchParams.get('id');

  if (!workflowId) {
    return (
      <div className="space-y-6 p-10 flex-1 flex flex-col justify-center">
        <EmptyState 
          icon={<AlertCircle className="h-8 w-8 text-destructive" />}
          title="No Workflow Selected"
          description="Please provide a valid workflow ID in the URL (e.g. ?id=123e4567-e89b-12d3-a456-426614174000) or navigate here from a job execution link."
        />
      </div>
    );
  }

  return (
    <div className="space-y-6 h-[calc(100vh-8rem)] flex flex-col">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Workflow Workspace</h1>
        <p className="text-muted-foreground mt-2">
          Operational control center for LangGraph execution observability.
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col min-h-0">
        <TabsList className="grid w-full grid-cols-7 lg:w-[800px]">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="graph">Graph</TabsTrigger>
          <TabsTrigger value="timeline">Timeline</TabsTrigger>
          <TabsTrigger value="nodes">Nodes</TabsTrigger>
          <TabsTrigger value="events">Events</TabsTrigger>
          <TabsTrigger value="checkpoints">Checkpoints</TabsTrigger>
          <TabsTrigger value="statistics">Stats</TabsTrigger>
        </TabsList>
        
        <div className="flex-1 mt-4 min-h-0 overflow-auto pb-4">
          <TabsContent value="overview" className="h-full m-0">
            <WorkflowOverviewWidget workflowId={workflowId} />
          </TabsContent>
          
          <TabsContent value="graph" className="h-full m-0">
            <WorkflowGraphWidget workflowId={workflowId} />
          </TabsContent>
          
          <TabsContent value="timeline" className="h-full m-0">
            <WorkflowTimelineWidget workflowId={workflowId} />
          </TabsContent>
          
          <TabsContent value="nodes" className="h-full m-0">
            <WorkflowNodesWidget workflowId={workflowId} />
          </TabsContent>
          
          <TabsContent value="events" className="h-full m-0">
            <WorkflowEventsWidget workflowId={workflowId} />
          </TabsContent>
          
          <TabsContent value="checkpoints" className="h-full m-0">
            <WorkflowCheckpointsWidget workflowId={workflowId} />
          </TabsContent>
          
          <TabsContent value="statistics" className="h-full m-0">
            <WorkflowStatisticsWidget workflowId={workflowId} />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
