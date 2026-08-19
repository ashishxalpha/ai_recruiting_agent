import { Combine } from "lucide-react";
import { useMemoryConsolidations } from "@/hooks/useMemory";
import { MemoryWidgetWrapper } from "./MemoryWidgetWrapper";

export function MemoryConsolidationsWidget() {
  const { data, isLoading, isError } = useMemoryConsolidations();

  return (
    <MemoryWidgetWrapper
      title="Consolidation History"
      description="Record of memory summarization and deduplication."
      icon={<Combine className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </MemoryWidgetWrapper>
  );
}
