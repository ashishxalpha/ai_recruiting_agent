"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { apiClient } from "@/lib/api-client";
import { Loader2, ArrowLeft } from "lucide-react";

export default function NewJobPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    title: "",
    description: "",
    skills_required: "",
    experience_required: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const skillsArray = formData.skills_required
        .split(",")
        .map(s => s.trim())
        .filter(s => s.length > 0);

      const payload = {
        title: formData.title,
        description: formData.description,
        skills_required: skillsArray,
        experience_required: formData.experience_required,
      };

      const response = await apiClient.post("/api/v1/jobs/requirements", payload) as unknown as { id: string };
      router.push(`/jobs/${response.id}`);
    } catch (err: any) {
      setError(err.message || "Failed to create job requirement.");
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center space-x-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">New Job Requirement</h1>
          <p className="text-muted-foreground mt-2">
            Create a new requisition to match candidates against.
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <Card>
          <CardHeader>
            <CardTitle>Job Details</CardTitle>
            <CardDescription>Enter the core details of the role.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {error && (
              <div className="p-3 text-sm text-red-500 bg-red-50 dark:bg-red-950/50 rounded-md border border-red-200 dark:border-red-900">
                {error}
              </div>
            )}
            <div className="space-y-2">
              <label htmlFor="title" className="text-sm font-medium">Job Title</label>
              <Input
                id="title"
                name="title"
                placeholder="e.g. Senior Frontend Engineer"
                value={formData.title}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="space-y-2">
              <label htmlFor="description" className="text-sm font-medium">Description</label>
              <Textarea
                id="description"
                name="description"
                placeholder="Describe the role, responsibilities, and team..."
                className="min-h-[150px]"
                value={formData.description}
                onChange={handleChange}
                required
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="skills_required" className="text-sm font-medium">Required Skills (comma-separated)</label>
              <Input
                id="skills_required"
                name="skills_required"
                placeholder="e.g. React, TypeScript, Next.js"
                value={formData.skills_required}
                onChange={handleChange}
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="experience_required" className="text-sm font-medium">Experience Required</label>
              <Input
                id="experience_required"
                name="experience_required"
                placeholder="e.g. 5+ years"
                value={formData.experience_required}
                onChange={handleChange}
              />
            </div>
          </CardContent>
          <CardFooter className="flex justify-end space-x-2">
            <Button type="button" variant="outline" onClick={() => router.back()} disabled={isSubmitting}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Create Requirement
            </Button>
          </CardFooter>
        </Card>
      </form>
    </div>
  );
}
