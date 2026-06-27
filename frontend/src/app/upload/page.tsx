"use client";

import { useState, useRef } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, FileText, CheckCircle2 } from "lucide-react";
import { toast } from "sonner";

export default function ResumeUploadPage() {
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast.error("File is too large. Maximum size is 10MB.");
      return;
    }

    // Validate type
    const validTypes = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
    if (!validTypes.includes(file.type)) {
      toast.error("Invalid file type. Only PDF and DOCX are allowed.");
      return;
    }

    setUploading(true);
    
    try {
      const formData = new FormData();
      formData.append("file", file);

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiUrl}/api/v1/resumes/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || "Upload failed");
      }

      toast.success("Resume uploaded successfully. Extraction pipeline started.");
    } catch (error: any) {
      toast.error(error.message || "Failed to upload resume.");
    } finally {
      setUploading(false);
      // Reset input
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
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
            <p className="text-sm font-medium mb-1">Click to upload</p>
            <p className="text-xs text-muted-foreground mb-4">Max file size: 10MB</p>
            
            <input 
              type="file" 
              className="hidden" 
              ref={fileInputRef} 
              onChange={handleFileChange} 
              accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document" 
            />
            
            <Button onClick={handleButtonClick} disabled={uploading}>
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
