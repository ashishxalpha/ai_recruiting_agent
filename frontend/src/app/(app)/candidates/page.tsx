"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useRouter } from "next/navigation";
import { Search, Loader2, ArrowUpDown } from "lucide-react";
import { useCandidateList } from "@/hooks/useCandidates";
import { ErrorState } from "@/components/ui/error-state";
import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";

export default function CandidatesPage() {
  const router = useRouter();
  
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [searchInput, setSearchInput] = useState("");
  const [sortBy, setSortBy] = useState("created_at");
  const [sortOrder, setSortOrder] = useState("desc");

  const { data, isLoading, isError, refetch, isFetching } = useCandidateList({
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
      title="Failed to load candidates"
      message="We could not fetch the candidate database. Please try again."
      onRetry={() => refetch()}
    />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Candidates</h1>
          <p className="text-muted-foreground mt-2">
            Manage and search candidate profiles.
          </p>
        </div>
        <div className="flex items-center gap-2">
          {isFetching && <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />}
          <Button onClick={() => router.push("/upload")}>Upload Resume</Button>
        </div>
      </div>

      <Card>
        <CardHeader className="pb-4">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Candidate Database</CardTitle>
              <CardDescription>View all extracted and parsed candidates.</CardDescription>
            </div>
            <form onSubmit={handleSearch} className="flex max-w-sm w-full items-center space-x-2">
              <Input 
                type="text" 
                placeholder="Search candidates..." 
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
                    <Button variant="ghost" size="sm" onClick={() => toggleSort("first_name")} className="-ml-3 h-8">
                      Name <ArrowUpDown className="ml-2 h-4 w-4" />
                    </Button>
                  </TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>
                    <Button variant="ghost" size="sm" onClick={() => toggleSort("status")} className="-ml-3 h-8">
                      Status <ArrowUpDown className="ml-2 h-4 w-4" />
                    </Button>
                  </TableHead>
                  <TableHead className="text-right">
                    <Button variant="ghost" size="sm" onClick={() => toggleSort("created_at")} className="ml-auto -mr-3 h-8">
                      Joined <ArrowUpDown className="ml-2 h-4 w-4" />
                    </Button>
                  </TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {isLoading ? (
                  Array.from({ length: 5 }).map((_, i) => (
                    <TableRow key={i}>
                      <TableCell><Skeleton className="h-4 w-[150px]" /></TableCell>
                      <TableCell><Skeleton className="h-4 w-[200px]" /></TableCell>
                      <TableCell><Skeleton className="h-6 w-[80px] rounded-full" /></TableCell>
                      <TableCell className="text-right"><Skeleton className="h-4 w-[100px] ml-auto" /></TableCell>
                    </TableRow>
                  ))
                ) : data?.items.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={4} className="h-24 text-center">
                      <EmptyState 
                        icon={<Search className="w-8 h-8" />} 
                        title="No candidates found" 
                        description="Try adjusting your search criteria or upload a new resume."
                      />
                    </TableCell>
                  </TableRow>
                ) : (
                  data?.items.map((candidate) => (
                    <TableRow 
                      key={candidate.id} 
                      className="cursor-pointer hover:bg-muted/50"
                      onClick={() => router.push(`/candidates/${candidate.id}`)}
                    >
                      <TableCell className="font-medium">{candidate.full_name}</TableCell>
                      <TableCell className="text-muted-foreground">{candidate.email || "N/A"}</TableCell>
                      <TableCell>
                        <Badge variant="outline">{candidate.current_status.replace("_", " ")}</Badge>
                      </TableCell>
                      <TableCell className="text-right text-muted-foreground">
                        {new Date(candidate.created_at).toLocaleDateString()}
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
