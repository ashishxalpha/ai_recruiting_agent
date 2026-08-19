"use client";

import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Bot, Activity, History, Brain, Wrench, Hammer, Database, Lightbulb, PlaySquare } from "lucide-react";
import { 
  AgentOverviewWidget,
  AgentRuntimeWidget,
  AgentSessionsWidget,
  AgentThoughtsWidget,
  AgentActionsWidget,
  AgentToolsWidget,
  AgentMemoryWidget,
  AgentReflectionWidget,
  AgentReplayWidget 
} from "./components/AgentWidgets";

export default function AgentStudioPage() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Agent Studio</h1>
        <p className="text-muted-foreground mt-2">
          Engineering portal for monitoring agent execution, cognitive traces, and session replays.
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col min-h-0">
        <TabsList className="grid w-full grid-cols-9 lg:w-[1100px]">
          <TabsTrigger value="overview"><Bot className="w-4 h-4 mr-2" /> Overview</TabsTrigger>
          <TabsTrigger value="runtime"><Activity className="w-4 h-4 mr-2" /> Runtime</TabsTrigger>
          <TabsTrigger value="sessions"><History className="w-4 h-4 mr-2" /> Sessions</TabsTrigger>
          <TabsTrigger value="thoughts"><Brain className="w-4 h-4 mr-2" /> Thoughts</TabsTrigger>
          <TabsTrigger value="actions"><Wrench className="w-4 h-4 mr-2" /> Actions</TabsTrigger>
          <TabsTrigger value="tools"><Hammer className="w-4 h-4 mr-2" /> Tools</TabsTrigger>
          <TabsTrigger value="memory"><Database className="w-4 h-4 mr-2" /> Memory</TabsTrigger>
          <TabsTrigger value="reflection"><Lightbulb className="w-4 h-4 mr-2" /> Reflection</TabsTrigger>
          <TabsTrigger value="replay"><PlaySquare className="w-4 h-4 mr-2" /> Replay</TabsTrigger>
        </TabsList>
        
        <div className="flex-1 mt-4 min-h-0 overflow-auto pb-4">
          <TabsContent value="overview" className="h-full m-0"><AgentOverviewWidget /></TabsContent>
          <TabsContent value="runtime" className="h-full m-0"><AgentRuntimeWidget /></TabsContent>
          <TabsContent value="sessions" className="h-full m-0"><AgentSessionsWidget /></TabsContent>
          <TabsContent value="thoughts" className="h-full m-0"><AgentThoughtsWidget /></TabsContent>
          <TabsContent value="actions" className="h-full m-0"><AgentActionsWidget /></TabsContent>
          <TabsContent value="tools" className="h-full m-0"><AgentToolsWidget /></TabsContent>
          <TabsContent value="memory" className="h-full m-0"><AgentMemoryWidget /></TabsContent>
          <TabsContent value="reflection" className="h-full m-0"><AgentReflectionWidget /></TabsContent>
          <TabsContent value="replay" className="h-full m-0"><AgentReplayWidget /></TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
