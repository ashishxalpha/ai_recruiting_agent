"use client";

import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Users, History, CheckSquare, ArrowRightLeft, ShieldAlert } from "lucide-react";
import { 
  CoordinationOverviewWidget,
  CoordinationSessionsWidget,
  CoordinationConsensusWidget,
  CoordinationHandoffsWidget,
  CoordinationConflictsWidget
} from "./components/CoordinationWidgets";

export default function CoordinationStudioPage() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Coordination Studio</h1>
        <p className="text-muted-foreground mt-2">
          Engineering portal for multi-agent synchronization, message buses, shared contexts, and conflict resolution.
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col min-h-0">
        <TabsList className="grid w-full grid-cols-5 lg:w-[700px]">
          <TabsTrigger value="overview"><Users className="w-4 h-4 mr-2" /> Overview</TabsTrigger>
          <TabsTrigger value="sessions"><History className="w-4 h-4 mr-2" /> Sessions</TabsTrigger>
          <TabsTrigger value="consensus"><CheckSquare className="w-4 h-4 mr-2" /> Consensus</TabsTrigger>
          <TabsTrigger value="handoffs"><ArrowRightLeft className="w-4 h-4 mr-2" /> Handoffs</TabsTrigger>
          <TabsTrigger value="conflicts"><ShieldAlert className="w-4 h-4 mr-2" /> Conflicts</TabsTrigger>
        </TabsList>
        
        <div className="flex-1 mt-4 min-h-0 overflow-auto pb-4">
          <TabsContent value="overview" className="h-full m-0"><CoordinationOverviewWidget /></TabsContent>
          <TabsContent value="sessions" className="h-full m-0"><CoordinationSessionsWidget /></TabsContent>
          <TabsContent value="consensus" className="h-full m-0"><CoordinationConsensusWidget /></TabsContent>
          <TabsContent value="handoffs" className="h-full m-0"><CoordinationHandoffsWidget /></TabsContent>
          <TabsContent value="conflicts" className="h-full m-0"><CoordinationConflictsWidget /></TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
