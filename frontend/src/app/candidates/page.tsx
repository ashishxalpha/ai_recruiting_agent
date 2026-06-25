"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

export default function CandidatesPage() {
  const router = useRouter();
  // Mock data
  const candidates = [
    { id: "e4f8d9b0-1a2c", name: "John Doe", title: "Senior Software Engineer", status: "HIRED", score: 95 },
    { id: "f2c4d8e9-3b1a", name: "Jane Smith", title: "Frontend Developer", status: "UNDER_REVIEW", score: 88 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Candidates</h1>
          <p className="text-muted-foreground mt-2">
            Manage and search candidate profiles.
          </p>
        </div>
        <Button onClick={() => router.push("/upload")}>Upload Resume</Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Candidate Database</CardTitle>
          <CardDescription>View all extracted and parsed candidates.</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Title</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Profile Quality</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {candidates.map((candidate) => (
                <TableRow 
                  key={candidate.id} 
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => router.push(`/candidates/${candidate.id}`)}
                >
                  <TableCell className="font-medium">{candidate.name}</TableCell>
                  <TableCell>{candidate.title}</TableCell>
                  <TableCell>
                    <Badge variant="outline">{candidate.status}</Badge>
                  </TableCell>
                  <TableCell className="text-right">{candidate.score}%</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
