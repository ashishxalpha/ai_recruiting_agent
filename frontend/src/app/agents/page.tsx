"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Activity, Brain, History, ListTree, Play, PlaySquare, Settings2, SkipForward } from "lucide-react";

export default function AgentStudioPage() {
  const agents = [
    { id: "eval_agent_1", name: "Evaluation Specialist", state: "RUNNING", mode: "NORMAL", latency: "1.2s", cost: "$0.04" },
    { id: "sourcing_agent_2", name: "Outbound Sourcer", state: "PAUSED", mode: "SIMULATION", latency: "0.8s", cost: "$0.01" },
    { id: "matcher_3", name: "Relevancy Matcher", state: "TERMINATED", mode: "REPLAY", latency: "0.1s", cost: "$0.00" },
  ];

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Agent Studio</h1>
        <p className="text-muted-foreground mt-2">
          Engineering portal for monitoring agent execution, cognitive traces, and session replays.
        </p>
      </div>

      <Tabs defaultValue="dashboard" className="flex-1 flex flex-col">
        <TabsList className="grid w-full grid-cols-6 lg:w-[800px]">
          <TabsTrigger value="dashboard"><Activity className="w-4 h-4 mr-2" /> Dashboard</TabsTrigger>
          <TabsTrigger value="registry"><Settings2 className="w-4 h-4 mr-2" /> Registry</TabsTrigger>
          <TabsTrigger value="trace"><Brain className="w-4 h-4 mr-2" /> Trace Viewer</TabsTrigger>
          <TabsTrigger value="inspector"><ListTree className="w-4 h-4 mr-2" /> Inspector</TabsTrigger>
          <TabsTrigger value="sessions"><History className="w-4 h-4 mr-2" /> Sessions</TabsTrigger>
          <TabsTrigger value="replay"><PlaySquare className="w-4 h-4 mr-2" /> Replay</TabsTrigger>
        </TabsList>
        
        {/* Dashboard Tab */}
        <TabsContent value="dashboard" className="flex-1 mt-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {agents.map((a) => (
              <Card key={a.id} className="flex flex-col border-l-4 border-l-primary">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <Badge variant={a.state === 'RUNNING' ? 'default' : a.state === 'PAUSED' ? 'secondary' : 'destructive'}>
                      {a.state}
                    </Badge>
                    <Badge variant="outline" className="text-xs text-muted-foreground">{a.mode}</Badge>
                  </div>
                  <CardTitle className="text-lg mt-3">{a.name}</CardTitle>
                </CardHeader>
                <CardContent className="mt-auto border-t pt-3 flex justify-between items-center text-sm text-muted-foreground">
                  <span>Latency: {a.latency}</span>
                  <span className="font-mono text-xs">Cost: {a.cost}</span>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Trace Viewer Tab */}
        <TabsContent value="trace" className="flex-1 mt-6 border rounded-lg p-8 flex flex-col items-center justify-center text-muted-foreground text-center">
          <Brain className="w-12 h-12 mb-4 text-muted" />
          <h2 className="text-lg font-semibold text-foreground mb-2">Cognitive Trace Viewer</h2>
          <p className="max-w-md">
            Observe → Retrieve → Reason → Plan → Execute → Reflect → Learn
          </p>
          <p className="mt-4 text-sm">Select an active agent to stream the ReasoningTrace over SSE.</p>
        </TabsContent>

        {/* Replay Tab */}
        <TabsContent value="replay" className="flex-1 mt-6 border rounded-lg p-8 flex flex-col items-center justify-center text-muted-foreground text-center bg-muted/10">
          <PlaySquare className="w-12 h-12 mb-4 text-muted" />
          <h2 className="text-lg font-semibold text-foreground mb-2">Session Replay Engine</h2>
          <p className="max-w-md mb-6">
            Time-travel through historic sessions frame-by-frame using cached SessionSnapshots and mocked Execution Mode.
          </p>
          <div className="flex space-x-4">
            <Badge variant="outline" className="p-2 cursor-pointer hover:bg-secondary"><SkipForward className="w-4 h-4" /></Badge>
            <Badge variant="outline" className="p-2 cursor-pointer hover:bg-secondary"><Play className="w-4 h-4" /></Badge>
          </div>
        </TabsContent>

        {/* Placeholder Tabs */}
        <TabsContent value="registry" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">Template & Plugin Registry</TabsContent>
        <TabsContent value="inspector" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">Live Agent State Inspector</TabsContent>
        <TabsContent value="sessions" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">Session History Explorer</TabsContent>
      </Tabs>
    </div>
  );
}
