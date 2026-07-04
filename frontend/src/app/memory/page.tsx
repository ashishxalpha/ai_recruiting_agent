"use client";

import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { BrainCircuit, Search, GitGraph, Database, Activity, Clock, Link } from "lucide-react";
import { MemoryOverviewWidget } from "./components/MemoryOverviewWidget";
import { MemorySearchWidget } from "./components/MemorySearchWidget";
import { MemoryTimelineWidget } from "./components/MemoryTimelineWidget";
import { MemoryGraphWidget } from "./components/MemoryGraphWidget";
import { MemoryRelationshipsWidget } from "./components/MemoryRelationshipsWidget";
import { MemoryConsolidationsWidget } from "./components/MemoryConsolidationsWidget";
import { MemoryStatisticsWidget } from "./components/MemoryStatisticsWidget";

const DUMMY_MEMORY_ID = "00000000-0000-0000-0000-000000000001";

export default function MemoryExplorerPage() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div className="space-y-6 h-[calc(100vh-8rem)] flex flex-col">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">AI Memory Explorer</h1>
        <p className="text-muted-foreground mt-2">
          Inspect the cognitive state, episodic logs, semantic knowledge base, and retrieval debugger.
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col min-h-0">
        <TabsList className="grid w-full grid-cols-7 lg:w-[900px]">
          <TabsTrigger value="overview"><BrainCircuit className="w-4 h-4 mr-2" /> Overview</TabsTrigger>
          <TabsTrigger value="debugger"><Search className="w-4 h-4 mr-2" /> Debugger</TabsTrigger>
          <TabsTrigger value="timeline"><Clock className="w-4 h-4 mr-2" /> Timeline</TabsTrigger>
          <TabsTrigger value="graph"><GitGraph className="w-4 h-4 mr-2" /> Graph</TabsTrigger>
          <TabsTrigger value="relationships"><Link className="w-4 h-4 mr-2" /> Relations</TabsTrigger>
          <TabsTrigger value="consolidation"><Database className="w-4 h-4 mr-2" /> Consolidate</TabsTrigger>
          <TabsTrigger value="statistics"><Activity className="w-4 h-4 mr-2" /> Statistics</TabsTrigger>
        </TabsList>
        
        <div className="flex-1 mt-4 min-h-0 overflow-auto pb-4">
          <TabsContent value="overview" className="h-full m-0">
            <MemoryOverviewWidget />
          </TabsContent>

          <TabsContent value="debugger" className="h-full m-0">
            <MemorySearchWidget />
          </TabsContent>

          <TabsContent value="timeline" className="h-full m-0">
            <MemoryTimelineWidget memoryId={DUMMY_MEMORY_ID} />
          </TabsContent>

          <TabsContent value="graph" className="h-full m-0">
            <MemoryGraphWidget />
          </TabsContent>

          <TabsContent value="relationships" className="h-full m-0">
            <MemoryRelationshipsWidget memoryId={DUMMY_MEMORY_ID} />
          </TabsContent>

          <TabsContent value="consolidation" className="h-full m-0">
            <MemoryConsolidationsWidget />
          </TabsContent>

          <TabsContent value="statistics" className="h-full m-0">
            <MemoryStatisticsWidget />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
