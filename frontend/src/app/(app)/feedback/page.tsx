"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ThumbsUp, X, HelpCircle } from "lucide-react";

export default function FeedbackPage() {
  const matches = [
    { id: "1", candidate: "Jane Smith", job: "Frontend Developer", score: 88, status: "PENDING" },
    { id: "2", candidate: "Alex Johnson", job: "Python Backend Dev", score: 92, status: "PENDING" },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Feedback Hub</h1>
        <p className="text-muted-foreground mt-2">
          Review pending AI matches to train the ranking engine.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Needs Review</CardTitle>
          <CardDescription>The system needs your input on these candidate matches.</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Candidate</TableHead>
                <TableHead>Job</TableHead>
                <TableHead>AI Score</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {matches.map((match) => (
                <TableRow key={match.id}>
                  <TableCell className="font-medium">{match.candidate}</TableCell>
                  <TableCell>{match.job}</TableCell>
                  <TableCell>
                    <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20">{match.score}%</Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end space-x-2">
                      <Button size="sm" variant="outline" className="text-green-500 hover:text-green-600 hover:bg-green-50"><ThumbsUp className="w-4 h-4" /></Button>
                      <Button size="sm" variant="outline" className="text-yellow-500 hover:text-yellow-600 hover:bg-yellow-50"><HelpCircle className="w-4 h-4" /></Button>
                      <Button size="sm" variant="outline" className="text-red-500 hover:text-red-600 hover:bg-red-50"><X className="w-4 h-4" /></Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
