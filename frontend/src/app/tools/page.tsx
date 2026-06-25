"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Wrench, Network, LayoutGrid, Activity, History, ServerCrash } from "lucide-react";

export default function ToolManagementPage() {
  const tools = [
    { id: "read_file", name: "Read File", provider: "mcp_filesystem", category: "FILESYSTEM", capabilities: ["filesystem"], target: "MCP", status: "healthy" },
    { id: "query_db", name: "Query Postgres", provider: "mcp_postgres", category: "DATABASE", capabilities: ["database"], target: "MCP", status: "healthy" },
    { id: "get_repo", name: "Get Repository", provider: "mcp_github", category: "DEVELOPMENT", capabilities: ["github"], target: "MCP", status: "degraded" },
  ];

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Enterprise Tool Platform</h1>
        <p className="text-muted-foreground mt-2">
          Manage integrations, monitor health, test capabilities, and audit tool executions across Local and MCP providers.
        </p>
      </div>

      <Tabs defaultValue="dashboard" className="flex-1 flex flex-col">
        <TabsList className="grid w-full grid-cols-6 lg:w-[800px]">
          <TabsTrigger value="dashboard"><LayoutGrid className="w-4 h-4 mr-2" /> Dashboard</TabsTrigger>
          <TabsTrigger value="providers"><Network className="w-4 h-4 mr-2" /> Providers</TabsTrigger>
          <TabsTrigger value="capabilities"><Wrench className="w-4 h-4 mr-2" /> Capabilities</TabsTrigger>
          <TabsTrigger value="playground"><Activity className="w-4 h-4 mr-2" /> Playground</TabsTrigger>
          <TabsTrigger value="inspector"><History className="w-4 h-4 mr-2" /> Inspector</TabsTrigger>
          <TabsTrigger value="health"><ServerCrash className="w-4 h-4 mr-2" /> Health</TabsTrigger>
        </TabsList>
        
        {/* Dashboard Tab */}
        <TabsContent value="dashboard" className="flex-1 mt-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {tools.map((t) => (
              <Card key={t.id} className="flex flex-col">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <Badge variant={t.status === 'healthy' ? 'default' : 'destructive'}>{t.status}</Badge>
                    <Badge variant="outline" className="text-xs text-muted-foreground">{t.target}</Badge>
                  </div>
                  <CardTitle className="text-base mt-2">{t.name}</CardTitle>
                </CardHeader>
                <CardContent className="mt-auto border-t pt-3 flex justify-between items-center text-sm text-muted-foreground">
                  <span>{t.provider}</span>
                  <span className="font-mono text-xs">{t.category}</span>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Providers Tab */}
        <TabsContent value="providers" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">
          Provider Management (Manage MCP Connections, stdio vs SSE settings)
        </TabsContent>

        {/* Capabilities Tab */}
        <TabsContent value="capabilities" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">
          Capability Explorer (Capability → Provider → Tool → Operation)
        </TabsContent>

        {/* Playground Tab */}
        <TabsContent value="playground" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">
          Tool Playground (Manual Execution with schema validation & tracing)
        </TabsContent>

        {/* Inspector Tab */}
        <TabsContent value="inspector" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">
          Execution Inspector (Audit inputs, outputs, errors, and traces)
        </TabsContent>
        
        {/* Health Tab */}
        <TabsContent value="health" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">
          Health & Cache Monitor (Latency, Errors, Connection Drops)
        </TabsContent>
      </Tabs>
    </div>
  );
}
