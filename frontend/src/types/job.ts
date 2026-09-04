import { z } from "zod";
import { PaginatedResponse } from "./pagination";

export const JobSummarySchema = z.object({
  id: z.string().uuid(),
  title: z.string(),
  department: z.string().nullable().optional(),
  location: z.string().nullable().optional(),
  employment_type: z.string().nullable().optional(),
  status: z.string(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
  candidate_count: z.number().default(0),
  shortlisted_count: z.number().default(0),
  interview_count: z.number().default(0),
  hired_count: z.number().default(0),
});

export const JobDetailsSchema = z.object({
  id: z.string().uuid(),
  title: z.string(),
  department: z.string().nullable().optional(),
  location: z.string().nullable().optional(),
  employment_type: z.string().nullable().optional(),
  hiring_manager: z.string().nullable().optional(),
  status: z.string(),
  description: z.string(),
  skills_required: z.array(z.string()).default([]),
  experience_required: z.string().nullable().optional(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

export type JobSummaryDTO = z.infer<typeof JobSummarySchema>;
export type JobDetailsDTO = z.infer<typeof JobDetailsSchema>;

export interface JobCandidateMatchDTO {
  id: string;
  candidate_id: string;
  first_name?: string | null;
  last_name?: string | null;
  email?: string | null;
  semantic_score: number;
  skills_score: number;
  experience_score: number;
  education_score: number;
  quality_score: number;
  final_score: number;
  strengths: string[];
  gaps: string[];
  recommendations: string[];
  created_at: string;
}

export interface JobWorkflowDTO {
  id: string;
  workflow_name: string;
  workflow_version: string;
  status: string;
  current_node?: string | null;
  started_at?: string | null;
  completed_at?: string | null;
  candidate_id?: string | null;
  last_error?: string | null;
}

export interface JobAnalyticsDTO {
  total_candidates: number;
  average_match_score: number;
  candidates_by_status: Record<string, number>;
  top_skills_matched: string[];
}

export type JobListResponse = PaginatedResponse<JobSummaryDTO>;
