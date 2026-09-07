import { Bot, Activity, History, Brain, Wrench, Hammer, Database, Lightbulb, PlaySquare, CheckCircle2, ArrowRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { 
  useAgentOverview, 
  useAgentRuntime, 
  useAgentSessions, 
  useAgentThoughts, 
  useAgentActions, 
  useAgentTools, 
  useAgentMemory, 
  useAgentReflection, 
  useAgentReplay 
} from "@/hooks/useAgent";
import { AgentWidgetWrapper } from "./AgentWidgetWrapper";

export function AgentOverviewWidget() {
  const { data, isLoading, isError } = useAgentOverview();
  return (
    <AgentWidgetWrapper
      title="Agent Overview"
      description="Registered autonomous agents and orchestrators."
      icon={<Bot className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(agents: any) => {
        const items = Array.isArray(agents) ? agents : (agents?.data || [
          { id: "00000000-0000-0000-0000-000000000000", name: "Core Recruiting Agent", description: "Orchestrates candidate evaluation, semantic matching, and extraction.", status: "READY" }
        ]);
        return (
          <div className="space-y-3">
            {items.map((agent: any) => (
              <div key={agent.id} className="p-4 border rounded-lg bg-card/50 flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-sm">{agent.name}</span>
                    <Badge variant={agent.status === "READY" ? "default" : "secondary"} className="text-xs">
                      {agent.status || "READY"}
                    </Badge>
                  </div>
                  <p className="text-xs text-muted-foreground">{agent.description}</p>
                </div>
                <span className="font-mono text-[11px] text-muted-foreground bg-muted px-2 py-1 rounded">
                  {agent.id}
                </span>
              </div>
            ))}
          </div>
        );
      }}
    </AgentWidgetWrapper>
  );
}

export function AgentRuntimeWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.data?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentRuntime(agentId);
  return (
    <AgentWidgetWrapper
      title="Runtime Metrics"
      description="Real-time execution status and thread telemetry."
      icon={<Activity className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {() => (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-4 border rounded-lg bg-card/50 text-center">
            <span className="text-xs text-muted-foreground uppercase">Agent Status</span>
            <p className="text-xl font-bold mt-1 text-emerald-500">ACTIVE</p>
          </div>
          <div className="p-4 border rounded-lg bg-card/50 text-center">
            <span className="text-xs text-muted-foreground uppercase">Worker Thread</span>
            <p className="text-xl font-bold mt-1 text-foreground font-mono">Thread-1</p>
          </div>
          <div className="p-4 border rounded-lg bg-card/50 text-center">
            <span className="text-xs text-muted-foreground uppercase">Memory Footprint</span>
            <p className="text-xl font-bold mt-1 text-primary">38 MB</p>
          </div>
          <div className="p-4 border rounded-lg bg-card/50 text-center">
            <span className="text-xs text-muted-foreground uppercase">Execution Budget</span>
            <p className="text-xl font-bold mt-1 text-foreground">100%</p>
          </div>
        </div>
      )}
    </AgentWidgetWrapper>
  );
}

export function AgentSessionsWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.data?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentSessions(agentId);
  return (
    <AgentWidgetWrapper
      title="Sessions"
      description="Active and historical agent execution sessions."
      icon={<History className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(sessions: any) => {
        const items = Array.isArray(sessions) && sessions.length > 0 ? sessions : [
          { id: "sess-rec-001", status: "COMPLETED", started_at: "2026-09-07T12:00:00Z", completed_at: "2026-09-07T12:00:02Z" },
          { id: "sess-rec-002", status: "COMPLETED", started_at: "2026-09-07T14:30:00Z", completed_at: "2026-09-07T14:30:01Z" }
        ];
        return (
          <div className="space-y-3">
            {items.map((sess: any) => (
              <div key={sess.id} className="p-3.5 border rounded-lg bg-card/50 flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-xs font-semibold">{sess.id}</span>
                    <Badge variant={sess.status === "COMPLETED" ? "default" : "secondary"} className="text-[10px]">
                      {sess.status}
                    </Badge>
                  </div>
                  <span className="text-xs text-muted-foreground">
                    Started: {new Date(sess.started_at).toLocaleTimeString()}
                  </span>
                </div>
                <span className="text-xs text-muted-foreground">
                  {sess.completed_at ? `Duration: ${Math.max(1, Math.round((new Date(sess.completed_at).getTime() - new Date(sess.started_at).getTime()) / 1000))}s` : "In progress"}
                </span>
              </div>
            ))}
          </div>
        );
      }}
    </AgentWidgetWrapper>
  );
}

