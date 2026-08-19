"use client";

import { use } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Briefcase, Network, History, ArrowLeft, Play, Users, BarChart3, CheckCircle, FileText, Settings } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { 
  useJobDetails,
  useJobCandidates,
  useJobMatches,
  useJobWorkflow,
  useJobAnalytics,
  useJobFeedback,
  useJobDocuments,
  useJobHistory
} from "@/hooks/useJobs";
import { ErrorState } from "@/components/ui/error-state";
import { Skeleton } from "@/components/ui/skeleton";

import { EmptyState } from "@/components/ui/empty-state";

// Isolated Tab Components for Lazy Loading

function CandidatesTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useJobCandidates(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load candidates" />;
  return (
    <Card>
      <CardHeader><CardTitle>Applied Candidates</CardTitle></CardHeader>
      <CardContent>
        {data && data.length > 0 ? (
          <pre className="text-xs bg-muted p-4 rounded-md">{JSON.stringify(data, null, 2)}</pre>
        ) : (
          <EmptyState 
            icon={<Users className="w-8 h-8" />} 
            title="No Candidates Found" 
            description="There are no candidates associated with this job requirement yet." 
          />
        )}
      </CardContent>
    </Card>
  );
}

import { useRouter } from "next/navigation";
import { useState } from "react";
import { toast } from "sonner";
import { Loader2 } from "lucide-react";

