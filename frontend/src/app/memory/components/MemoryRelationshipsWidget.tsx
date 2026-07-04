import { Link } from "lucide-react";
import { useMemoryRelationships } from "@/hooks/useMemory";
import { MemoryWidgetWrapper } from "./MemoryWidgetWrapper";

export function MemoryRelationshipsWidget({ memoryId }: { memoryId: string }) {
  const { data, isLoading, isError } = useMemoryRelationships(memoryId);

  return (
    <MemoryWidgetWrapper
      title="Relationships"
      description="Direct edge connections for this memory."
      icon={<Link className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </MemoryWidgetWrapper>
  );
}
