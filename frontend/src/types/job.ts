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

export type JobListResponse = PaginatedResponse<JobSummaryDTO>;