function MatchingTab({ id }: { id: string }) {
  const { data, isLoading, isError, refetch } = useJobMatches(id);
  const router = useRouter();
  const [isRunning, setIsRunning] = useState(false);

  const handleRunMatch = async () => {
    setIsRunning(true);
    toast.info("Running AI Semantic Matcher...");
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/v1/jobs/${id}/match`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });
      if (!res.ok) throw new Error("Failed to run match");
      toast.success("Matching complete!");
      refetch();
      router.push(`/jobs/${id}/matching`);
    } catch (e) {
      toast.error("Failed to execute matching");
    } finally {
      setIsRunning(false);
    }
  };

  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load matches" />;
  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>Semantic Matching Results</CardTitle>
          <div className="flex gap-2">
            <Button variant="default" size="sm" onClick={handleRunMatch} disabled={isRunning}>
              {isRunning ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Play className="w-4 h-4 mr-2" />}
              {isRunning ? "Running..." : "Run AI Matcher"}
            </Button>
            <Link href={`/jobs/${id}/matching`}>
              <Button variant="outline" size="sm">View Details</Button>
            </Link>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {data && data.length > 0 ? (
          <pre className="text-xs bg-muted p-4 rounded-md overflow-y-auto max-h-96">{JSON.stringify(data, null, 2)}</pre>
        ) : (
          <EmptyState 
            icon={<CheckCircle className="w-8 h-8" />} 
            title="No Matches Found" 
            description="Run the AI matcher to find the best candidates for this role."
          />
        )}
      </CardContent>
    </Card>
  );
}

function WorkflowTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useJobWorkflow(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load workflow data" />;
  return (
    <Card>
      <CardHeader><CardTitle>Recruitment Workflow</CardTitle></CardHeader>
      <CardContent>
        {data && data.length > 0 ? (
          <pre className="text-xs bg-muted p-4 rounded-md">{JSON.stringify(data, null, 2)}</pre>
        ) : (
          <EmptyState 
            icon={<Settings className="w-8 h-8" />} 
            title="No Workflow Data" 
            description="There are no active or historical workflows for this job." 
          />
        )}
      </CardContent>
    </Card>
  );
}

function AnalyticsTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useJobAnalytics(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load analytics" />;
  return (
    <Card>
      <CardHeader><CardTitle>Recruitment Analytics</CardTitle></CardHeader>
      <CardContent>
        {data && data.total_candidates > 0 ? (
          <pre className="text-xs bg-muted p-4 rounded-md">{JSON.stringify(data, null, 2)}</pre>
        ) : (
          <EmptyState 
            icon={<BarChart3 className="w-8 h-8" />} 
            title="No Analytics Data" 
            description="Insufficient data to generate analytics for this job." 
          />
        )}
      </CardContent>
    </Card>
  );
}

function FeedbackTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useJobFeedback(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load feedback" />;
  return (
    <Card>
      <CardHeader><CardTitle>Recruiter Feedback</CardTitle></CardHeader>
      <CardContent>
        {data && data.length > 0 ? (
          <pre className="text-xs bg-muted p-4 rounded-md">{JSON.stringify(data, null, 2)}</pre>
        ) : (
          <EmptyState 
            icon={<History className="w-8 h-8" />} 
            title="No Feedback Yet" 
            description="You haven't provided any feedback on candidate matches." 
          />
        )}
      </CardContent>
    </Card>
  );
}

function DocumentsTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useJobDocuments(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load documents" />;
  return (
    <Card>
      <CardHeader><CardTitle>Job Documents</CardTitle></CardHeader>
      <CardContent>
        {data && data.length > 0 ? (
          <pre className="text-xs bg-muted p-4 rounded-md">{JSON.stringify(data, null, 2)}</pre>
        ) : (
          <EmptyState 
            icon={<FileText className="w-8 h-8" />} 
            title="No Documents" 
            description="No supplementary documents have been uploaded for this job." 
          />
        )}
      </CardContent>
    </Card>
  );
}

function HistoryTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useJobHistory(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load history" />;
  return (
    <Card>
      <CardHeader><CardTitle>Search Sessions (Ranking History)</CardTitle></CardHeader>
      <CardContent>
        {data && data.length > 0 ? (
          <pre className="text-xs bg-muted p-4 rounded-md">{JSON.stringify(data, null, 2)}</pre>
        ) : (
          <EmptyState 
            icon={<History className="w-8 h-8" />} 
            title="No History" 
            description="No search or matching sessions have been recorded." 
          />
        )}
      </CardContent>
    </Card>
  );
}

export default function JobDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const jobId = resolvedParams.id;

  const { data: job, isLoading, isError, refetch } = useJobDetails(jobId);

  if (isLoading) {
    return (
      <div className="space-y-6 animate-pulse">
        <Skeleton className="h-20 w-3/4" />
        <Skeleton className="h-[400px] w-full" />
      </div>
    );
  }

  if (isError || !job) {
    return <ErrorState 
      title="Job not found"
      message="We could not retrieve the details for this job requirement."
      onRetry={() => refetch()}
    />;
  }

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
            <h1 className="text-3xl font-bold tracking-tight">{job.title}</h1>
            <p className="text-muted-foreground mt-1 flex items-center space-x-2">
              <span>{job.department || "General"}</span>
              <span>•</span>
              <span>{job.location || "Remote"}</span>
              <span>•</span>
              <span>ID: {jobId.substring(0, 8)}...</span>
              <span>•</span>
              <Badge variant="outline" className="text-primary border-primary/20 bg-primary/10">
                {job.status.replace("_", " ")}
              </Badge>
            </p>
          </div>
        </div>
      </div>

      <Tabs defaultValue="overview">
        <TabsList className="mb-4 flex-wrap h-auto">
          <TabsTrigger value="overview"><Briefcase className="w-4 h-4 mr-2"/> Overview</TabsTrigger>
          <TabsTrigger value="candidates"><Users className="w-4 h-4 mr-2"/> Candidates</TabsTrigger>
          <TabsTrigger value="matching"><CheckCircle className="w-4 h-4 mr-2"/> Matching</TabsTrigger>
          <TabsTrigger value="workflow"><Settings className="w-4 h-4 mr-2"/> Workflow</TabsTrigger>
          <TabsTrigger value="analytics"><BarChart3 className="w-4 h-4 mr-2"/> Analytics</TabsTrigger>
          <TabsTrigger value="feedback"><History className="w-4 h-4 mr-2"/> Feedback</TabsTrigger>
          <TabsTrigger value="documents"><FileText className="w-4 h-4 mr-2"/> Documents</TabsTrigger>
          <TabsTrigger value="history"><History className="w-4 h-4 mr-2"/> History</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Briefcase className="w-5 h-5 text-muted-foreground" />
                  <span>Job Description</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-sm whitespace-pre-wrap">{job.description}</p>
                {job.experience_required && (
                  <div className="mt-4 border-t pt-4">
                    <h4 className="text-sm font-semibold mb-2">Experience Required</h4>
                    <p className="text-sm text-muted-foreground">{job.experience_required}</p>
                  </div>
                )}
                {job.skills_required && job.skills_required.length > 0 && (
                  <div className="mt-4 border-t pt-4">
                    <h4 className="text-sm font-semibold mb-2">Required Skills</h4>
                    <div className="flex flex-wrap gap-2">
                      {job.skills_required.map(skill => (
                        <Badge key={skill}>{skill}</Badge>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Network className="w-5 h-5 text-muted-foreground" />
                  <span>Hiring Context</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between items-center text-sm border-b pb-2">
                  <span className="text-muted-foreground">Hiring Manager</span>
                  <span className="font-medium">{job.hiring_manager || "Unassigned"}</span>
                </div>
                <div className="flex justify-between items-center text-sm border-b pb-2">
                  <span className="text-muted-foreground">Employment Type</span>
                  <span className="font-medium">{job.employment_type || "Full-time"}</span>
                </div>
                <div className="flex justify-between items-center text-sm pb-2">
                  <span className="text-muted-foreground">Created At</span>
                  <span className="font-medium">{new Date(job.created_at).toLocaleDateString()}</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="candidates">
          <CandidatesTab id={jobId} />
        </TabsContent>
        <TabsContent value="matching">
          <MatchingTab id={jobId} />
        </TabsContent>
        <TabsContent value="workflow">
          <WorkflowTab id={jobId} />
        </TabsContent>
        <TabsContent value="analytics">
          <AnalyticsTab id={jobId} />
        </TabsContent>
        <TabsContent value="feedback">
          <FeedbackTab id={jobId} />
        </TabsContent>
        <TabsContent value="documents">
          <DocumentsTab id={jobId} />
        </TabsContent>
        <TabsContent value="history">
          <HistoryTab id={jobId} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
