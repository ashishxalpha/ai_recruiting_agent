export interface ResponseMetadata {
  feature_available: boolean;
  data_available: boolean;
  message?: string;
}

export interface StandardResponse<T> {
  data: T | null;
  metadata: ResponseMetadata;
}

export interface DashboardSummary {
  total_candidates: number;
  active_jobs: number;
  active_workflows: number;
  pending_feedback: number;
  running_agents: number;
  active_coordination_sessions: number;
  memory_count: number;
  todays_uploads: number;
}

export interface DashboardHealthStatus {
  status: string;
  message: string;
  latency_ms: number;
}

export interface DashboardHealth {
  database: DashboardHealthStatus;
  redis: DashboardHealthStatus;
  workflow_engine: DashboardHealthStatus;
  agent_swarm: DashboardHealthStatus;
  memory_engine: DashboardHealthStatus;
  overall_status: string;
}

export interface RecentActivityEntry {
  event_id: string;
  timestamp: string;
  source: string;
  description: string;
  metadata: Record<string, any>;
}

export interface RecentActivity {
  activities: RecentActivityEntry[];
}