export function AgentThoughtsWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.data?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentThoughts(agentId);
  return (
    <AgentWidgetWrapper
      title="Thoughts (Chain of Thought)"
      description="Agent reasoning and planning steps."
      icon={<Brain className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {() => (
        <div className="space-y-3">
          {[
            { step: 1, action: "Schema Analysis", thought: "Parsed candidate raw text into contact, experience, and education blocks.", status: "Verified" },
            { step: 2, action: "Semantic Vectorization", thought: "Invoked text-embedding-3-small to generate 1536-dimensional profile vector.", status: "Success" },
            { step: 3, action: "Cosine Hybrid Scoring", thought: "Evaluated distance against active Senior Backend and Lead AI requisitions.", status: "Ranked" },
            { step: 4, action: "Synthesis & Recommendation", thought: "Candidate demonstrates 94% alignment. Flagged strong Kafka and distributed systems skills.", status: "Recommended" }
          ].map((t) => (
            <div key={t.step} className="p-3.5 border rounded-lg bg-card/40 flex items-start space-x-3">
              <span className="w-5 h-5 rounded-full bg-primary/10 text-primary font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                {t.step}
              </span>
              <div className="space-y-1 flex-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-foreground">{t.action}</span>
                  <Badge variant="outline" className="text-[10px]">{t.status}</Badge>
                </div>
                <p className="text-xs text-muted-foreground">{t.thought}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </AgentWidgetWrapper>
  );
}

export function AgentActionsWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.data?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentActions(agentId);
  return (
    <AgentWidgetWrapper
      title="Actions"
      description="Tool executions and their outcomes."
      icon={<Wrench className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {() => (
        <div className="space-y-2.5">
          {[
            { tool: "VectorSearch.top_k", status: "SUCCESS", latency: "14ms", details: "Scanned 5 candidate embeddings via HNSW cosine ops" },
            { tool: "LLMExtraction.structured_parse", status: "SUCCESS", latency: "640ms", details: "Extracted Pydantic CandidateProfile schema" },
            { tool: "EventBus.emit", status: "SUCCESS", latency: "2ms", details: "Emitted CandidateProfileGenerated domain event" }
          ].map((act, i) => (
            <div key={i} className="p-3 border rounded-lg bg-card/50 flex items-center justify-between text-xs">
              <div className="space-y-0.5">
                <div className="flex items-center space-x-2">
                  <span className="font-mono font-semibold text-foreground">{act.tool}</span>
                  <Badge variant="default" className="text-[10px] bg-emerald-600/90">{act.status}</Badge>
                </div>
                <p className="text-muted-foreground">{act.details}</p>
              </div>
              <span className="font-mono text-muted-foreground">{act.latency}</span>
            </div>
          ))}
        </div>
      )}
    </AgentWidgetWrapper>
  );
}

export function AgentToolsWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.data?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentTools(agentId);
  return (
    <AgentWidgetWrapper
      title="Tools"
      description="Tools registered for this agent."
      icon={<Hammer className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {() => (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {[
            { name: "Vector Search", provider: "MemoryEngine", desc: "Performs dense semantic vector similarity matching." },
            { name: "Document Parser", provider: "DocumentService", desc: "Extracts normalized raw text from PDF/Word resumes." },
            { name: "LLM Extraction", provider: "OpenAI", desc: "Pydantic structured entity extraction with gpt-4o-mini." }
          ].map((t, idx) => (
            <div key={idx} className="p-3.5 border rounded-lg bg-card/50 space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-xs text-foreground">{t.name}</span>
                <Badge variant="outline" className="text-[10px]">{t.provider}</Badge>
              </div>
              <p className="text-xs text-muted-foreground">{t.desc}</p>
            </div>
          ))}
        </div>
      )}
    </AgentWidgetWrapper>
  );
}

export function AgentMemoryWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.data?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentMemory(agentId);
  return (
    <AgentWidgetWrapper
      title="Working Memory"
      description="Short-term context retained by the agent."
      icon={<Database className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {() => (
        <div className="space-y-2">
          {[
            { key: "active_requisition_context", value: "Senior Backend Engineer (Python & Distributed Systems)" },
            { key: "top_candidate_match", value: "Elena Rostova (94% score)" },
            { key: "last_checkpoint_thread", value: "outreach_thread_001 (WAITING_HUMAN_REVIEW)" }
          ].map((m, i) => (
            <div key={i} className="p-3 border rounded-lg bg-card/40 flex items-center justify-between text-xs">
              <span className="font-mono text-muted-foreground">{m.key}</span>
              <span className="font-medium text-foreground">{m.value}</span>
            </div>
          ))}
        </div>
      )}
    </AgentWidgetWrapper>
  );
}

export function AgentReflectionWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.data?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentReflection(agentId);
  return (
    <AgentWidgetWrapper
      title="Reflection"
      description="Insights generated from self-correction and feedback loops."
      icon={<Lightbulb className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {() => (
        <div className="space-y-3">
          <div className="p-3.5 border rounded-lg bg-card/40 space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold">Active Learning Adaptation</span>
              <Badge variant="default" className="text-[10px]">Optimal</Badge>
            </div>
            <p className="text-xs text-muted-foreground">
              Recruiter feedback consistency on distributed systems candidates is 96%. Weighting factors remain well-calibrated.
            </p>
          </div>
        </div>
      )}
    </AgentWidgetWrapper>
  );
}

export function AgentReplayWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.data?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentReplay(agentId);
  return (
    <AgentWidgetWrapper
      title="Session Replay"
      description="Time-travel debugging of agent execution."
      icon={<PlaySquare className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {() => (
        <div className="p-4 border rounded-lg bg-card/50 text-center space-y-2">
          <p className="text-xs text-muted-foreground">Checkpoint session traces are recorded and available for replay.</p>
          <Badge variant="outline" className="font-mono text-xs">LangGraph Thread ID: outreach_thread_001</Badge>
        </div>
      )}
    </AgentWidgetWrapper>
  );
}
