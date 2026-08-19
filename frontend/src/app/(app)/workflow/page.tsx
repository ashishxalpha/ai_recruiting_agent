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

import { useWorkflowList } from '@/hooks/useWorkflow';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowRight, PlayCircle } from "lucide-react";
import Link from "next/link";
import { Skeleton } from "@/components/ui/skeleton";

function WorkflowSelector() {
  const { data: workflowsResponse, isLoading, isError } = useWorkflowList();

  if (isLoading) return <div className="p-10 space-y-4"><Skeleton className="h-20 w-full"/><Skeleton className="h-20 w-full"/></div>;
  if (isError || !workflowsResponse || !workflowsResponse.data) return <div className="p-10 text-destructive">Failed to load recent workflows.</div>;

  const workflows = workflowsResponse.data;

  if (workflows.length === 0) {
    return (
      <div className="space-y-6 p-10 flex-1 flex flex-col justify-center">
        <EmptyState 
          icon={<AlertCircle className="h-8 w-8 text-muted-foreground" />}
          title="No Workflows Found"
          description="There are no recorded LangGraph workflow executions yet. Upload a resume to trigger a workflow."
        />
      </div>
    );
  }

  return (
    <div className="space-y-6 p-10 max-w-4xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Recent Workflows</h1>
        <p className="text-muted-foreground mt-2">
          Select a workflow execution to inspect its LangGraph trace, events, and performance.
        </p>
      </div>

      <div className="grid gap-4">
        {workflows.map(wf => (
          <Card key={wf.id} className="hover:bg-muted/50 transition-colors">
            <CardContent className="flex items-center justify-between p-6">
              <div className="space-y-1">
                <div className="flex items-center space-x-2">
                  <PlayCircle className="w-5 h-5 text-primary" />
                  <span className="font-semibold">{wf.id}</span>
                </div>
                <div className="text-sm text-muted-foreground flex items-center space-x-2">
                  <span>Started: {new Date(wf.started_at).toLocaleString()}</span>
                  <span>•</span>
                  <span>Version: {wf.workflow_version}</span>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <Badge variant={wf.status === "COMPLETED" ? "default" : wf.status === "FAILED" ? "destructive" : "secondary"}>
                  {wf.status}
                </Badge>
                <Link href={`/workflow?id=${wf.id}`}>
                  <Button variant="ghost" size="sm">
                    Inspect <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default function WorkflowWorkspace() {
  const [activeTab, setActiveTab] = useState("overview");
  const searchParams = useSearchParams();
  const workflowId = searchParams.get('id');

  if (!workflowId) {
    return <WorkflowSelector />;
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
