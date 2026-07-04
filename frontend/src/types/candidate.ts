import { z } from "zod";
import { PaginatedResponse } from "./pagination";

export const CandidateSummarySchema = z.object({
  id: z.string().uuid(),
  full_name: z.string(),
  email: z.string().email().nullable().optional(),
  phone: z.string().nullable().optional(),
  current_status: z.string(),
  profile_quality: z.number(),
  latest_workflow_status: z.string().nullable().optional(),
  latest_extraction_confidence: z.number().nullable().optional(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

export const CandidateSkillSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  proficiency: z.string().nullable().optional(),
});

export const CandidateExperienceSchema = z.object({
  id: z.string().uuid(),
  company: z.string(),
  title: z.string(),
  start_date: z.string().datetime().nullable().optional(),
  end_date: z.string().datetime().nullable().optional(),
  description: z.string().nullable().optional(),
});

export const CandidateEducationSchema = z.object({
  id: z.string().uuid(),
  institution: z.string(),
  degree: z.string().nullable().optional(),
  field_of_study: z.string().nullable().optional(),
  start_date: z.string().datetime().nullable().optional(),
  end_date: z.string().datetime().nullable().optional(),
  description: z.string().nullable().optional(),
});

export const CandidateProjectSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  description: z.string().nullable().optional(),
  url: z.string().url().nullable().optional(),
});

export const CandidateProfileSchema = z.object({
  id: z.string().uuid(),
  status: z.string(),
  first_name: z.string().nullable().optional(),
  last_name: z.string().nullable().optional(),
  email: z.string().email().nullable().optional(),
  phone: z.string().nullable().optional(),
  summary: z.string().nullable().optional(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

export const CandidateDetailsSchema = z.object({
  profile: CandidateProfileSchema,
  skills: z.array(CandidateSkillSchema).default([]),
  experience: z.array(CandidateExperienceSchema).default([]),
  education: z.array(CandidateEducationSchema).default([]),
  projects: z.array(CandidateProjectSchema).default([]),
});

export type CandidateSummaryDTO = z.infer<typeof CandidateSummarySchema>;
export type CandidateSkillDTO = z.infer<typeof CandidateSkillSchema>;
export type CandidateExperienceDTO = z.infer<typeof CandidateExperienceSchema>;
export type CandidateEducationDTO = z.infer<typeof CandidateEducationSchema>;
export type CandidateProjectDTO = z.infer<typeof CandidateProjectSchema>;
export type CandidateProfileDTO = z.infer<typeof CandidateProfileSchema>;
export type CandidateDetailsDTO = z.infer<typeof CandidateDetailsSchema>;

export type CandidateListResponse = PaginatedResponse<CandidateSummaryDTO>;
