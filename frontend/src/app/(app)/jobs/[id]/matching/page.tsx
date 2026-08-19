"use client";

import { use } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Check, X, HelpCircle, ThumbsUp } from "lucide-react";
import Link from "next/link";
import { Progress } from "@/components/ui/progress";

export default function CandidateMatchingPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const jobId = resolvedParams.id;

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-6">
      <div className="flex items-center space-x-4">
        <Link href={`/jobs/${jobId}`}>
          <Button variant="ghost" size="icon">
            <ArrowLeft className="w-4 h-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Candidate Matching</h1>
          <p className="text-muted-foreground mt-1">Review AI generated matches for Senior React Engineer.</p>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-6 overflow-hidden">
        {/* Ranked Candidate List */}
        <div className="col-span-1 border rounded-lg flex flex-col bg-card overflow-hidden">
          <div className="p-4 border-b bg-muted/30">
            <h3 className="font-semibold text-sm">Ranked Results (Session: 9f82d)</h3>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className={`p-3 border rounded-md cursor-pointer transition-colors ${i === 1 ? 'border-primary bg-primary/5' : 'hover:bg-muted/50'}`}>
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-semibold text-sm">John Doe {i}</p>
                    <p className="text-xs text-muted-foreground">Software Engineer</p>
                  </div>
                  <Badge variant="secondary" className="text-xs">{95 - i}% Match</Badge>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Match Details & Explainability */}
        <div className="col-span-2 flex flex-col space-y-6 overflow-y-auto pb-6 pr-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex justify-between items-center">
                <span>John Doe 1</span>
                <span className="text-2xl text-primary">94%</span>
              </CardTitle>
              <CardDescription>Hybrid Match Breakdown</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span>Semantic Vector (40%)</span>
                  <span>96%</span>
                </div>
                <Progress value={96} className="h-2" />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span>Skills Match (25%)</span>
                  <span>90%</span>
                </div>
                <Progress value={90} className="h-2" />
              </div>
              
              <div className="grid grid-cols-2 gap-4 mt-6">
                <div className="space-y-2">
                  <h4 className="text-sm font-semibold flex items-center text-green-500"><Check className="w-4 h-4 mr-2"/> Strengths</h4>
                  <ul className="text-sm text-muted-foreground list-disc list-inside">
                    <li>Strong React experience (5+ years)</li>
                    <li>Led migration to Next.js previously</li>
                  </ul>
                </div>
                <div className="space-y-2">
                  <h4 className="text-sm font-semibold flex items-center text-red-500"><X className="w-4 h-4 mr-2"/> Gaps</h4>
                  <ul className="text-sm text-muted-foreground list-disc list-inside">
                    <li>No explicit mention of Tailwind CSS</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Feedback Action Card */}
          <Card className="border-primary/50 shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-lg">Recruiter Feedback</CardTitle>
              <CardDescription>Train the system by rating this match.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-3">
                <Button className="flex-1 bg-green-600 hover:bg-green-700"><ThumbsUp className="w-4 h-4 mr-2"/> Approve</Button>
                <Button className="flex-1" variant="outline"><HelpCircle className="w-4 h-4 mr-2"/> Shortlist</Button>
                <Button className="flex-1" variant="destructive"><X className="w-4 h-4 mr-2"/> Reject</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
