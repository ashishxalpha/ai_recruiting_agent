"use client";

import { use } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Briefcase, Network, History, ArrowLeft, Play } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

export default function JobDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const jobId = resolvedParams.id;
  const router = useRouter();

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Link href="/jobs">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="w-4 h-4" />
          </Button>
        </Link>
        <div className="flex-1 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Senior React Engineer</h1>
            <p className="text-muted-foreground mt-1 flex items-center space-x-2">
              <span>Job ID: {jobId}</span>
              <span>•</span>
              <Badge variant="outline" className="text-blue-500 border-blue-500/20 bg-blue-500/10">OPEN</Badge>
            </p>
          </div>
          <Button onClick={() => router.push(`/jobs/${jobId}/matching`)}>
            <Play className="w-4 h-4 mr-2" />
            Run Matching Engine
          </Button>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Briefcase className="w-5 h-5 text-muted-foreground" />
              <span>Job Description</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-muted-foreground">Looking for an experienced React engineer to lead our frontend architecture transition to Next.js App Router.</p>
            <div className="flex flex-wrap gap-2">
              <Badge>React</Badge>
              <Badge>Next.js</Badge>
              <Badge>TypeScript</Badge>
              <Badge>Tailwind</Badge>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Network className="w-5 h-5 text-muted-foreground" />
              <span>Embedding Metadata</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex justify-between items-center text-sm border-b pb-2">
              <span className="text-muted-foreground">Model</span>
              <span>text-embedding-3-small</span>
            </div>
            <div className="flex justify-between items-center text-sm border-b pb-2">
              <span className="text-muted-foreground">Vector Dimensions</span>
              <span>1536</span>
            </div>
            <div className="flex justify-between items-center text-sm pb-2">
              <span className="text-muted-foreground">Generated At</span>
              <span>Oct 24, 2026</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <History className="w-5 h-5 text-muted-foreground" />
            <span>Search Sessions (Ranking History)</span>
          </CardTitle>
          <CardDescription>Previous AI matching runs and their recruiter feedback conversion.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="p-4 border rounded-md flex justify-between items-center">
              <div>
                <p className="font-medium text-sm">Session ID: 9f82d...e12a</p>
                <p className="text-xs text-muted-foreground">Run on Oct 25, 2026 • 142 Candidates Matched</p>
              </div>
              <div className="flex space-x-2">
                <Badge variant="secondary">3 Approved</Badge>
                <Badge variant="secondary">1 Shortlisted</Badge>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
