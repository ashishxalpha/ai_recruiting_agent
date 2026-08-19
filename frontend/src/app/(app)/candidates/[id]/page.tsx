"use client";

import { use } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Brain, FileText, CheckCircle2, History, Network, ArrowLeft, Star, FileQuestion, Activity, Loader2 } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { 
  useCandidateDetails, 
  useCandidateWorkflow,
  useCandidateEvaluation,
  useCandidateEmbeddings,
  useCandidateMatches,
  useCandidateFeedback,
  useCandidateMemory,
  useCandidateDocuments
} from "@/hooks/useCandidates";
import { ErrorState } from "@/components/ui/error-state";
import { Skeleton } from "@/components/ui/skeleton";

// Isolated Tab Components for Lazy Loading

function WorkflowTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useCandidateWorkflow(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load workflow data" />;
  return (
    <Card>
      <CardHeader><CardTitle>Workflow Execution</CardTitle></CardHeader>
      <CardContent><pre className="text-xs bg-muted p-4 rounded-md">{JSON.stringify(data, null, 2)}</pre></CardContent>
    </Card>
  );
}

function EvaluationTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useCandidateEvaluation(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load evaluation data" />;
  return (
    <Card>
      <CardHeader><CardTitle>AI Evaluation</CardTitle></CardHeader>
      <CardContent><pre className="text-xs bg-muted p-4 rounded-md">{JSON.stringify(data, null, 2)}</pre></CardContent>
    </Card>
  );
}

function EmbeddingsTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useCandidateEmbeddings(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load embeddings data" />;
  return (
    <Card>
      <CardHeader><CardTitle>Vector Embeddings</CardTitle></CardHeader>
      <CardContent><pre className="text-xs bg-muted p-4 rounded-md">{JSON.stringify(data, null, 2)}</pre></CardContent>
    </Card>
  );
}

function MatchingTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useCandidateMatches(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load matches" />;
  return (
    <Card>
      <CardHeader><CardTitle>Match History</CardTitle></CardHeader>
      <CardContent><pre className="text-xs bg-muted p-4 rounded-md">{JSON.stringify(data, null, 2)}</pre></CardContent>
    </Card>
  );
}

function FeedbackTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useCandidateFeedback(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load feedback" />;
  return (
    <Card>
      <CardHeader><CardTitle>Recruiter Feedback</CardTitle></CardHeader>
      <CardContent><pre className="text-xs bg-muted p-4 rounded-md">{JSON.stringify(data, null, 2)}</pre></CardContent>
    </Card>
  );
}

function MemoryTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useCandidateMemory(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load memory" />;
  return (
    <Card>
      <CardHeader><CardTitle>Memory & Ground Truth</CardTitle></CardHeader>
      <CardContent><pre className="text-xs bg-muted p-4 rounded-md">{JSON.stringify(data, null, 2)}</pre></CardContent>
    </Card>
  );
}

function DocumentsTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useCandidateDocuments(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load documents" />;
  return (
    <Card>
      <CardHeader><CardTitle>Source Documents</CardTitle></CardHeader>
      <CardContent>
        {Array.isArray(data) && data.length > 0 ? (
          <ul className="space-y-2">
            {data.map((doc: any) => (
              <li key={doc.id} className="text-sm border p-3 rounded-md flex justify-between items-center">
                <span>{doc.original_name}</span>
                <Badge variant="outline">{doc.file_type}</Badge>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-muted-foreground">No documents found.</p>
        )}
      </CardContent>
    </Card>
  );
}

export default function CandidateDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const candidateId = resolvedParams.id;

  const { data: details, isLoading, isError, refetch } = useCandidateDetails(candidateId);

  if (isLoading) {
    return (
      <div className="space-y-6 animate-pulse">
        <Skeleton className="h-20 w-3/4" />
        <Skeleton className="h-[400px] w-full" />
      </div>
    );
  }

  if (isError || !details) {
    return <ErrorState 
      title="Candidate not found"
      message="We could not retrieve the details for this candidate."
      onRetry={() => refetch()}
    />;
  }

  const { profile, skills, experience, education, projects } = details;
  const fullName = `${profile.first_name || ''} ${profile.last_name || ''}`.trim() || 'Unknown Candidate';

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Link href="/candidates">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="w-4 h-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{fullName}</h1>
          <p className="text-muted-foreground mt-1 flex items-center space-x-2">
            <span>{experience.length > 0 ? experience[0].title : "Candidate"}</span>
            <span>•</span>
            <span>ID: {candidateId.substring(0, 8)}...</span>
            <span>•</span>
            <Badge variant="outline" className="text-primary border-primary/20 bg-primary/10">
              {profile.status.replace("_", " ")}
            </Badge>
          </p>
        </div>
      </div>

      <Tabs defaultValue="profile">
        <TabsList className="mb-4 flex-wrap h-auto">
          <TabsTrigger value="profile"><FileText className="w-4 h-4 mr-2"/> Profile</TabsTrigger>
          <TabsTrigger value="documents"><FileText className="w-4 h-4 mr-2"/> Documents</TabsTrigger>
          <TabsTrigger value="workflow"><Activity className="w-4 h-4 mr-2"/> Workflow</TabsTrigger>
          <TabsTrigger value="evaluation"><Star className="w-4 h-4 mr-2"/> Evaluation</TabsTrigger>
          <TabsTrigger value="embeddings"><Network className="w-4 h-4 mr-2"/> Embeddings</TabsTrigger>
          <TabsTrigger value="matching"><CheckCircle2 className="w-4 h-4 mr-2"/> Matches</TabsTrigger>
          <TabsTrigger value="feedback"><FileQuestion className="w-4 h-4 mr-2"/> Feedback</TabsTrigger>
          <TabsTrigger value="memory"><History className="w-4 h-4 mr-2"/> Memory</TabsTrigger>
        </TabsList>

        <TabsContent value="profile" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Professional Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm whitespace-pre-wrap">{profile.summary || "No summary available."}</p>
            </CardContent>
          </Card>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Skills</CardTitle>
              </CardHeader>
              <CardContent>
                {skills.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {skills.map(s => (
                      <Badge key={s.id}>{s.name} {s.proficiency && `(${s.proficiency})`}</Badge>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-muted-foreground">No skills extracted.</p>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Experience</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {experience.length > 0 ? experience.map(e => (
                  <div key={e.id} className="border-b last:border-0 pb-3 last:pb-0">
                    <h4 className="text-sm font-semibold">{e.title} at {e.company}</h4>
                    <p className="text-xs text-muted-foreground mb-1">
                      {e.start_date ? new Date(e.start_date).getFullYear() : 'Unknown'} - 
                      {e.end_date ? new Date(e.end_date).getFullYear() : ' Present'}
                    </p>
                    {e.description && <p className="text-xs line-clamp-2">{e.description}</p>}
                  </div>
                )) : (
                  <p className="text-sm text-muted-foreground">No experience listed.</p>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Education</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {education.length > 0 ? education.map(e => (
                  <div key={e.id} className="border-b last:border-0 pb-3 last:pb-0">
                    <h4 className="text-sm font-semibold">{e.degree || 'Degree'} at {e.institution}</h4>
                    <p className="text-xs text-muted-foreground mb-1">
                      {e.start_date ? new Date(e.start_date).getFullYear() : 'Unknown'} - 
                      {e.end_date ? new Date(e.end_date).getFullYear() : ' Unknown'}
                    </p>
                  </div>
                )) : (
                  <p className="text-sm text-muted-foreground">No education listed.</p>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Projects</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {projects.length > 0 ? projects.map(p => (
                  <div key={p.id} className="border-b last:border-0 pb-3 last:pb-0">
                    <h4 className="text-sm font-semibold">{p.name}</h4>
                    {p.description && <p className="text-xs mt-1">{p.description}</p>}
                  </div>
                )) : (
                  <p className="text-sm text-muted-foreground">No projects listed.</p>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="documents">
          <DocumentsTab id={candidateId} />
        </TabsContent>
        <TabsContent value="workflow">
          <WorkflowTab id={candidateId} />
        </TabsContent>
        <TabsContent value="evaluation">
          <EvaluationTab id={candidateId} />
        </TabsContent>
        <TabsContent value="embeddings">
          <EmbeddingsTab id={candidateId} />
        </TabsContent>
        <TabsContent value="matching">
          <MatchingTab id={candidateId} />
        </TabsContent>
        <TabsContent value="feedback">
          <FeedbackTab id={candidateId} />
        </TabsContent>
        <TabsContent value="memory">
          <MemoryTab id={candidateId} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
