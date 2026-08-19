"use client";

import { useState, useRef } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, FileText, Code, BarChart, Server, Activity, Loader2, CheckCircle2, Circle, XCircle, AlertTriangle } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { toast } from "sonner";
import { 
  usePlaygroundDocument, 
  usePlaygroundStatus,
  usePlaygroundExtraction, 
  usePlaygroundEmbeddings, 
  usePlaygroundEvaluation 
} from "@/hooks/usePlayground";

export default function PlaygroundPage() {
  const [file, setFile] = useState<File | null>(null);
  const [documentId, setDocumentId] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { data: statusData } = usePlaygroundStatus(documentId);
  const isFailed = statusData?.status === 'FAILED';
  const errorMessage = statusData?.error_message || "Pipeline failed. Check logs for details (likely missing API key).";
  
  const { data: documentData, isLoading: docLoading } = usePlaygroundDocument(documentId, isFailed);
  const { data: extractionData, isLoading: extractLoading } = usePlaygroundExtraction(documentId, isFailed);
  
  const candidateId = documentData?.candidate_id || null;
  const { data: embeddingsData } = usePlaygroundEmbeddings(candidateId, statusData?.status === 'COMPLETED' || isFailed);
  const { data: evaluationData } = usePlaygroundEvaluation(candidateId, statusData?.status === 'COMPLETED' || isFailed);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleSelectClick = () => {
    fileInputRef.current?.click();
  };

  const handleRunPipeline = async () => {
    if (!file) {
      toast.error("Please select a file first");
      return;
    }

    setUploading(true);
    setDocumentId(null);
    try {
      const formData = new FormData();
      formData.append("file", file);

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiUrl}/api/v1/resumes/upload`, {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();
      setDocumentId(data.document_id);
      toast.success("Pipeline started. Waiting for results...");
    } catch (error) {
      toast.error("Pipeline failed to start");
    } finally {
      setUploading(false);
    }
  };

  const isPipelineRunning = !!documentId && !isFailed && statusData?.status !== 'COMPLETED';

  const getPipelineStep = () => {
    if (isFailed) return -1;
    if (!documentId && !uploading) return 0;
    if (uploading) return 1;
    if (statusData?.status === 'QUEUED') return 1;
    if (!documentData?.raw_text) return 2;
    if (!extractionData) return 3;
    if (statusData?.status !== 'COMPLETED') return 4;
    return 5;
  };

  const currentStep = getPipelineStep();

  const steps = [
    { id: 1, name: "Upload" },
    { id: 2, name: "Parse" },
    { id: 3, name: "AI Extraction" },
    { id: 4, name: "Finalize" }
  ];

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">AI Playground</h1>
        <p className="text-muted-foreground mt-2">
          Debug raw extraction, embeddings, and prompt versions.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Input Context</CardTitle>
            <CardDescription>Upload a raw resume.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="border-2 border-dashed rounded-lg p-6 flex flex-col items-center justify-center text-center">
              <Upload className="w-8 h-8 text-muted-foreground mb-4" />
              {file ? (
                <p className="text-sm font-medium mb-2 truncate max-w-full">{file.name}</p>
              ) : (
                <p className="text-sm text-muted-foreground mb-2">Drag and drop resume here</p>
              )}
              
              <input 
                type="file" 
                className="hidden" 
                ref={fileInputRef} 
                onChange={handleFileChange} 
                accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document" 
              />
              <Button variant="outline" size="sm" onClick={handleSelectClick} disabled={isPipelineRunning}>
                {file ? "Change File" : "Select File"}
              </Button>
            </div>
            
            <div className="space-y-2">
              <h3 className="text-sm font-medium">Configuration</h3>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Prompt Version</span>
                <Badge variant="outline">v1.2.0</Badge>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Embedding Model</span>
                <Badge variant="outline">{process.env.NEXT_PUBLIC_AI_EMBEDDING_MODEL || "text-embedding-3-small"}</Badge>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Extraction Model</span>
                <Badge variant="outline">{process.env.NEXT_PUBLIC_AI_EXTRACTION_MODEL || "gpt-4o"}</Badge>
              </div>
            </div>

            <Button 
              className="w-full" 
              onClick={handleRunPipeline} 
              disabled={!file || isPipelineRunning || uploading}
            >
              {uploading || isPipelineRunning ? (
                <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Running Pipeline...</>
              ) : (
                "Run AI Pipeline"
              )}
            </Button>
          </CardContent>
        </Card>

        <Card className="col-span-2">
          <CardHeader>
            <CardTitle className="flex justify-between items-center">
              <span>Pipeline Output</span>
              {extractionData && (
                <div className="flex space-x-2 text-xs font-normal">
                  {extractionData.total_tokens && (
                    <Badge variant="secondary" className="flex items-center">
                      <Server className="w-3 h-3 mr-1"/> 
                      {extractionData.total_tokens.toLocaleString()} Tokens
                    </Badge>
                  )}
                  {extractionData.processing_time_ms && (
                    <Badge variant="secondary" className="flex items-center">
                      <Activity className="w-3 h-3 mr-1"/> 
                      {(extractionData.processing_time_ms / 1000).toFixed(1)}s Latency
                    </Badge>
                  )}
                </div>
              )}
            </CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col h-full">
            {/* Progress Bar Area */}
            {(documentId || uploading) && (
              <div className="mb-12 px-6 mt-2">
                <div className="flex items-center justify-between relative">
                  {/* Background Track */}
                  <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-full h-1.5 bg-secondary/50 rounded-full -z-10"></div>
                  
                  {/* Active Track */}
                  <div 
                    className={`absolute left-0 top-1/2 transform -translate-y-1/2 h-1.5 rounded-full -z-10 transition-all duration-700 ease-in-out ${isPipelineRunning ? 'bg-gradient-to-r from-primary/80 via-primary to-primary/80 bg-[length:200%_auto] animate-pulse' : 'bg-primary'}`}
                    style={{ width: `${Math.min(100, Math.max(0, (currentStep - 1) / (steps.length - 1) * 100))}%` }}
                  ></div>

                  {steps.map((step, idx) => {
                    const isCompleted = currentStep > step.id || currentStep === 5;
                    const isCurrent = currentStep === step.id;
                    const isError = isFailed && currentStep === -1 && idx === (statusData?.status === 'QUEUED' ? 0 : 2); 
                    
                    return (
                      <div key={step.id} className="flex flex-col items-center bg-card px-2 relative">
                        {isCurrent && (
                          <div className="absolute top-0 w-8 h-8 rounded-full bg-primary/30 animate-ping" />
                        )}
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 transition-all duration-500 relative z-10 ${
                          isCompleted ? 'bg-primary border-primary text-primary-foreground shadow-[0_0_10px_theme(colors.primary.DEFAULT)]' :
                          isCurrent ? 'bg-background border-primary text-primary shadow-[0_0_15px_theme(colors.primary.DEFAULT)]' :
                          isError ? 'bg-destructive border-destructive text-destructive-foreground shadow-[0_0_15px_theme(colors.destructive.DEFAULT)]' :
                          'bg-background border-muted text-muted-foreground'
                        }`}>
                          {isCompleted ? <CheckCircle2 className="w-5 h-5" /> : 
                           isError ? <XCircle className="w-5 h-5" /> :
                           isCurrent ? <Loader2 className="w-4 h-4 animate-spin" /> : 
                           <span className="w-2.5 h-2.5 rounded-full bg-muted-foreground/30" />}
                        </div>
                        <span className={`text-xs mt-3 font-semibold absolute -bottom-7 w-24 text-center transition-colors duration-500 ${
                          isCurrent ? 'text-primary' : 
                          isError ? 'text-destructive' : 
                          isCompleted ? 'text-foreground' : 
                          'text-muted-foreground'
                        }`}>
                          {step.name}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Error Display Area */}
            {isFailed && (
              <Alert variant="destructive" className="mb-6 shadow-md border-destructive/50 bg-destructive/10">
                <AlertTriangle className="h-5 w-5" />
                <AlertTitle className="text-lg font-semibold ml-2">Pipeline Execution Failed</AlertTitle>
                <AlertDescription className="ml-2 mt-2">
                  <div className="font-mono text-sm bg-background/50 p-3 rounded-md border border-destructive/20 break-words whitespace-pre-wrap">
                    {errorMessage}
                  </div>
                  <div className="mt-3 text-sm">
                    The pipeline encountered an error and could not complete. Please check your configuration and try again.
                  </div>
                </AlertDescription>
              </Alert>
            )}

            {/* Tabs content below */}
            <Tabs defaultValue="raw" className="flex-1 flex flex-col min-h-0">
              <TabsList className="mb-4">
                <TabsTrigger value="raw"><FileText className="w-4 h-4 mr-2"/> Raw PDF Text</TabsTrigger>
                <TabsTrigger value="normalized"><Code className="w-4 h-4 mr-2"/> Normalized</TabsTrigger>
                <TabsTrigger value="evaluation"><BarChart className="w-4 h-4 mr-2"/> Evaluation</TabsTrigger>
                <TabsTrigger value="embeddings"><Server className="w-4 h-4 mr-2"/> Embeddings</TabsTrigger>
              </TabsList>
              
              <TabsContent value="raw">
                <pre className="bg-muted p-4 rounded-md h-[400px] overflow-y-auto text-sm font-mono text-muted-foreground whitespace-pre-wrap">
                  {documentData?.raw_text 
                    ? documentData.raw_text 
                    : isPipelineRunning 
                      ? "Extracting text from document..." 
                      : "Waiting for document..."}
                </pre>
              </TabsContent>
              
              <TabsContent value="normalized">
                <pre className="bg-muted p-4 rounded-md h-[400px] overflow-y-auto text-sm font-mono text-muted-foreground">
                  {extractionData?.normalized_response 
                    ? JSON.stringify(extractionData.normalized_response, null, 2)
                    : isFailed 
                      ? "Extraction failed."
                      : isPipelineRunning 
                        ? "Waiting for extraction..." 
                        : "No extraction available"}
                </pre>
              </TabsContent>
              
              <TabsContent value="evaluation">
                <div className={`h-[400px] flex ${evaluationData && evaluationData.length > 0 ? 'flex-col' : 'items-center justify-center'} overflow-y-auto border rounded-md p-4 text-muted-foreground`}>
                  {evaluationData && evaluationData.length > 0 ? (
                    <div className="space-y-4 w-full text-foreground">
                      {evaluationData.map((evalItem: any) => (
                        <div key={evalItem.id} className="p-4 border rounded bg-card">
                          <p className="font-medium">Job Requirement ID: <span className="font-mono text-xs text-muted-foreground">{evalItem.job_requirement_id}</span></p>
                          <p className="mt-2">Final Score: <Badge variant={evalItem.final_score > 0.7 ? 'default' : 'secondary'}>{(evalItem.final_score * 100).toFixed(0)}%</Badge></p>
                        </div>
                      ))}
                    </div>
                  ) : extractionData?.overall_confidence !== undefined ? (
                     <div className="space-y-4 w-full text-foreground">
                       <h3 className="font-medium text-lg mb-2">Extraction Confidence Scores</h3>
                       <div className="grid grid-cols-2 gap-4">
                         <div className="p-4 border rounded bg-card flex justify-between items-center">
                           <span>Overall</span>
                           <Badge variant="outline">{(extractionData.overall_confidence * 100).toFixed(0)}%</Badge>
                         </div>
                         {extractionData.education_confidence && (
                           <div className="p-4 border rounded bg-card flex justify-between items-center">
                             <span>Education</span>
                             <Badge variant="outline">{(extractionData.education_confidence * 100).toFixed(0)}%</Badge>
                           </div>
                         )}
                         {extractionData.experience_confidence && (
                           <div className="p-4 border rounded bg-card flex justify-between items-center">
                             <span>Experience</span>
                             <Badge variant="outline">{(extractionData.experience_confidence * 100).toFixed(0)}%</Badge>
                           </div>
                         )}
                         {extractionData.skills_confidence && (
                           <div className="p-4 border rounded bg-card flex justify-between items-center">
                             <span>Skills</span>
                             <Badge variant="outline">{(extractionData.skills_confidence * 100).toFixed(0)}%</Badge>
                           </div>
                         )}
                       </div>
                       <p className="text-xs text-muted-foreground mt-4">Note: Candidate matches against specific job requirements are not yet generated for a newly uploaded document until a search session occurs.</p>
                     </div>
                  ) : (
                    isFailed ? "Evaluation failed." : isPipelineRunning ? "Waiting for evaluation..." : "No evaluation available"
                  )}
                </div>
              </TabsContent>
              
              <TabsContent value="embeddings">
                <div className={`h-[400px] flex ${embeddingsData && embeddingsData.length > 0 ? 'flex-col' : 'items-center justify-center'} overflow-y-auto border rounded-md p-4 text-muted-foreground`}>
                  {embeddingsData && embeddingsData.length > 0 ? (
                     <div className="space-y-4 w-full text-foreground">
                       <h3 className="font-medium text-lg mb-2">Generated Vector Embeddings</h3>
                       {embeddingsData.map((embed: any) => (
                         <div key={embed.id} className="p-4 border rounded bg-card space-y-2">
                           <div className="flex justify-between">
                             <span className="font-medium capitalize">{embed.embedding_type}</span>
                             <Badge variant="outline">{embed.embedding_model}</Badge>
                           </div>
                           <p className="text-sm text-muted-foreground">Dimensions: {embed.dimensions}</p>
                           <div className="mt-2">
                             <p className="text-xs text-muted-foreground mb-1">Vector Preview (first 5 of {embed.dimensions}):</p>
                             <pre className="text-xs bg-muted p-2 rounded overflow-x-auto">
                               [{embed.vector_preview?.map((v: number) => v.toFixed(4)).join(", ")}, ...]
                             </pre>
                           </div>
                         </div>
                       ))}
                     </div>
                  ) : (
                    isFailed ? "Vector generation failed." : isPipelineRunning ? "Generating vectors..." : "No vectors generated"
                  )}
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
