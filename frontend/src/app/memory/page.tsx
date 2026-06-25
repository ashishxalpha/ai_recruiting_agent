"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { BrainCircuit, Search, GitGraph, Database, Activity, Clock } from "lucide-react";

export default function MemoryExplorerPage() {
  const memories = [
    { id: "1", type: "SEMANTIC", content: "Strong preference for React experts with >5 years experience.", importance: 0.9, confidence: 0.85, decay: 0.05, namespace: "RECRUITER" },
    { id: "2", type: "EPISODIC", content: "Workflow 9f82d manually paused by recruiter due to low confidence on candidate 12a.", importance: 0.7, confidence: 1.0, decay: 0.2, namespace: "WORKFLOW" },
  ];

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">AI Memory Explorer</h1>
        <p className="text-muted-foreground mt-2">
          Inspect the cognitive state, episodic logs, and semantic knowledge base of the AI Copilot.
        </p>
      </div>

      <Tabs defaultValue="explorer" className="flex-1 flex flex-col">
        <TabsList className="grid w-full grid-cols-6 lg:w-[800px]">
          <TabsTrigger value="explorer"><BrainCircuit className="w-4 h-4 mr-2" /> Explorer</TabsTrigger>
          <TabsTrigger value="timeline"><Clock className="w-4 h-4 mr-2" /> Timeline</TabsTrigger>
          <TabsTrigger value="debugger"><Search className="w-4 h-4 mr-2" /> Debugger</TabsTrigger>
          <TabsTrigger value="graph"><GitGraph className="w-4 h-4 mr-2" /> Graph</TabsTrigger>
          <TabsTrigger value="consolidation"><Database className="w-4 h-4 mr-2" /> Consolidation</TabsTrigger>
          <TabsTrigger value="statistics"><Activity className="w-4 h-4 mr-2" /> Statistics</TabsTrigger>
        </TabsList>
        
        {/* Explorer Tab */}
        <TabsContent value="explorer" className="flex-1 mt-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {memories.map((m) => (
              <Card key={m.id} className="flex flex-col">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <Badge variant={m.type === 'SEMANTIC' ? 'default' : 'secondary'}>{m.type}</Badge>
                    <Badge variant="outline" className="text-xs text-muted-foreground">{m.namespace}</Badge>
                  </div>
                  <CardTitle className="text-base mt-2 line-clamp-2">{m.content}</CardTitle>
                </CardHeader>
                <CardContent className="mt-auto">
                  <div className="grid grid-cols-3 gap-2 text-xs text-center border-t pt-3">
                    <div>
                      <div className="font-semibold text-primary">{m.importance.toFixed(2)}</div>
                      <div className="text-muted-foreground">Importance</div>
                    </div>
                    <div>
                      <div className="font-semibold text-primary">{m.confidence.toFixed(2)}</div>
                      <div className="text-muted-foreground">Confidence</div>
                    </div>
                    <div>
                      <div className="font-semibold text-red-500">{m.decay.toFixed(2)}</div>
                      <div className="text-muted-foreground">Decay</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Timeline Tab */}
        <TabsContent value="timeline" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">
          Memory Timeline Visualization (Chronological episodic events)
        </TabsContent>

        {/* Debugger Tab */}
        <TabsContent value="debugger" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">
          Retrieval Debugger (Test Hybrid Retrieval Policies and view resulting MemoryContext scores)
        </TabsContent>

        {/* Graph Tab */}
        <TabsContent value="graph" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">
          Knowledge Graph Visualization (React Flow representing MemoryNodes and MemoryEdges)
        </TabsContent>

        {/* Consolidation Tab */}
        <TabsContent value="consolidation" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">
          Consolidation Jobs Dashboard (Insight Extraction → Deduplication → Summarization)
        </TabsContent>

        {/* Statistics Tab */}
        <TabsContent value="statistics" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">
          Memory Statistics (Hit Rates, Latency, Drift, Duplication)
        </TabsContent>
      </Tabs>
    </div>
  );
}
