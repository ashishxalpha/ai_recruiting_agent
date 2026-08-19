"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useRouter } from "next/navigation";
import { Search, Loader2, ArrowUpDown } from "lucide-react";
import { useJobList } from "@/hooks/useJobs";
import { ErrorState } from "@/components/ui/error-state";
import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";

export default function JobsPage() {
  const router = useRouter();
  
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [searchInput, setSearchInput] = useState("");
  const [sortBy, setSortBy] = useState("created_at");
  const [sortOrder, setSortOrder] = useState("desc");

  const { data, isLoading, isError, refetch, isFetching } = useJobList({
    page,
    page_size: 20,
    search: search || undefined,
    sort_by: sortBy,
    sort_order: sortOrder
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setSearch(searchInput);
    setPage(1);
  };

  const toggleSort = (field: string) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortBy(field);
      setSortOrder("desc");
    }
    setPage(1);
  };

  if (isError) {
    return <ErrorState 
      title="Failed to load jobs"
      message="We could not fetch the jobs database. Please try again."
      onRetry={() => refetch()}
    />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Jobs Workspace</h1>
          <p className="text-muted-foreground mt-2">
            Manage open requisitions and run AI candidate matching.
          </p>
        </div>
        <div className="flex items-center gap-2">
          {isFetching && <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />}
          <Button onClick={() => router.push("/jobs/new")}>New Job Requirement</Button>
        </div>
      </div>

      <Card>
        <CardHeader className="pb-4">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Active Jobs</CardTitle>
              <CardDescription>Click a job to view details or run semantic matching.</CardDescription>
            </div>
            <form onSubmit={handleSearch} className="flex max-w-sm w-full items-center space-x-2">
              <Input 
                type="text" 
                placeholder="Search jobs..." 
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
              />
              <Button type="submit" size="icon" variant="outline">
                <Search className="w-4 h-4" />
              </Button>
            </form>
          </div>
        </CardHeader>
        <CardContent>
          <div className="border rounded-md">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>
                    <Button variant="ghost" size="sm" onClick={() => toggleSort("title")} className="-ml-3 h-8">
                      Title <ArrowUpDown className="ml-2 h-4 w-4" />
                    </Button>
                  </TableHead>
                  <TableHead>Department</TableHead>
                  <TableHead>
                    <Button variant="ghost" size="sm" onClick={() => toggleSort("status")} className="-ml-3 h-8">
                      Status <ArrowUpDown className="ml-2 h-4 w-4" />
                    </Button>
                  </TableHead>
                  <TableHead className="text-right">Candidates</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {isLoading ? (
                  Array.from({ length: 5 }).map((_, i) => (
                    <TableRow key={i}>
                      <TableCell><Skeleton className="h-4 w-[200px]" /></TableCell>
                      <TableCell><Skeleton className="h-4 w-[150px]" /></TableCell>
                      <TableCell><Skeleton className="h-6 w-[80px] rounded-full" /></TableCell>
                      <TableCell className="text-right"><Skeleton className="h-4 w-[50px] ml-auto" /></TableCell>
                    </TableRow>
                  ))
                ) : data?.items.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={4} className="h-24 text-center">
                      <EmptyState 
                        icon={<Search className="w-8 h-8" />} 
                        title="No jobs found" 
                        description="Try adjusting your search criteria or create a new job."
                      />
                    </TableCell>
                  </TableRow>
                ) : (
                  data?.items.map((job) => (
                    <TableRow 
                      key={job.id} 
                      className="cursor-pointer hover:bg-muted/50"
                      onClick={() => router.push(`/jobs/${job.id}`)}
                    >
                      <TableCell className="font-medium">{job.title}</TableCell>
                      <TableCell className="text-muted-foreground">{job.department || "N/A"}</TableCell>
                      <TableCell>
                        <Badge variant="outline">{job.status.replace("_", " ")}</Badge>
                      </TableCell>
                      <TableCell className="text-right font-medium">
                        {job.candidate_count}
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
          
          {/* Pagination */}
          {data && data.total_pages > 1 && (
            <div className="flex items-center justify-between mt-4">
              <p className="text-sm text-muted-foreground">
                Showing {((data.page - 1) * data.page_size) + 1} to {Math.min(data.page * data.page_size, data.total)} of {data.total} entries
              </p>
              <div className="flex items-center space-x-2">
                <Button 
                  variant="outline" 
                  size="sm" 
                  disabled={!data.has_previous}
                  onClick={() => setPage(p => p - 1)}
                >
                  Previous
                </Button>
                <div className="text-sm font-medium">
                  Page {data.page} of {data.total_pages}
                </div>
                <Button 
                  variant="outline" 
                  size="sm" 
                  disabled={!data.has_next}
                  onClick={() => setPage(p => p + 1)}
                >
                  Next
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
