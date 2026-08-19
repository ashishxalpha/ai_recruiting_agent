import { useState } from "react";
import { Search, BrainCircuit, CheckCircle2, XCircle } from "lucide-react";
import { useMemorySearch } from "@/hooks/useMemory";
import { MemoryWidgetWrapper } from "./MemoryWidgetWrapper";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export function MemorySearchWidget() {
  const [query, setQuery] = useState("");
  const [submittedQuery, setSubmittedQuery] = useState("");
  const { data, isLoading, isError } = useMemorySearch(submittedQuery);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      setSubmittedQuery(query);
    }
  };

  return (
    <div className="space-y-4 h-full flex flex-col">
      <form onSubmit={handleSearch} className="flex gap-2">
        <Input 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Test semantic retrieval... (e.g. 'python developer')"
          className="flex-1"
        />
        <Button type="submit" disabled={isLoading}>Search</Button>
      </form>

      {submittedQuery ? (
        <MemoryWidgetWrapper
          title={`Retrieval Debugger: "${submittedQuery}"`}
          description="Detailed breakdown of semantic matching, scoring, and policy exclusion."
          icon={<BrainCircuit className="w-5 h-5 text-muted-foreground" />}
          isLoading={isLoading}
          isError={isError}
          data={data}
          contentClassName="h-full overflow-y-auto"
          className="flex-1 min-h-0"
        >
          {(retrieval) => (
            <div className="space-y-6">
              <div className="grid grid-cols-3 gap-4 text-sm bg-muted/50 p-4 rounded-lg">
                <div>
                  <p className="text-muted-foreground">Embedding Model</p>
                  <p className="font-mono">{retrieval.embedding_model}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Retrieval Policy</p>
                  <p className="font-mono">{retrieval.retrieval_policy}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Execution Time</p>
                  <p className="font-mono">{retrieval.execution_time_ms}ms</p>
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="text-sm font-semibold border-b pb-2">Candidate Rankings</h3>
                {retrieval.candidates.map((candidate, i) => (
                  <div key={candidate.memory_id} className={`p-4 rounded-lg border ${candidate.exclusion_reason ? 'bg-red-50/50 border-red-100' : 'bg-green-50/50 border-green-100'}`}>
                    <div className="flex items-start justify-between">
                      <div className="flex gap-3">
                        <div className="mt-1">
                          {candidate.exclusion_reason ? (
                            <XCircle className="w-5 h-5 text-red-500" />
                          ) : (
                            <CheckCircle2 className="w-5 h-5 text-green-500" />
                          )}
                        </div>
                        <div>
                          <p className="font-medium">Rank #{candidate.final_ranking} <span className="text-xs text-muted-foreground ml-2 font-mono">{candidate.memory_id}</span></p>
                          <p className="text-sm mt-1">{candidate.content_snippet}</p>
                          
                          <div className="mt-3 grid grid-cols-4 gap-4 text-xs font-mono text-muted-foreground">
                            <p>Sim: {candidate.similarity_score.toFixed(2)}</p>
                            <p>Rank: {candidate.reranking_score.toFixed(2)}</p>
                            <p>Imp: {candidate.importance.toFixed(2)}</p>
                            <p>Decay: {candidate.decay.toFixed(2)}</p>
                          </div>
                          
                          <div className="mt-3 text-sm">
                            {candidate.inclusion_reason && (
                              <p className="text-green-700"><span className="font-semibold">Included:</span> {candidate.inclusion_reason}</p>
                            )}
                            {candidate.exclusion_reason && (
                              <p className="text-red-700"><span className="font-semibold">Excluded:</span> {candidate.exclusion_reason}</p>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </MemoryWidgetWrapper>
      ) : (
        <div className="flex-1 flex flex-col items-center justify-center border-dashed border-2 rounded-lg text-muted-foreground">
          <Search className="w-10 h-10 mb-4 opacity-50" />
          <p>Enter a query to debug the retrieval pipeline.</p>
        </div>
      )}
    </div>
  );
}
