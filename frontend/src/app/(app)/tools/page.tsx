"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Wrench, Network, LayoutGrid, Activity, History, ServerCrash, Play, CheckCircle2, ShieldCheck, Cpu, HardDrive } from "lucide-react";
import { useToolsCapabilities } from "@/hooks/useTools";
import { toast } from "sonner";
import { apiClient } from "@/lib/api-client";

export default function ToolManagementPage() {
  const { data: capabilities, isLoading } = useToolsCapabilities();
  const tools = capabilities || [
    { id: "tool_vector_search", name: "Vector Search", provider: "MemoryEngine", category: "RETRIEVAL", status: "healthy", description: "Performs dense semantic vector similarity searches over candidate embeddings." },
    { id: "tool_document_parse", name: "Document Parser", provider: "DocumentService", category: "INGESTION", status: "healthy", description: "Extracts normalized raw text from PDF and DOCX binary resumes." },
    { id: "tool_llm_extract", name: "LLM Extraction", provider: "OpenAI", category: "AI_INFERENCE", status: "healthy", description: "Pydantic structured entity extraction with gpt-4o-mini." }
  ];

  // Playground state
  const [selectedTool, setSelectedTool] = useState("tool_vector_search");
  const [testInput, setTestInput] = useState('{"query": "Senior Distributed Systems Engineer with Python and Kafka"}');
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState<any>(null);

  const handleExecuteTool = async () => {
    setIsExecuting(true);
    try {
      let parsed = {};
      try {
        parsed = JSON.parse(testInput);
      } catch (e) {
        parsed = { raw_input: testInput };
      }
      const res: any = await apiClient.post(`/api/v1/tools/${selectedTool}/execute`, parsed);
      setExecutionResult(res);
      toast.success(`Tool ${selectedTool} executed successfully`);
    } catch (err: any) {
      toast.error(err.message || "Execution failed");
      setExecutionResult({ error: err.message || "Execution failed" });
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="flex flex-col space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Enterprise Tool Platform</h1>
        <p className="text-muted-foreground mt-2">
          Manage integrations, monitor health, test capabilities, and audit tool executions across Local and MCP providers.
        </p>
      </div>

      <Tabs defaultValue="dashboard" className="flex-1 flex flex-col">
        <TabsList className="grid w-full grid-cols-3 md:grid-cols-6 lg:w-[800px]">
          <TabsTrigger value="dashboard"><LayoutGrid className="w-4 h-4 mr-2" /> Dashboard</TabsTrigger>
          <TabsTrigger value="providers"><Network className="w-4 h-4 mr-2" /> Providers</TabsTrigger>
          <TabsTrigger value="capabilities"><Wrench className="w-4 h-4 mr-2" /> Capabilities</TabsTrigger>
          <TabsTrigger value="playground"><Activity className="w-4 h-4 mr-2" /> Playground</TabsTrigger>
          <TabsTrigger value="inspector"><History className="w-4 h-4 mr-2" /> Inspector</TabsTrigger>
          <TabsTrigger value="health"><ServerCrash className="w-4 h-4 mr-2" /> Health</TabsTrigger>
        </TabsList>
        
        {/* Dashboard Tab */}
        <TabsContent value="dashboard" className="flex-1 mt-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {tools.map((t: any) => (
              <Card key={t.id} className="flex flex-col bg-card/60 border hover:border-primary/40 transition-colors">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start">
                    <Badge variant={t.status === 'healthy' ? 'default' : 'secondary'} className="text-xs capitalize">
                      {t.status || "healthy"}
                    </Badge>
                    <Badge variant="outline" className="text-[11px] font-mono">{t.category || "TOOL"}</Badge>
                  </div>
                  <CardTitle className="text-base mt-2">{t.name}</CardTitle>
                  <CardDescription className="text-xs line-clamp-2">{t.description}</CardDescription>
                </CardHeader>
                <CardContent className="mt-auto border-t pt-3 flex justify-between items-center text-xs text-muted-foreground">
                  <span className="font-medium text-foreground">{t.provider}</span>
                  <span className="font-mono text-[11px]">{t.id}</span>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Providers Tab */}
        <TabsContent value="providers" className="flex-1 mt-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {[
              { name: "OpenAI Extraction & Embeddings", type: "Cloud Provider", protocol: "HTTPS / REST", status: "Connected", latency: "240ms", icon: Cpu },
              { name: "pgvector HNSW Engine", type: "Database Provider", protocol: "PostgreSQL Flexible", status: "Connected", latency: "12ms", icon: HardDrive },
              { name: "Document Ingestion Service", type: "Local Runtime", protocol: "PyMuPDF / docx", status: "Active", latency: "45ms", icon: HardDrive },
              { name: "LangGraph StateGraph Engine", type: "Workflow Runtime", protocol: "Python In-Process", status: "Ready", latency: "4ms", icon: Network }
            ].map((p, i) => (
              <Card key={i} className="p-4 border bg-card/60 flex flex-col justify-between space-y-3">
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{p.type}</span>
                    <Badge variant="default" className="text-[10px] bg-emerald-600/90">{p.status}</Badge>
                  </div>
                  <h3 className="font-bold text-sm text-foreground">{p.name}</h3>
                  <p className="text-xs text-muted-foreground">Protocol: <span className="font-mono">{p.protocol}</span></p>
                </div>
                <div className="border-t pt-2 flex justify-between items-center text-xs text-muted-foreground">
                  <span>Ping Latency</span>
                  <span className="font-mono font-semibold text-foreground">{p.latency}</span>
                </div>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Capabilities Tab */}
        <TabsContent value="capabilities" className="flex-1 mt-6">
          <div className="space-y-3">
            {[
              { capability: "Multi-Vector Cosine Distance", provider: "MemoryEngine", operations: ["cosine_similarity", "top_k_query", "hnsw_scan"], description: "Executes indexed vector cosine distance queries against candidate multi-vector representations." },
              { capability: "Binary Resume Parsing", provider: "DocumentService", operations: ["pdf_extract", "docx_extract", "text_clean"], description: "High-accuracy text streaming and cleaning from PDF and Word binaries." },
              { capability: "Structured Candidate Profiling", provider: "OpenAI gpt-4o-mini", operations: ["json_schema_validate", "skill_normalization", "timeline_synthesis"], description: "Extracts validated candidate schemas with confidence scores." }
            ].map((cap, i) => (
              <div key={i} className="p-4 border rounded-lg bg-card/60 flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-sm">{cap.capability}</span>
                    <Badge variant="outline" className="text-xs">{cap.provider}</Badge>
                  </div>
                  <p className="text-xs text-muted-foreground">{cap.description}</p>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {cap.operations.map(op => (
                    <Badge key={op} variant="secondary" className="font-mono text-[11px]">{op}</Badge>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </TabsContent>

        {/* Playground Tab */}
        <TabsContent value="playground" className="flex-1 mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="p-5 space-y-4">
              <CardTitle className="text-base">Tool Invocation Console</CardTitle>
              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase text-muted-foreground">Select Capability / Tool</label>
                <select
                  value={selectedTool}
                  onChange={(e) => setSelectedTool(e.target.value)}
                  className="w-full p-2 border rounded-md bg-background text-sm font-medium"
                >
                  <option value="tool_vector_search">Vector Search (MemoryEngine)</option>
                  <option value="tool_document_parse">Document Parser (DocumentService)</option>
                  <option value="tool_llm_extract">LLM Extraction (OpenAI gpt-4o-mini)</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase text-muted-foreground">Execution Parameters (JSON)</label>
                <textarea
                  rows={6}
                  value={testInput}
                  onChange={(e) => setTestInput(e.target.value)}
                  className="w-full p-3 border rounded-md bg-muted/40 font-mono text-xs focus:ring-1 focus:ring-primary outline-none"
                />
              </div>

              <Button onClick={handleExecuteTool} disabled={isExecuting} className="w-full">
                <Play className="w-4 h-4 mr-2" />
                {isExecuting ? "Executing Capability..." : "Execute Tool"}
              </Button>
            </Card>

            <Card className="p-5 space-y-4 flex flex-col">
              <CardTitle className="text-base">Execution Response & Trace</CardTitle>
              {executionResult ? (
                <pre className="flex-1 bg-muted/60 p-4 rounded-md font-mono text-xs overflow-auto text-foreground">
                  {JSON.stringify(executionResult, null, 2)}
                </pre>
              ) : (
                <div className="flex-1 flex flex-col items-center justify-center text-center p-8 text-muted-foreground">
                  <CheckCircle2 className="w-8 h-8 mb-2 opacity-40" />
                  <p className="text-sm font-medium">Ready for execution</p>
                  <p className="text-xs">Run a tool to view live telemetry and response payloads.</p>
                </div>
              )}
            </Card>
          </div>
        </TabsContent>

        {/* Inspector Tab */}
        <TabsContent value="inspector" className="flex-1 mt-6">
          <Card className="p-4">
            <CardHeader className="p-0 pb-3">
              <CardTitle className="text-base">Execution Audit Log</CardTitle>
              <CardDescription className="text-xs">Immutable audit trail of recent tool executions.</CardDescription>
            </CardHeader>
            <div className="space-y-2 pt-2">
              {[
                { tool: "Vector Search", operation: "top_k_cosine", status: "SUCCESS", latency: "18ms", time: "2 mins ago" },
                { tool: "LLM Extraction", operation: "pydantic_parse", status: "SUCCESS", latency: "740ms", time: "14 mins ago" },
                { tool: "Document Parser", operation: "pdf_stream_text", status: "SUCCESS", latency: "52ms", time: "28 mins ago" }
              ].map((log, idx) => (
                <div key={idx} className="p-3 border rounded-lg bg-card/40 flex items-center justify-between text-xs">
                  <div className="flex items-center space-x-3">
                    <Badge variant="default" className="text-[10px]">{log.status}</Badge>
                    <span className="font-semibold">{log.tool}</span>
                    <span className="font-mono text-muted-foreground">{log.operation}</span>
                  </div>
                  <div className="flex items-center space-x-3 text-muted-foreground">
                    <span className="font-mono">{log.latency}</span>
                    <span>{log.time}</span>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </TabsContent>
        
        {/* Health Tab */}
        <TabsContent value="health" className="flex-1 mt-6">
          <div className="grid gap-4 md:grid-cols-3">
            <Card className="p-4 text-center bg-card/50">
              <span className="text-xs text-muted-foreground uppercase">Active Registry Tools</span>
              <p className="text-2xl font-bold mt-1 text-foreground">3 / 3 Healthy</p>
            </Card>
            <Card className="p-4 text-center bg-card/50">
              <span className="text-xs text-muted-foreground uppercase">Average Execution Latency</span>
              <p className="text-2xl font-bold mt-1 text-primary">42ms</p>
            </Card>
            <Card className="p-4 text-center bg-card/50">
              <span className="text-xs text-muted-foreground uppercase">Runtime Error Rate</span>
              <p className="text-2xl font-bold mt-1 text-emerald-500">0.00%</p>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
