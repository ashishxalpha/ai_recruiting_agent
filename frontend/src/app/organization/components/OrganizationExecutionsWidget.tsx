import { PlayCircle } from "lucide-react";
import { useOrganizationExecutions } from "@/hooks/useOrganization";
import { OrganizationWidgetWrapper } from "./OrganizationWidgetWrapper";

export function OrganizationExecutionsWidget() {
  const { data, isLoading, isError } = useOrganizationExecutions();

  return (
    <OrganizationWidgetWrapper
      title="Executions"
      description="Agent executions and workflow assignments."
      icon={<PlayCircle className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(executions) => <pre>{JSON.stringify(executions, null, 2)}</pre>}
    </OrganizationWidgetWrapper>
  );
}
