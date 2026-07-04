export type AnalyticsStatus = "available" | "not_available" | "loading" | "error";

export interface AnalyticsResponse<T> {
  status: AnalyticsStatus;
  reason?: string;
  data?: T | null;
}

export interface RecruitingFunnelData {
  applications: number;
  processing: number;
  review: number;
  shortlisted: number;
  interview: number;
  offer: number;
  hired: number;
}

export interface MatchingAnalyticsData {
  average_match_score: number;
  average_confidence: number;
  precision: number;
  recall: number;
  ndcg: number;
  approval_rate: number;
  recruiter_agreement: number;
  hire_conversion: number;
}

export interface WorkflowAnalyticsData {
  average_duration_ms: number;
  success_rate: number;
  retry_count: number;
  paused_workflows: number;
  failed_workflows: number;
  human_approvals: number;
  checkpoint_recovery: number;
}

export interface MemoryAnalyticsData {
  memory_count: number;
  memory_types: Record<string, number>;
  retrieval_latency_ms: number;
  average_importance: number;
  decay_distribution: Record<string, number>;
  consolidation_metrics: Record<string, any>;
}

export interface AgentAnalyticsData {
  running_agents: number;
  completed_sessions: number;
  iterations: number;
  thoughts: number;
  actions: number;
  reflections: number;
  replay_count: number;
}

export interface ToolAnalyticsData {
  executions: number;
  latency_ms: number;
  failures: number;
  provider_health: Record<string, string>;
  cache_hit_rate: number;
  cost_usd: number;
}

export interface OrganizationAnalyticsData {
  goals_active: number;
  executions: number;
  role_utilization: Record<string, number>;
  skill_usage: Record<string, number>;
  learning_loop_metrics: Record<string, any>;
  policy_violations: number;
}

export interface HealthComponent {
  status: string;
  latency_ms?: number;
  error?: string;
}

export interface PlatformHealthData {
  database: HealthComponent;
  workflow_engine: HealthComponent;
  memory_engine: HealthComponent;
  agent_runtime: HealthComponent;
  coordination_platform: HealthComponent;
  tool_platform: HealthComponent;
  sse: HealthComponent;
  opentelemetry: HealthComponent;
}
