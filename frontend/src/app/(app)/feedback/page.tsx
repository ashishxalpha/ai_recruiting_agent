"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ThumbsUp, X, HelpCircle } from "lucide-react";
import { usePendingFeedback, useSubmitFeedback } from "@/hooks/useFeedback";
import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";

export default function FeedbackPage() {
  const { data: matches, isLoading, isError } = usePendingFeedback();
  const submitFeedback = useSubmitFeedback();

  const handleFeedback = (matchId: string, decision: "APPROVED" | "REJECTED") => {
    submitFeedback.mutate({
      matchId,
      data: { decision, confidence: 1.0 }
    });
  };

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
          {isLoading ? (
            <div className="space-y-4">
              <Skeleton className="h-10 w-full" />
              <Skeleton className="h-10 w-full" />
              <Skeleton className="h-10 w-full" />
            </div>
          ) : isError ? (
            <div className="text-red-500 py-4 text-center">Failed to load pending feedback.</div>
          ) : !matches || matches.length === 0 ? (
            <EmptyState 
              icon={<ThumbsUp className="w-8 h-8" />} 
              title="All Caught Up!" 
              description="There are no pending candidate matches requiring your feedback." 
            />
          ) : (
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
                      <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20">{(match.score).toFixed(1)}%</Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end space-x-2">
                        <Button 
                          size="sm" 
                          variant="outline" 
                          className="text-green-500 hover:text-green-600 hover:bg-green-50"
                          onClick={() => handleFeedback(match.id, "APPROVED")}
                          disabled={submitFeedback.isPending}
                        >
                          <ThumbsUp className="w-4 h-4" />
                        </Button>
                        <Button 
                          size="sm" 
                          variant="outline" 
                          className="text-red-500 hover:text-red-600 hover:bg-red-50"
                          onClick={() => handleFeedback(match.id, "REJECTED")}
                          disabled={submitFeedback.isPending}
                        >
                          <X className="w-4 h-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
