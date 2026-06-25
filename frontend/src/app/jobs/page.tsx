"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

export default function JobsPage() {
  const router = useRouter();
  // Mock data
  const jobs = [
    { id: "e4f8d9b0-1a2c", title: "Senior React Engineer", status: "OPEN", candidates: 45 },
    { id: "f2c4d8e9-3b1a", title: "Python Backend Dev", status: "OPEN", candidates: 12 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Job Requirements</h1>
          <p className="text-muted-foreground mt-2">
            Manage open requisitions and run AI candidate matching.
          </p>
        </div>
        <Button>New Job Requirement</Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Active Jobs</CardTitle>
          <CardDescription>Click a job to view details or run semantic matching.</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Title</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Candidates Matched</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {jobs.map((job) => (
                <TableRow 
                  key={job.id} 
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => router.push(`/jobs/${job.id}`)}
                >
                  <TableCell className="font-medium">{job.title}</TableCell>
                  <TableCell>
                    <Badge variant="outline">{job.status}</Badge>
                  </TableCell>
                  <TableCell className="text-right">{job.candidates}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
