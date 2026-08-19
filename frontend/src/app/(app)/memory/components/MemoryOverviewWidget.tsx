import { Info } from "lucide-react";
import { useMemoryList } from "@/hooks/useMemory";
import { MemoryWidgetWrapper } from "./MemoryWidgetWrapper";

export function MemoryOverviewWidget() {
  const { data, isLoading, isError } = useMemoryList();

  return (
    <MemoryWidgetWrapper
      title="Memory Repository Overview"
      description="Top-level view of persisted memories."
      icon={<Info className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </MemoryWidgetWrapper>
  );
}
