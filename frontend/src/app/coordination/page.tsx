"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Activity, Mail, Combine, Network, Map, Bug, MessagesSquare } from "lucide-react";

export default function CoordinationStudioPage() {
  const goals = [
    { id: "goal_1", description: "Evaluate 5 Candidates for Staff Engineer", status: "EXECUTING", delegated_to: 3, strategy: "Parallel" },
    { id: "goal_2", description: "Source outbound profiles", status: "COMPLETED", delegated_to: 2, strategy: "Sequential" },
  ];

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Coordination Studio</h1>
        <p className="text-muted-foreground mt-2">
          Engineering portal for multi-agent synchronization, message buses, shared contexts, and conflict resolution.
        </p>
      </div>

      <Tabs defaultValue="dashboard" className="flex-1 flex flex-col">
        <TabsList className="grid w-full grid-cols-7 lg:w-[1000px]">
          <TabsTrigger value="dashboard"><Activity className="w-4 h-4 mr-2" /> Dashboard</TabsTrigger>
          <TabsTrigger value="debugger"><Bug className="w-4 h-4 mr-2" /> Debugger</TabsTrigger>
          <TabsTrigger value="messages"><Mail className="w-4 h-4 mr-2" /> Mailbox</TabsTrigger>
          <TabsTrigger value="delegation"><Map className="w-4 h-4 mr-2" /> Delegation</TabsTrigger>
          <TabsTrigger value="consensus"><Combine className="w-4 h-4 mr-2" /> Consensus</TabsTrigger>
          <TabsTrigger value="context"><Network className="w-4 h-4 mr-2" /> Context</TabsTrigger>
          <TabsTrigger value="conflicts"><MessagesSquare className="w-4 h-4 mr-2" /> Conflicts</TabsTrigger>
        </TabsList>
        
        {/* Dashboard Tab */}
        <TabsContent value="dashboard" className="flex-1 mt-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {goals.map((g) => (
              <Card key={g.id} className="flex flex-col border-l-4 border-l-primary">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <Badge variant={g.status === 'EXECUTING' ? 'default' : 'secondary'}>{g.status}</Badge>
                    <Badge variant="outline" className="text-xs text-muted-foreground">{g.strategy}</Badge>
                  </div>
                  <CardTitle className="text-base mt-2">{g.description}</CardTitle>
                </CardHeader>
                <CardContent className="mt-auto border-t pt-3 flex justify-between items-center text-sm text-muted-foreground">
                  <span>Delegated Tasks: {g.delegated_to}</span>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Debugger Tab */}
        <TabsContent value="debugger" className="flex-1 mt-6 border rounded-lg p-8 flex flex-col items-center justify-center text-muted-foreground text-center bg-muted/10">
          <Bug className="w-12 h-12 mb-4 text-muted" />
          <h2 className="text-lg font-semibold text-foreground mb-2">Coordination Debugger</h2>
          <p className="max-w-xl">
            Trace the exact execution lifecycle across the cluster:<br/><br/>
            <span className="font-mono text-sm text-primary">Goal → Delegation → Messages → Votes → Consensus → Conflict → Resolution</span>
          </p>
          <p className="mt-4 text-sm">Select an active Coordination Session to begin tracing.</p>
        </TabsContent>

        {/* Placeholder Tabs */}
        <TabsContent value="messages" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">Agent Communication Bus & Mailbox Explorer</TabsContent>
        <TabsContent value="delegation" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">Goal Dependency Graph & Delegation Engine</TabsContent>
        <TabsContent value="consensus" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">Consensus Engine Evaluator</TabsContent>
        <TabsContent value="context" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">Shared Context Snapshot Viewer</TabsContent>
        <TabsContent value="conflicts" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">Conflict Resolution Center</TabsContent>
      </Tabs>
    </div>
  );
}
