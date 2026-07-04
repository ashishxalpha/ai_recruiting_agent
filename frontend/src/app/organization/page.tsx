"use client";

import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Building2, Target, Users, Lightbulb, PlayCircle, Shield, BookOpen, LineChart, Activity } from "lucide-react";
import { OrganizationOverviewWidget } from "./components/OrganizationOverviewWidget";
import { OrganizationGoalsWidget } from "./components/OrganizationGoalsWidget";
import { OrganizationRolesWidget } from "./components/OrganizationRolesWidget";
import { OrganizationSkillsWidget } from "./components/OrganizationSkillsWidget";
import { OrganizationExecutionsWidget } from "./components/OrganizationExecutionsWidget";
import { OrganizationPoliciesWidget } from "./components/OrganizationPoliciesWidget";
import { OrganizationLearningWidget } from "./components/OrganizationLearningWidget";
import { OrganizationMetricsWidget } from "./components/OrganizationMetricsWidget";
import { OrganizationActivityWidget } from "./components/OrganizationActivityWidget";

export default function OrganizationStudioPage() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Organization Studio</h1>
        <p className="text-muted-foreground mt-2">
          Engineering portal for Managing Roles, Skills, Learning Loops, and Organization Policies.
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col min-h-0">
        <TabsList className="grid w-full grid-cols-9 lg:w-[1100px]">
          <TabsTrigger value="overview"><Building2 className="w-4 h-4 mr-2" /> Overview</TabsTrigger>
          <TabsTrigger value="goals"><Target className="w-4 h-4 mr-2" /> Goals</TabsTrigger>
          <TabsTrigger value="roles"><Users className="w-4 h-4 mr-2" /> Roles</TabsTrigger>
          <TabsTrigger value="skills"><Lightbulb className="w-4 h-4 mr-2" /> Skills</TabsTrigger>
          <TabsTrigger value="executions"><PlayCircle className="w-4 h-4 mr-2" /> Executions</TabsTrigger>
          <TabsTrigger value="policies"><Shield className="w-4 h-4 mr-2" /> Policies</TabsTrigger>
          <TabsTrigger value="learning"><BookOpen className="w-4 h-4 mr-2" /> Learning</TabsTrigger>
          <TabsTrigger value="metrics"><LineChart className="w-4 h-4 mr-2" /> Metrics</TabsTrigger>
          <TabsTrigger value="activity"><Activity className="w-4 h-4 mr-2" /> Activity</TabsTrigger>
        </TabsList>
        
        <div className="flex-1 mt-4 min-h-0 overflow-auto pb-4">
          <TabsContent value="overview" className="h-full m-0"><OrganizationOverviewWidget /></TabsContent>
          <TabsContent value="goals" className="h-full m-0"><OrganizationGoalsWidget /></TabsContent>
          <TabsContent value="roles" className="h-full m-0"><OrganizationRolesWidget /></TabsContent>
          <TabsContent value="skills" className="h-full m-0"><OrganizationSkillsWidget /></TabsContent>
          <TabsContent value="executions" className="h-full m-0"><OrganizationExecutionsWidget /></TabsContent>
          <TabsContent value="policies" className="h-full m-0"><OrganizationPoliciesWidget /></TabsContent>
          <TabsContent value="learning" className="h-full m-0"><OrganizationLearningWidget /></TabsContent>
          <TabsContent value="metrics" className="h-full m-0"><OrganizationMetricsWidget /></TabsContent>
          <TabsContent value="activity" className="h-full m-0"><OrganizationActivityWidget /></TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
