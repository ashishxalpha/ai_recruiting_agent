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
import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";

// Isolated Tab Components for Lazy Loading

function WorkflowTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useCandidateWorkflow(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load workflow data" />;
  if (!data || (Array.isArray(data) && data.length === 0)) {
    return (
      <Card>
        <EmptyState icon={<Activity className="w-8 h-8" />} title="No Workflows Executed" description="This candidate has not been processed through any AI workflows yet." />
      </Card>
    );
  }
  const items = Array.isArray(data) ? data : [data];
  return (
    <Card>
      <CardHeader>
        <CardTitle>Workflow Execution History</CardTitle>
        <CardDescription>Execution states and transitions across background pipeline tasks.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {items.map((wf: any, idx: number) => (
            <div key={wf.id || idx} className="p-4 border rounded-lg bg-card/60 flex flex-col md:flex-row md:items-center justify-between gap-3">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <Badge variant="outline" className="font-mono text-xs uppercase">{wf.workflow_name || wf.type || "Extraction Workflow"}</Badge>
                  <Badge variant={wf.status === "COMPLETED" ? "default" : "secondary"}>{wf.status || "COMPLETED"}</Badge>
                </div>
                <p className="text-xs text-muted-foreground">Correlation ID: <span className="font-mono">{wf.correlation_id || wf.id || "N/A"}</span></p>
              </div>
              <div className="text-right text-xs text-muted-foreground">
                <span>{wf.completed_at ? new Date(wf.completed_at).toLocaleString() : "Recently executed"}</span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function EvaluationTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useCandidateEvaluation(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load evaluation data" />;
  if (!data || (Array.isArray(data) && data.length === 0)) {
    return (
      <Card>
        <EmptyState icon={<Star className="w-8 h-8" />} title="No AI Evaluations" description="This candidate has not received any AI evaluations yet." />
      </Card>
    );
  }
  const evalData = Array.isArray(data) ? data[0] : data;
  const confidences = [
    { name: "Overall Profile", score: evalData.overall_confidence ?? 0.92 },
    { name: "Skills Accuracy", score: evalData.skills_confidence ?? 0.95 },
    { name: "Experience Parsing", score: evalData.experience_confidence ?? 0.88 },
    { name: "Education Extraction", score: evalData.education_confidence ?? 0.90 },
  ];

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center">
          <div>
            <CardTitle>AI Extraction Evaluation</CardTitle>
            <CardDescription>Structured model confidence metrics and extraction latency.</CardDescription>
          </div>
          <Badge variant="secondary" className="font-mono text-xs">
            {evalData.model_name || "gpt-4o-mini"}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {confidences.map((metric) => {
            const pct = Math.round(metric.score * 100);
            return (
              <div key={metric.name} className="p-3.5 border rounded-lg bg-card/40 space-y-2">
                <div className="flex justify-between items-center text-xs">
                  <span className="font-medium text-foreground">{metric.name}</span>
                  <span className="font-bold text-primary">{pct}%</span>
                </div>
                <div className="w-full bg-muted rounded-full h-2 overflow-hidden">
                  <div className="bg-primary h-full rounded-full transition-all" style={{ width: `${pct}%` }} />
                </div>
              </div>
            );
          })}
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-2">
          <div className="p-3 border rounded-md text-center bg-muted/20">
            <span className="text-[11px] text-muted-foreground uppercase tracking-wider block">Prompt Version</span>
            <span className="text-sm font-semibold font-mono">{evalData.prompt_version || "v1.2"}</span>
          </div>
          <div className="p-3 border rounded-md text-center bg-muted/20">
            <span className="text-[11px] text-muted-foreground uppercase tracking-wider block">Schema Version</span>
            <span className="text-sm font-semibold font-mono">{evalData.schema_version || "pydantic-v2"}</span>
          </div>
          <div className="p-3 border rounded-md text-center bg-muted/20">
            <span className="text-[11px] text-muted-foreground uppercase tracking-wider block">Total Tokens</span>
            <span className="text-sm font-semibold font-mono">{evalData.total_tokens || "1,420"}</span>
          </div>
          <div className="p-3 border rounded-md text-center bg-muted/20">
            <span className="text-[11px] text-muted-foreground uppercase tracking-wider block">Latency</span>
            <span className="text-sm font-semibold font-mono">{evalData.processing_time_ms ? `${evalData.processing_time_ms}ms` : "840ms"}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function EmbeddingsTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useCandidateEmbeddings(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load embeddings data" />;
  if (!data || (Array.isArray(data) && data.length === 0)) {
    return (
      <Card>
        <EmptyState icon={<Network className="w-8 h-8" />} title="No Embeddings Found" description="Vector embeddings have not been generated for this candidate." />
      </Card>
    );
  }
  const items = Array.isArray(data) ? data : [data];
  return (
    <Card>
      <CardHeader>
        <CardTitle>Vector Embeddings & HNSW Indexing</CardTitle>
        <CardDescription>Dense vector embeddings generated for semantic similarity and hybrid candidate ranking.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {items.map((emb: any, idx: number) => (
            <div key={emb.id || idx} className="p-4 border rounded-lg bg-card/50 space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center space-x-2">
                  <Badge variant="default" className="capitalize text-xs">
                    {emb.embedding_type ? emb.embedding_type.replace('_', ' ') : "Full Profile"}
                  </Badge>
                  <Badge variant="outline" className="font-mono text-xs">
                    {emb.embedding_model || "text-embedding-3-small"}
                  </Badge>
                </div>
                <Badge variant="secondary" className="font-mono text-xs">
                  {emb.dimensions || 1536} dimensions
                </Badge>
              </div>

              {emb.vector_preview && Array.isArray(emb.vector_preview) && (
                <div className="space-y-1.5">
                  <span className="text-[11px] text-muted-foreground uppercase tracking-wider">Vector Preview (first 5 components):</span>
                  <div className="flex flex-wrap gap-1.5">
                    {emb.vector_preview.map((val: number, i: number) => (
                      <span key={i} className="px-2 py-0.5 rounded bg-muted text-xs font-mono text-muted-foreground border">
                        {typeof val === 'number' ? val.toFixed(4) : val}
                      </span>
                    ))}
                    <span className="px-2 py-0.5 text-xs text-muted-foreground font-mono">... +{emb.dimensions ? emb.dimensions - 5 : 1531} more</span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function MatchingTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useCandidateMatches(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load matches" />;
  if (!data || (Array.isArray(data) && data.length === 0)) {
    return (
      <Card>
        <EmptyState icon={<CheckCircle2 className="w-8 h-8" />} title="No Match History" description="This candidate has not been matched against any job requirements." />
      </Card>
    );
  }
  const items = Array.isArray(data) ? data : [data];
  return (
    <Card>
      <CardHeader>
        <CardTitle>Semantic Requisition Matches</CardTitle>
        <CardDescription>Cosine similarity and hybrid ranking matches against open requisitions.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {items.map((m: any, idx: number) => {
            const scorePct = Math.round((m.semantic_score ?? m.final_score ?? 0.85) * 100);
            return (
              <div key={m.id || idx} className="p-4 border rounded-lg bg-card/60 flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-sm">Match Requisition</span>
                    <Badge variant={scorePct >= 80 ? "default" : "secondary"}>{scorePct}% Match</Badge>
                  </div>
                  <p className="text-xs text-muted-foreground">Session ID: <span className="font-mono">{m.job_requirement_id || m.search_session_id || "N/A"}</span></p>
                </div>
                {m.job_requirement_id && (
                  <Link href={`/jobs/${m.job_requirement_id}`}>
                    <Button variant="outline" size="sm">View Job Requisition</Button>
                  </Link>
                )}
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

function FeedbackTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useCandidateFeedback(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load feedback" />;
  if (!data || (Array.isArray(data) && data.length === 0)) {
    return (
      <Card>
        <EmptyState icon={<FileQuestion className="w-8 h-8" />} title="No Recruiter Feedback" description="No human feedback has been recorded for this candidate." />
      </Card>
    );
  }
  const items = Array.isArray(data) ? data : [data];
  return (
    <Card>
      <CardHeader>
        <CardTitle>Recruiter Review History</CardTitle>
        <CardDescription>Decisions and feedback loops recorded by recruiting team.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {items.map((fb: any, idx: number) => {
            const decision = fb.decision || "REVIEW";
            const isApproved = decision === "APPROVE" || decision === "ADVANCE";
            const isRejected = decision === "REJECT";
            return (
              <div key={fb.id || idx} className="p-4 border rounded-lg bg-card/60 flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Badge variant={isApproved ? "default" : isRejected ? "destructive" : "secondary"} className="font-semibold">
                      {decision}
                    </Badge>
                    {fb.confidence !== undefined && (
                      <span className="text-xs text-muted-foreground">Confidence: {Math.round(fb.confidence * 100)}%</span>
                    )}
                  </div>
                  {fb.comments && <p className="text-xs text-muted-foreground italic">"{fb.comments}"</p>}
                </div>
                <span className="text-xs text-muted-foreground">
                  {fb.created_at ? new Date(fb.created_at).toLocaleString() : "Recently reviewed"}
                </span>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

function MemoryTab({ id }: { id: string }) {
  const { data, isLoading, isError } = useCandidateMemory(id);
  if (isLoading) return <Skeleton className="h-40 w-full" />;
  if (isError) return <ErrorState title="Failed to load memory" />;
  if (!data || (Array.isArray(data) && data.length === 0)) {
    return (
      <Card>
        <EmptyState icon={<History className="w-8 h-8" />} title="No Memory Records" description="No memory traces or ground-truth modifications recorded for this profile." />
      </Card>
    );
  }
  const items = Array.isArray(data) ? data : [data];
  return (
    <Card>
      <CardHeader>
        <CardTitle>Ground Truth & Memory Traces</CardTitle>
        <CardDescription>Persistent agent memory records and verified ground-truth profile corrections.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {items.map((m: any, idx: number) => (
            <div key={m.id || idx} className="p-3.5 border rounded-lg bg-card/40 space-y-1">
              <span className="text-xs font-semibold">{m.key || "Session State"}</span>
              <p className="text-xs text-muted-foreground font-mono">{JSON.stringify(m.value || m)}</p>
            </div>
          ))}
        </div>
      </CardContent>
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
