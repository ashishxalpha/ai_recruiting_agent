import { StandardResponse } from "./dashboard";

export interface OrganizationGoal {
  id: string;
  title: string;
  description: string;
  status: string;
  target_date: string;
}

export interface OrganizationRole {
  id: string;
  title: string;
  department: string;
  headcount: number;
}

export interface OrganizationSkill {
  id: string;
  name: string;
  category: string;
  demand_score: number;
}

export interface OrganizationExecution {
  execution_id: string;
  agent_id: string;
  status: string;
  started_at: string;
  completed_at: string | null;
}

export interface OrganizationPolicy {
  id: string;
  name: string;
  description: string;
  enforced: boolean;
}

export interface OrganizationLearning {
  id: string;
  topic: string;
  insight: string;
  confidence: number;
  discovered_at: string;
}

export interface OrganizationMetric {
  metric_name: string;
  value: number;
  trend: 'up' | 'down' | 'stable';
}

export interface OrganizationActivity {
  event_id: string;
  timestamp: string;
  actor: string;
  action: string;
  target: string;
}
