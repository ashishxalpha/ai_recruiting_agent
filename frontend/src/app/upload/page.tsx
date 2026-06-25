"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, FileText, CheckCircle2 } from "lucide-react";
import { toast } from "sonner";

export default function ResumeUploadPage() {
  const [uploading, setUploading] = useState(false);

  const handleUpload = () => {
    setUploading(true);
    // Simulate upload delay
    setTimeout(() => {
      setUploading(false);
      toast.success("Resume uploaded successfully. Extraction pipeline started.");
    }, 2000);
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Upload Resume</h1>
        <p className="text-muted-foreground mt-2">
          Upload PDF or DOCX resumes to extract and generate structured profiles.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>File Upload</CardTitle>
          <CardDescription>Supported formats: .pdf, .docx</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="border-2 border-dashed border-muted-foreground/25 hover:border-primary/50 transition-colors rounded-lg p-12 flex flex-col items-center justify-center text-center">
            <Upload className="w-10 h-10 text-muted-foreground mb-4" />
            <p className="text-sm font-medium mb-1">Click to upload or drag and drop</p>
            <p className="text-xs text-muted-foreground mb-4">Max file size: 10MB</p>
            <Button onClick={handleUpload} disabled={uploading}>
              {uploading ? "Uploading..." : "Select File"}
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Recent Uploads</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 border rounded-md">
              <div className="flex items-center space-x-3">
                <FileText className="w-5 h-5 text-blue-500" />
                <div>
                  <p className="text-sm font-medium">john_doe_resume_2026.pdf</p>
                  <p className="text-xs text-muted-foreground">Uploaded 2 hours ago</p>
                </div>
              </div>
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
