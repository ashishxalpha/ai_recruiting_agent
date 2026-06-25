"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Building2, Network, Users, Code2, HeartPulse, GraduationCap, ShieldCheck } from "lucide-react";

export default function OrganizationStudioPage() {
  const roles = [
    { title: "Resume Intelligence Lead", skills: 5, health: "HEALTHY" },
    { title: "Candidate Intelligence Lead", skills: 4, health: "HEALTHY" },
    { title: "Recruiter Assistant Lead", skills: 4, health: "DEGRADED" },
    { title: "Interview Operations Lead", skills: 4, health: "HEALTHY" },
    { title: "Communication Lead", skills: 4, health: "HEALTHY" },
  ];

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Organization Studio</h1>
        <p className="text-muted-foreground mt-2">
          Engineering portal for Managing Roles, Skills, Learning Loops, and Organization Policies.
        </p>
      </div>

      <Tabs defaultValue="dashboard" className="flex-1 flex flex-col">
        <TabsList className="grid w-full grid-cols-7 lg:w-[1000px]">
          <TabsTrigger value="dashboard"><Building2 className="w-4 h-4 mr-2" /> Dashboard</TabsTrigger>
          <TabsTrigger value="roles"><Users className="w-4 h-4 mr-2" /> Roles</TabsTrigger>
          <TabsTrigger value="skills"><Code2 className="w-4 h-4 mr-2" /> Registry</TabsTrigger>
          <TabsTrigger value="explorer"><Network className="w-4 h-4 mr-2" /> Explorer</TabsTrigger>
          <TabsTrigger value="health"><HeartPulse className="w-4 h-4 mr-2" /> Health</TabsTrigger>
          <TabsTrigger value="learning"><GraduationCap className="w-4 h-4 mr-2" /> Learning</TabsTrigger>
          <TabsTrigger value="policies"><ShieldCheck className="w-4 h-4 mr-2" /> Policies</TabsTrigger>
        </TabsList>
        
        {/* Roles Tab */}
        <TabsContent value="roles" className="flex-1 mt-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {roles.map((r) => (
              <Card key={r.title} className="flex flex-col border-l-4 border-l-primary">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <Badge variant={r.health === 'HEALTHY' ? 'default' : 'destructive'}>{r.health}</Badge>
                  </div>
                  <CardTitle className="text-base mt-2">{r.title}</CardTitle>
                </CardHeader>
                <CardContent className="mt-auto border-t pt-3 flex justify-between items-center text-sm text-muted-foreground">
                  <span>Assigned Skills: {r.skills}</span>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Explorer Tab */}
        <TabsContent value="explorer" className="flex-1 mt-6 border rounded-lg p-8 flex flex-col items-center justify-center text-muted-foreground text-center bg-muted/10">
          <Network className="w-12 h-12 mb-4 text-muted" />
          <h2 className="text-lg font-semibold text-foreground mb-2">Skill Dependency Explorer</h2>
          <p className="max-w-xl">
            Visualize the exact pipeline resolving complex workflows:<br/><br/>
            <span className="font-mono text-sm text-primary">Skill → Dependencies → Tools → Memory → Policies</span>
          </p>
        </TabsContent>

        {/* Placeholder Tabs */}
        <TabsContent value="dashboard" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">Organization Goal Dashboard</TabsContent>
        <TabsContent value="skills" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">Skill Registry & Playground</TabsContent>
        <TabsContent value="health" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">Organization Metrics & Health Status</TabsContent>
        <TabsContent value="learning" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">Learning Loop & Memory Consolidation Center</TabsContent>
        <TabsContent value="policies" className="flex-1 mt-6 border rounded-lg p-8 flex items-center justify-center text-muted-foreground">Organization Policy Firewalls & Budgets</TabsContent>
      </Tabs>
    </div>
  );
}
