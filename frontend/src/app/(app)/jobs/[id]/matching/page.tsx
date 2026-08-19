"use client";

import { use } from "react";
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Check, X, HelpCircle, ThumbsUp, CheckCircle, Search } from "lucide-react";
import Link from "next/link";
import { Progress } from "@/components/ui/progress";
import { useJobMatches, useJobDetails } from "@/hooks/useJobs";
import { Skeleton } from "@/components/ui/skeleton";
import { ErrorState } from "@/components/ui/error-state";
import { EmptyState } from "@/components/ui/empty-state";

export default function CandidateMatchingPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const jobId = resolvedParams.id;
  const [selectedMatchIdx, setSelectedMatchIdx] = useState<number>(0);

  const { data: jobDetails, isLoading: isJobLoading } = useJobDetails(jobId);
  const { data: matches, isLoading: isMatchesLoading, isError: isMatchesError } = useJobMatches(jobId);

  if (isMatchesLoading || isJobLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-1/3" />
        <Skeleton className="h-[500px] w-full" />
      </div>
    );
  }

  if (isMatchesError) {
    return <ErrorState title="Failed to load match results" />;
  }

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
          <p className="text-muted-foreground mt-1">Review AI generated matches for {jobDetails?.title || "this role"}.</p>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-6 overflow-hidden">
        {/* Ranked Candidate List */}
        <div className="col-span-1 border rounded-lg flex flex-col bg-card overflow-hidden">
          <div className="p-4 border-b bg-muted/30">
            <h3 className="font-semibold text-sm">Ranked Results</h3>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {matches && matches.length > 0 ? (
              matches.map((match: any, i: number) => {
                const isSelected = selectedMatchIdx === i;
                return (
                  <div 
                    key={match.id} 
                    onClick={() => setSelectedMatchIdx(i)}
                    className={`p-3 border rounded-md cursor-pointer transition-colors ${isSelected ? 'border-primary bg-primary/5' : 'hover:bg-muted/50'}`}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-semibold text-sm">{match.first_name} {match.last_name}</p>
                        <p className="text-xs text-muted-foreground truncate w-32">{match.email || "No email"}</p>
                      </div>
                      <Badge variant={match.final_score > 0.8 ? "default" : "secondary"} className="text-xs">
                        {(match.final_score * 100).toFixed(0)}% Match
                      </Badge>
                    </div>
                  </div>
                );
              })
            ) : (
              <EmptyState 
                icon={<Search className="w-6 h-6" />} 
                title="No Matches" 
                description="Run the matcher from the job page." 
              />
            )}
          </div>
        </div>

        {/* Match Details & Explainability */}
        <div className="col-span-2 flex flex-col space-y-6 overflow-y-auto pb-6 pr-2">
          {matches && matches.length > 0 && matches[selectedMatchIdx] ? (
            <>
              <Card>
                <CardHeader>
                  <CardTitle className="flex justify-between items-center">
                    <span>{matches[selectedMatchIdx].first_name} {matches[selectedMatchIdx].last_name}</span>
                    <span className="text-2xl text-primary">{(matches[selectedMatchIdx].final_score * 100).toFixed(0)}%</span>
                  </CardTitle>
                  <CardDescription>Hybrid Match Breakdown</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span>Semantic Vector (40%)</span>
                      <span>{(matches[selectedMatchIdx].semantic_score * 100).toFixed(0)}%</span>
                    </div>
                    <Progress value={matches[selectedMatchIdx].semantic_score * 100} className="h-2" />
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span>AI Skills Match (60%)</span>
                      <span>{(matches[selectedMatchIdx].skills_score * 100).toFixed(0)}%</span>
                    </div>
                    <Progress value={matches[selectedMatchIdx].skills_score * 100} className="h-2" />
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span>AI Experience Match</span>
                      <span>{(matches[selectedMatchIdx].experience_score * 100).toFixed(0)}%</span>
                    </div>
                    <Progress value={matches[selectedMatchIdx].experience_score * 100} className="h-2" />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 mt-6">
                    <div className="space-y-2">
                      <h4 className="text-sm font-semibold flex items-center text-green-500"><Check className="w-4 h-4 mr-2"/> Strengths</h4>
                      <ul className="text-sm text-muted-foreground list-disc list-inside">
                        {matches[selectedMatchIdx].strengths && matches[selectedMatchIdx].strengths.length > 0 ? (
                          matches[selectedMatchIdx].strengths.map((s: string, idx: number) => (
                            <li key={idx} className="leading-tight mb-1">{s}</li>
                          ))
                        ) : (
                          <li>No specific strengths highlighted</li>
                        )}
                      </ul>
                    </div>
                    <div className="space-y-2">
                      <h4 className="text-sm font-semibold flex items-center text-red-500"><X className="w-4 h-4 mr-2"/> Gaps</h4>
                      <ul className="text-sm text-muted-foreground list-disc list-inside">
                        {matches[selectedMatchIdx].gaps && matches[selectedMatchIdx].gaps.length > 0 ? (
                          matches[selectedMatchIdx].gaps.map((s: string, idx: number) => (
                            <li key={idx} className="leading-tight mb-1">{s}</li>
                          ))
                        ) : (
                          <li>No specific gaps highlighted</li>
                        )}
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Feedback Action Card */}
              <Card className="border-primary/50 shadow-sm mt-auto">
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
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center border rounded-lg bg-card">
              <EmptyState 
                icon={<Search className="w-8 h-8" />} 
                title="No match details" 
                description="Run the matcher or select a candidate to view details." 
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
