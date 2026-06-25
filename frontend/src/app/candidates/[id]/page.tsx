"use client";

import { use } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Brain, FileText, CheckCircle2, History, Network, ArrowLeft, Star, FileQuestion } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function CandidateDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const candidateId = resolvedParams.id;

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Link href="/candidates">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="w-4 h-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">John Doe</h1>
          <p className="text-muted-foreground mt-1 flex items-center space-x-2">
            <span>Senior Software Engineer</span>
            <span>•</span>
            <span>Candidate ID: {candidateId}</span>
            <span>•</span>
            <Badge variant="outline" className="text-green-500 border-green-500/20 bg-green-500/10">HIRED</Badge>
          </p>
        </div>
      </div>

      <Tabs defaultValue="profile">
        <TabsList className="mb-4">
          <TabsTrigger value="profile"><FileText className="w-4 h-4 mr-2"/> Profile</TabsTrigger>
          <TabsTrigger value="extraction"><Brain className="w-4 h-4 mr-2"/> Extraction</TabsTrigger>
          <TabsTrigger value="evaluation"><Star className="w-4 h-4 mr-2"/> Evaluation</TabsTrigger>
          <TabsTrigger value="embeddings"><Network className="w-4 h-4 mr-2"/> Embeddings</TabsTrigger>
          <TabsTrigger value="matching"><CheckCircle2 className="w-4 h-4 mr-2"/> Matching History</TabsTrigger>
          <TabsTrigger value="feedback"><FileQuestion className="w-4 h-4 mr-2"/> Feedback</TabsTrigger>
          <TabsTrigger value="timeline"><History className="w-4 h-4 mr-2"/> Ground Truth</TabsTrigger>
        </TabsList>

        <TabsContent value="profile" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Professional Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">Experienced software engineer with a focus on React, Node.js, and Python. Proven track record of scaling high-traffic applications.</p>
            </CardContent>
          </Card>
          
          <div className="grid grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Skills</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  <Badge>React</Badge>
                  <Badge>TypeScript</Badge>
                  <Badge>Python</Badge>
                  <Badge>AWS</Badge>
                  <Badge>PostgreSQL</Badge>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Experience</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h4 className="text-sm font-semibold">Senior Engineer at TechCorp</h4>
                  <p className="text-xs text-muted-foreground">2020 - Present</p>
                </div>
                <div>
                  <h4 className="text-sm font-semibold">Engineer at WebSys</h4>
                  <p className="text-xs text-muted-foreground">2018 - 2020</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="extraction">
          <Card>
            <CardHeader>
              <CardTitle>AI Extraction Metadata</CardTitle>
              <CardDescription>Raw JSON extracted by the pipeline.</CardDescription>
            </CardHeader>
            <CardContent>
              <pre className="bg-muted p-4 rounded-md text-xs font-mono">
                {JSON.stringify({ "model": "gpt-4o", "confidence": 0.98, "tokens_used": 1450 }, null, 2)}
              </pre>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="evaluation">
          <Card>
            <CardHeader>
              <CardTitle>Profile Quality Evaluation</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">Overall Profile Quality: 95%</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="embeddings">
          <Card>
            <CardHeader>
              <CardTitle>Vector Embeddings</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">Generated using: text-embedding-3-small</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="matching">
          <Card>
            <CardHeader>
              <CardTitle>Job Match History</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">Matched against 3 jobs.</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="feedback">
          <Card>
            <CardHeader>
              <CardTitle>Recruiter Feedback</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">Feedback log will appear here.</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="timeline">
          <Card>
            <CardHeader>
              <CardTitle>Ground Truth Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-300 before:to-transparent">
                 {/* Timeline items would go here */}
                 <p className="text-center text-sm text-muted-foreground relative z-10">Timeline Events Flow</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
